import sqlite3
import hashlib
import os
from datetime import datetime
from typing import Optional, Dict, Any
import logging
from cryptography.fernet import Fernet
import base64
from dotenv import load_dotenv

load_dotenv()


class UserDatabase:
    def __init__(self, db_path: str = "friday_users.db"):
        self.db_path = db_path
        self.secret_key = os.getenv("JWT_SECRET", "your-secret-key-change-this")
        self.cipher = Fernet(
            base64.urlsafe_b64encode(self.secret_key[:32].encode().ljust(32, b"\0"))
        )
        self.init_database()

    def init_database(self):
        """Initialize the database with required tables"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()

            # Users table
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    email TEXT UNIQUE NOT NULL,
                    password_hash TEXT NOT NULL,
                    timezone TEXT DEFAULT 'UTC',
                    language TEXT DEFAULT 'en',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """
            )

            # User details table - stores user's own contact information for tools
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS user_details (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    phone_number TEXT,
                    email_password_hash TEXT,
                    backup_email TEXT,
                    address TEXT,
                    notes TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users (id),
                    UNIQUE(user_id)
                )
            """
            )

            # Chat sessions table - stores chat session information
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS chat_sessions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    session_id TEXT NOT NULL,
                    room_name TEXT,
                    started_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    ended_at TIMESTAMP,
                    status TEXT DEFAULT 'active',
                    metadata TEXT,
                    FOREIGN KEY (user_id) REFERENCES users (id),
                    UNIQUE(user_id, session_id)
                )
            """
            )

            # Chat messages table - stores individual chat messages/transcripts
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS chat_messages (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    session_id TEXT NOT NULL,
                    role TEXT NOT NULL CHECK (role IN ('user', 'assistant', 'system')),
                    content TEXT NOT NULL,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    metadata TEXT,
                    FOREIGN KEY (user_id) REFERENCES users (id)
                )
            """
            )

            # Create indexes for chat_messages table
            cursor.execute(
                """
                CREATE INDEX IF NOT EXISTS idx_chat_messages_user_session 
                ON chat_messages(user_id, session_id)
            """
            )

            cursor.execute(
                """
                CREATE INDEX IF NOT EXISTS idx_chat_messages_timestamp 
                ON chat_messages(timestamp)
            """
            )

            conn.commit()
            logging.info("Database initialized successfully")

    def hash_password(self, password: str) -> str:
        """Hash password using SHA256"""
        return hashlib.sha256(password.encode()).hexdigest()

    def verify_password(self, password: str, password_hash: str) -> bool:
        """Verify password against hash"""
        return hashlib.sha256(password.encode()).hexdigest() == password_hash

    def encrypt_password(self, password: str) -> str:
        """Encrypt email password"""
        return self.cipher.encrypt(password.encode()).decode()

    def decrypt_password(self, encrypted_password: str) -> str:
        """Decrypt email password"""
        return self.cipher.decrypt(encrypted_password.encode()).decode()

    def create_user(
        self,
        name: str,
        email: str,
        password: str,
        timezone: str = "UTC",
        language: str = "en",
    ) -> Optional[int]:
        """Create a new user"""
        try:
            password_hash = self.hash_password(password)
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    """
                    INSERT INTO users (name, email, password_hash, timezone, language)
                    VALUES (?, ?, ?, ?, ?)
                """,
                    (name, email, password_hash, timezone, language),
                )
                conn.commit()
                user_id = cursor.lastrowid
                logging.info(f"User created successfully: {email}")
                return user_id
        except sqlite3.IntegrityError:
            logging.error(f"User with email {email} already exists")
            return None
        except Exception as e:
            logging.error(f"Error creating user: {e}")
            return None

    def authenticate_user(self, email: str, password: str) -> Optional[Dict[str, Any]]:
        """Authenticate user and return user data"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    """
                    SELECT id, name, email, password_hash, timezone, language
                    FROM users WHERE email = ?
                """,
                    (email,),
                )
                user = cursor.fetchone()

                if user and self.verify_password(password, user[3]):
                    return {
                        "id": user[0],
                        "name": user[1],
                        "email": user[2],
                        "timezone": user[4],
                        "language": user[5],
                    }
                return None
        except Exception as e:
            logging.error(f"Error authenticating user: {e}")
            return None

    def get_user_by_id(self, user_id: int) -> Optional[Dict[str, Any]]:
        """Get user by ID"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    """
                    SELECT id, name, email, timezone, language, created_at
                    FROM users WHERE id = ?
                """,
                    (user_id,),
                )
                user = cursor.fetchone()

                if user:
                    return {
                        "id": user[0],
                        "name": user[1],
                        "email": user[2],
                        "timezone": user[3],
                        "language": user[4],
                        "created_at": user[5],
                    }
                return None
        except Exception as e:
            logging.error(f"Error getting user: {e}")
            return None

    def set_user_details(
        self,
        user_id: int,
        phone_number: str = None,
        email_password: str = None,
        backup_email: str = None,
        address: str = None,
        notes: str = None,
    ) -> bool:
        """Set or update user details"""
        try:
            # Hash email password if provided
            email_password_hash = None
            if email_password:
                email_password_hash = self.encrypt_password(email_password)

            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()

                # Check if user details already exist
                cursor.execute(
                    "SELECT id FROM user_details WHERE user_id = ?", (user_id,)
                )
                existing = cursor.fetchone()

                if existing:
                    # Update existing record
                    update_fields = []
                    update_values = []

                    if phone_number is not None:
                        update_fields.append("phone_number = ?")
                        update_values.append(phone_number)
                    if email_password_hash is not None:
                        update_fields.append("email_password_hash = ?")
                        update_values.append(email_password_hash)
                    if backup_email is not None:
                        update_fields.append("backup_email = ?")
                        update_values.append(backup_email)
                    if address is not None:
                        update_fields.append("address = ?")
                        update_values.append(address)
                    if notes is not None:
                        update_fields.append("notes = ?")
                        update_values.append(notes)

                    if update_fields:
                        update_fields.append("updated_at = CURRENT_TIMESTAMP")
                        update_values.append(user_id)

                        query = f"UPDATE user_details SET {', '.join(update_fields)} WHERE user_id = ?"
                        cursor.execute(query, update_values)
                else:
                    # Insert new record
                    cursor.execute(
                        """
                        INSERT INTO user_details 
                        (user_id, phone_number, email_password_hash, backup_email, address, notes)
                        VALUES (?, ?, ?, ?, ?, ?)
                    """,
                        (
                            user_id,
                            phone_number,
                            email_password_hash,
                            backup_email,
                            address,
                            notes,
                        ),
                    )

                conn.commit()
                return True
        except Exception as e:
            logging.error(f"Error setting user details: {e}")
            return False

    def get_user_details(self, user_id: int) -> Optional[Dict[str, Any]]:
        """Get user details"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    """
                    SELECT phone_number, email_password_hash, backup_email, address, notes, created_at, updated_at
                    FROM user_details WHERE user_id = ?
                """,
                    (user_id,),
                )
                details = cursor.fetchone()

                if details:
                    email_password = None
                    if details[1]:  # email_password_hash exists
                        try:
                            email_password = self.decrypt_password(details[1])
                        except:
                            email_password = None

                    return {
                        "phone_number": details[0],
                        "email_password": email_password,
                        "backup_email": details[2],
                        "address": details[3],
                        "notes": details[4],
                        "created_at": details[5],
                        "updated_at": details[6],
                    }
                return None
        except Exception as e:
            logging.error(f"Error getting user details: {e}")
            return None

    def get_user_email_password(self, user_id: int) -> Optional[str]:
        """Get user's email password (for tools to use)"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    """
                    SELECT email_password_hash FROM user_details WHERE user_id = ?
                """,
                    (user_id,),
                )
                result = cursor.fetchone()

                if result and result[0]:
                    return self.decrypt_password(result[0])
                return None
        except Exception as e:
            logging.error(f"Error getting email password: {e}")
            return None

    def start_chat_session(
        self, user_id: int, session_id: str, room_name: str = None, metadata: str = None
    ) -> bool:
        """Start a new chat session"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    """
                    INSERT OR REPLACE INTO chat_sessions 
                    (user_id, session_id, room_name, metadata, started_at, status)
                    VALUES (?, ?, ?, ?, ?, 'active')
                """,
                    (user_id, session_id, room_name, metadata, datetime.now()),
                )
                conn.commit()
                return True
        except Exception as e:
            logging.error(f"Error starting chat session: {e}")
            return False

    def end_chat_session(self, user_id: int, session_id: str) -> bool:
        """End a chat session"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    """
                    UPDATE chat_sessions 
                    SET ended_at = ?, status = 'ended'
                    WHERE user_id = ? AND session_id = ?
                """,
                    (datetime.now(), user_id, session_id),
                )
                conn.commit()
                return True
        except Exception as e:
            logging.error(f"Error ending chat session: {e}")
            return False

    def save_chat_message(
        self,
        user_id: int,
        session_id: str,
        role: str,
        content: str,
        metadata: str = None,
    ) -> bool:
        """Save a chat message/transcript to the database"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()

                # First, ensure the session exists
                cursor.execute(
                    """
                    INSERT OR IGNORE INTO chat_sessions 
                    (user_id, session_id, started_at, status)
                    VALUES (?, ?, ?, 'active')
                """,
                    (user_id, session_id, datetime.now()),
                )

                # Then save the message
                cursor.execute(
                    """
                    INSERT INTO chat_messages 
                    (user_id, session_id, role, content, metadata, timestamp)
                    VALUES (?, ?, ?, ?, ?, ?)
                """,
                    (user_id, session_id, role, content, metadata, datetime.now()),
                )
                conn.commit()
                return True
        except Exception as e:
            logging.error(f"Error saving chat message: {e}")
            return False

    def get_chat_messages(
        self, user_id: int, session_id: str = None, limit: int = 100
    ) -> list:
        """Get chat messages for a user (optionally filtered by session)"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()

                if session_id:
                    cursor.execute(
                        """
                        SELECT id, session_id, role, content, timestamp, metadata
                        FROM chat_messages 
                        WHERE user_id = ? AND session_id = ?
                        ORDER BY timestamp DESC
                        LIMIT ?
                    """,
                        (user_id, session_id, limit),
                    )
                else:
                    cursor.execute(
                        """
                        SELECT id, session_id, role, content, timestamp, metadata
                        FROM chat_messages 
                        WHERE user_id = ?
                        ORDER BY timestamp DESC
                        LIMIT ?
                    """,
                        (user_id, limit),
                    )

                messages = []
                for row in cursor.fetchall():
                    messages.append(
                        {
                            "id": row[0],
                            "session_id": row[1],
                            "role": row[2],
                            "content": row[3],
                            "timestamp": row[4],
                            "metadata": row[5],
                        }
                    )

                return messages
        except Exception as e:
            logging.error(f"Error getting chat messages: {e}")
            return []

    def get_user_sessions(self, user_id: int, limit: int = 50) -> list:
        """Get chat sessions for a user"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    """
                    SELECT session_id, room_name, started_at, ended_at, status, metadata,
                           COUNT(cm.id) as message_count
                    FROM chat_sessions cs
                    LEFT JOIN chat_messages cm ON cs.session_id = cm.session_id AND cs.user_id = cm.user_id
                    WHERE cs.user_id = ?
                    GROUP BY cs.session_id
                    ORDER BY cs.started_at DESC
                    LIMIT ?
                """,
                    (user_id, limit),
                )

                sessions = []
                for row in cursor.fetchall():
                    sessions.append(
                        {
                            "session_id": row[0],
                            "room_name": row[1],
                            "started_at": row[2],
                            "ended_at": row[3],
                            "status": row[4],
                            "metadata": row[5],
                            "message_count": row[6],
                        }
                    )

                return sessions
        except Exception as e:
            logging.error(f"Error getting user sessions: {e}")
            return []


# Initialize database instance
db = UserDatabase()

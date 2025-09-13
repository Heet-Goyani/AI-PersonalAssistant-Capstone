import os
import uuid
import sqlite3
from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional, Dict, Any
import jwt
from datetime import datetime, timedelta
from livekit import api
from livekit.api import LiveKitAPI, ListRoomsRequest
from dotenv import load_dotenv
import logging
from database import db
from models import UserCreate, UserLogin, UserDetails, TokenResponse

# Configure logging
logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

load_dotenv()

app = FastAPI(title="Friday AI Assistant API", version="1.0.0")

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure this properly for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Security
security = HTTPBearer()
JWT_SECRET = os.getenv("JWT_SECRET", "your-secret-key-change-this")
JWT_ALGORITHM = "HS256"
JWT_EXPIRATION_HOURS = 24


# JWT utility functions
def create_access_token(data: dict):
    logging.debug("=== JWT Token Creation Started ===")
    logging.debug(f"Input data: {data}")

    to_encode = data.copy()

    # SOLUTION: Ensure 'sub' field is always a string (JWT standard requirement)
    if "sub" in to_encode:
        original_sub = to_encode["sub"]
        to_encode["sub"] = str(original_sub)  # Convert to string
        logging.debug(
            f"Converting subject from {type(original_sub).__name__} '{original_sub}' to string '{to_encode['sub']}'"
        )
    else:
        logging.warning("No 'sub' field found in token data")

    expire = datetime.utcnow() + timedelta(hours=JWT_EXPIRATION_HOURS)
    to_encode.update({"exp": expire})
    logging.debug(f"Token payload before encoding: {to_encode}")

    try:
        encoded_jwt = jwt.encode(to_encode, JWT_SECRET, algorithm=JWT_ALGORITHM)
        logging.debug(f"Generated token successfully")
        return encoded_jwt
    except Exception as e:
        logging.error(f"Error creating JWT token: {e}")
        raise


def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    try:
        # Decode token
        payload = jwt.decode(
            credentials.credentials, JWT_SECRET, algorithms=[JWT_ALGORITHM]
        )
        logging.debug(f"JWT payload decoded successfully: {payload}")

        # SOLUTION: Extract string subject and convert back to integer for database lookup
        user_id_str = payload.get("sub")
        logging.debug(f"Extracted user_id (string) from token: {user_id_str}")

        if user_id_str is None:
            logging.error("No user ID found in token")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="No user ID in token",
                headers={"WWW-Authenticate": "Bearer"},
            )

        # Convert string user_id back to integer for database operations
        try:
            user_id = int(user_id_str)
            logging.debug(f"Converted user_id to integer: {user_id}")
        except (ValueError, TypeError) as e:
            logging.error(f"Could not convert user_id '{user_id_str}' to integer: {e}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid user ID format in token",
                headers={"WWW-Authenticate": "Bearer"},
            )

        return user_id

    except jwt.InvalidTokenError as e:
        logging.error(f"Invalid JWT token: {e}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid token: {str(e)}",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except HTTPException:
        # Re-raise HTTPException as is
        raise
    except Exception as e:
        logging.error(f"Unexpected error in token verification: {e}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )


# LiveKit utility functions
async def generate_room_name():
    name = "friday-room-" + str(uuid.uuid4())[:8]
    rooms = await get_rooms()
    while name in rooms:
        name = "friday-room-" + str(uuid.uuid4())[:8]
    return name


async def get_rooms():
    try:
        livekit_api = LiveKitAPI()
        rooms = await livekit_api.room.list_rooms(ListRoomsRequest())
        await livekit_api.aclose()
        return [room.name for room in rooms.rooms]
    except Exception as e:
        logging.error(f"Error getting rooms: {e}")
        return []


# Authentication endpoints
@app.post("/auth/register", response_model=TokenResponse)
async def register(user_data: UserCreate):
    """Register a new user"""
    user_id = db.create_user(
        name=user_data.name,
        email=user_data.email,
        password=user_data.password,
        timezone=user_data.timezone,
        language=user_data.language,
    )

    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exists",
        )

    user = db.get_user_by_id(user_id)
    access_token = create_access_token(data={"sub": user_id})

    return TokenResponse(access_token=access_token, token_type="bearer", user=user)


@app.post("/auth/login", response_model=TokenResponse)
async def login(user_data: UserLogin):
    """Login user"""
    user = db.authenticate_user(user_data.email, user_data.password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
        )

    access_token = create_access_token(data={"sub": user["id"]})

    return TokenResponse(access_token=access_token, token_type="bearer", user=user)


# User management endpoints
@app.get("/user/profile")
async def get_profile(user_id: int = Depends(verify_token)):
    """Get user profile"""
    user = db.get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@app.get("/user/details")
async def get_user_details(user_id: int = Depends(verify_token)):
    """Get user details"""
    details = db.get_user_details(user_id)
    if not details:
        return {"message": "No details found", "details": {}}
    return {"details": details}


@app.post("/user/details")
async def set_user_details(details: UserDetails, user_id: int = Depends(verify_token)):
    """Set user details"""
    success = db.set_user_details(
        user_id=user_id,
        phone_number=details.phone_number,
        email_password=details.email_password,
        backup_email=details.backup_email,
        address=details.address,
    )

    if not success:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to set user details",
        )

    return {"message": "User details updated successfully"}


# LiveKit endpoints
@app.get("/livekit/token")
async def get_livekit_token(
    room_name: Optional[str] = None, user_id: int = Depends(verify_token)
):
    """Generate LiveKit token for authenticated user"""
    user = db.get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if not room_name:
        room_name = await generate_room_name()

    try:
        token = (
            api.AccessToken(
                os.getenv("LIVEKIT_API_KEY"), os.getenv("LIVEKIT_API_SECRET")
            )
            .with_identity(user["name"])
            .with_name(user["name"])
            .with_grants(api.VideoGrants(room_join=True, room=room_name))
        )

        return {
            "token": token.to_jwt(),
            "room_name": room_name,
            "user_name": user["name"],
        }
    except Exception as e:
        logging.error(f"Error generating LiveKit token: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to generate LiveKit token",
        )


@app.get("/livekit/rooms")
async def list_rooms(user_id: int = Depends(verify_token)):
    """List available rooms"""
    rooms = await get_rooms()
    return {"rooms": rooms}


# Debug endpoints
@app.get("/debug/create-test-token")
async def debug_create_test_token():
    """Debug endpoint to create a test token"""
    test_payload = {"sub": "1", "test": True}  # Use string for sub (JWT standard)
    token = create_access_token(test_payload)
    return {"token": token, "payload": test_payload}


@app.get("/debug/verify-test-token")
async def debug_verify_test_token(user_id: int = Depends(verify_token)):
    """Debug endpoint to verify token"""
    return {"message": "Token verified successfully", "user_id": user_id}


# Chat history endpoints
@app.get("/chat/sessions")
async def get_user_chat_sessions(user_id: int = Depends(verify_token), limit: int = 50):
    """Get user's chat sessions"""
    try:
        sessions = db.get_user_sessions(user_id, limit)
        return {"sessions": sessions, "count": len(sessions)}
    except Exception as e:
        logging.error(f"Error getting user sessions: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve chat sessions",
        )


@app.get("/chat/session/{session_id}/messages")
async def get_session_messages(
    session_id: str, user_id: int = Depends(verify_token), limit: int = 100
):
    """Get messages for a specific chat session"""
    try:
        messages = db.get_chat_messages(user_id, session_id, limit)
        return {"messages": messages, "count": len(messages)}
    except Exception as e:
        logging.error(f"Error getting session messages: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve session messages",
        )


@app.get("/chat/messages")
async def get_all_user_messages(user_id: int = Depends(verify_token), limit: int = 200):
    """Get all messages for a user across all sessions"""
    try:
        messages = db.get_chat_messages(user_id, None, limit)
        return {"messages": messages, "count": len(messages)}
    except Exception as e:
        logging.error(f"Error getting user messages: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve user messages",
        )


@app.delete("/chat/session/{session_id}")
async def delete_chat_session(session_id: str, user_id: int = Depends(verify_token)):
    """Delete a chat session and all its messages"""
    try:
        # First, delete all messages for this session
        with sqlite3.connect(db.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "DELETE FROM chat_messages WHERE user_id = ? AND session_id = ?",
                (user_id, session_id),
            )
            cursor.execute(
                "DELETE FROM chat_sessions WHERE user_id = ? AND session_id = ?",
                (user_id, session_id),
            )
            conn.commit()

        return {"message": "Chat session deleted successfully"}
    except Exception as e:
        logging.error(f"Error deleting chat session: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete chat session",
        )


@app.get("/")
async def root():
    """Root endpoint"""
    return {"message": "Friday AI Assistant API", "version": "1.0.0", "docs": "/docs"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)

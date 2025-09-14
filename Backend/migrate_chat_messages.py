"""
Initial Migration Script for Chat Analytics

This script inserts all existing chat_messages into log_inserts table
for initial processing by the analytics pipeline.

Run this script once to populate log_inserts with all historical messages
that haven't been analyzed yet.
"""

import sys
import os
import sqlite3
from datetime import datetime

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database import db
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def get_all_chat_message_ids():
    """Get all chat message IDs from chat_messages table"""
    try:
        with sqlite3.connect(db.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id FROM chat_messages ORDER BY id")
            return [row[0] for row in cursor.fetchall()]
    except Exception as e:
        logger.error(f"Error getting chat message IDs: {e}")
        return []


def get_existing_log_message_ids():
    """Get message IDs that are already in log_inserts table"""
    try:
        with sqlite3.connect(db.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT chat_message_id FROM log_inserts")
            return set(row[0] for row in cursor.fetchall())
    except Exception as e:
        logger.error(f"Error getting existing log message IDs: {e}")
        return set()


def insert_missing_message_ids(missing_ids):
    """Insert missing message IDs into log_inserts table"""
    if not missing_ids:
        return True

    try:
        with sqlite3.connect(db.db_path) as conn:
            cursor = conn.cursor()

            # Prepare batch insert
            insert_data = [(msg_id, datetime.now(), 0) for msg_id in missing_ids]

            cursor.executemany(
                """
                INSERT OR IGNORE INTO log_inserts (chat_message_id, inserted_at, processed)
                VALUES (?, ?, ?)
                """,
                insert_data,
            )

            conn.commit()
            inserted_count = cursor.rowcount
            logger.info(f"Inserted {inserted_count} message IDs into log_inserts")
            return True

    except Exception as e:
        logger.error(f"Error inserting message IDs: {e}")
        return False


def get_analytics_counts():
    """Get current analytics counts for comparison"""
    try:
        with sqlite3.connect(db.db_path) as conn:
            cursor = conn.cursor()

            # Count total chat messages
            cursor.execute("SELECT COUNT(*) FROM chat_messages")
            total_messages = cursor.fetchone()[0]

            # Count messages in log_inserts
            cursor.execute("SELECT COUNT(*) FROM log_inserts")
            log_entries = cursor.fetchone()[0]

            # Count unprocessed messages
            cursor.execute("SELECT COUNT(*) FROM log_inserts WHERE processed = 0")
            unprocessed = cursor.fetchone()[0]

            # Count processed analytics
            cursor.execute("SELECT COUNT(*) FROM message_analytics")
            analytics_count = cursor.fetchone()[0]

            return {
                "total_messages": total_messages,
                "log_entries": log_entries,
                "unprocessed": unprocessed,
                "analytics_count": analytics_count,
            }
    except Exception as e:
        logger.error(f"Error getting analytics counts: {e}")
        return {}


def run_migration():
    """Run the complete migration process"""
    print("🚀 Starting Chat Analytics Migration...")
    print("=" * 50)

    # Step 1: Get current status
    print("📊 Getting current database status...")
    counts_before = get_analytics_counts()

    if counts_before:
        print(f"   - Total chat messages: {counts_before['total_messages']}")
        print(f"   - Log entries: {counts_before['log_entries']}")
        print(f"   - Unprocessed messages: {counts_before['unprocessed']}")
        print(f"   - Analytics entries: {counts_before['analytics_count']}")

    # Step 2: Get all chat message IDs
    print("\n📥 Getting all chat message IDs...")
    all_message_ids = get_all_chat_message_ids()
    print(f"   Found {len(all_message_ids)} total chat messages")

    if not all_message_ids:
        print("⚠️ No chat messages found. Nothing to migrate.")
        return True

    # Step 3: Get existing log entries
    print("\n🔍 Checking existing log entries...")
    existing_log_ids = get_existing_log_message_ids()
    print(f"   Found {len(existing_log_ids)} existing log entries")

    # Step 4: Find missing message IDs
    missing_ids = [
        msg_id for msg_id in all_message_ids if msg_id not in existing_log_ids
    ]
    print(f"   Found {len(missing_ids)} messages missing from log_inserts")

    if not missing_ids:
        print("✅ All chat messages are already in log_inserts table!")
        return True

    # Step 5: Insert missing message IDs
    print(f"\n📝 Inserting {len(missing_ids)} missing message IDs...")
    success = insert_missing_message_ids(missing_ids)

    if not success:
        print("❌ Failed to insert missing message IDs")
        return False

    # Step 6: Verify results
    print("\n✅ Migration completed! Getting updated status...")
    counts_after = get_analytics_counts()

    if counts_after:
        print(f"   - Total chat messages: {counts_after['total_messages']}")
        print(f"   - Log entries: {counts_after['log_entries']}")
        print(f"   - Unprocessed messages: {counts_after['unprocessed']}")
        print(f"   - Analytics entries: {counts_after['analytics_count']}")

    print("\n🎉 Migration successful!")
    print("\n📋 Next steps:")
    print("1. Run the dashboard: python streamlit_dashboard/run_dashboard.py")
    print("2. Click 'Refresh Data' to process all unprocessed messages")
    print("3. The log_inserts table will be automatically cleared after processing")

    return True


def verify_database_schema():
    """Verify that all required tables exist"""
    try:
        with sqlite3.connect(db.db_path) as conn:
            cursor = conn.cursor()

            # Check required tables
            cursor.execute(
                """
                SELECT name FROM sqlite_master 
                WHERE type='table' AND name IN ('chat_messages', 'log_inserts', 'message_analytics')
            """
            )
            tables = [row[0] for row in cursor.fetchall()]

            required_tables = ["chat_messages", "log_inserts", "message_analytics"]
            missing_tables = [t for t in required_tables if t not in tables]

            if missing_tables:
                print(f"❌ Missing required tables: {missing_tables}")
                print(
                    "Please run the main application first to initialize the database schema."
                )
                return False

            # Check trigger
            cursor.execute(
                """
                SELECT name FROM sqlite_master 
                WHERE type='trigger' AND name='trigger_log_chat_message_inserts'
            """
            )
            trigger = cursor.fetchone()

            if not trigger:
                print("❌ Missing required trigger: trigger_log_chat_message_inserts")
                print(
                    "Please run the main application first to initialize the database schema."
                )
                return False

            return True
    except Exception as e:
        print(f"❌ Database schema verification failed: {e}")
        return False


if __name__ == "__main__":
    print("🏗️ Chat Analytics Migration Script")
    print("This script will populate log_inserts with all existing chat messages.")
    print("")

    # Verify database schema first
    if not verify_database_schema():
        sys.exit(1)

    # Run migration
    success = run_migration()

    if success:
        print("\n✅ Migration completed successfully!")
        sys.exit(0)
    else:
        print("\n❌ Migration failed!")
        sys.exit(1)

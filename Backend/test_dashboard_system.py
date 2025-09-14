"""
Test script for Chat Analytics Dashboard

This script tests the complete system:
1. Database schema and trigger
2. Pipeline processing functions
3. Dashboard data functions

Run this script to validate the implementation.
"""

import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database import db
from chat_process_pipeline import process_unprocessed_messages, get_analytics_data
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def test_database_schema():
    """Test that all required tables and triggers exist"""
    print("🧪 Testing database schema...")

    try:
        import sqlite3

        with sqlite3.connect(db.db_path) as conn:
            cursor = conn.cursor()

            # Check if tables exist
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
                print(f"❌ Missing tables: {missing_tables}")
                return False

            # Check if trigger exists
            cursor.execute(
                """
                SELECT name FROM sqlite_master 
                WHERE type='trigger' AND name='trigger_log_chat_message_inserts'
            """
            )
            trigger = cursor.fetchone()

            if not trigger:
                print("❌ Missing trigger: trigger_log_chat_message_inserts")
                return False

            print("✅ Database schema is correct")
            return True

    except Exception as e:
        print(f"❌ Database schema test failed: {e}")
        return False


def test_trigger_functionality():
    """Test that the SQLite trigger works correctly"""
    print("🧪 Testing SQLite trigger...")

    try:
        # Insert a test message
        test_user_id = 1
        test_session_id = "test_session_trigger"
        test_content = "This is a test message for trigger validation"

        # Save the test message
        success = db.save_chat_message(
            user_id=test_user_id,
            session_id=test_session_id,
            role="user",
            content=test_content,
        )

        if not success:
            print("❌ Failed to save test message")
            return False

        # Check if trigger created log entry
        unprocessed_ids = db.get_unprocessed_message_ids()

        if not unprocessed_ids:
            print("❌ Trigger did not create log entry")
            return False

        print(
            f"✅ Trigger working correctly - found {len(unprocessed_ids)} unprocessed messages"
        )
        return True

    except Exception as e:
        print(f"❌ Trigger test failed: {e}")
        return False


def test_pipeline_functions():
    """Test pipeline processing functions"""
    print("🧪 Testing pipeline functions...")

    try:
        # Test getting analytics data
        data = get_analytics_data()

        if not isinstance(data, dict):
            print("❌ get_analytics_data should return a dictionary")
            return False

        required_keys = [
            "latest_analytics",
            "sentiment_data",
            "keyword_frequency",
            "total_messages",
            "success",
        ]
        missing_keys = [key for key in required_keys if key not in data]

        if missing_keys:
            print(f"❌ Missing keys in analytics data: {missing_keys}")
            return False

        print("✅ Analytics data function working correctly")

        # Test unprocessed messages pipeline (if there are unprocessed messages)
        unprocessed_count = len(db.get_unprocessed_message_ids())
        print(f"📊 Found {unprocessed_count} unprocessed messages")

        if unprocessed_count > 0:
            print("🔄 Testing pipeline processing...")
            result = process_unprocessed_messages()

            if not isinstance(result, dict) or "success" not in result:
                print(
                    "❌ Pipeline function should return a dictionary with 'success' key"
                )
                return False

            if result["success"]:
                print(
                    f"✅ Pipeline processed {result.get('processed_count', 0)} messages"
                )
            else:
                print(
                    f"⚠️ Pipeline completed but with issues: {result.get('error', 'Unknown error')}"
                )
        else:
            print("ℹ️ No unprocessed messages to test pipeline with")

        return True

    except Exception as e:
        print(f"❌ Pipeline function test failed: {e}")
        return False


def test_dashboard_data_functions():
    """Test that dashboard data functions work correctly"""
    print("🧪 Testing dashboard data functions...")

    try:
        # Test get_analytics_data function
        data = get_analytics_data()

        if not data["success"]:
            print(
                f"❌ Analytics data function failed: {data.get('error', 'Unknown error')}"
            )
            return False

        # Validate data structure
        print(f"📊 Analytics data summary:")
        print(f"   - Total messages: {data['total_messages']}")
        print(f"   - Latest analytics entries: {len(data['latest_analytics'])}")
        print(f"   - Sentiment categories: {len(data['sentiment_data'])}")
        print(f"   - Unique keywords: {len(data['keyword_frequency'])}")

        print("✅ Dashboard data functions working correctly")
        return True

    except Exception as e:
        print(f"❌ Dashboard data test failed: {e}")
        return False


def create_sample_data():
    """Create some sample data for testing"""
    print("🧪 Creating sample data for testing...")

    try:
        sample_messages = [
            {
                "role": "user",
                "content": "I'm really happy with this service! It's amazing.",
            },
            {"role": "user", "content": "This is terrible, I hate it so much."},
            {"role": "user", "content": "The weather is okay today, nothing special."},
            {"role": "user", "content": "I love the new features! Great work team."},
            {
                "role": "user",
                "content": "Could you help me with my account settings please?",
            },
        ]

        test_user_id = 1
        test_session_id = "test_sample_session"

        for i, msg in enumerate(sample_messages):
            success = db.save_chat_message(
                user_id=test_user_id,
                session_id=f"{test_session_id}_{i}",
                role=msg["role"],
                content=msg["content"],
            )

            if not success:
                print(f"❌ Failed to create sample message {i}")
                return False

        print(f"✅ Created {len(sample_messages)} sample messages")
        return True

    except Exception as e:
        print(f"❌ Sample data creation failed: {e}")
        return False


def run_complete_test():
    """Run all tests"""
    print("🚀 Starting complete system test...")
    print("=" * 50)

    tests = [
        ("Database Schema", test_database_schema),
        ("Sample Data Creation", create_sample_data),
        ("Trigger Functionality", test_trigger_functionality),
        ("Pipeline Functions", test_pipeline_functions),
        ("Dashboard Data Functions", test_dashboard_data_functions),
    ]

    passed = 0
    failed = 0

    for test_name, test_func in tests:
        print(f"\n🧪 Running {test_name}...")
        try:
            if test_func():
                passed += 1
            else:
                failed += 1
        except Exception as e:
            print(f"❌ {test_name} failed with exception: {e}")
            failed += 1

    print("\n" + "=" * 50)
    print(f"📊 Test Results: {passed} passed, {failed} failed")

    if failed == 0:
        print("🎉 All tests passed! The system is ready to use.")
        print("\n📋 Next steps:")
        print("1. Run the dashboard: python streamlit_dashboard/run_dashboard.py")
        print("2. Click 'Refresh Data' in the dashboard to process messages")
        print("3. View the analytics visualizations")
    else:
        print("⚠️ Some tests failed. Please check the errors above.")

    return failed == 0


if __name__ == "__main__":
    success = run_complete_test()
    sys.exit(0 if success else 1)

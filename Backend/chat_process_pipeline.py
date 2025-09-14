"""
Chat Message Analytics Pipeline

This module processes chat messages from a given session to extract sentiment analysis,
emotion detection, and keyword extraction using Google Gemini API, then saves the
analytics to the database.

Main entry point: process_session_analytics(session_id)
"""

import os
import re
import json
import logging
from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime
import google.generativeai as genai
from dotenv import load_dotenv

from database import db

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configure Google Gemini API
GEMINI_API_KEY = os.getenv("GOOGLE_API_KEY")
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel("gemini-1.5-flash")
else:
    logger.warning("GEMINI_API_KEY not found in environment variables")
    model = None


class ChatMessageParser:
    """Handles parsing of chat message content from various formats"""

    @staticmethod
    def parse_chat_message_content(content: str) -> Tuple[Optional[str], Optional[str]]:
        """
        Parse chat message content to extract role and message text.

        Handles formats like:
        {type='conversation_item_added' item=ChatMessage(id='GR_ec10573c3db7',
         type='message', role='assistant', content=[' I will now search...'], ...)}

        Args:
            content (str): Raw content string from database

        Returns:
            Tuple[Optional[str], Optional[str]]: (role, message_text)
        """
        try:
            # Pattern to extract role and content from ChatMessage format
            chat_message_pattern = r"role='(\w+)'.*?content=\[(.*?)\]"
            match = re.search(chat_message_pattern, content, re.DOTALL)

            if match:
                role = match.group(1)
                message_content = match.group(2)

                # Clean up the message content - remove quotes and extra whitespace
                message_text = re.sub(r'^[\'"]|[\'"]$', "", message_content.strip())
                message_text = message_text.replace("\\n", " ").strip()

                return role, message_text

            # Fallback: try to extract just the text content if it's a simple message
            simple_text_pattern = r'[\'"]([^\'\"]+)[\'"]'
            simple_match = re.search(simple_text_pattern, content)
            if simple_match:
                return "user", simple_match.group(1)

            # If no pattern matches, return the content as is
            return None, content.strip()

        except Exception as e:
            logger.error(f"Error parsing chat message content: {e}")
            return None, content


class MessageAnalyzer:
    """Handles sentiment analysis, emotion detection, and keyword extraction using Gemini API"""

    def __init__(self):
        self.model = model

    def analyze_message(self, message: str) -> Dict[str, Any]:
        """
        Analyze a message for sentiment, emotion, and keywords using Gemini API.

        Args:
            message (str): The message text to analyze

        Returns:
            Dict containing sentiment_score, sentiment_label, emotion_label, contains_keywords
        """
        if not self.model:
            logger.error("Gemini model not configured. Please set GEMINI_API_KEY.")
            return self._get_default_analysis()

        try:
            # Create a comprehensive prompt for analysis
            prompt = f"""
            Analyze the following message for sentiment, emotion, and keywords:
            
            Message: "{message}"
            
            Please provide your analysis in the following JSON format:
            {{
                "sentiment_score": <float between -1.0 and 1.0, where -1 is very negative, 0 is neutral, 1 is very positive>,
                "sentiment_label": "<positive|neutral|negative>",
                "emotion_label": "<primary emotion like joy, sadness, anger, fear, surprise, disgust, neutral>",
                "contains_keywords": [<list of 3-5 relevant keywords or phrases from the message>]
            }}
            
            Only return the JSON, no additional text.
            """

            response = self.model.generate_content(prompt)
            response_text = response.text.strip()

            # Try to parse the JSON response
            try:
                # Remove any markdown code block formatting
                if response_text.startswith("```"):
                    response_text = re.sub(r"^```(?:json)?\s*", "", response_text)
                    response_text = re.sub(r"\s*```$", "", response_text)

                analysis = json.loads(response_text)

                # Validate and clean the analysis
                return self._validate_analysis(analysis)

            except json.JSONDecodeError as je:
                logger.error(f"Failed to parse Gemini response as JSON: {je}")
                logger.error(f"Response text: {response_text}")
                return self._get_default_analysis()

        except Exception as e:
            logger.error(f"Error analyzing message with Gemini: {e}")
            return self._get_default_analysis()

    def _validate_analysis(self, analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Validate and clean the analysis results"""
        validated = {}

        # Validate sentiment_score
        sentiment_score = analysis.get("sentiment_score", 0.0)
        if isinstance(sentiment_score, (int, float)):
            validated["sentiment_score"] = max(-1.0, min(1.0, float(sentiment_score)))
        else:
            validated["sentiment_score"] = 0.0

        # Validate sentiment_label
        sentiment_label = analysis.get("sentiment_label", "neutral").lower()
        if sentiment_label in ["positive", "negative", "neutral"]:
            validated["sentiment_label"] = sentiment_label
        else:
            # Infer from score if label is invalid
            score = validated["sentiment_score"]
            if score > 0.1:
                validated["sentiment_label"] = "positive"
            elif score < -0.1:
                validated["sentiment_label"] = "negative"
            else:
                validated["sentiment_label"] = "neutral"

        # Validate emotion_label
        emotion_label = analysis.get("emotion_label", "neutral").lower()
        valid_emotions = [
            "joy",
            "sadness",
            "anger",
            "fear",
            "surprise",
            "disgust",
            "neutral",
        ]
        if emotion_label in valid_emotions:
            validated["emotion_label"] = emotion_label
        else:
            validated["emotion_label"] = "neutral"

        # Validate keywords
        keywords = analysis.get("contains_keywords", [])
        if isinstance(keywords, list):
            # Clean and limit keywords
            validated["contains_keywords"] = [
                str(kw).strip() for kw in keywords[:5] if str(kw).strip()
            ]
        else:
            validated["contains_keywords"] = []

        return validated

    def _get_default_analysis(self) -> Dict[str, Any]:
        """Return default analysis when API fails"""
        return {
            "sentiment_score": 0.0,
            "sentiment_label": "neutral",
            "emotion_label": "neutral",
            "contains_keywords": [],
        }


class ChatAnalyticsPipeline:
    """Main pipeline for processing chat session analytics"""

    def __init__(self):
        self.parser = ChatMessageParser()
        self.analyzer = MessageAnalyzer()

    def get_session_messages(self, session_id: str) -> List[Dict[str, Any]]:
        """
        Retrieve all chat messages for a given session_id.

        Args:
            session_id (str): The session ID to fetch messages for

        Returns:
            List of message dictionaries
        """
        try:
            # We need to get messages without specifying user_id
            # Let's modify the query to get all messages for the session
            import sqlite3

            with sqlite3.connect(db.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    """
                    SELECT id, user_id, session_id, role, content, timestamp, metadata
                    FROM chat_messages 
                    WHERE session_id = ?
                    ORDER BY timestamp ASC
                    """,
                    (session_id,),
                )

                messages = []
                for row in cursor.fetchall():
                    messages.append(
                        {
                            "id": row[0],
                            "user_id": row[1],
                            "session_id": row[2],
                            "role": row[3],
                            "content": row[4],
                            "timestamp": row[5],
                            "metadata": row[6],
                        }
                    )
                return messages

        except Exception as e:
            logger.error(f"Error retrieving session messages: {e}")
            return []

    def process_user_messages(
        self, messages: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """
        Process messages to extract user messages and parse content.

        Args:
            messages: List of raw message dictionaries

        Returns:
            List of processed user messages with parsed content
        """
        user_messages = []

        for message in messages:
            try:
                # Parse the content to extract role and message text
                parsed_role, parsed_message = self.parser.parse_chat_message_content(
                    message["content"]
                )

                # Keep only user messages (filter by parsed role or database role)
                if parsed_role == "user" or message["role"] == "user":
                    user_messages.append(
                        {
                            "id": message["id"],
                            "user_id": message["user_id"],
                            "session_id": message["session_id"],
                            "role": "user",
                            "message": parsed_message or message["content"],
                            "timestamp": message["timestamp"],
                        }
                    )

            except Exception as e:
                logger.error(
                    f"Error processing message {message.get('id', 'unknown')}: {e}"
                )
                continue

        return user_messages

    def analyze_and_save_messages(self, user_messages: List[Dict[str, Any]]) -> int:
        """
        Analyze user messages and save analytics to database.

        Args:
            user_messages: List of processed user messages

        Returns:
            Number of messages successfully processed
        """
        processed_count = 0

        for idx, message in enumerate(user_messages, 1):
            try:
                # Analyze the message
                analysis = self.analyzer.analyze_message(message["message"])

                # Save to database
                success = db.save_message_analytics(
                    user_id=message["user_id"],
                    session_id=message["session_id"],
                    message=message["message"],
                    role=message["role"],
                    sequence_number=idx,
                    message_length=len(message["message"].split()),
                    sentiment_score=analysis["sentiment_score"],
                    sentiment_label=analysis["sentiment_label"],
                    emotion_label=analysis["emotion_label"],
                    toxicity_flag=False,  # Could be extended to include toxicity detection
                    contains_keywords=analysis["contains_keywords"],
                )

                if success:
                    processed_count += 1
                    logger.info(
                        f"Processed message {idx}: {analysis['sentiment_label']} sentiment, {analysis['emotion_label']} emotion"
                    )
                else:
                    logger.error(f"Failed to save analytics for message {idx}")

            except Exception as e:
                logger.error(f"Error analyzing message {idx}: {e}")
                continue

        return processed_count


def process_session_analytics(session_id: str) -> Dict[str, Any]:
    """
    Main entry point for processing chat session analytics.

    Args:
        session_id (str): The session ID to process

    Returns:
        Dict with processing results and statistics
    """
    pipeline = ChatAnalyticsPipeline()

    try:
        logger.info(f"Starting analytics processing for session: {session_id}")

        # Step 1: Get all messages for the session
        all_messages = pipeline.get_session_messages(session_id)
        logger.info(f"Retrieved {len(all_messages)} total messages")

        if not all_messages:
            return {
                "success": False,
                "error": "No messages found for session",
                "session_id": session_id,
                "processed_count": 0,
            }

        # Step 2: Process and filter user messages
        user_messages = pipeline.process_user_messages(all_messages)
        logger.info(f"Filtered to {len(user_messages)} user messages")

        if not user_messages:
            return {
                "success": False,
                "error": "No user messages found for session",
                "session_id": session_id,
                "processed_count": 0,
            }

        # Step 3: Analyze and save messages
        processed_count = pipeline.analyze_and_save_messages(user_messages)

        success = processed_count > 0
        logger.info(
            f"Processing complete. Successfully processed {processed_count}/{len(user_messages)} messages"
        )

        return {
            "success": success,
            "session_id": session_id,
            "total_messages": len(all_messages),
            "user_messages": len(user_messages),
            "processed_count": processed_count,
            "error": None if success else "Failed to process any messages",
        }

    except Exception as e:
        logger.error(f"Error in process_session_analytics: {e}")
        return {
            "success": False,
            "error": str(e),
            "session_id": session_id,
            "processed_count": 0,
        }


def process_unprocessed_messages() -> Dict[str, Any]:
    """
    Pipeline function that processes all unprocessed messages from log_inserts.

    This function:
    1. Checks log_inserts for unprocessed message IDs
    2. Fetches corresponding rows from chat_messages
    3. Applies analytics processing
    4. Inserts results into message_analytics
    5. Marks processed IDs as completed

    Returns:
        Dict with processing results and statistics
    """
    try:
        logger.info("Starting unprocessed messages pipeline")

        # Step 1: Get unprocessed message IDs
        unprocessed_ids = db.get_unprocessed_message_ids()
        logger.info(f"Found {len(unprocessed_ids)} unprocessed messages")

        if not unprocessed_ids:
            return {
                "success": True,
                "message": "No unprocessed messages found",
                "processed_count": 0,
                "total_unprocessed": 0,
            }

        # Step 2: Fetch corresponding chat messages
        messages = db.get_chat_messages_by_ids(unprocessed_ids)
        logger.info(f"Retrieved {len(messages)} messages for processing")

        if not messages:
            return {
                "success": False,
                "error": "Failed to retrieve messages for processing",
                "processed_count": 0,
                "total_unprocessed": len(unprocessed_ids),
            }

        # Step 3: Process messages through the analytics pipeline
        pipeline = ChatAnalyticsPipeline()
        analyzer = MessageAnalyzer()

        processed_count = 0
        processed_message_ids = []

        for idx, message in enumerate(messages, 1):
            try:
                # Parse the message content
                parsed_role, parsed_message = (
                    pipeline.parser.parse_chat_message_content(message["content"])
                )

                # Use parsed message or fall back to original content
                message_text = parsed_message or message["content"]
                role = parsed_role or message["role"]

                # Skip if message is empty
                if not message_text.strip():
                    logger.warning(f"Skipping empty message {message['id']}")
                    processed_message_ids.append(message["id"])
                    continue

                # Analyze the message
                analysis = analyzer.analyze_message(message_text)

                # Save analytics to database
                success = db.save_message_analytics(
                    user_id=message["user_id"],
                    session_id=message["session_id"],
                    message=message_text,
                    role=role,
                    sequence_number=idx,
                    message_length=len(message_text.split()),
                    sentiment_score=analysis["sentiment_score"],
                    sentiment_label=analysis["sentiment_label"],
                    emotion_label=analysis["emotion_label"],
                    toxicity_flag=False,
                    contains_keywords=analysis["contains_keywords"],
                )

                if success:
                    processed_count += 1
                    processed_message_ids.append(message["id"])
                    logger.info(
                        f"Processed message {message['id']}: {analysis['sentiment_label']} sentiment, {analysis['emotion_label']} emotion"
                    )
                else:
                    logger.error(
                        f"Failed to save analytics for message {message['id']}"
                    )

            except Exception as e:
                logger.error(
                    f"Error processing message {message.get('id', 'unknown')}: {e}"
                )
                # Still mark as processed to avoid infinite retry
                processed_message_ids.append(message["id"])
                continue

        # Step 4: Mark processed messages as completed and clear them from log_inserts
        if processed_message_ids:
            mark_success = db.mark_messages_processed(processed_message_ids)
            if not mark_success:
                logger.warning("Failed to mark some messages as processed")

            # Clear processed entries from log_inserts table to keep it clean
            clear_success = db.clear_processed_log_entries()
            if clear_success:
                logger.info(
                    f"Cleared {len(processed_message_ids)} processed entries from log_inserts"
                )
            else:
                logger.warning("Failed to clear processed entries from log_inserts")

        logger.info(
            f"Pipeline completed. Processed {processed_count}/{len(messages)} messages"
        )

        return {
            "success": processed_count > 0,
            "processed_count": processed_count,
            "total_unprocessed": len(unprocessed_ids),
            "total_retrieved": len(messages),
            "marked_processed": len(processed_message_ids),
            "error": (
                None
                if processed_count > 0
                else "No messages were successfully processed"
            ),
        }

    except Exception as e:
        logger.error(f"Error in process_unprocessed_messages pipeline: {e}")
        return {
            "success": False,
            "error": str(e),
            "processed_count": 0,
            "total_unprocessed": 0,
        }


def get_analytics_data() -> Dict[str, Any]:
    """
    Get analytics data for dashboard visualization.
    Only queries message_analytics table.

    Returns:
        Dict containing analytics data for dashboard
    """
    try:
        import sqlite3
        import json
        from collections import Counter

        with sqlite3.connect(db.db_path) as conn:
            cursor = conn.cursor()

            # Get latest analytics (for table display)
            cursor.execute(
                """
                SELECT message, sentiment_label, emotion_label, sentiment_score, 
                       contains_keywords, created_at
                FROM message_analytics 
                ORDER BY created_at DESC 
                LIMIT 50
            """
            )

            latest_analytics = []
            for row in cursor.fetchall():
                keywords = []
                if row[4]:  # contains_keywords
                    try:
                        keywords = json.loads(row[4])
                    except:
                        keywords = []

                latest_analytics.append(
                    {
                        "message": (
                            row[0][:100] + "..." if len(row[0]) > 100 else row[0]
                        ),
                        "sentiment_label": row[1],
                        "emotion_label": row[2],
                        "sentiment_score": row[3],
                        "keywords": keywords,
                        "created_at": row[5],
                    }
                )

            # Get sentiment distribution for bar chart
            cursor.execute(
                """
                SELECT sentiment_label, COUNT(*) as count, AVG(sentiment_score) as avg_score
                FROM message_analytics 
                GROUP BY sentiment_label
                ORDER BY count DESC
            """
            )

            sentiment_data = []
            for row in cursor.fetchall():
                sentiment_data.append(
                    {
                        "sentiment": row[0],
                        "count": row[1],
                        "avg_score": round(row[2], 3) if row[2] else 0,
                    }
                )

            # Get keyword frequency
            cursor.execute(
                """
                SELECT contains_keywords 
                FROM message_analytics 
                WHERE contains_keywords IS NOT NULL AND contains_keywords != ''
            """
            )

            all_keywords = []
            for row in cursor.fetchall():
                try:
                    keywords = json.loads(row[0])
                    if isinstance(keywords, list):
                        all_keywords.extend(keywords)
                except:
                    continue

            keyword_freq = Counter(all_keywords).most_common(20)

            # Get total counts
            cursor.execute("SELECT COUNT(*) FROM message_analytics")
            total_messages = cursor.fetchone()[0]

            return {
                "latest_analytics": latest_analytics,
                "sentiment_data": sentiment_data,
                "keyword_frequency": keyword_freq,
                "total_messages": total_messages,
                "success": True,
            }

    except Exception as e:
        logger.error(f"Error getting analytics data: {e}")
        return {
            "latest_analytics": [],
            "sentiment_data": [],
            "keyword_frequency": [],
            "total_messages": 0,
            "success": False,
            "error": str(e),
        }


# Example usage and testing
if __name__ == "__main__":
    # Example usage
    test_session_id = "room_abc_123"
    result = process_session_analytics(test_session_id)
    print(f"Processing result: {result}")

    # Test unprocessed messages pipeline
    pipeline_result = process_unprocessed_messages()
    print(f"Pipeline result: {pipeline_result}")

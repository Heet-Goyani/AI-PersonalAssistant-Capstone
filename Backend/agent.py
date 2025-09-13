from dotenv import load_dotenv
from livekit import agents
from livekit.agents import AgentSession, Agent, RoomInputOptions
from livekit.plugins import (
    noise_cancellation,
)
from livekit.plugins import google
from prompts import AGENT_INSTRUCTION, SESSION_INSTRUCTION
from tools import (
    get_weather,
    search_web,
    send_email,
    update_user_details,
    get_my_details,
)
import logging
import json
from datetime import datetime
from database import UserDatabase

load_dotenv()

# Initialize database
db = UserDatabase()


class Assistant(Agent):
    def __init__(self) -> None:
        super().__init__(
            instructions=AGENT_INSTRUCTION,
            llm=google.beta.realtime.RealtimeModel(
                voice="Aoede",
                temperature=0.8,
            ),
            tools=[
                get_weather,
                search_web,
                send_email,
                update_user_details,
                get_my_details,
            ],
        )


def extract_user_id_from_context(ctx: agents.JobContext) -> int:
    """Extract user_id from LiveKit room/participant context"""
    user_id = None

    # Try to get user_id from room metadata
    if ctx.room.metadata:
        try:
            metadata = json.loads(ctx.room.metadata)
            user_id = metadata.get("user_id")
            if user_id:
                logging.info(f"Found user_id {user_id} in room metadata")
                return int(user_id)
        except (json.JSONDecodeError, ValueError) as e:
            logging.warning(f"Failed to parse room metadata: {e}")

    # Try to get user_id from participants metadata
    for participant in ctx.room.remote_participants.values():
        try:
            if participant.metadata:
                metadata = json.loads(participant.metadata)
                user_id = metadata.get("user_id")
                if user_id:
                    logging.info(f"Found user_id {user_id} in participant metadata")
                    return int(user_id)
        except (json.JSONDecodeError, ValueError) as e:
            logging.warning(f"Failed to parse participant metadata: {e}")

    # Default fallback - you might want to handle this differently
    logging.warning("No user_id found in context, using default user_id=1")
    return 1


def save_chat_message(
    user_id: int, role: str, content: str, session_id: str = None, metadata: dict = None
):
    """Save chat message to database"""
    try:
        # Use room name as session_id if not provided
        if not session_id:
            session_id = f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

        # Save message to database
        db.save_chat_message(
            user_id=user_id,
            session_id=session_id,
            role=role,
            content=content,
            metadata=json.dumps(metadata) if metadata else None,
        )
        logging.info(f"Saved {role} message to database for user {user_id}")
    except Exception as e:
        logging.error(f"Failed to save chat message: {e}")


async def entrypoint(ctx: agents.JobContext):
    # Extract user_id from context
    user_id = extract_user_id_from_context(ctx)

    # Create session_id based on room name
    session_id = f"room_{ctx.room.name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

    session = AgentSession()

    # Event handler for conversation items (transcriptions/messages)
    @session.on("conversation_item_added")
    def on_conversation_item_added(item):
        """Handle new conversation items (user input, agent responses)"""
        try:
            # Determine the role based on the item type
            if hasattr(item, "role"):
                role = item.role
            elif hasattr(item, "source") and item.source == "user":
                role = "user"
            else:
                role = "assistant"

            # Get the content
            content = ""
            if hasattr(item, "content"):
                content = item.content
            elif hasattr(item, "text"):
                content = item.text
            elif hasattr(item, "message"):
                content = item.message
            else:
                content = str(item)

            # Skip empty content
            if not content.strip():
                return

            # Create metadata
            metadata = {
                "timestamp": datetime.now().isoformat(),
                "room_name": ctx.room.name,
                "item_type": type(item).__name__,
            }

            # Add additional metadata if available
            if hasattr(item, "participant_identity"):
                metadata["participant_identity"] = item.participant_identity
            if hasattr(item, "track_id"):
                metadata["track_id"] = item.track_id
            if hasattr(item, "id"):
                metadata["item_id"] = item.id

            print("\n\n Content ::"+content+"\n\n")
            # Save to database
            save_chat_message(
                user_id=user_id,
                role=role,
                content=content,
                session_id=session_id,
                metadata=json.dumps(metadata),
            )

        except Exception as e:
            logging.error(f"Error handling conversation item: {e}")

    # Additional event handlers for comprehensive transcript capture
    @session.on("user_transcription_completed")
    def on_user_transcription_completed(transcription):
        """Handle completed user transcriptions"""
        try:
            if transcription and transcription.text.strip():
                metadata = {
                    "timestamp": datetime.now().isoformat(),
                    "room_name": ctx.room.name,
                    "event_type": "user_transcription_completed",
                    "confidence": getattr(transcription, "confidence", None),
                    "language": getattr(transcription, "language", None),
                }

                save_chat_message(
                    user_id=user_id,
                    role="user",
                    content=transcription.text,
                    session_id=session_id,
                    metadata=json.dumps(metadata),
                )
        except Exception as e:
            logging.error(f"Error handling user transcription: {e}")

    @session.on("agent_speech_committed")
    def on_agent_speech_committed(speech):
        """Handle committed agent speech"""
        try:
            if speech and speech.text.strip():
                metadata = {
                    "timestamp": datetime.now().isoformat(),
                    "room_name": ctx.room.name,
                    "event_type": "agent_speech_committed",
                }

                save_chat_message(
                    user_id=user_id,
                    role="assistant",
                    content=speech.text,
                    session_id=session_id,
                    metadata=json.dumps(metadata),
                )
        except Exception as e:
            logging.error(f"Error handling agent speech: {e}")

    await session.start(
        room=ctx.room,
        agent=Assistant(),
        room_input_options=RoomInputOptions(
            # LiveKit Cloud enhanced noise cancellation
            # - If self-hosting, omit this parameter
            # - For telephony applications, use `BVCTelephony` for best results
            video_enabled=False,
            noise_cancellation=noise_cancellation.BVC(),
        ),
    )

    await ctx.connect()

    # Log session start
    save_chat_message(
        user_id=user_id,
        role="system",
        content=f"Chat session started in room {ctx.room.name}",
        session_id=session_id,
        metadata={"event": "session_start", "room_name": ctx.room.name},
    )

    try:
        await session.generate_reply(
            instructions=SESSION_INSTRUCTION,
        )
    finally:
        # Log session end when the agent disconnects
        save_chat_message(
            user_id=user_id,
            role="system",
            content=f"Chat session ended in room {ctx.room.name}",
            session_id=session_id,
            metadata={"event": "session_end", "room_name": ctx.room.name},
        )

        # Mark session as ended in database
        try:
            db.end_chat_session(user_id=user_id, session_id=session_id)
        except Exception as e:
            logging.error(f"Failed to end chat session: {e}")


if __name__ == "__main__":
    agents.cli.run_app(agents.WorkerOptions(entrypoint_fnc=entrypoint))

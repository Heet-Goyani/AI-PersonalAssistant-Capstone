import os
import uuid
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
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(hours=JWT_EXPIRATION_HOURS)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return encoded_jwt


def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    try:
        payload = jwt.decode(
            credentials.credentials, JWT_SECRET, algorithms=[JWT_ALGORITHM]
        )
        user_id: int = payload.get("sub")
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return user_id
    except jwt.PyJWTError:
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



@app.get("/")
async def root():
    """Root endpoint"""
    return {"message": "Friday AI Assistant API", "version": "1.0.0", "docs": "/docs"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)

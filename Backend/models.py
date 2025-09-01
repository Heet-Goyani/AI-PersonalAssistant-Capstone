from pydantic import BaseModel
from typing import Optional, Dict, Any


# Pydantic models
class UserCreate(BaseModel):
    name: str
    email: str
    password: str
    timezone: str = "UTC"
    language: str = "en"


class UserLogin(BaseModel):
    email: str
    password: str


class UserDetails(BaseModel):
    phone_number: Optional[str] = None
    email_password: Optional[str] = None
    backup_email: Optional[str] = None
    address: Optional[str] = None


class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    user: Dict[str, Any]


class LiveKitTokenRequest(BaseModel):
    room_name: Optional[str] = None

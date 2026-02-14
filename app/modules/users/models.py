"""User model for MongoDB."""
from typing import Optional
from datetime import datetime
from beanie import Document
from pydantic import EmailStr, Field


class User(Document):
    """User document model."""
    
    email: EmailStr = Field(..., unique=True, index=True)
    username: str = Field(..., unique=True, index=True)
    hashed_password: str
    full_name: Optional[str] = None
    is_active: bool = Field(default=True)
    is_superuser: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Settings:
        """Beanie document settings."""
        name = "users"
        indexes = [
            "email",
            "username",
        ]
    
    class Config:
        """Pydantic config."""
        json_schema_extra = {
            "example": {
                "email": "user@example.com",
                "username": "johndoe",
                "full_name": "John Doe",
                "is_active": True,
                "is_superuser": False,
            }
        }

"""Create user DTO."""
from typing import Optional
from pydantic import BaseModel, EmailStr, Field


class CreateUserRequest(BaseModel):
    """Create user request model."""
    email: EmailStr
    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=8)
    full_name: Optional[str] = None
    is_superuser: bool = Field(default=False)
    
    class Config:
        json_schema_extra = {
            "example": {
                "email": "newuser@example.com",
                "username": "newuser",
                "password": "SecurePass123",
                "full_name": "New User",
                "is_superuser": False
            }
        }


class UpdateUserRequest(BaseModel):
    """Update user request model."""
    email: Optional[EmailStr] = None
    username: Optional[str] = Field(None, min_length=3, max_length=50)
    full_name: Optional[str] = None
    is_active: Optional[bool] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "full_name": "Updated Name",
                "is_active": True
            }
        }

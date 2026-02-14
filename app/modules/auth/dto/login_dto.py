"""Login DTOs."""
from pydantic import BaseModel, EmailStr


class LoginRequest(BaseModel):
    """Login request model."""
    email: EmailStr
    password: str
    
    class Config:
        json_schema_extra = {
            "example": {
                "email": "user@example.com",
                "password": "secretpassword"
            }
        }


class LoginResponse(BaseModel):
    """Login response model."""
    message: str
    user: dict
    
    class Config:
        json_schema_extra = {
            "example": {
                "message": "Login successful",
                "user": {
                    "id": "507f1f77bcf86cd799439011",
                    "email": "user@example.com",
                    "username": "johndoe",
                    "full_name": "John Doe"
                }
            }
        }

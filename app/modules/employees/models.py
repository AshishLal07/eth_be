"""Employee model for MongoDB."""
from typing import Optional
from datetime import datetime
from beanie import Document
from pydantic import EmailStr, Field


class Employee(Document):
    """Employee document model."""
    
    employee_id: str = Field(..., unique=True, index=True)
    full_name: str = Field(..., min_length=2)
    email: EmailStr = Field(..., unique=True, index=True)
    department: str = Field(..., min_length=2)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Settings:
        """Beanie document settings."""
        name = "employees"
        indexes = [
            "employee_id",
            "email",
            "department",
        ]
    
    class Config:
        """Pydantic config."""
        json_schema_extra = {
            "example": {
                "employee_id": "EMP001",
                "full_name": "John Doe",
                "email": "john.doe@example.com",
                "department": "Engineering",
            }
        }

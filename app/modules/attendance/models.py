"""Attendance model for MongoDB."""
from datetime import datetime
from enum import Enum
from beanie import Document
from pydantic import Field, ConfigDict


class AttendanceStatus(str, Enum):
    """Attendance status enum."""
    PRESENT = "present"
    ABSENT = "absent"


class Attendance(Document):
    """Attendance document model."""
    
    model_config = ConfigDict(
        arbitrary_types_allowed=True,
    )
    
    employee_id: str = Field(..., index=True)
    attendance_date: datetime = Field(..., index=True)  # Changed to datetime for MongoDB compatibility
    status: AttendanceStatus
    marked_by: str  # User ID who marked the attendance
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Settings:
        """Beanie document settings."""
        name = "attendance"
        indexes = [
            "employee_id",
            "attendance_date",
            [("employee_id", 1), ("attendance_date", 1)],  # Compound index for uniqueness
        ]

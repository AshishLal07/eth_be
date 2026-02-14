"""Attendance DTOs."""
from datetime import date as date_type
from typing import Optional
from pydantic import BaseModel, EmailStr, Field, validator
from app.modules.attendance.models import AttendanceStatus


class MarkAttendanceRequest(BaseModel):
    """Mark attendance request model."""
    employee_id: str = Field(..., min_length=3)
    attendance_date: date_type
    status: AttendanceStatus
    
    @validator('attendance_date')
    def date_not_future(cls, v):
        """Validate date is not in the future."""
        from datetime import date as dt_date
        if v > dt_date.today():
            raise ValueError('Date cannot be in the future')
        return v
    
    class Config:
        json_schema_extra = {
            "example": {
                "employee_id": "EMP001",
                "date": "2026-02-14",
                "status": "present"
            }
        }


class UpdateAttendanceRequest(BaseModel):
    """Update attendance request model."""
    status: AttendanceStatus
    
    class Config:
        json_schema_extra = {
            "example": {
                "status": "absent"
            }
        }


class AttendanceResponse(BaseModel):
    """Attendance response model."""
    id: str
    employee_id: str
    date: str
    status: str
    marked_by: str
    created_at: str
    updated_at: str
    
    class Config:
        json_schema_extra = {
            "example": {
                "id": "507f1f77bcf86cd799439011",
                "employee_id": "EMP001",
                "date": "2026-02-14",
                "status": "present",
                "marked_by": "507f1f77bcf86cd799439012",
                "created_at": "2026-02-14T12:00:00",
                "updated_at": "2026-02-14T12:00:00"
            }
        }


class AttendanceQueryParams(BaseModel):
    """Attendance query parameters."""
    employee_id: Optional[str] = None
    start_date: Optional[date_type] = None
    end_date: Optional[date_type] = None
    status: Optional[AttendanceStatus] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "employee_id": "EMP001",
                "start_date": "2026-02-01",
                "end_date": "2026-02-14",
                "status": "present"
            }
        }

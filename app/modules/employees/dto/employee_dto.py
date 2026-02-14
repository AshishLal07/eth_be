"""Employee DTOs."""
from typing import Optional
from pydantic import BaseModel, EmailStr, Field, validator


class CreateEmployeeRequest(BaseModel):
    """Create employee request model."""
    employee_id: str = Field(..., min_length=3, max_length=50)
    full_name: str = Field(..., min_length=2, max_length=100)
    email: EmailStr
    department: str = Field(..., min_length=2, max_length=100)
    
    @validator('employee_id')
    def employee_id_format(cls, v):
        """Validate employee ID format."""
        if not v.replace('-', '').replace('_', '').isalnum():
            raise ValueError('Employee ID must be alphanumeric (- and _ allowed)')
        return v.upper()  # Normalize to uppercase
    
    class Config:
        json_schema_extra = {
            "example": {
                "employee_id": "EMP001",
                "full_name": "John Doe",
                "email": "john.doe@example.com",
                "department": "Engineering"
            }
        }


class UpdateEmployeeRequest(BaseModel):
    """Update employee request model."""
    full_name: Optional[str] = Field(None, min_length=2, max_length=100)
    email: Optional[EmailStr] = None
    department: Optional[str] = Field(None, min_length=2, max_length=100)
    
    class Config:
        json_schema_extra = {
            "example": {
                "full_name": "John Smith",
                "department": "Product"
            }
        }


class EmployeeResponse(BaseModel):
    """Employee response model."""
    id: str
    employee_id: str
    full_name: str
    email: str
    department: str
    created_at: str
    updated_at: str
    
    class Config:
        json_schema_extra = {
            "example": {
                "id": "507f1f77bcf86cd799439011",
                "employee_id": "EMP001",
                "full_name": "John Doe",
                "email": "john.doe@example.com",
                "department": "Engineering",
                "created_at": "2026-02-14T12:00:00",
                "updated_at": "2026-02-14T12:00:00"
            }
        }

"""Attendance controller with API endpoints."""
from typing import List, Optional
from datetime import date as date_type
from fastapi import APIRouter, HTTPException, status, Depends, Query
from app.modules.attendance.dto.attendance_dto import (
    MarkAttendanceRequest,
    UpdateAttendanceRequest,
    AttendanceResponse
)
from app.modules.attendance.attendance_service import AttendanceService
from app.modules.attendance.models import AttendanceStatus
from app.common.guards import get_current_superuser
from app.common.pipes import PaginationParams
from app.modules.users.models import User

router = APIRouter()


@router.post("/mark", response_model=AttendanceResponse, status_code=status.HTTP_201_CREATED)
async def mark_attendance(
    request: MarkAttendanceRequest,
    current_user: User = Depends(get_current_superuser)
):
    """
    Mark attendance for an employee (admin only).
    
    Args:
        request: Attendance marking request
        current_user: Current superuser
        
    Returns:
        Created attendance record
        
    Raises:
        HTTPException: If employee not found or duplicate attendance
    """
    try:
        print("Marking attendance for employee:", request)
        attendance = await AttendanceService.mark_attendance(
            employee_id=request.employee_id,
            attendance_date=request.attendance_date,
            status=request.status,
            marked_by_user_id=str(current_user.id)
        )
        
        return AttendanceResponse(
            id=str(attendance.id),
            employee_id=attendance.employee_id,
            date=attendance.attendance_date.isoformat(),
            status=attendance.status.value,
            marked_by=attendance.marked_by,
            created_at=attendance.created_at.isoformat(),
            updated_at=attendance.updated_at.isoformat()
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/", response_model=List[AttendanceResponse])
async def get_attendance_records(
    employee_id: Optional[str] = Query(None, description="Filter by employee ID"),
    start_date: Optional[date_type] = Query(None, description="Filter from date"),
    end_date: Optional[date_type] = Query(None, description="Filter to date"),
    status: Optional[AttendanceStatus] = Query(None, description="Filter by status"),
    pagination: PaginationParams = Depends(),
    current_user: User = Depends(get_current_superuser)
):
    """
    Get attendance records with optional filters (admin only).
    
    Args:
        employee_id: Optional employee ID filter
        start_date: Optional start date filter
        end_date: Optional end date filter
        status: Optional status filter
        pagination: Pagination parameters
        current_user: Current superuser
        
    Returns:
        List of attendance records
    """
    records = await AttendanceService.get_attendance_by_filters(
        employee_id=employee_id,
        start_date=start_date,
        end_date=end_date,
        status=status,
        skip=pagination.skip,
        limit=pagination.limit
    )
    
    return [
        AttendanceResponse(
            id=str(rec.id),
            employee_id=rec.employee_id,
            date=rec.attendance_date.isoformat(),
            status=rec.status.value,
            marked_by=rec.marked_by,
            created_at=rec.created_at.isoformat(),
            updated_at=rec.updated_at.isoformat()
        )
        for rec in records
    ]


@router.get("/employee/{employee_id}", response_model=List[AttendanceResponse])
async def get_employee_attendance(
    employee_id: str,
    pagination: PaginationParams = Depends(),
    current_user: User = Depends(get_current_superuser)
):
    """
    Get all attendance records for a specific employee (admin only).
    
    Args:
        employee_id: Employee ID
        pagination: Pagination parameters
        current_user: Current superuser
        
    Returns:
        List of attendance records for the employee
    """
    records = await AttendanceService.get_attendance_by_employee(
        employee_id=employee_id,
        skip=pagination.skip,
        limit=pagination.limit
    )
    
    return [
        AttendanceResponse(
            id=str(rec.id),
            employee_id=rec.employee_id,
            date=rec.attendance_date.isoformat(),
            status=rec.status.value,
            marked_by=rec.marked_by,
            created_at=rec.created_at.isoformat(),
            updated_at=rec.updated_at.isoformat()
        )
        for rec in records
    ]


@router.get("/date/{attendance_date}", response_model=List[AttendanceResponse])
async def get_attendance_by_date(
    attendance_date: date_type,
    pagination: PaginationParams = Depends(),
    current_user: User = Depends(get_current_superuser)
):
    """
    Get all attendance records for a specific date (admin only).
    
    Args:
        attendance_date: Attendance date
        pagination: Pagination parameters
        current_user: Current superuser
        
    Returns:
        List of attendance records for the date
    """
    records = await AttendanceService.get_attendance_by_date(
        attendance_date=attendance_date,
        skip=pagination.skip,
        limit=pagination.limit
    )
    
    return [
        AttendanceResponse(
            id=str(rec.id),
            employee_id=rec.employee_id,
            date=rec.attendance_date.isoformat(),
            status=rec.status.value,
            marked_by=rec.marked_by,
            created_at=rec.created_at.isoformat(),
            updated_at=rec.updated_at.isoformat()
        )
        for rec in records
    ]


@router.put("/{attendance_id}", response_model=AttendanceResponse)
async def update_attendance(
    attendance_id: str,
    request: UpdateAttendanceRequest,
    current_user: User = Depends(get_current_superuser)
):
    """
    Update an attendance record (admin only).
    
    Args:
        attendance_id: Attendance record MongoDB ID
        request: Update request
        current_user: Current superuser
        
    Returns:
        Updated attendance record
        
    Raises:
        HTTPException: If attendance record not found
    """
    update_data = request.model_dump(exclude_unset=True)
    attendance = await AttendanceService.update_attendance(attendance_id, update_data)
    
    if not attendance:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Attendance record not found"
        )
    
    return AttendanceResponse(
        id=str(attendance.id),
        employee_id=attendance.employee_id,
        date=attendance.attendance_date.isoformat(),
        status=attendance.status.value,
        marked_by=attendance.marked_by,
        created_at=attendance.created_at.isoformat(),
        updated_at=attendance.updated_at.isoformat()
    )


@router.delete("/{attendance_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_attendance(
    attendance_id: str,
    current_user: User = Depends(get_current_superuser)
):
    """
    Delete an attendance record (admin only).
    
    Args:
        attendance_id: Attendance record MongoDB ID
        current_user: Current superuser
        
    Raises:
        HTTPException: If attendance record not found
    """
    deleted = await AttendanceService.delete_attendance(attendance_id)
    
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Attendance record not found"
        )

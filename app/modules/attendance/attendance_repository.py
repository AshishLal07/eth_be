"""Attendance repository for data access."""
from typing import List, Optional
from datetime import date as date_type, datetime
from beanie import PydanticObjectId
from app.modules.attendance.models import Attendance, AttendanceStatus


class AttendanceRepository:
    """Repository for attendance-related database operations."""
    
    @staticmethod
    async def get_all_attendance(skip: int = 0, limit: int = 100) -> List[Attendance]:
        """
        Get all attendance records with pagination.
        
        Args:
            skip: Number of records to skip
            limit: Maximum number of records to return
            
        Returns:
            List of attendance records
        """
        records = await Attendance.find_all().skip(skip).limit(limit).to_list()
        return records
    
    @staticmethod
    async def get_attendance_by_id(attendance_id: str) -> Optional[Attendance]:
        """
        Get an attendance record by ID.
        
        Args:
            attendance_id: Attendance record MongoDB ID
            
        Returns:
            Attendance object if found, None otherwise
        """
        try:
            return await Attendance.get(PydanticObjectId(attendance_id))
        except Exception:
            return None
    
    @staticmethod
    async def get_attendance_by_employee_and_date(
        employee_id: str,
        attendance_date: datetime
    ) -> Optional[Attendance]:
        """
        Get attendance record for an employee on a specific date.
        
        Args:
            employee_id: Employee ID
            attendance_date: Attendance date
            
        Returns:
            Attendance object if found, None otherwise
        """
        return await Attendance.find_one(
            {
                "employee_id": employee_id.upper(),
                "attendance_date": attendance_date
            }
        )
    
    @staticmethod
    async def get_attendance_by_employee(
        employee_id: str,
        skip: int = 0,
        limit: int = 100
    ) -> List[Attendance]:
        """
        Get all attendance records for an employee.
        
        Args:
            employee_id: Employee ID
            skip: Number of records to skip
            limit: Maximum number of records to return
            
        Returns:
            List of attendance records
        """
        records = await Attendance.find(
            Attendance.employee_id == employee_id.upper()
        ).skip(skip).limit(limit).to_list()
        return records
    
    @staticmethod
    async def get_attendance_by_date(
        attendance_date: datetime,
        skip: int = 0,
        limit: int = 100
    ) -> List[Attendance]:
        """
        Get all attendance records for a specific date.
        
        Args:
            attendance_date: Attendance date
            skip: Number of records to skip
            limit: Maximum number of records to return
            
        Returns:
            List of attendance records
        """
        records = await Attendance.find(
            Attendance.attendance_date == attendance_date
        ).skip(skip).limit(limit).to_list()
        return records
    
    @staticmethod
    async def get_attendance_by_filters(
        employee_id: Optional[str] = None,
        start_date: Optional[date_type] = None,
        end_date: Optional[date_type] = None,
        status: Optional[AttendanceStatus] = None,
        skip: int = 0,
        limit: int = 100
    ) -> List[Attendance]:
        """
        Get attendance records with filters.
        
        Args:
            employee_id: Optional employee ID filter
            start_date: Optional start date filter
            end_date: Optional end date filter
            status: Optional status filter
            skip: Number of records to skip
            limit: Maximum number of records to return
            
        Returns:
            List of attendance records
        """
        query = {}
        
        if employee_id:
            query[Attendance.employee_id] = employee_id.upper()
        
        if start_date and end_date:
            query[Attendance.attendance_date] = {"$gte": start_date, "$lte": end_date}
        elif start_date:
            query[Attendance.attendance_date] = {"$gte": start_date}
        elif end_date:
            query[Attendance.attendance_date] = {"$lte": end_date}
        
        if status:
            query[Attendance.status] = status
        
        if query:
            records = await Attendance.find(query).skip(skip).limit(limit).to_list()
        else:
            records = await AttendanceRepository.get_all_attendance(skip, limit)
        
        return records
    
    @staticmethod
    async def update_attendance(attendance_id: str, update_data: dict) -> Optional[Attendance]:
        """
        Update an attendance record.
        
        Args:
            attendance_id: Attendance record MongoDB ID
            update_data: Dictionary of fields to update
            
        Returns:
            Updated attendance object if found, None otherwise
        """
        attendance = await AttendanceRepository.get_attendance_by_id(attendance_id)
        if not attendance:
            return None
        
        # Update fields
        for key, value in update_data.items():
            if value is not None and hasattr(attendance, key):
                setattr(attendance, key, value)
        
        await attendance.save()
        return attendance
    
    @staticmethod
    async def delete_attendance(attendance_id: str) -> bool:
        """
        Delete an attendance record.
        
        Args:
            attendance_id: Attendance record MongoDB ID
            
        Returns:
            True if deleted, False otherwise
        """
        attendance = await AttendanceRepository.get_attendance_by_id(attendance_id)
        if not attendance:
            return False
        
        await attendance.delete()
        return True

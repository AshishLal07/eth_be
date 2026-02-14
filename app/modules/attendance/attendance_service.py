"""Attendance service with business logic."""
from typing import List, Optional
from datetime import date as date_type, datetime
from app.modules.attendance.models import Attendance, AttendanceStatus
from app.modules.attendance.attendance_repository import AttendanceRepository
from app.modules.employees.employees_repository import EmployeesRepository


class AttendanceService:
    """Service for attendance management business logic."""
    
    @staticmethod
    async def mark_attendance(
        employee_id: str,
        attendance_date: date_type,
        status: AttendanceStatus,
        marked_by_user_id: str
    ) -> Attendance:
        """
        Mark attendance for an employee.
        
        Args:
            employee_id: Employee ID
            attendance_date: Attendance date
            status: Attendance status (present/absent)
            marked_by_user_id: User ID who is marking attendance
            
        Returns:
            Created attendance record
            
        Raises:
            ValueError: If employee doesn't exist or duplicate attendance
        """
        # Verify employee exists
        employee = await EmployeesRepository.get_employee_by_employee_id(employee_id)
        if not employee:
            raise ValueError(f"Employee '{employee_id}' not found")
        
        
        # Check for duplicate attendance - convert date to datetime
        attendance_datetime = datetime.combine(attendance_date, datetime.min.time())
        existing = await AttendanceRepository.get_attendance_by_employee_and_date(
            employee_id=employee_id,
            attendance_date=attendance_datetime
        )
        print("Existing attendance:", existing)

        
        if existing:
            raise ValueError(
                f"Attendance already marked for employee '{employee_id}' on {attendance_date}"
            )
        
        # Create attendance record - convert date to datetime for MongoDB
        attendance_datetime = datetime.combine(attendance_date, datetime.min.time())
        attendance = Attendance(
            employee_id=employee_id.upper(),
            attendance_date=attendance_datetime,
            status=status,
            marked_by=marked_by_user_id
        )
        print("Attendance created:", attendance)
        await attendance.insert()
        return attendance
    
    @staticmethod
    async def get_all_attendance(skip: int = 0, limit: int = 100) -> List[Attendance]:
        """
        Get all attendance records.
        
        Args:
            skip: Number of records to skip
            limit: Maximum number of records to return
            
        Returns:
            List of attendance records
        """
        return await AttendanceRepository.get_all_attendance(skip, limit)
    
    @staticmethod
    async def get_attendance_by_employee(
        employee_id: str,
        skip: int = 0,
        limit: int = 100
    ) -> List[Attendance]:
        """
        Get attendance records for a specific employee.
        
        Args:
            employee_id: Employee ID
            skip: Number of records to skip
            limit: Maximum number of records to return
            
        Returns:
            List of attendance records
        """
        return await AttendanceRepository.get_attendance_by_employee(
            employee_id, skip, limit
        )
    
    @staticmethod
    async def get_attendance_by_date(
        attendance_date: date_type,
        skip: int = 0,
        limit: int = 100
    ) -> List[Attendance]:
        """
        Get attendance records for a specific date.
        
        Args:
            attendance_date: Attendance date
            skip: Number of records to skip
            limit: Maximum number of records to return
            
        Returns:
            List of attendance records
        """
        return await AttendanceRepository.get_attendance_by_date(
            attendance_date, skip, limit
        )
    
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
        return await AttendanceRepository.get_attendance_by_filters(
            employee_id=employee_id,
            start_date=start_date,
            end_date=end_date,
            status=status,
            skip=skip,
            limit=limit
        )
    
    @staticmethod
    async def update_attendance(
        attendance_id: str,
        update_data: dict
    ) -> Optional[Attendance]:
        """
        Update an attendance record.
        
        Args:
            attendance_id: Attendance record MongoDB ID
            update_data: Dictionary of fields to update
            
        Returns:
            Updated attendance object if found, None otherwise
        """
        # Add updated_at timestamp
        update_data['updated_at'] = datetime.utcnow()
        return await AttendanceRepository.update_attendance(attendance_id, update_data)
    
    @staticmethod
    async def delete_attendance(attendance_id: str) -> bool:
        """
        Delete an attendance record.
        
        Args:
            attendance_id: Attendance record MongoDB ID
            
        Returns:
            True if deleted, False otherwise
        """
        return await AttendanceRepository.delete_attendance(attendance_id)

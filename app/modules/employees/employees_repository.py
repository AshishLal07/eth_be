"""Employees repository for data access."""
from typing import List, Optional
from beanie import PydanticObjectId
from app.modules.employees.models import Employee


class EmployeesRepository:
    """Repository for employee-related database operations."""
    
    @staticmethod
    async def get_all_employees(skip: int = 0, limit: int = 100) -> List[Employee]:
        """
        Get all employees with pagination.
        
        Args:
            skip: Number of records to skip
            limit: Maximum number of records to return
            
        Returns:
            List of employees
        """
        employees = await Employee.find_all().skip(skip).limit(limit).to_list()
        return employees
    
    @staticmethod
    async def get_employee_by_id(employee_id: str) -> Optional[Employee]:
        """
        Get an employee by MongoDB ID.
        
        Args:
            employee_id: MongoDB document ID
            
        Returns:
            Employee object if found, None otherwise
        """
        try:
            return await Employee.get(PydanticObjectId(employee_id))
        except Exception:
            return None
    
    @staticmethod
    async def get_employee_by_employee_id(employee_id: str) -> Optional[Employee]:
        """
        Get an employee by employee ID.
        
        Args:
            employee_id: Employee ID (e.g., EMP001)
            
        Returns:
            Employee object if found, None otherwise
        """
        return await Employee.find_one(Employee.employee_id == employee_id.upper())
    
    @staticmethod
    async def get_employee_by_email(email: str) -> Optional[Employee]:
        """
        Get an employee by email.
        
        Args:
            email: Employee email
            
        Returns:
            Employee object if found, None otherwise
        """
        return await Employee.find_one(Employee.email == email)
    
    @staticmethod
    async def employee_exists(employee_id: str = None, email: str = None) -> bool:
        """
        Check if an employee exists by employee_id or email.
        
        Args:
            employee_id: Optional employee ID to check
            email: Optional email to check
            
        Returns:
            True if employee exists, False otherwise
        """
        if employee_id:
            emp = await EmployeesRepository.get_employee_by_employee_id(employee_id)
            if emp:
                return True
        
        if email:
            emp = await EmployeesRepository.get_employee_by_email(email)
            if emp:
                return True
        
        return False
    
    @staticmethod
    async def update_employee(employee_id: str, update_data: dict) -> Optional[Employee]:
        """
        Update an employee.
        
        Args:
            employee_id: MongoDB document ID
            update_data: Dictionary of fields to update
            
        Returns:
            Updated employee object if found, None otherwise
        """
        employee = await EmployeesRepository.get_employee_by_id(employee_id)
        if not employee:
            return None
        
        # Update fields
        for key, value in update_data.items():
            if value is not None and hasattr(employee, key):
                setattr(employee, key, value)
        
        await employee.save()
        return employee
    
    @staticmethod
    async def delete_employee(employee_id: str) -> bool:
        """
        Delete an employee.
        
        Args:
            employee_id: MongoDB document ID
            
        Returns:
            True if deleted, False otherwise
        """
        employee = await EmployeesRepository.get_employee_by_id(employee_id)
        if not employee:
            return False
        
        await employee.delete()
        return True

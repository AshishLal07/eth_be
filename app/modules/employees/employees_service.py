"""Employees service with business logic."""
from typing import List, Optional
from datetime import datetime
from app.modules.employees.models import Employee
from app.modules.employees.employees_repository import EmployeesRepository


class EmployeesService:
    """Service for employee management business logic."""
    
    @staticmethod
    async def get_all_employees(skip: int = 0, limit: int = 100) -> List[Employee]:
        """
        Get all employees.
        
        Args:
            skip: Number of records to skip
            limit: Maximum number of records to return
            
        Returns:
            List of employees
        """
        return await EmployeesRepository.get_all_employees(skip, limit)
    
    @staticmethod
    async def get_employee_by_id(employee_id: str) -> Optional[Employee]:
        """
        Get an employee by ID.
        
        Args:
            employee_id: MongoDB document ID
            
        Returns:
            Employee object if found, None otherwise
        """
        return await EmployeesRepository.get_employee_by_id(employee_id)
    
    @staticmethod
    async def get_employee_by_employee_id(employee_id: str) -> Optional[Employee]:
        """
        Get an employee by employee ID.
        
        Args:
            employee_id: Employee ID (e.g., EMP001)
            
        Returns:
            Employee object if found, None otherwise
        """
        return await EmployeesRepository.get_employee_by_employee_id(employee_id)
    
    @staticmethod
    async def create_employee(
        employee_id: str,
        full_name: str,
        email: str,
        department: str
    ) -> Employee:
        """
        Create a new employee.
        
        Args:
            employee_id: Unique employee identifier
            full_name: Employee full name
            email: Employee email
            department: Department name
            
        Returns:
            Created employee object
        """
        employee = Employee(
            employee_id=employee_id.upper(),
            full_name=full_name,
            email=email,
            department=department
        )
        await employee.insert()
        return employee
    
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
        # Add updated_at timestamp
        update_data['updated_at'] = datetime.utcnow()
        return await EmployeesRepository.update_employee(employee_id, update_data)
    
    @staticmethod
    async def delete_employee(employee_id: str) -> bool:
        """
        Delete an employee.
        
        Args:
            employee_id: MongoDB document ID
            
        Returns:
            True if deleted, False otherwise
        """
        return await EmployeesRepository.delete_employee(employee_id)

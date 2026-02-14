"""Employees controller with API endpoints."""
from typing import List
from fastapi import APIRouter, HTTPException, status, Depends
from app.modules.employees.dto.employee_dto import (
    CreateEmployeeRequest,
    UpdateEmployeeRequest,
    EmployeeResponse
)
from app.modules.employees.employees_service import EmployeesService
from app.modules.employees.employees_repository import EmployeesRepository
from app.common.guards import get_current_superuser
from app.common.pipes import PaginationParams
from app.modules.users.models import User

router = APIRouter()


@router.post("/", response_model=EmployeeResponse, status_code=status.HTTP_201_CREATED)
async def create_employee(
    request: CreateEmployeeRequest,
    current_user: User = Depends(get_current_superuser)
):
    """
    Create a new employee (admin only).
    
    Args:
        request: Employee creation request
        current_user: Current superuser
        
    Returns:
        Created employee data
        
    Raises:
        HTTPException: If employee_id or email already exists
    """
    # Check if employee already exists
    if await EmployeesRepository.employee_exists(employee_id=request.employee_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Employee ID '{request.employee_id}' already exists"
        )
    
    if await EmployeesRepository.employee_exists(email=request.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Email '{request.email}' already registered"
        )
    
    # Create employee
    employee = await EmployeesService.create_employee(
        employee_id=request.employee_id,
        full_name=request.full_name,
        email=request.email,
        department=request.department
    )
    
    return EmployeeResponse(
        id=str(employee.id),
        employee_id=employee.employee_id,
        full_name=employee.full_name,
        email=employee.email,
        department=employee.department,
        created_at=employee.created_at.isoformat(),
        updated_at=employee.updated_at.isoformat()
    )


@router.get("/", response_model=List[EmployeeResponse])
async def get_all_employees(
    pagination: PaginationParams = Depends(),
    current_user: User = Depends(get_current_superuser)
):
    """
    Get all employees (admin only).
    
    Args:
        pagination: Pagination parameters
        current_user: Current superuser
        
    Returns:
        List of employees
    """
    employees = await EmployeesService.get_all_employees(
        skip=pagination.skip,
        limit=pagination.limit
    )
    
    return [
        EmployeeResponse(
            id=str(emp.id),
            employee_id=emp.employee_id,
            full_name=emp.full_name,
            email=emp.email,
            department=emp.department,
            created_at=emp.created_at.isoformat(),
            updated_at=emp.updated_at.isoformat()
        )
        for emp in employees
    ]


@router.get("/{employee_id}", response_model=EmployeeResponse)
async def get_employee_by_id(
    employee_id: str,
    current_user: User = Depends(get_current_superuser)
):
    """
    Get employee by ID (admin only).
    
    Args:
        employee_id: Employee MongoDB ID
        current_user: Current superuser
        
    Returns:
        Employee data
        
    Raises:
        HTTPException: If employee not found
    """
    employee = await EmployeesService.get_employee_by_id(employee_id)
    
    if not employee:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Employee not found"
        )
    
    return EmployeeResponse(
        id=str(employee.id),
        employee_id=employee.employee_id,
        full_name=employee.full_name,
        email=employee.email,
        department=employee.department,
        created_at=employee.created_at.isoformat(),
        updated_at=employee.updated_at.isoformat()
    )


@router.put("/{employee_id}", response_model=EmployeeResponse)
async def update_employee(
    employee_id: str,
    request: UpdateEmployeeRequest,
    current_user: User = Depends(get_current_superuser)
):
    """
    Update employee (admin only).
    
    Args:
        employee_id: Employee MongoDB ID
        request: Update request
        current_user: Current superuser
        
    Returns:
        Updated employee data
        
    Raises:
        HTTPException: If employee not found or email already exists
    """
    # Check if email is being updated and already exists
    if request.email:
        existing = await EmployeesRepository.get_employee_by_email(request.email)
        if existing and str(existing.id) != employee_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Email '{request.email}' already registered"
            )
    
    update_data = request.model_dump(exclude_unset=True)
    employee = await EmployeesService.update_employee(employee_id, update_data)
    
    if not employee:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Employee not found"
        )
    
    return EmployeeResponse(
        id=str(employee.id),
        employee_id=employee.employee_id,
        full_name=employee.full_name,
        email=employee.email,
        department=employee.department,
        created_at=employee.created_at.isoformat(),
        updated_at=employee.updated_at.isoformat()
    )


@router.delete("/{employee_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_employee(
    employee_id: str,
    current_user: User = Depends(get_current_superuser)
):
    """
    Delete employee (admin only).
    
    Args:
        employee_id: Employee MongoDB ID
        current_user: Current superuser
        
    Raises:
        HTTPException: If employee not found
    """
    deleted = await EmployeesService.delete_employee(employee_id)
    
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Employee not found"
        )

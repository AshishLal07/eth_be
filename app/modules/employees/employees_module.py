"""Employees module configuration."""
from fastapi import APIRouter
from app.modules.employees import employees_controller


def get_employees_router() -> APIRouter:
    """
    Get the employees module router.
    
    Returns:
        Configured employees router
    """
    router = APIRouter(prefix="/employees", tags=["Employees"])
    router.include_router(employees_controller.router)
    return router

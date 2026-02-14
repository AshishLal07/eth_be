"""Attendance module configuration."""
from fastapi import APIRouter
from app.modules.attendance import attendance_controller


def get_attendance_router() -> APIRouter:
    """
    Get the attendance module router.
    
    Returns:
        Configured attendance router
    """
    router = APIRouter(prefix="/attendance", tags=["Attendance"])
    router.include_router(attendance_controller.router)
    return router

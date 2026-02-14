"""Auth module configuration."""
from fastapi import APIRouter
from app.modules.auth import auth_controller


def get_auth_router() -> APIRouter:
    """
    Get the auth module router.
    
    Returns:
        Configured auth router
    """
    router = APIRouter(prefix="/auth", tags=["Authentication"])
    router.include_router(auth_controller.router)
    return router

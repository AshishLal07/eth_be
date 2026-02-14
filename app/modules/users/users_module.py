"""Users module configuration."""
from fastapi import APIRouter
from app.modules.users import users_controller


def get_users_router() -> APIRouter:
    """
    Get the users module router.
    
    Returns:
        Configured users router
    """
    router = APIRouter(prefix="/users", tags=["Users"])
    router.include_router(users_controller.router)
    return router

"""Users controller with API endpoints."""
from typing import List
from fastapi import APIRouter, HTTPException, status, Depends
from app.modules.users.dto.create_user_dto import CreateUserRequest, UpdateUserRequest
from app.modules.users.dto.user_response_dto import UserResponse
from app.modules.users.users_service import UsersService
from app.common.guards import get_current_active_user, get_current_superuser
from app.common.pipes import PaginationParams
from app.modules.users.models import User

router = APIRouter()


@router.get("/me", response_model=UserResponse)
async def get_current_user(current_user: User = Depends(get_current_active_user)):
    """
    Get current authenticated user.
    
    Args:
        current_user: Current user from JWT token
        
    Returns:
        Current user data
    """
    return UserResponse(
        id=str(current_user.id),
        email=current_user.email,
        username=current_user.username,
        full_name=current_user.full_name,
        is_active=current_user.is_active,
        is_superuser=current_user.is_superuser,
        created_at=current_user.created_at,
        updated_at=current_user.updated_at
    )


@router.get("/", response_model=List[UserResponse])
async def get_all_users(
    pagination: PaginationParams = Depends(),
    current_user: User = Depends(get_current_superuser)
):
    """
    Get all users (admin only).
    
    Args:
        pagination: Pagination parameters
        current_user: Current superuser
        
    Returns:
        List of users
    """
    users = await UsersService.get_all_users(
        skip=pagination.skip,
        limit=pagination.limit
    )
    
    return [
        UserResponse(
            id=str(user.id),
            email=user.email,
            username=user.username,
            full_name=user.full_name,
            is_active=user.is_active,
            is_superuser=user.is_superuser,
            created_at=user.created_at,
            updated_at=user.updated_at
        )
        for user in users
    ]


@router.get("/{user_id}", response_model=UserResponse)
async def get_user_by_id(
    user_id: str,
    current_user: User = Depends(get_current_active_user)
):
    """
    Get user by ID.
    
    Args:
        user_id: User ID
        current_user: Current authenticated user
        
    Returns:
        User data
        
    Raises:
        HTTPException: If user not found
    """
    user = await UsersService.get_user_by_id(user_id)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return UserResponse(
        id=str(user.id),
        email=user.email,
        username=user.username,
        full_name=user.full_name,
        is_active=user.is_active,
        is_superuser=user.is_superuser,
        created_at=user.created_at,
        updated_at=user.updated_at
    )


@router.put("/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: str,
    request: UpdateUserRequest,
    current_user: User = Depends(get_current_active_user)
):
    """
    Update user.
    
    Args:
        user_id: User ID
        request: Update request
        current_user: Current authenticated user
        
    Returns:
        Updated user data
        
    Raises:
        HTTPException: If user not found or no permission
    """
    # Only allow users to update themselves unless they're superuser
    if str(current_user.id) != user_id and not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    update_data = request.model_dump(exclude_unset=True)
    user = await UsersService.update_user(user_id, update_data)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return UserResponse(
        id=str(user.id),
        email=user.email,
        username=user.username,
        full_name=user.full_name,
        is_active=user.is_active,
        is_superuser=user.is_superuser,
        created_at=user.created_at,
        updated_at=user.updated_at
    )


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: str,
    current_user: User = Depends(get_current_superuser)
):
    """
    Delete user (admin only).
    
    Args:
        user_id: User ID
        current_user: Current superuser
        
    Raises:
        HTTPException: If user not found
    """
    deleted = await UsersService.delete_user(user_id)
    
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

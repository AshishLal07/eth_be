"""Users repository for data access."""
from typing import List, Optional
from beanie import PydanticObjectId
from app.modules.users.models import User


class UsersRepository:
    """Repository for user-related database operations."""
    
    @staticmethod
    async def get_all_users(skip: int = 0, limit: int = 100) -> List[User]:
        """
        Get all users with pagination.
        
        Args:
            skip: Number of records to skip
            limit: Maximum number of records to return
            
        Returns:
            List of users
        """
        users = await User.find_all().skip(skip).limit(limit).to_list()
        return users
    
    @staticmethod
    async def get_user_by_id(user_id: str) -> Optional[User]:
        """
        Get a user by ID.
        
        Args:
            user_id: User ID
            
        Returns:
            User object if found, None otherwise
        """
        try:
            return await User.get(PydanticObjectId(user_id))
        except Exception:
            return None
    
    @staticmethod
    async def update_user(user_id: str, update_data: dict) -> Optional[User]:
        """
        Update a user.
        
        Args:
            user_id: User ID
            update_data: Dictionary of fields to update
            
        Returns:
            Updated user object if found, None otherwise
        """
        user = await UsersRepository.get_user_by_id(user_id)
        if not user:
            return None
        
        # Update fields
        for key, value in update_data.items():
            if value is not None and hasattr(user, key):
                setattr(user, key, value)
        
        await user.save()
        return user
    
    @staticmethod
    async def delete_user(user_id: str) -> bool:
        """
        Delete a user.
        
        Args:
            user_id: User ID
            
        Returns:
            True if deleted, False otherwise
        """
        user = await UsersRepository.get_user_by_id(user_id)
        if not user:
            return False
        
        await user.delete()
        return True

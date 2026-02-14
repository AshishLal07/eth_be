"""Users service with business logic."""
from typing import List, Optional
from datetime import datetime
from app.modules.users.models import User
from app.modules.users.users_repository import UsersRepository
from app.modules.auth.auth_service import AuthService


class UsersService:
    """Service for user management business logic."""
    
    @staticmethod
    async def get_all_users(skip: int = 0, limit: int = 100) -> List[User]:
        """
        Get all users.
        
        Args:
            skip: Number of records to skip
            limit: Maximum number of records to return
            
        Returns:
            List of users
        """
        return await UsersRepository.get_all_users(skip, limit)
    
    @staticmethod
    async def get_user_by_id(user_id: str) -> Optional[User]:
        """
        Get a user by ID.
        
        Args:
            user_id: User ID
            
        Returns:
            User object if found, None otherwise
        """
        return await UsersRepository.get_user_by_id(user_id)
    
    @staticmethod
    async def create_user(
        email: str,
        username: str,
        password: str,
        full_name: Optional[str] = None,
        is_superuser: bool = False
    ) -> User:
        """
        Create a new user.
        
        Args:
            email: User email
            username: Username
            password: Plain text password
            full_name: Optional full name
            is_superuser: Whether user is a superuser
            
        Returns:
            Created user object
        """
        hashed_password = AuthService.get_password_hash(password)
        user = User(
            email=email,
            username=username,
            hashed_password=hashed_password,
            full_name=full_name,
            is_superuser=is_superuser
        )
        await user.insert()
        return user
    
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
        # Add updated_at timestamp
        update_data['updated_at'] = datetime.utcnow()
        return await UsersRepository.update_user(user_id, update_data)
    
    @staticmethod
    async def delete_user(user_id: str) -> bool:
        """
        Delete a user.
        
        Args:
            user_id: User ID
            
        Returns:
            True if deleted, False otherwise
        """
        return await UsersRepository.delete_user(user_id)

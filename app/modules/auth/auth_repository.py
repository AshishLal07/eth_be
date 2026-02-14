"""Authentication repository for data access."""
from typing import Optional
from app.modules.users.models import User


class AuthRepository:
    """Repository for authentication-related database operations."""
    
    @staticmethod
    async def find_user_by_email(email: str) -> Optional[User]:
        """
        Find a user by email.
        
        Args:
            email: User email
            
        Returns:
            User object if found, None otherwise
        """
        return await User.find_one(User.email == email)
    
    @staticmethod
    async def find_user_by_username(username: str) -> Optional[User]:
        """
        Find a user by username.
        
        Args:
            username: Username
            
        Returns:
            User object if found, None otherwise
        """
        return await User.find_one(User.username == username)
    
    @staticmethod
    async def user_exists(email: str = None, username: str = None) -> bool:
        """
        Check if a user exists by email or username.
        
        Args:
            email: Optional email to check
            username: Optional username to check
            
        Returns:
            True if user exists, False otherwise
        """
        if email:
            user = await AuthRepository.find_user_by_email(email)
            if user:
                return True
        
        if username:
            user = await AuthRepository.find_user_by_username(username)
            if user:
                return True
        
        return False

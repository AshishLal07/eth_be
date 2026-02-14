"""Data transformation and validation pipes."""
from typing import Any
from pydantic import BaseModel, validator


class PaginationParams(BaseModel):
    """Pagination parameters."""
    skip: int = 0
    limit: int = 100
    
    @validator('skip')
    def skip_must_be_positive(cls, v):
        if v < 0:
            raise ValueError('skip must be positive')
        return v
    
    @validator('limit')
    def limit_must_be_reasonable(cls, v):
        if v < 1:
            raise ValueError('limit must be at least 1')
        if v > 1000:
            raise ValueError('limit cannot exceed 1000')
        return v


def sanitize_string(value: str) -> str:
    """
    Sanitize string input by removing dangerous characters.
    
    Args:
        value: Input string
        
    Returns:
        Sanitized string
    """
    if not value:
        return value
    
    # Remove common dangerous characters
    dangerous_chars = ['<', '>', '"', "'", '&']
    sanitized = value
    for char in dangerous_chars:
        sanitized = sanitized.replace(char, '')
    
    return sanitized.strip()

"""Common decorators."""
from functools import wraps
from typing import Callable


def cache_response(ttl: int = 300):
    """
    Decorator to cache response for specified time.
    
    Args:
        ttl: Time to live in seconds (default: 300)
    """
    def decorator(func: Callable):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # TODO: Implement caching logic with Redis or similar
            return await func(*args, **kwargs)
        return wrapper
    return decorator


def log_execution(func: Callable):
    """
    Decorator to log function execution.
    """
    @wraps(func)
    async def wrapper(*args, **kwargs):
        print(f"Executing: {func.__name__}")
        result = await func(*args, **kwargs)
        print(f"Completed: {func.__name__}")
        return result
    return wrapper

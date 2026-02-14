"""Request/Response interceptors."""
import time
from fastapi import Request


async def log_requests_middleware(request: Request, call_next):
    """
    Middleware to log all requests.
    
    Args:
        request: Incoming request
        call_next: Next middleware/endpoint
        
    Returns:
        Response from the endpoint
    """
    start_time = time.time()
    
    print(f"Request: {request.method} {request.url.path}")
    
    response = await call_next(request)
    
    process_time = time.time() - start_time
    print(f"Completed in {process_time:.2f}s with status {response.status_code}")
    
    return response

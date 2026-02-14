"""Authentication controller with API endpoints."""
from fastapi import APIRouter, HTTPException, status, Response
from app.modules.auth.dto.login_dto import LoginRequest, LoginResponse
from app.modules.auth.dto.register_dto import RegisterRequest, RegisterResponse
from app.modules.auth.auth_service import AuthService
from app.modules.auth.auth_repository import AuthRepository
from app.config.settings import settings

router = APIRouter()


@router.post("/register", response_model=RegisterResponse, status_code=status.HTTP_201_CREATED)
async def register(request: RegisterRequest):
    """
    Register a new user.
    
    Args:
        request: Registration request with user details
        
    Returns:
        Registration response with user data
        
    Raises:
        HTTPException: If user already exists
    """
    # Check if user already exists
    if await AuthRepository.user_exists(email=request.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    if await AuthRepository.user_exists(username=request.username):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already taken"
        )
    
    # Create user
    user = await AuthService.register_user(
        email=request.email,
        username=request.username,
        password=request.password,
        full_name=request.full_name
    )
    
    return RegisterResponse(
        message="Registration successful",
        user={
            "id": str(user.id),
            "email": user.email,
            "username": user.username,
            "full_name": user.full_name
        }
    )


@router.post("/login", response_model=LoginResponse)
async def login(request: LoginRequest, response: Response):
    """
    Login user and set JWT cookie.
    
    Args:
        request: Login request with credentials
        response: FastAPI response object
        
    Returns:
        Login response with user data
        
    Raises:
        HTTPException: If credentials are invalid
    """
    # Authenticate user
    user = await AuthService.authenticate_user(request.email, request.password)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user"
        )
    
    # Create access token
    access_token = AuthService.create_access_token(data={"sub": str(user.id)})
    
    # Set cookie
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=settings.cookie_httponly,
        secure=settings.cookie_secure,
        samesite=settings.cookie_samesite,
        max_age=settings.jwt_access_token_expire_minutes * 60
    )
    
    return LoginResponse(
        message="Login successful",
        user={
            "id": str(user.id),
            "email": user.email,
            "username": user.username,
            "full_name": user.full_name
        }
    )


@router.post("/logout")
async def logout(response: Response):
    """
    Logout user by clearing JWT cookie.
    
    Args:
        response: FastAPI response object
        
    Returns:
        Success message
    """
    response.delete_cookie(key="access_token")
    return {"message": "Logout successful"}


@router.post("/refresh")
async def refresh_token(response: Response):
    """
    Refresh JWT token.
    
    Args:
        response: FastAPI response object
        
    Returns:
        Success message
    """
    # TODO: Implement refresh token logic
    return {"message": "Token refreshed"}

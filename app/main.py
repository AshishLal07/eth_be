"""FastAPI application entry point."""
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config.settings import settings
from app.config.database import Database
from app.common.interceptors import log_requests_middleware
from app.modules.auth.auth_module import get_auth_router
from app.modules.users.users_module import get_users_router
from app.modules.employees.employees_module import get_employees_router
from app.modules.attendance.attendance_module import get_attendance_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan manager.
    
    Handles startup and shutdown events.
    """
    # Startup
    print(f"Starting {settings.app_name} v{settings.app_version}")
    await Database.connect_db()
    yield
    # Shutdown
    await Database.close_db()
    print("Application shutdown complete")


# Create FastAPI application
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="FastAPI backend with MongoDB and JWT authentication",
    docs_url=settings.docs_url,  # Auto-disabled in production
    redoc_url=settings.redoc_url,  # Auto-disabled in production
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=settings.cors_credentials,
    allow_methods=settings.cors_methods,
    allow_headers=settings.cors_headers,
)

# Add custom middleware
app.middleware("http")(log_requests_middleware)

# Include routers
app.include_router(get_auth_router(), prefix="/api")
app.include_router(get_users_router(), prefix="/api")
app.include_router(get_employees_router(), prefix="/api")
app.include_router(get_attendance_router(), prefix="/api")


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": f"Welcome to {settings.app_name}",
        "version": settings.app_version,
        "docs": "/docs",
        "redoc": "/redoc"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint with database connectivity status."""
    # Check database connectivity
    db_status = "unknown"
    try:
        from app.config.database import Database
        if Database.client is not None:
            # Ping the database to verify connection
            await Database.client.admin.command('ping')
            db_status = "connected"
        else:
            db_status = "not_initialized"
    except Exception as e:
        db_status = f"error: {str(e)}"
    
    return {
        "status": "healthy",
        "app": settings.app_name,
        "version": settings.app_version,
        "environment": settings.environment,
        "database": db_status,
        "docs_enabled": settings.docs_url is not None
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug
    )

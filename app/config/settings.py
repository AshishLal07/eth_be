"""Application configuration settings using Pydantic Settings."""
from typing import List, Optional, Union
from pydantic_settings import BaseSettings
from pydantic import Field, field_validator, computed_field
import warnings
import json


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # Application
    app_name: str = Field(default="Ethara API", alias="APP_NAME")
    app_version: str = Field(default="1.0.0", alias="APP_VERSION")
    environment: str = Field(default="development", alias="ENVIRONMENT")
    debug: bool = Field(default=True, alias="DEBUG")
    
    # Server
    host: str = Field(default="0.0.0.0", alias="HOST")
    port: int = Field(default=8000, alias="PORT")
    
    # Database
    mongodb_url: str = Field(default="mongodb://localhost:27017", alias="MONGODB_URL")
    database_name: str = Field(default="ethara_db", alias="DATABASE_NAME")
    
    # JWT Configuration
    jwt_secret_key: str = Field(..., alias="JWT_SECRET_KEY")
    jwt_algorithm: str = Field(default="HS256", alias="JWT_ALGORITHM")
    jwt_access_token_expire_minutes: int = Field(default=30, alias="JWT_ACCESS_TOKEN_EXPIRE_MINUTES")
    jwt_refresh_token_expire_days: int = Field(default=7, alias="JWT_REFRESH_TOKEN_EXPIRE_DAYS")
    
    # CORS
    cors_origins: List[str] = Field(
        default=["http://localhost:3000", "http://localhost:5173"],
        alias="CORS_ORIGINS"
    )
    cors_credentials: bool = Field(default=True, alias="CORS_CREDENTIALS")
    cors_methods: List[str] = Field(default=["*"], alias="CORS_METHODS")
    cors_headers: List[str] = Field(default=["*"], alias="CORS_HEADERS")
    
    # Security - Cookie Configuration
    cookie_httponly: bool = Field(default=True, alias="COOKIE_HTTPONLY")
    cookie_samesite: str = Field(default="lax", alias="COOKIE_SAMESITE")
    
    @field_validator("jwt_secret_key")
    @classmethod
    def validate_jwt_secret(cls, v: str, info) -> str:
        """Ensure JWT secret is strong in production."""
        # Get environment from values
        env = info.data.get("environment", "development")
        
        # Check for insecure secrets in production
        insecure_secrets = [
            "your-super-secret-jwt-key-change-this-in-production",
            "REPLACE_WITH_SECURE_RANDOM_KEY",
            "secret",
            "changeme"
        ]
        
        if env == "production" and (v in insecure_secrets or len(v) < 32):
            raise ValueError(
                "Production requires a strong JWT secret key (minimum 32 characters). "
                "Generate one using: python -c \"import secrets; print(secrets.token_urlsafe(64))\""
            )
        
        return v
    
    @computed_field
    @property
    def is_production(self) -> bool:
        """Check if running in production environment."""
        return self.environment.lower() == "production"
    
    @computed_field
    @property
    def cookie_secure(self) -> bool:
        """Auto-configure cookie secure flag based on environment.
        
        In production, cookies MUST be secure (HTTPS only).
        In development, allow insecure cookies for local testing.
        """
        if self.is_production:
            return True
        return False
    
    @computed_field
    @property
    def docs_url(self) -> Optional[str]:
        """Disable API documentation in production for security."""
        return None if self.is_production else "/docs"
    
    @computed_field
    @property
    def redoc_url(self) -> Optional[str]:
        """Disable ReDoc documentation in production for security."""
        return None if self.is_production else "/redoc"
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False
        
        @classmethod
        def parse_env_var(cls, field_name: str, raw_val: str):
            """Custom parser for environment variables.
            
            Handles JSON strings for list fields (CORS_ORIGINS, etc.)
            """
            if field_name in ['CORS_ORIGINS', 'CORS_METHODS', 'CORS_HEADERS']:
                # Try to parse as JSON first
                try:
                    return json.loads(raw_val)
                except (json.JSONDecodeError, TypeError):
                    # If not JSON, treat as comma-separated
                    if isinstance(raw_val, str):
                        return [item.strip() for item in raw_val.split(",") if item.strip()]
            return raw_val


# Global settings instance
settings = Settings()

# Production warnings
if settings.is_production:
    print("🚀 Running in PRODUCTION mode")
    print(f"   - Cookie Secure: {settings.cookie_secure}")
    print(f"   - API Docs: {'Disabled' if settings.docs_url is None else 'Enabled'}")
    print(f"   - Debug: {settings.debug}")
else:
    print("🔧 Running in DEVELOPMENT mode")


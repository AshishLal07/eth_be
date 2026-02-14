"""Database configuration and initialization."""
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from app.config.settings import settings


class Database:
    """Database connection manager."""
    
    client: AsyncIOMotorClient = None
    
    @classmethod
    async def connect_db(cls):
        """Initialize database connection and Beanie ODM."""
        cls.client = AsyncIOMotorClient(settings.mongodb_url)
        
        # Import all document models here
        from app.modules.users.models import User
        from app.modules.employees.models import Employee
        from app.modules.attendance.models import Attendance
        
        # Initialize Beanie with the database and document models
        await init_beanie(
            database=cls.client[settings.database_name],
            document_models=[User, Employee, Attendance]
        )
        print(f"Connected to MongoDB: {settings.database_name}")
    
    @classmethod
    async def close_db(cls):
        """Close database connection."""
        if cls.client:
            cls.client.close()
            print("Closed MongoDB connection")


# Dependency to get database
async def get_database():
    """Dependency for getting database instance."""
    return Database.client[settings.database_name]

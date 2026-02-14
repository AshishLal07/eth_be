# Ethara API - FastAPI Backend

A production-ready FastAPI backend with MongoDB and JWT cookie-based authentication, following a modular architecture.

## Features

- ✅ **FastAPI** - Modern, fast web framework for Python
- ✅ **MongoDB** with **Beanie ODM** - Async MongoDB with Pydantic models
- ✅ **JWT Authentication** - Secure cookie-based authentication
- ✅ **Type Safety** - Full Pydantic validation
- ✅ **Auto Documentation** - Swagger UI and ReDoc
- ✅ **CORS** - Configured for cross-origin requests

## Setup Instructions

### Prerequisites

- Python 3.8+
- MongoDB (running locally or remote)

### Installation

1. **Clone the repository** (if applicable)

2. **Create a virtual environment**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**

   ```bash
   cp .env.example .env
   ```

   Then edit `.env` and update the following:
   - `JWT_SECRET_KEY` - Generate a secure secret key
   - `MONGODB_URL` - Your MongoDB connection string
   - `DATABASE_NAME` - Your database name

5. **Start MongoDB** (if running locally)

   ```bash
   mongod
   ```

6. **Run the application**

   ```bash
   uvicorn app.main:app --reload
   ```

   Or using Python directly:

   ```bash
   python -m app.main
   ```

## API Documentation

Once the server is running, visit:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## API Endpoints

### Authentication (`/api/auth`)

- `POST /api/auth/register` - Register a new user
- `POST /api/auth/login` - Login (sets JWT cookie)
- `POST /api/auth/logout` - Logout (clears cookie)
- `POST /api/auth/refresh` - Refresh JWT token

### Users (`/api/users`)

- `GET /api/users/me` - Get current user (authenticated)
- `PUT /api/users/{id}` - Update user (self or admin)

### Attendance (`/api/attendance`)

- `POST /api/attendance/mark` - Mark attendance (authenticated)
- `GET /api/attendance` - List all attendance records (admin only)
- `GET /api/attendance/employee/{employee_id}` - Get attendance by employee ID (authenticated)
- `GET /api/attendance/date/{date}` - Get attendance by date (authenticated)
- `PUT /api/attendance/{id}` - Update attendance (self or admin)
- `DELETE /api/attendance/{id}` - Delete attendance (admin only)

### Employees (`/api/employees`)

- `GET /api/employees` - List all employees (admin only)
- `GET /api/employees/{id}` - Get employee by ID (authenticated)
- `PUT /api/employees/{id}` - Update employee (self or admin)
- `POST /api/employees` - Create employee (admin only)
- `DELETE /api/employees/{id}` - Delete employee (admin only)

## Environment Variables

| Variable                          | Description               | Default                     |
| --------------------------------- | ------------------------- | --------------------------- |
| `APP_NAME`                        | Application name          | "Ethara API"                |
| `MONGODB_URL`                     | MongoDB connection string | "mongodb://localhost:27017" |
| `DATABASE_NAME`                   | Database name             | "ethara_db"                 |
| `JWT_SECRET_KEY`                  | Secret key for JWT        | **Required**                |
| `JWT_ALGORITHM`                   | JWT algorithm             | "HS256"                     |
| `JWT_ACCESS_TOKEN_EXPIRE_MINUTES` | Token expiry              | 30                          |
| `CORS_ORIGINS`                    | Allowed origins           | ["http://localhost:3000"]   |

## Development

### Running in Development Mode

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Code Structure

The application follows a modular architecture:

- **Controllers** - Handle HTTP requests and responses
- **Services** - Contain business logic
- **Repositories** - Handle database operations
- **DTOs** - Data Transfer Objects for validation
- **Models** - Beanie document models

## Security

- Passwords are hashed using bcrypt
- JWT tokens stored in httpOnly cookies
- CORS configured for trusted origins
- Input validation with Pydantic

# Task Management API

A RESTful API for managing tasks with user authentication, built with Flask and SQLAlchemy.

## Features

- User registration and authentication using JWT
- Complete CRUD operations for tasks
- RESTful API design
- Database support (SQLite for development, PostgreSQL for production)
- Secure password handling
- Environment variable configuration

## API Endpoints

### Authentication

- `POST /api/auth/register` - Register a new user
- `POST /api/auth/login` - Login and get JWT token
- `GET /api/auth/me` - Get current user profile (requires authentication)

### Tasks

- `POST /api/tasks/` - Create a new task (requires authentication)
- `GET /api/tasks/` - Get all tasks for the current user (requires authentication)
- `GET /api/tasks/<id>` - Get a specific task by ID (requires authentication)
- `PUT /api/tasks/<id>` - Update a task (requires authentication)
- `DELETE /api/tasks/<id>` - Delete a task (requires authentication)

## Setup Instructions

### Prerequisites

- Python 3.8+
- pip (Python package manager)
- PostgreSQL (for production deployment)

### Local Development Setup

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/task-management-api.git
   cd task-management-api
   ```

2. Create a virtual environment and activate it:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the root directory with the following variables (use `.env.example` as a template):
   ```
   SECRET_KEY=your_secret_key_here
   JWT_SECRET_KEY=your_jwt_secret_key_here
   DATABASE_URL=sqlite:///tasks.db
   ```

5. Initialize the database:
   ```
   flask db init
   flask db migrate -m "Initial migration"
   flask db upgrade
   ```

6. Run the application:
   ```
   python wsgi.py
   ```

   The API will be available at `http://127.0.0.1:5000/`

## Deployment

This API is deployed on Render. 

- Deployed API URL: [https://api-2-e7ut.onrender.com](https://api-2-e7ut.onrender.com)

### Deployment Steps on Render

1. Sign up for a [Render account](https://render.com)
2. Connect your GitHub repository
3. Create a new Web Service and select your repo
4. Configure the service:
   - Environment: Python
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn wsgi:app`
   - Add environment variables (SECRET_KEY, JWT_SECRET_KEY, DATABASE_URL)
5. Create a PostgreSQL database on Render and link it to your web service

## Postman Collection

[![Run in Postman](https://run.pstmn.io/button.svg)](https://app.getpostman.com/run-collection/your-collection-id)

You can import the [Task Management API.postman_collection.json](./Task%20Management%20API.postman_collection.json) file into Postman to test all the API endpoints.

### Example Requests

#### Register a User
```
POST /api/auth/register
Content-Type: application/json

{
  "username": "testuser",
  "email": "test@example.com",
  "password": "securepassword123"
}
```

Response:
```json
{
  "message": "User registered successfully",
  "user": {
    "id": 1,
    "username": "testuser",
    "email": "test@example.com",
    "created_at": "2023-08-01T12:00:00Z"
  }
}
```

#### Login
```
POST /api/auth/login
Content-Type: application/json

{
  "username": "testuser",
  "password": "securepassword123"
}
```

Response:
```json
{
  "message": "Login successful",
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "user": {
    "id": 1,
    "username": "testuser",
    "email": "test@example.com",
    "created_at": "2023-08-01T12:00:00Z"
  }
}
```

#### Create a Task
```
POST /api/tasks/
Content-Type: application/json
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...

{
  "title": "Complete project",
  "description": "Finish the task management API project",
  "status": "in-progress"
}
```

Response:
```json
{
  "message": "Task created successfully",
  "task": {
    "id": 1,
    "title": "Complete project",
    "description": "Finish the task management API project",
    "status": "in-progress",
    "user_id": 1,
    "created_at": "2023-08-01T14:30:00Z",
    "updated_at": "2023-08-01T14:30:00Z"
  }
}
```

#### Get All Tasks
```
GET /api/tasks/
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

Response:
```json
{
  "count": 1,
  "tasks": [
    {
      "id": 1,
      "title": "Complete project",
      "description": "Finish the task management API project",
      "status": "in-progress",
      "user_id": 1,
      "created_at": "2023-08-01T14:30:00Z",
      "updated_at": "2023-08-01T14:30:00Z"
    }
  ]
}
```

## License

MIT

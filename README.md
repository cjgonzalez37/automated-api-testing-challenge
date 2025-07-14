# Automated API Testing Challenge

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.116.1-green.svg)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0.41-red.svg)
![SQLite](https://img.shields.io/badge/SQLite-3-blue.svg)
![Tests](https://img.shields.io/badge/tests-automated-brightgreen.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Status](https://img.shields.io/badge/status-active-success.svg)
![WSL](https://img.shields.io/badge/WSL-Ubuntu-orange.svg)

This project contains a REST API for user management built with FastAPI and SQLite database with SQLAlchemy ORM.

## Project Files

- `main.py` - Main API with FastAPI
- `database.py` - **SQLAlchemy database configuration and CRUD operations**
- `models.py` - Pydantic models for request/response validation
- `init_db.py` - **Database initialization script**
- `create_user.py` - Client script to create users
- `test_api.py` - **Complete automated testing script**
- `run_tests.py` - Quick testing script
- `.venv/` - Python virtual environment

## Database Features

- **SQLite database** with WAL mode for better concurrency
- **SQLAlchemy ORM** for robust database operations
- **Persistent storage** - data survives server restarts
- **Automatic table creation** and schema management
- **Proper error handling** for database operations

## How to Run

### 1. Activate the virtual environment
```bash
source .venv/bin/activate
```

**⚠️ Troubleshooting for macOS users:**
If you encounter this error when activating the virtual environment:
```
.venv/bin/activate:4: defining function based on alias `deactivate'
.venv/bin/activate:4: parse error near `()'
```

This happens when you have a `deactivate` alias defined in your shell. To fix it:
```bash
unalias deactivate
source .venv/bin/activate
```

This removes the conflicting alias and allows the virtual environment to activate properly.

### 2. Install dependencies (if necessary)
```bash
pip install fastapi uvicorn requests pydantic sqlalchemy
```

### 3. Initialize the database
```bash
python init_db.py
```

### 4. Run the API
```bash
uvicorn main:app --reload
```
The API will be available at: http://127.0.0.1:8000

### 5. View automatic documentation
- Swagger UI: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc

## Database Architecture

### SQLAlchemy Models
- **DBUser**: SQLAlchemy model for database operations
- **User**: Pydantic model for request validation
- **UserResponse**: Pydantic model for response serialization

### Database Configuration
- **Engine**: SQLite with WAL mode and optimized settings
- **Session Management**: Proper connection handling with dependency injection
- **Error Handling**: Robust error handling for database operations

## Automated Testing

### Complete Testing Script (`test_api.py`)

This script performs exhaustive tests on the API with database integration:

**Validations performed:**
- ✅ Status codes (200, 201, 400, 404)
- ✅ Content-Type headers
- ✅ JSON response structure
- ✅ Required fields in responses
- ✅ Specific data validation (name, email)
- ✅ Password is not returned
- ✅ Error handling (duplicate email, user not found)
- ✅ Correct data types
- ✅ Database persistence and integrity

**How to run:**
```bash
# Make sure the API is running first
python test_api.py
```

**Example output:**
```
🚀 Starting Complete API Tests (CRUD)
==================================================
🧪 Testing API connectivity
✅ PASS - API Health Check

🧪 Testing GET /users (initial state)
✅ PASS - GET /users - Status Code
✅ PASS - GET /users - Content-Type
✅ PASS - GET /users - Response is list
✅ PASS - GET /users - Is empty initially

🧪 Testing POST /users (create user)
✅ PASS - POST /users - Status Code
✅ PASS - POST /users - Content-Type
...

🧪 Testing PUT /users/1 (update user)
✅ PASS - PUT /users/1 - Status Code
...

🧪 Testing DELETE /users/1
✅ PASS - DELETE /users/1 - Status Code
...

📊 TEST SUMMARY
==================================================
Total Tests: 45
✅ Passed: 45
❌ Failed: 0
📈 Success Rate: 100.0%

🎉 All tests passed! Your API is working correctly.
```

### Quick Testing Script (`run_tests.py`)

For quick tests during development:

```bash
python run_tests.py
```

## API Endpoints

### GET /users
Gets all users from the database
- **Response:** List of users (without passwords)

### POST /users
Creates a new user in the database
- **Body:** `{"name": "string", "email": "string", "password": "string"}`
- **Response:** Created user (without password)
- **Status:** 201 if successful, 400 if email already exists

### GET /users/{user_id}
Gets a user by ID from the database
- **Response:** Specific user
- **Status:** 200 if it exists, 404 if it does not exist

### PUT /users/{user_id}
Updates an existing user in the database
- **Body:** `{"name": "string", "email": "string", "password": "string"}`
- **Response:** Updated user (without password)
- **Status:** 200 if successful, 404 if user not found, 400 if email already exists

### DELETE /users/{user_id}
Deletes a user from the database
- **Response:** `{"message": "User deleted successfully"}`
- **Status:** 200 if successful, 404 if user not found

## Testing Features

### Implemented Assertions
1. **Status Code Validation** - Verifies correct HTTP codes
2. **Content-Type Validation** - Ensures JSON responses
3. **Field Validation** - Verifies required fields
4. **Data Integrity** - Confirms that sent data matches received data
5. **Security Validation** - Verifies that passwords are not returned
6. **Error Handling** - Tests correct error handling
7. **Type Validation** - Verifies correct data types
8. **Database Persistence** - Ensures data survives server restarts

### Test Cases Covered
- ✅ Get initial users (empty database)
- ✅ Create a valid user
- ✅ Try to create a user with a duplicate email
- ✅ Get user by valid ID
- ✅ Try to get a non-existent user
- ✅ Update existing user (PUT)
- ✅ Try to update user with duplicate email
- ✅ Try to update non-existent user
- ✅ Delete existing user
- ✅ Verify user deletion
- ✅ Try to delete non-existent user
- ✅ Basic API connectivity
- ✅ Database integrity checks
- ✅ Complete CRUD operations validation

## Development Setup

### For WSL/Linux Users
This project works best in a native Linux environment. If you're using WSL, consider copying the project to your home directory:

```bash
cp -r /mnt/c/path/to/project ~/workspace/
cd ~/workspace/automated-api-testing-challenge
```

### Database Initialization
The database is automatically created when you run the API, but you can also initialize it manually:

```bash
python init_db.py
```

## CI/CD Usage

The `test_api.py` script returns appropriate exit codes:
- `0` if all tests pass
- `1` if any test fails

This allows for easy integration into CI/CD pipelines.

## Technical Stack

- **FastAPI** - Modern, fast web framework for building APIs
- **SQLAlchemy** - SQL toolkit and ORM
- **SQLite** - Lightweight, serverless database
- **Pydantic** - Data validation using Python type annotations
- **Uvicorn** - ASGI server implementation
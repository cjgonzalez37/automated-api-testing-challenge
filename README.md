# Automated API Testing Challenge

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.104.1-green.svg)
![Pydantic](https://img.shields.io/badge/Pydantic-2.5.0-red.svg)
![Tests](https://img.shields.io/badge/tests-automated-brightgreen.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Status](https://img.shields.io/badge/status-active-success.svg)

This project contains a REST API for user management built with FastAPI.

## Project Files

- `main.py` - Main API with FastAPI
- `create_user.py` - Client script to create users
- `test_api.py` - **Complete automated testing script**
- `run_tests.py` - Quick testing script
- `.venv/` - Python virtual environment

## How to Run

### 1. Activate the virtual environment
```bash
source .venv/bin/activate
```

### 2. Install dependencies (if necessary)
```bash
pip install fastapi uvicorn requests pydantic
```

### 3. Run the API
```bash
uvicorn main:app --reload
```
The API will be available at: http://127.0.0.1:8000

### 4. View automatic documentation
- Swagger UI: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc

## Automated Testing

### Complete Testing Script (`test_api.py`)

This script performs exhaustive tests on the API:

**Validations performed:**
- ✅ Status codes (200, 201, 400, 404)
- ✅ Content-Type headers
- ✅ JSON response structure
- ✅ Required fields in responses
- ✅ Specific data validation (name, email)
- ✅ Password is not returned
- ✅ Error handling (duplicate email, user not found)
- ✅ Correct data types

**How to run:**
```bash
# Make sure the API is running first
python test_api.py
```

**Example output:**
```
🚀 Starting API Tests
==================================================
🧪 Testing API connectivity
✅ PASS - API Health Check

🧪 Testing GET /users (initial state)
✅ PASS - GET /users - Status Code
✅ PASS - GET /users - Content-Type
✅ PASS - GET /users - Response is list
✅ PASS - GET /users - Has initial user
✅ PASS - GET /users - Required Fields
✅ PASS - GET /users - Field name
✅ PASS - GET /users - Field email

📊 TEST SUMMARY
==================================================
Total Tests: 15
✅ Passed: 15
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
Gets all users
- **Response:** List of users (without passwords)

### POST /users
Creates a new user
- **Body:** `{"name": "string", "email": "string", "password": "string"}`
- **Response:** Created user (without password)
- **Status:** 201 if successful, 400 if email already exists

### GET /users/{user_id}
Gets a user by ID
- **Response:** Specific user
- **Status:** 200 if it exists, 404 if it does not exist

## Testing Features

### Implemented Assertions
1. **Status Code Validation** - Verifies correct HTTP codes
2. **Content-Type Validation** - Ensures JSON responses
3. **Field Validation** - Verifies required fields
4. **Data Integrity** - Confirms that sent data matches received data
5. **Security Validation** - Verifies that passwords are not returned
6. **Error Handling** - Tests correct error handling
7. **Type Validation** - Verifies correct data types

### Test Cases Covered
- ✅ Get initial users
- ✅ Create a valid user
- ✅ Try to create a user with a duplicate email
- ✅ Get user by valid ID
- ✅ Try to get a non-existent user
- ✅ Basic API connectivity

## CI/CD Usage

The `test_api.py` script returns appropriate exit codes:
- `0` if all tests pass
- `1` if any test fails

This allows for easy integration into CI/CD pipelines.
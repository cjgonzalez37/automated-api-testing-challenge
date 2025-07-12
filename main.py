from fastapi import FastAPI, HTTPException
from typing import List

# Import models and database functions from separate modules
from models import User, UserResponse
from database import get_all_users, get_user_by_id, get_user_by_email, create_new_user

# Create the FastAPI application
app = FastAPI()

# Endpoint to create a user (POST)
@app.post("/users", response_model=UserResponse, status_code=201)
def create_user(user: User):
    """
    Creates a new user after checking if the email is already in use.
    """
    # Check if user with this email already exists
    db_user = get_user_by_email(user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Create and return the new user
    return create_new_user(user)

# Endpoint to get all users (GET)
@app.get("/users", response_model=List[UserResponse])
def get_users():
    """
    Returns the complete list of users from the database.
    """
    return get_all_users()

# Endpoint to get a user by their ID (GET)
@app.get("/users/{user_id}", response_model=UserResponse)
def get_user(user_id: int):
    """
    Searches for and returns a user by their ID from the database.
    """
    # Retrieve the user from the database
    db_user = get_user_by_id(user_id)
    if db_user is None:
        # If the user is not found, raise an HTTP 404 error
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

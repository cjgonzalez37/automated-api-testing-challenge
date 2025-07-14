from fastapi import FastAPI, HTTPException, Depends
from typing import List
from sqlalchemy.orm import Session

# Import models and database functions from separate modules
from models import User, UserResponse
from database import get_all_users, get_user_by_id, get_user_by_email, create_new_user, update_user, delete_user, get_db

# Create the FastAPI application
app = FastAPI()

# Endpoint to create a user (POST)
@app.post("/users", response_model=UserResponse, status_code=201)
def create_user(user: User, db: Session = Depends(get_db)):
    """
    Creates a new user after checking if the email is already in use.
    """
    # Check if user with this email already exists
    db_user = get_user_by_email(db, user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Create and return the new user
    return create_new_user(db, user)

# Endpoint to get all users (GET)
@app.get("/users", response_model=List[UserResponse])
def get_users(db: Session = Depends(get_db)):
    """
    Returns the complete list of users from the database.
    """
    return get_all_users(db)

# Endpoint to get a user by their ID (GET)
@app.get("/users/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    """
    Searches for and returns a user by their ID from the database.
    """
    # Retrieve the user from the database
    db_user = get_user_by_id(db, user_id)
    if db_user is None:
        # If the user is not found, raise an HTTP 404 error
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

# Endpoint to update a user by their ID (PUT)
@app.put("/users/{user_id}", response_model=UserResponse)
def update_user_endpoint(user_id: int, user: User, db: Session = Depends(get_db)):
    """
    Updates an existing user in the database.
    """
    try:
        updated_user = update_user(db, user_id, user)
        if updated_user is None:
            raise HTTPException(status_code=404, detail="User not found")
        return updated_user
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

# Endpoint to delete a user by their ID (DELETE)
@app.delete("/users/{user_id}")
def delete_user_endpoint(user_id: int, db: Session = Depends(get_db)):
    """
    Deletes a user from the database.
    """
    success = delete_user(db, user_id)
    if not success:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deleted successfully"}

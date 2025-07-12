from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

# 1. Pydantic data model
# FastAPI will use this to validate that the data coming in the POST request is correct.
class User(BaseModel):
    name: str
    email: str
    password: str

# Response model, to avoid returning the password
class UserResponse(BaseModel):
    id: int
    name: str
    email: str

# 2. Create the FastAPI application
app = FastAPI()

# 3. In-memory "database"
# A simple list to store the users we create.
# We start with an example user.
usuarios_db: List[UserResponse] = [
    UserResponse(id=0, name="Initial User", email="admin@example.com")
]

# 4. Endpoint to create a user (POST)
@app.post("/users", response_model=UserResponse, status_code=201)
def create_user(user: User):
    """
    Creates a new user and adds it to the in-memory database.
    """
    if any(u.email == user.email for u in usuarios_db):
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Assign a new ID
    new_id = len(usuarios_db)
    
    # Create the response object without the password
    user_response = UserResponse(id=new_id, name=user.name, email=user.email)
    
    # Save it in our "database"
    usuarios_db.append(user_response)
    
    return user_response

# 5. Endpoint to get all users (GET)
@app.get("/users", response_model=List[UserResponse])
def get_users():
    """
    Returns the complete list of users.
    """
    return usuarios_db

# 6. Endpoint to get a user by their ID (GET)
@app.get("/users/{user_id}", response_model=UserResponse)
def get_user(user_id: int):
    """
    Searches for and returns a user by their ID.
    """
    # Search for the user in the "database"
    for usuario in usuarios_db:
        if usuario.id == user_id:
            return usuario
    
    # If the loop finishes and the user was not found, raise an HTTP 404 error
    raise HTTPException(status_code=404, detail="User not found")

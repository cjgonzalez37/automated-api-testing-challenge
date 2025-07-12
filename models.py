from pydantic import BaseModel

# Pydantic data model for incoming user data
# FastAPI uses this to validate the data from POST requests.
class User(BaseModel):
    name: str
    email: str
    password: str

# Response model to avoid returning the password
class UserResponse(BaseModel):
    id: int
    name: str
    email: str

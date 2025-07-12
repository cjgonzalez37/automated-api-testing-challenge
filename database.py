from typing import List, Union, Optional
from models import User, UserResponse

# In-memory "database"
# A simple list to store the users we create.
# We start with an example user.
usuarios_db: List[UserResponse] = [
    UserResponse(id=0, name="Initial User", email="admin@example.com")
]

def get_all_users() -> List[UserResponse]:
    """Returns the complete list of users."""
    return usuarios_db

def get_user_by_id(user_id: int) -> Optional[UserResponse]:
    """Searches for and returns a user by their ID."""
    for usuario in usuarios_db:
        if usuario.id == user_id:
            return usuario
    return None

def get_user_by_email(email: str) -> Optional[UserResponse]:
    """Searches for and returns a user by their email."""
    for usuario in usuarios_db:
        if usuario.email == email:
            return usuario
    return None

def create_new_user(user: User) -> UserResponse:
    """Creates a new user and adds it to the in-memory database."""
    new_id = len(usuarios_db)
    user_response = UserResponse(id=new_id, name=user.name, email=user.email)
    usuarios_db.append(user_response)
    return user_response

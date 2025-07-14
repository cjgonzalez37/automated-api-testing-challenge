from sqlalchemy import create_engine, Column, Integer, String, event
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine import Engine
from models import User, UserResponse
from typing import List, Optional
import sqlite3

# Database configuration
DATABASE_URL = "sqlite:///./test.db"

# SQLite-specific configuration to enable WAL mode and proper locking
@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    if isinstance(dbapi_connection, sqlite3.Connection):
        cursor = dbapi_connection.cursor()
        # Enable WAL mode for better concurrency
        cursor.execute("PRAGMA journal_mode=WAL")
        # Set timeout for busy database
        cursor.execute("PRAGMA busy_timeout=30000")
        # Enable foreign keys
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()

# Create engine with specific SQLite configuration
engine = create_engine(
    DATABASE_URL, 
    connect_args={
        "check_same_thread": False,
        "timeout": 30
    },
    echo=False,
    pool_pre_ping=True
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# SQLAlchemy User Model
class DBUser(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)

# Create database tables
Base.metadata.create_all(bind=engine)

def get_db():
    """Dependency to get a database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_all_users(db: SessionLocal) -> List[UserResponse]:
    """Returns the complete list of users."""
    users = db.query(DBUser).all()
    return [UserResponse(id=u.id, name=u.name, email=u.email) for u in users]

def get_user_by_id(db: SessionLocal, user_id: int) -> Optional[UserResponse]:
    """Searches for and returns a user by their ID."""
    user = db.query(DBUser).filter(DBUser.id == user_id).first()
    if user:
        return UserResponse(id=user.id, name=user.name, email=user.email)
    return None

def get_user_by_email(db: SessionLocal, email: str) -> Optional[UserResponse]:
    """Searches for and returns a user by their email."""
    user = db.query(DBUser).filter(DBUser.email == email).first()
    if user:
        return UserResponse(id=user.id, name=user.name, email=user.email)
    return None

def create_new_user(db: SessionLocal, user: User) -> UserResponse:
    """Creates a new user and adds it to the database."""
    # In a real app, you'd hash the password
    fake_hashed_password = user.password + "notreallyhashed"
    
    db_user = DBUser(name=user.name, email=user.email, hashed_password=fake_hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    return UserResponse(id=db_user.id, name=db_user.name, email=db_user.email)

def update_user(db: SessionLocal, user_id: int, user: User) -> Optional[UserResponse]:
    """Updates an existing user in the database."""
    db_user = db.query(DBUser).filter(DBUser.id == user_id).first()
    if not db_user:
        return None
    
    # Check if email is being changed and if it already exists
    if user.email != db_user.email:
        existing_user = db.query(DBUser).filter(DBUser.email == user.email).first()
        if existing_user:
            raise ValueError("Email already registered")
    
    # Update user fields
    db_user.name = user.name
    db_user.email = user.email
    # In a real app, you'd hash the password
    db_user.hashed_password = user.password + "notreallyhashed"
    
    db.commit()
    db.refresh(db_user)
    
    return UserResponse(id=db_user.id, name=db_user.name, email=db_user.email)

def delete_user(db: SessionLocal, user_id: int) -> bool:
    """Deletes a user from the database."""
    db_user = db.query(DBUser).filter(DBUser.id == user_id).first()
    if not db_user:
        return False
    
    db.delete(db_user)
    db.commit()
    return True
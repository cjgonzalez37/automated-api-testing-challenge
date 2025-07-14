#!/usr/bin/env python3
"""
Script to initialize the database and create tables.
"""

import os
from database import Base, engine, DBUser
from sqlalchemy import text

def init_database():
    """Initialize the database and create all tables."""
    print("🔧 Initializing database...")
    
    # Remove existing database if it exists
    if os.path.exists("test.db"):
        os.remove("test.db")
        print("🗑️  Removed existing database")
    
    # Create all tables
    Base.metadata.create_all(bind=engine)
    
    # Verify the database was created
    with engine.connect() as conn:
        result = conn.execute(text("SELECT name FROM sqlite_master WHERE type='table';"))
        tables = result.fetchall()
        print(f"✅ Database created with tables: {[table[0] for table in tables]}")
    
    # Verify we can write to the database
    try:
        with engine.connect() as conn:
            conn.execute(text("CREATE TABLE IF NOT EXISTS test_write (id INTEGER);"))
            conn.execute(text("DROP TABLE test_write;"))
            conn.commit()
        print("✅ Database write permissions verified")
    except Exception as e:
        print(f"❌ Database write test failed: {e}")
        return False
    
    print("✅ Database initialization complete!")
    return True

if __name__ == "__main__":
    success = init_database()
    exit(0 if success else 1)

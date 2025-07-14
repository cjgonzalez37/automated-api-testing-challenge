#!/usr/bin/env python3
"""
Quick test script for the new CRUD endpoints (PUT and DELETE)
"""
import requests
import json

BASE_URL = "http://127.0.0.1:8000"

def test_complete_crud():
    print("🧪 Testing Complete CRUD Operations")
    print("=" * 50)
    
    # 1. Create a test user
    print("\n1. Creating test user...")
    user_data = {
        "name": "Test User",
        "email": "test@example.com",
        "password": "testpass123"
    }
    
    response = requests.post(f"{BASE_URL}/users", json=user_data)
    if response.status_code == 201:
        created_user = response.json()
        user_id = created_user["id"]
        print(f"✅ User created with ID: {user_id}")
        print(f"   Name: {created_user['name']}, Email: {created_user['email']}")
    else:
        print(f"❌ Failed to create user: {response.status_code}")
        return
    
    # 2. Test PUT - Update user
    print(f"\n2. Testing PUT /users/{user_id}...")
    updated_data = {
        "name": "Updated Test User",
        "email": "updated@example.com",
        "password": "newpass123"
    }
    
    response = requests.put(f"{BASE_URL}/users/{user_id}", json=updated_data)
    if response.status_code == 200:
        updated_user = response.json()
        print("✅ User updated successfully")
        print(f"   New Name: {updated_user['name']}")
        print(f"   New Email: {updated_user['email']}")
    else:
        print(f"❌ Failed to update user: {response.status_code} - {response.text}")
    
    # 3. Test PUT with duplicate email (should fail)
    print(f"\n3. Testing PUT with duplicate email...")
    # First create another user
    user_data2 = {
        "name": "Another User",
        "email": "another@example.com",
        "password": "pass123"
    }
    response = requests.post(f"{BASE_URL}/users", json=user_data2)
    if response.status_code == 201:
        user2_id = response.json()["id"]
        
        # Try to update first user with second user's email
        duplicate_data = {
            "name": "Test User",
            "email": "another@example.com",  # This should fail
            "password": "testpass123"
        }
        response = requests.put(f"{BASE_URL}/users/{user_id}", json=duplicate_data)
        if response.status_code == 400:
            print("✅ Duplicate email validation working correctly")
        else:
            print(f"❌ Duplicate email validation failed: {response.status_code}")
    
    # 4. Test PUT with non-existent user
    print(f"\n4. Testing PUT with non-existent user...")
    response = requests.put(f"{BASE_URL}/users/999", json=updated_data)
    if response.status_code == 404:
        print("✅ PUT returns 404 for non-existent user")
    else:
        print(f"❌ Expected 404, got: {response.status_code}")
    
    # 5. Test DELETE
    print(f"\n5. Testing DELETE /users/{user_id}...")
    response = requests.delete(f"{BASE_URL}/users/{user_id}")
    if response.status_code == 200:
        result = response.json()
        print("✅ User deleted successfully")
        print(f"   Message: {result['message']}")
    else:
        print(f"❌ Failed to delete user: {response.status_code}")
    
    # 6. Verify user is deleted
    print(f"\n6. Verifying user is deleted...")
    response = requests.get(f"{BASE_URL}/users/{user_id}")
    if response.status_code == 404:
        print("✅ User successfully deleted (GET returns 404)")
    else:
        print(f"❌ User still exists: {response.status_code}")
    
    # 7. Test DELETE with non-existent user
    print(f"\n7. Testing DELETE with non-existent user...")
    response = requests.delete(f"{BASE_URL}/users/999")
    if response.status_code == 404:
        print("✅ DELETE returns 404 for non-existent user")
    else:
        print(f"❌ Expected 404, got: {response.status_code}")
    
    print("\n" + "=" * 50)
    print("🎉 CRUD Complete Testing Finished!")

if __name__ == "__main__":
    try:
        test_complete_crud()
    except requests.exceptions.ConnectionError:
        print("❌ Error: Could not connect to API. Make sure the server is running on http://127.0.0.1:8000")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
#!/usr/bin/env python3
"""
Script simple para ejecutar tests rápidos de la API
"""

import requests
import json

def quick_test():
    """Test rápido de funcionalidad básica"""
    base_url = "http://127.0.0.1:8000"
    
    print("🚀 Quick API Test")
    print("-" * 30)
    
    try:
        # Test 1: GET usuarios
        print("1. Testing GET /users...")
        response = requests.get(f"{base_url}/users")
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        users = response.json()
        assert isinstance(users, list), "Response should be a list"
        print(f"   ✅ Found {len(users)} users")
        
        # Test 2: POST crear usuario
        print("2. Testing POST /users...")
        import time
        timestamp = int(time.time())
        new_user = {
            "name": "Quick Test User",
            "email": f"quicktest{timestamp}@example.com",
            "password": "testpass123"
        }
        
        response = requests.post(
            f"{base_url}/users",
            headers={"Content-Type": "application/json"},
            data=json.dumps(new_user)
        )
        assert response.status_code == 201, f"Expected 201, got {response.status_code}"
        created_user = response.json()
        assert created_user["name"] == new_user["name"], "Name mismatch"
        assert created_user["email"] == new_user["email"], "Email mismatch"
        assert "password" not in created_user, "Password should not be in response"
        print(f"   ✅ Created user with ID {created_user['id']}")
        
        # Test 3: GET usuario por ID
        print("3. Testing GET /users/{id}...")
        user_id = created_user["id"]
        response = requests.get(f"{base_url}/users/{user_id}")
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        user = response.json()
        assert user["id"] == user_id, "ID mismatch"
        print(f"   ✅ Retrieved user: {user['name']}")
        
        print("\n🎉 All quick tests passed!")
        
    except requests.exceptions.RequestException as e:
        print(f"❌ Connection error: {e}")
        print("Make sure the API server is running on http://127.0.0.1:8000")
    except AssertionError as e:
        print(f"❌ Test failed: {e}")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")

if __name__ == "__main__":
    quick_test()

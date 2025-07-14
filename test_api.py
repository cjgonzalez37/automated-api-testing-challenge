#!/usr/bin/env python3
"""
Automated script to test the user API.
Validates status codes, body content, headers, and specific data.
"""

import requests
import json
import sys
import os
from typing import Dict, Any

# Ensure a clean database for each test run
if os.path.exists("test.db"):
    os.remove("test.db")


class APITester:
    def __init__(self, base_url: str = "http://127.0.0.1:8000"):
        self.base_url = base_url
        self.test_results = []
        self.passed_tests = 0
        self.failed_tests = 0
    
    def log_test(self, test_name: str, passed: bool, message: str = ""):
        """Logs the result of a test."""
        status = "✅ PASS" if passed else "❌ FAIL"
        result = f"{status} - {test_name}"
        if message:
            result += f": {message}"
        
        print(result)
        self.test_results.append({
            'test': test_name,
            'passed': passed,
            'message': message
        })
        
        if passed:
            self.passed_tests += 1
        else:
            self.failed_tests += 1
    
    def assert_status_code(self, response: requests.Response, expected: int, test_name: str):
        """Validates the response status code."""
        actual = response.status_code
        passed = actual == expected
        message = f"Expected {expected}, got {actual}"
        self.log_test(f"{test_name} - Status Code", passed, message if not passed else "")
        return passed
    
    def assert_content_type(self, response: requests.Response, expected: str, test_name: str):
        """Validates the Content-Type header."""
        actual = response.headers.get('content-type', '').split(';')[0]
        passed = actual == expected
        message = f"Expected '{expected}', got '{actual}'"
        self.log_test(f"{test_name} - Content-Type", passed, message if not passed else "")
        return passed
    
    def assert_json_field(self, data: Dict[Any, Any], field: str, expected_value: Any, test_name: str):
        """Validates that a specific JSON field has the expected value."""
        actual_value = data.get(field)
        passed = actual_value == expected_value
        message = f"Field '{field}': expected '{expected_value}', got '{actual_value}'"
        self.log_test(f"{test_name} - Field {field}", passed, message if not passed else "")
        return passed
    
    def assert_json_has_fields(self, data: Dict[Any, Any], required_fields: list, test_name: str):
        """Validates that the JSON contains all required fields."""
        missing_fields = [field for field in required_fields if field not in data]
        passed = len(missing_fields) == 0
        message = f"Missing fields: {missing_fields}" if missing_fields else ""
        self.log_test(f"{test_name} - Required Fields", passed, message)
        return passed
    
    def test_get_initial_users(self):
        """Test: Get initial users (should be an empty list)."""
        print("\n🧪 Testing GET /users (initial state)")
        
        try:
            response = requests.get(f"{self.base_url}/users")
            
            self.assert_status_code(response, 200, "GET /users")
            self.assert_content_type(response, "application/json", "GET /users")
            
            data = response.json()
            passed = isinstance(data, list)
            self.log_test("GET /users - Response is list", passed, 
                         f"Expected list, got {type(data).__name__}")
            
            # With a clean DB, the initial list should be empty
            passed = len(data) == 0
            self.log_test("GET /users - Is empty initially", passed, 
                         f"Expected 0 users, got {len(data)}")
            
            return data
            
        except requests.exceptions.RequestException as e:
            self.log_test("GET /users - Connection", False, f"Request failed: {e}")
            return []
    
    def test_create_user(self):
        """Test: Create a new user."""
        print("\n🧪 Testing POST /users (create user)")
        
        # Generate a unique email using a timestamp and random number to avoid duplicates
        import time
        import random
        timestamp = int(time.time())
        random_num = random.randint(1000, 9999)
        test_user = {
            'name': 'Test User',
            'email': f'test{timestamp}{random_num}@example.com',
            'password': 'testpassword123'
        }
        
        try:
            response = requests.post(
                f"{self.base_url}/users",
                headers={'Content-Type': 'application/json'},
                data=json.dumps(test_user)
            )
            
            # Validate status code
            self.assert_status_code(response, 201, "POST /users")
            
            # Validate content-type
            self.assert_content_type(response, "application/json", "POST /users")
            
            # Only continue with validations if the status code is correct
            if response.status_code == 201:
                # Validate response structure
                data = response.json()
                self.assert_json_has_fields(data, ['id', 'name', 'email'], "POST /users")
                
                # Validate that the data matches what was sent
                self.assert_json_field(data, 'name', test_user['name'], "POST /users")
                self.assert_json_field(data, 'email', test_user['email'], "POST /users")
                
                # Validate that the password is NOT returned
                passed = 'password' not in data
                self.log_test("POST /users - Password not in response", passed, 
                             "Password should not be returned in response")
                
                # Validate that the ID is a number
                passed = isinstance(data.get('id'), int)
                self.log_test("POST /users - ID is integer", passed, 
                             f"Expected int, got {type(data.get('id')).__name__}")
                
                return data
            else:
                # If creation failed, return None but do no more validations
                self.log_test("POST /users - Skipping field validations", True, 
                             "Skipped due to failed creation")
                return None
            
        except requests.exceptions.RequestException as e:
            self.log_test("POST /users - Connection", False, f"Request failed: {e}")
            return None
    
    def test_create_duplicate_user(self, email_to_test: str):
        """Test: Attempt to create a user with a duplicate email."""
        print("\n🧪 Testing POST /users (duplicate email)")
        
        duplicate_user = {
            'name': 'Another User',
            'email': email_to_test,  # Use the email from the user we just created
            'password': 'anotherpassword'
        }
        
        try:
            response = requests.post(
                f"{self.base_url}/users",
                headers={'Content-Type': 'application/json'},
                data=json.dumps(duplicate_user)
            )
            
            # Should return a 400 error
            self.assert_status_code(response, 400, "POST /users (duplicate)")
            
            # Validate error message
            data = response.json()
            expected_detail = "Email already registered"
            actual_detail = data.get('detail', '')
            passed = expected_detail in actual_detail
            self.log_test("POST /users (duplicate) - Error message", passed, 
                         f"Expected '{expected_detail}' in '{actual_detail}'")
            
        except requests.exceptions.RequestException as e:
            self.log_test("POST /users (duplicate) - Connection", False, f"Request failed: {e}")
    
    def test_get_user_by_id(self, user_id: int):
        """Test: Get user by ID."""
        print(f"\n🧪 Testing GET /users/{user_id}")
        
        try:
            response = requests.get(f"{self.base_url}/users/{user_id}")
            
            # Validate status code
            self.assert_status_code(response, 200, f"GET /users/{user_id}")
            
            # Validate content-type
            self.assert_content_type(response, "application/json", f"GET /users/{user_id}")
            
            # Validate structure
            data = response.json()
            self.assert_json_has_fields(data, ['id', 'name', 'email'], f"GET /users/{user_id}")
            
            # Validate that the ID matches
            self.assert_json_field(data, 'id', user_id, f"GET /users/{user_id}")
            
            return data
            
        except requests.exceptions.RequestException as e:
            self.log_test(f"GET /users/{user_id} - Connection", False, f"Request failed: {e}")
            return None
    
    def test_get_nonexistent_user(self):
        """Test: Get a user that does not exist."""
        print("\n🧪 Testing GET /users/999 (non-existent)")
        
        try:
            response = requests.get(f"{self.base_url}/users/999")
            
            # Should return a 404 error
            self.assert_status_code(response, 404, "GET /users/999 (non-existent)")
            
            # Validate error message
            data = response.json()
            expected_detail = "User not found"
            actual_detail = data.get('detail', '')
            passed = expected_detail in actual_detail
            self.log_test("GET /users/999 - Error message", passed, 
                         f"Expected '{expected_detail}' in '{actual_detail}'")
            
        except requests.exceptions.RequestException as e:
            self.log_test("GET /users/999 - Connection", False, f"Request failed: {e}")
    
    def test_update_user(self, user_id: int, original_email: str):
        """Test: Update an existing user."""
        print(f"\n🧪 Testing PUT /users/{user_id} (update user)")
        
        # Generate unique email for update
        import time
        timestamp = int(time.time())
        updated_user = {
            'name': 'Updated Test User',
            'email': f'updated{timestamp}@example.com',
            'password': 'newpassword123'
        }
        
        try:
            response = requests.put(
                f"{self.base_url}/users/{user_id}",
                headers={'Content-Type': 'application/json'},
                data=json.dumps(updated_user)
            )
            
            # Validate status code
            self.assert_status_code(response, 200, f"PUT /users/{user_id}")
            
            # Validate content-type
            self.assert_content_type(response, "application/json", f"PUT /users/{user_id}")
            
            if response.status_code == 200:
                # Validate response structure
                data = response.json()
                self.assert_json_has_fields(data, ['id', 'name', 'email'], f"PUT /users/{user_id}")
                
                # Validate that the data was updated
                self.assert_json_field(data, 'name', updated_user['name'], f"PUT /users/{user_id}")
                self.assert_json_field(data, 'email', updated_user['email'], f"PUT /users/{user_id}")
                self.assert_json_field(data, 'id', user_id, f"PUT /users/{user_id}")
                
                # Validate that the password is NOT returned
                passed = 'password' not in data
                self.log_test(f"PUT /users/{user_id} - Password not in response", passed, 
                             "Password should not be returned in response")
                
                return data
            
        except requests.exceptions.RequestException as e:
            self.log_test(f"PUT /users/{user_id} - Connection", False, f"Request failed: {e}")
            return None
    
    def test_update_user_duplicate_email(self, user_id: int, existing_email: str):
        """Test: Update user with duplicate email (should fail)."""
        print(f"\n🧪 Testing PUT /users/{user_id} (duplicate email)")
        
        duplicate_user = {
            'name': 'Test User',
            'email': existing_email,  # Use existing email
            'password': 'testpassword123'
        }
        
        try:
            response = requests.put(
                f"{self.base_url}/users/{user_id}",
                headers={'Content-Type': 'application/json'},
                data=json.dumps(duplicate_user)
            )
            
            # Should return a 400 error
            self.assert_status_code(response, 400, f"PUT /users/{user_id} (duplicate)")
            
            # Validate error message
            data = response.json()
            expected_detail = "Email already registered"
            actual_detail = data.get('detail', '')
            passed = expected_detail in actual_detail
            self.log_test(f"PUT /users/{user_id} (duplicate) - Error message", passed, 
                         f"Expected '{expected_detail}' in '{actual_detail}'")
            
        except requests.exceptions.RequestException as e:
            self.log_test(f"PUT /users/{user_id} (duplicate) - Connection", False, f"Request failed: {e}")
    
    def test_update_nonexistent_user(self):
        """Test: Update a user that does not exist."""
        print("\n🧪 Testing PUT /users/999 (non-existent)")
        
        updated_user = {
            'name': 'Non-existent User',
            'email': 'nonexistent@example.com',
            'password': 'password123'
        }
        
        try:
            response = requests.put(
                f"{self.base_url}/users/999",
                headers={'Content-Type': 'application/json'},
                data=json.dumps(updated_user)
            )
            
            # Should return a 404 error
            self.assert_status_code(response, 404, "PUT /users/999 (non-existent)")
            
            # Validate error message
            data = response.json()
            expected_detail = "User not found"
            actual_detail = data.get('detail', '')
            passed = expected_detail in actual_detail
            self.log_test("PUT /users/999 - Error message", passed, 
                         f"Expected '{expected_detail}' in '{actual_detail}'")
            
        except requests.exceptions.RequestException as e:
            self.log_test("PUT /users/999 - Connection", False, f"Request failed: {e}")
    
    def test_delete_user(self, user_id: int):
        """Test: Delete an existing user."""
        print(f"\n🧪 Testing DELETE /users/{user_id}")
        
        try:
            response = requests.delete(f"{self.base_url}/users/{user_id}")
            
            # Validate status code
            self.assert_status_code(response, 200, f"DELETE /users/{user_id}")
            
            # Validate content-type
            self.assert_content_type(response, "application/json", f"DELETE /users/{user_id}")
            
            if response.status_code == 200:
                # Validate response structure
                data = response.json()
                expected_message = "User deleted successfully"
                actual_message = data.get('message', '')
                passed = expected_message in actual_message
                self.log_test(f"DELETE /users/{user_id} - Success message", passed, 
                             f"Expected '{expected_message}' in '{actual_message}'")
                
                return True
            
        except requests.exceptions.RequestException as e:
            self.log_test(f"DELETE /users/{user_id} - Connection", False, f"Request failed: {e}")
            return False
    
    def test_verify_user_deleted(self, user_id: int):
        """Test: Verify that a deleted user no longer exists."""
        print(f"\n🧪 Testing GET /users/{user_id} (verify deletion)")
        
        try:
            response = requests.get(f"{self.base_url}/users/{user_id}")
            
            # Should return a 404 error
            self.assert_status_code(response, 404, f"GET /users/{user_id} (deleted)")
            
            # Validate error message
            data = response.json()
            expected_detail = "User not found"
            actual_detail = data.get('detail', '')
            passed = expected_detail in actual_detail
            self.log_test(f"GET /users/{user_id} (deleted) - Error message", passed, 
                         f"Expected '{expected_detail}' in '{actual_detail}'")
            
        except requests.exceptions.RequestException as e:
            self.log_test(f"GET /users/{user_id} (deleted) - Connection", False, f"Request failed: {e}")
    
    def test_delete_nonexistent_user(self):
        """Test: Delete a user that does not exist."""
        print("\n🧪 Testing DELETE /users/999 (non-existent)")
        
        try:
            response = requests.delete(f"{self.base_url}/users/999")
            
            # Should return a 404 error
            self.assert_status_code(response, 404, "DELETE /users/999 (non-existent)")
            
            # Validate error message
            data = response.json()
            expected_detail = "User not found"
            actual_detail = data.get('detail', '')
            passed = expected_detail in actual_detail
            self.log_test("DELETE /users/999 - Error message", passed, 
                         f"Expected '{expected_detail}' in '{actual_detail}'")
            
        except requests.exceptions.RequestException as e:
            self.log_test("DELETE /users/999 - Connection", False, f"Request failed: {e}")
    
    def test_api_health(self):
        """Basic connectivity test."""
        print("🧪 Testing API connectivity")
        
        try:
            response = requests.get(f"{self.base_url}/users", timeout=5)
            passed = response.status_code in [200, 404, 500]  # Any valid HTTP response
            self.log_test("API Health Check", passed, 
                         f"API is {'responsive' if passed else 'not responding'}")
            return passed
        except requests.exceptions.RequestException as e:
            self.log_test("API Health Check", False, f"Cannot connect to API: {e}")
            return False
    
    def run_all_tests(self):
        """Runs all tests including complete CRUD operations."""
        print("🚀 Starting Complete API Tests (CRUD)")
        print("=" * 50)
        
        # Connectivity test
        if not self.test_api_health():
            print("\n❌ API is not accessible. Make sure the server is running on http://127.0.0.1:8000")
            return
        
        # Basic CRUD tests
        initial_users = self.test_get_initial_users()
        created_user = self.test_create_user()
        
        if created_user and 'email' in created_user:
            self.test_create_duplicate_user(created_user['email'])
        else:
            self.log_test("POST /users (duplicate) - SKIPPED", False, "Could not run test because user creation failed.")
        
        if created_user and 'id' in created_user:
            retrieved_user = self.test_get_user_by_id(created_user['id'])
        
        self.test_get_nonexistent_user()
        
        # CREATE a second user for UPDATE tests
        second_user = self.test_create_user()
        
        # UPDATE tests
        if created_user and 'id' in created_user and 'email' in created_user:
            updated_user = self.test_update_user(created_user['id'], created_user['email'])
            
            # Test duplicate email validation for UPDATE
            if second_user and 'email' in second_user:
                self.test_update_user_duplicate_email(created_user['id'], second_user['email'])
        else:
            self.log_test("PUT /users - SKIPPED", False, "Could not run test because user creation failed.")
        
        self.test_update_nonexistent_user()
        
        # DELETE tests
        if created_user and 'id' in created_user:
            delete_success = self.test_delete_user(created_user['id'])
            if delete_success:
                self.test_verify_user_deleted(created_user['id'])
        else:
            self.log_test("DELETE /users - SKIPPED", False, "Could not run test because user creation failed.")
        
        self.test_delete_nonexistent_user()
        
        # Final summary
        self.print_summary()
    
    def print_summary(self):
        """Prints the test summary."""
        print("\n" + "=" * 50)
        print("📊 TEST SUMMARY")
        print("=" * 50)
        
        total_tests = self.passed_tests + self.failed_tests
        success_rate = (self.passed_tests / total_tests * 100) if total_tests > 0 else 0
        
        print(f"Total Tests: {total_tests}")
        print(f"✅ Passed: {self.passed_tests}")
        print(f"❌ Failed: {self.failed_tests}")
        print(f"📈 Success Rate: {success_rate:.1f}%")
        
        if self.failed_tests == 0:
            print("\n🎉 All tests passed! Your API is working correctly.")
        else:
            print(f"\n⚠️  {self.failed_tests} test(s) failed. Check the details above.")
            
        return self.failed_tests == 0

def main():
    """Main function."""
    print("🔧 FastAPI User Management API Tester")
    print("Make sure your API server is running on http://127.0.0.1:8000")
    print("You can start it with: uvicorn main:app --reload")
    
    
    
    tester = APITester()
    tester.run_all_tests()
    
    # Exit code for CI/CD
    sys.exit(0 if tester.failed_tests == 0 else 1)

if __name__ == "__main__":
    main()

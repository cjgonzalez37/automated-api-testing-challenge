#!/usr/bin/env python3
"""
Script automatizado mejorado para probar la API de usuarios
Incluye limpieza de datos y mejor aislamiento de tests
"""

import requests
import json
import sys
import time
import uuid
from typing import Dict, Any, List

class APITesterEnhanced:
    def __init__(self, base_url: str = "http://127.0.0.1:8000"):
        self.base_url = base_url
        self.test_results = []
        self.passed_tests = 0
        self.failed_tests = 0
        self.created_users = []  # Para tracking de usuarios creados
    
    def generate_unique_email(self, prefix: str = "test") -> str:
        """Genera un email único para evitar duplicados"""
        timestamp = int(time.time())
        unique_id = str(uuid.uuid4())[:8]
        return f"{prefix}_{timestamp}_{unique_id}@example.com"
    
    def log_test(self, test_name: str, passed: bool, message: str = ""):
        """Registra el resultado de un test"""
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
        """Valida el status code de la respuesta"""
        actual = response.status_code
        passed = actual == expected
        message = f"Expected {expected}, got {actual}"
        self.log_test(f"{test_name} - Status Code", passed, message if not passed else "")
        return passed
    
    def assert_content_type(self, response: requests.Response, expected: str, test_name: str):
        """Valida el Content-Type header"""
        actual = response.headers.get('content-type', '').split(';')[0]
        passed = actual == expected
        message = f"Expected '{expected}', got '{actual}'"
        self.log_test(f"{test_name} - Content-Type", passed, message if not passed else "")
        return passed
    
    def assert_json_field(self, data: Dict[Any, Any], field: str, expected_value: Any, test_name: str):
        """Valida que un campo específico del JSON tenga el valor esperado"""
        actual_value = data.get(field)
        passed = actual_value == expected_value
        message = f"Field '{field}': expected '{expected_value}', got '{actual_value}'"
        self.log_test(f"{test_name} - Field {field}", passed, message if not passed else "")
        return passed
    
    def assert_json_has_fields(self, data: Dict[Any, Any], required_fields: list, test_name: str):
        """Valida que el JSON contenga todos los campos requeridos"""
        missing_fields = [field for field in required_fields if field not in data]
        passed = len(missing_fields) == 0
        message = f"Missing fields: {missing_fields}" if missing_fields else ""
        self.log_test(f"{test_name} - Required Fields", passed, message)
        return passed
    
    def get_all_users(self) -> List[Dict]:
        """Obtiene todos los usuarios actuales"""
        try:
            response = requests.get(f"{self.base_url}/users")
            if response.status_code == 200:
                return response.json()
            return []
        except:
            return []
    
    def test_api_health(self):
        """Test básico de conectividad"""
        print("🧪 Testing API connectivity")
        
        try:
            response = requests.get(f"{self.base_url}/users", timeout=5)
            passed = response.status_code in [200, 404, 500]
            self.log_test("API Health Check", passed, 
                         f"API is {'responsive' if passed else 'not responding'}")
            return passed
        except requests.exceptions.RequestException as e:
            self.log_test("API Health Check", False, f"Cannot connect to API: {e}")
            return False
    
    def test_get_initial_users(self):
        """Test: Obtener usuarios iniciales"""
        print("\n🧪 Testing GET /users (initial state)")
        
        try:
            response = requests.get(f"{self.base_url}/users")
            
            # Validar status code
            self.assert_status_code(response, 200, "GET /users")
            
            # Validar content-type
            self.assert_content_type(response, "application/json", "GET /users")
            
            # Validar que devuelve una lista
            data = response.json()
            passed = isinstance(data, list)
            self.log_test("GET /users - Response is list", passed, 
                         f"Expected list, got {type(data).__name__}")
            
            # Validar que hay al menos un usuario inicial
            passed = len(data) >= 1
            self.log_test("GET /users - Has initial user", passed, 
                         f"Expected at least 1 user, got {len(data)}")
            
            if data and len(data) > 0:
                # Validar estructura del primer usuario
                user = data[0]
                self.assert_json_has_fields(user, ['id', 'name', 'email'], "GET /users")
                
                # Validar que tiene los campos esperados (pero no valores específicos ya que pueden cambiar)
                passed = isinstance(user.get('name'), str) and len(user.get('name', '')) > 0
                self.log_test("GET /users - Valid name field", passed, 
                             f"Name should be non-empty string, got: {user.get('name')}")
                
                passed = isinstance(user.get('email'), str) and '@' in user.get('email', '')
                self.log_test("GET /users - Valid email field", passed, 
                             f"Email should contain @, got: {user.get('email')}")
            
            return data
            
        except requests.exceptions.RequestException as e:
            self.log_test("GET /users - Connection", False, f"Request failed: {e}")
            return []
    
    def test_create_user(self):
        """Test: Crear un nuevo usuario con email único"""
        print("\n🧪 Testing POST /users (create user)")
        
        # Generar datos únicos para evitar conflictos
        unique_email = self.generate_unique_email("testuser")
        test_user = {
            'name': 'Test User',
            'email': unique_email,
            'password': 'testpassword123'
        }
        
        try:
            response = requests.post(
                f"{self.base_url}/users",
                headers={'Content-Type': 'application/json'},
                data=json.dumps(test_user)
            )
            
            # Validar status code
            status_ok = self.assert_status_code(response, 201, "POST /users")
            
            # Validar content-type
            self.assert_content_type(response, "application/json", "POST /users")
            
            # Solo continuar con validaciones si el status code es correcto
            if status_ok and response.status_code == 201:
                # Validar estructura de respuesta
                data = response.json()
                self.assert_json_has_fields(data, ['id', 'name', 'email'], "POST /users")
                
                # Validar que los datos coinciden con lo enviado
                self.assert_json_field(data, 'name', test_user['name'], "POST /users")
                self.assert_json_field(data, 'email', test_user['email'], "POST /users")
                
                # Validar que NO devuelve el password
                passed = 'password' not in data
                self.log_test("POST /users - Password not in response", passed, 
                             "Password should not be returned in response")
                
                # Validar que el ID es un número
                passed = isinstance(data.get('id'), int)
                self.log_test("POST /users - ID is integer", passed, 
                             f"Expected int, got {type(data.get('id')).__name__}")
                
                # Guardar usuario creado para tracking
                if 'id' in data:
                    self.created_users.append(data)
                
                return data
            else:
                # Si falló la creación, registrar pero no hacer más validaciones
                self.log_test("POST /users - Creation failed", False, 
                             f"Status code {response.status_code}, response: {response.text}")
                return None
            
        except requests.exceptions.RequestException as e:
            self.log_test("POST /users - Connection", False, f"Request failed: {e}")
            return None
    
    def test_create_duplicate_user(self):
        """Test: Intentar crear usuario con email duplicado"""
        print("\n🧪 Testing POST /users (duplicate email)")
        
        # Usar el email del usuario inicial que sabemos que existe
        duplicate_user = {
            'name': 'Another User',
            'email': 'admin@example.com',  # Email que ya existe
            'password': 'anotherpassword'
        }
        
        try:
            response = requests.post(
                f"{self.base_url}/users",
                headers={'Content-Type': 'application/json'},
                data=json.dumps(duplicate_user)
            )
            
            # Debe devolver error 400
            self.assert_status_code(response, 400, "POST /users (duplicate)")
            
            # Validar mensaje de error
            if response.status_code == 400:
                data = response.json()
                expected_detail = "El email ya está registrado"
                actual_detail = data.get('detail', '')
                passed = expected_detail in actual_detail
                self.log_test("POST /users (duplicate) - Error message", passed, 
                             f"Expected '{expected_detail}' in '{actual_detail}'")
            
        except requests.exceptions.RequestException as e:
            self.log_test("POST /users (duplicate) - Connection", False, f"Request failed: {e}")
    
    def test_get_user_by_id(self, user_id: int):
        """Test: Obtener usuario por ID"""
        print(f"\n🧪 Testing GET /users/{user_id}")
        
        try:
            response = requests.get(f"{self.base_url}/users/{user_id}")
            
            # Validar status code
            self.assert_status_code(response, 200, f"GET /users/{user_id}")
            
            # Validar content-type
            self.assert_content_type(response, "application/json", f"GET /users/{user_id}")
            
            # Validar estructura
            if response.status_code == 200:
                data = response.json()
                self.assert_json_has_fields(data, ['id', 'name', 'email'], f"GET /users/{user_id}")
                
                # Validar que el ID coincide
                self.assert_json_field(data, 'id', user_id, f"GET /users/{user_id}")
                
                return data
            
        except requests.exceptions.RequestException as e:
            self.log_test(f"GET /users/{user_id} - Connection", False, f"Request failed: {e}")
            return None
    
    def test_get_nonexistent_user(self):
        """Test: Obtener usuario que no existe"""
        print("\n🧪 Testing GET /users/999 (non-existent)")
        
        try:
            response = requests.get(f"{self.base_url}/users/999")
            
            # Debe devolver error 404
            self.assert_status_code(response, 404, "GET /users/999 (non-existent)")
            
            # Validar mensaje de error
            if response.status_code == 404:
                data = response.json()
                expected_detail = "Usuario no encontrado"
                actual_detail = data.get('detail', '')
                passed = expected_detail in actual_detail
                self.log_test("GET /users/999 - Error message", passed, 
                             f"Expected '{expected_detail}' in '{actual_detail}'")
            
        except requests.exceptions.RequestException as e:
            self.log_test("GET /users/999 - Connection", False, f"Request failed: {e}")
    
    def test_data_persistence(self):
        """Test: Verificar que los datos persisten entre requests"""
        print("\n🧪 Testing data persistence")
        
        # Obtener usuarios antes
        users_before = self.get_all_users()
        initial_count = len(users_before)
        
        # Crear un usuario
        unique_email = self.generate_unique_email("persistence")
        test_user = {
            'name': 'Persistence Test User',
            'email': unique_email,
            'password': 'testpass'
        }
        
        try:
            # Crear usuario
            response = requests.post(
                f"{self.base_url}/users",
                headers={'Content-Type': 'application/json'},
                data=json.dumps(test_user)
            )
            
            if response.status_code == 201:
                # Obtener usuarios después
                users_after = self.get_all_users()
                final_count = len(users_after)
                
                # Validar que aumentó la cantidad
                passed = final_count == initial_count + 1
                self.log_test("Data Persistence - User count increased", passed,
                             f"Expected {initial_count + 1}, got {final_count}")
                
                # Validar que el nuevo usuario está en la lista
                created_user = response.json()
                user_found = any(u.get('email') == unique_email for u in users_after)
                self.log_test("Data Persistence - New user in list", user_found,
                             f"User with email {unique_email} should be in users list")
                
        except requests.exceptions.RequestException as e:
            self.log_test("Data Persistence - Connection", False, f"Request failed: {e}")
    
    def run_all_tests(self):
        """Ejecuta todos los tests"""
        print("🚀 Starting Enhanced API Tests")
        print("=" * 50)
        
        # Test de conectividad
        if not self.test_api_health():
            print("\n❌ API is not accessible. Make sure the server is running on http://127.0.0.1:8000")
            return
        
        # Tests principales
        initial_users = self.test_get_initial_users()
        created_user = self.test_create_user()
        self.test_create_duplicate_user()
        
        if created_user and 'id' in created_user:
            self.test_get_user_by_id(created_user['id'])
        
        self.test_get_nonexistent_user()
        self.test_data_persistence()
        
        # Resumen final
        self.print_summary()
    
    def print_summary(self):
        """Imprime el resumen de los tests"""
        print("\n" + "=" * 50)
        print("📊 TEST SUMMARY")
        print("=" * 50)
        
        total_tests = self.passed_tests + self.failed_tests
        success_rate = (self.passed_tests / total_tests * 100) if total_tests > 0 else 0
        
        print(f"Total Tests: {total_tests}")
        print(f"✅ Passed: {self.passed_tests}")
        print(f"❌ Failed: {self.failed_tests}")
        print(f"📈 Success Rate: {success_rate:.1f}%")
        
        if len(self.created_users) > 0:
            print(f"\n📝 Created {len(self.created_users)} test users during this run")
        
        if self.failed_tests == 0:
            print("\n🎉 All tests passed! Your API is working correctly.")
        else:
            print(f"\n⚠️  {self.failed_tests} test(s) failed. Check the details above.")
            
        return self.failed_tests == 0

def main():
    """Función principal"""
    print("🔧 Enhanced FastAPI User Management API Tester")
    print("This version uses unique emails to avoid conflicts between test runs")
    print("Make sure your API server is running on http://127.0.0.1:8000")
    print("You can start it with: uvicorn main:app --reload")
    
    input("\nPress Enter to start testing...")
    
    tester = APITesterEnhanced()
    tester.run_all_tests()
    
    # Exit code para CI/CD
    sys.exit(0 if tester.failed_tests == 0 else 1)

if __name__ == "__main__":
    main()

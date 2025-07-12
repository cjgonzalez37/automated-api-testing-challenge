# Automated API Testing Challenge - FastAPI User Management

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.104.1-green.svg)
![Pydantic](https://img.shields.io/badge/Pydantic-2.5.0-red.svg)
![Tests](https://img.shields.io/badge/tests-automated-brightgreen.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Status](https://img.shields.io/badge/status-active-success.svg)

Este proyecto contiene una API REST para gestión de usuarios construida con FastAPI.

## Archivos del Proyecto

- `main.py` - API principal con FastAPI
- `create_user.py` - Script cliente para crear usuarios
- `test_api.py` - **Script de testing automatizado completo**
- `run_tests.py` - Script de testing rápido
- `.venv/` - Entorno virtual de Python

## Cómo Ejecutar

### 1. Activar el entorno virtual
```bash
source .venv/bin/activate
```

### 2. Instalar dependencias (si es necesario)
```bash
pip install fastapi uvicorn requests pydantic
```

### 3. Ejecutar la API
```bash
uvicorn main:app --reload
```
La API estará disponible en: http://127.0.0.1:8000

### 4. Ver documentación automática
- Swagger UI: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc

## Testing Automatizado

### Script Completo de Testing (`test_api.py`)

Este script realiza pruebas exhaustivas de la API:

**Validaciones que realiza:**
- ✅ Status codes (200, 201, 400, 404)
- ✅ Content-Type headers
- ✅ Estructura del JSON de respuesta
- ✅ Campos requeridos en las respuestas
- ✅ Validación de datos específicos (nombre, email)
- ✅ Que no se devuelva el password
- ✅ Manejo de errores (email duplicado, usuario no encontrado)
- ✅ Tipos de datos correctos

**Cómo ejecutar:**
```bash
# Asegúrate de que la API esté corriendo primero
python test_api.py
```

**Ejemplo de salida:**
```
🚀 Starting API Tests
==================================================
🧪 Testing API connectivity
✅ PASS - API Health Check

🧪 Testing GET /users (initial state)
✅ PASS - GET /users - Status Code
✅ PASS - GET /users - Content-Type
✅ PASS - GET /users - Response is list
✅ PASS - GET /users - Has initial user
✅ PASS - GET /users - Required Fields
✅ PASS - GET /users - Field name
✅ PASS - GET /users - Field email

📊 TEST SUMMARY
==================================================
Total Tests: 15
✅ Passed: 15
❌ Failed: 0
📈 Success Rate: 100.0%

🎉 All tests passed! Your API is working correctly.
```

### Script de Testing Rápido (`run_tests.py`)

Para pruebas rápidas durante el desarrollo:

```bash
python run_tests.py
```

## Endpoints de la API

### GET /users
Obtiene todos los usuarios
- **Response:** Lista de usuarios (sin passwords)

### POST /users
Crea un nuevo usuario
- **Body:** `{"name": "string", "email": "string", "password": "string"}`
- **Response:** Usuario creado (sin password)
- **Status:** 201 si es exitoso, 400 si el email ya existe

### GET /users/{user_id}
Obtiene un usuario por ID
- **Response:** Usuario específico
- **Status:** 200 si existe, 404 si no existe

## Características del Testing

### Aserciones Implementadas
1. **Status Code Validation** - Verifica códigos HTTP correctos
2. **Content-Type Validation** - Asegura respuestas JSON
3. **Field Validation** - Verifica campos requeridos
4. **Data Integrity** - Confirma que los datos enviados coinciden con los recibidos
5. **Security Validation** - Verifica que passwords no se devuelvan
6. **Error Handling** - Prueba manejo correcto de errores
7. **Type Validation** - Verifica tipos de datos correctos

### Casos de Prueba Cubiertos
- ✅ Obtener usuarios iniciales
- ✅ Crear usuario válido
- ✅ Intentar crear usuario con email duplicado
- ✅ Obtener usuario por ID válido
- ✅ Intentar obtener usuario inexistente
- ✅ Conectividad básica de la API

## Uso en CI/CD

El script `test_api.py` devuelve códigos de salida apropiados:
- `0` si todos los tests pasan
- `1` si algún test falla

Esto permite integrarlo fácilmente en pipelines de CI/CD.

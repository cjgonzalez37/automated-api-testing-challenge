from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

# 1. Modelo de datos con Pydantic
# FastAPI usará esto para validar que los datos que llegan en la petición POST son correctos.
class User(BaseModel):
    name: str
    email: str
    password: str

# Modelo para la respuesta, para no devolver el password
class UserResponse(BaseModel):
    id: int
    name: str
    email: str

# 2. Crear la aplicación FastAPI
app = FastAPI()

# 3. "Base de datos" en memoria
# Una lista simple para guardar los usuarios que vamos creando.
# Empezamos con un usuario de ejemplo.
usuarios_db: List[UserResponse] = [
    UserResponse(id=0, name="Usuario Inicial", email="admin@example.com")
]

# 4. Endpoint para crear un usuario (POST)
@app.post("/users", response_model=UserResponse, status_code=201)
def create_user(user: User):
    """
    Crea un nuevo usuario y lo añade a la base de datos en memoria.
    """
    if any(u.email == user.email for u in usuarios_db):
        raise HTTPException(status_code=400, detail="El email ya está registrado")
    
    # Asignamos un nuevo ID
    new_id = len(usuarios_db)
    
    # Creamos el objeto de respuesta sin el password
    user_response = UserResponse(id=new_id, name=user.name, email=user.email)
    
    # Lo guardamos en nuestra "base de datos"
    usuarios_db.append(user_response)
    
    return user_response

# 5. Endpoint para obtener todos los usuarios (GET)
@app.get("/users", response_model=List[UserResponse])
def get_users():
    """
    Devuelve la lista completa de usuarios.
    """
    return usuarios_db

# 6. Endpoint para obtener un usuario por su ID (GET)
@app.get("/users/{user_id}", response_model=UserResponse)
def get_user(user_id: int):
    """
    Busca y devuelve un usuario por su ID.
    """
    # Busca el usuario en la "base de datos"
    for usuario in usuarios_db:
        if usuario.id == user_id:
            return usuario
    
    # Si el bucle termina y no se encontró el usuario, levanta un error HTTP 404
    raise HTTPException(status_code=404, detail="Usuario no encontrado")

import requests
import json

def create_user():
    # --- CONFIGURACIÓN: MODIFICA ESTAS VARIABLES ---
    
    # 1. La URL del endpoint de tu API para crear usuarios
    url = 'http://127.0.0.1:8000/users'
    
    # 2. Los datos del usuario que quieres crear.
    #    Asegúrate de que las claves coincidan con lo que tu API espera.
    user_data = {
        'name': 'Evelin Test',
        'email': 'evelin.test@example.com',
        'password': 'supersecretpassword'
    }
    
    # 3. Encabezados de la petición. El Content-Type para JSON es estándar.
    #    Si tu API necesita un token de autenticación, descomenta y edita la línea de 'Authorization'.
    headers = {
        'Content-Type': 'application/json',
        # 'Authorization': 'Bearer TU_TOKEN_DE_API_AQUI'
    }
    
    # --- LÓGICA DE LA PETICIÓN ---
    
    try:
        # Hacemos la petición POST, enviando los datos como JSON
        response = requests.post(url, headers=headers, data=json.dumps(user_data))
        
        # Verificamos si la petición fue exitosa (código de estado 2xx)
        response.raise_for_status()
        
        print("¡Usuario creado exitosamente!")
        print("Respuesta de la API:")
        print(response.json())
        
    except requests.exceptions.HTTPError as http_err:
        print(f"Error HTTP: {http_err}")
        print(f"Cuerpo de la respuesta: {response.text}")
    except requests.exceptions.RequestException as req_err:
        print(f"Error en la petición: {req_err}")

if __name__ == "__main__":
    create_user()
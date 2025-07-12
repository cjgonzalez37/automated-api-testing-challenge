import requests
import json

def create_user():
    # --- CONFIGURATION: MODIFY THESE VARIABLES ---
    
    # 1. The URL of your API endpoint for creating users
    url = 'http://127.0.0.1:8000/users'
    
    # 2. The data of the user you want to create.
    #    Make sure the keys match what your API expects.
    user_data = {
        'name': 'Evelin Test',
        'email': 'evelin.test@example.com',
        'password': 'supersecretpassword'
    }
    
    # 3. Request headers. The Content-Type for JSON is standard.
    #    If your API needs an authentication token, uncomment and edit the 'Authorization' line.
    headers = {
        'Content-Type': 'application/json',
        # 'Authorization': 'Bearer YOUR_API_TOKEN_HERE'
    }
    
    # --- REQUEST LOGIC ---
    
    try:
        # We make the POST request, sending the data as JSON
        response = requests.post(url, headers=headers, data=json.dumps(user_data))
        
        # We check if the request was successful (2xx status code)
        response.raise_for_status()
        
        print("User created successfully!")
        print("API Response:")
        print(response.json())
        
    except requests.exceptions.HTTPError as http_err:
        print(f"Error HTTP: {http_err}")
        print(f"Cuerpo de la respuesta: {response.text}")
    except requests.exceptions.RequestException as req_err:
        print(f"Error en la petición: {req_err}")

if __name__ == "__main__":
    create_user()
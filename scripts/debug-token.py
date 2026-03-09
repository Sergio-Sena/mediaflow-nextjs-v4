import requests
import json

API_URL = 'https://gdb962d234.execute-api.us-east-1.amazonaws.com/prod'

print("=== DEBUG TOKEN JWT ===\n")

# Login
print("[1] Fazendo login...")
login_response = requests.post(f'{API_URL}/auth/login', json={
    'email': 'sergio@midiaflow.com',
    'password': 'admin123'
})

print(f"Status: {login_response.status_code}")
print(f"Response: {json.dumps(login_response.json(), indent=2)}\n")

if login_response.status_code == 200:
    data = login_response.json()
    token = data.get('token')
    
    print(f"[2] Token recebido:")
    print(f"Token: {token[:50]}...\n")
    
    # Testar com token
    print("[3] Testando endpoint /users/list...")
    headers = {'Authorization': f'Bearer {token}'}
    print(f"Headers: {headers}\n")
    
    users_response = requests.get(f'{API_URL}/users/list', headers=headers)
    print(f"Status: {users_response.status_code}")
    print(f"Response: {users_response.text}\n")
    
    # Testar sem Bearer
    print("[4] Testando SEM 'Bearer'...")
    headers2 = {'Authorization': token}
    users_response2 = requests.get(f'{API_URL}/users/list', headers=headers2)
    print(f"Status: {users_response2.status_code}")
    print(f"Response: {users_response2.text}\n")
    
    # Testar com x-access-token
    print("[5] Testando com 'x-access-token'...")
    headers3 = {'x-access-token': token}
    users_response3 = requests.get(f'{API_URL}/users/list', headers=headers3)
    print(f"Status: {users_response3.status_code}")
    print(f"Response: {users_response3.text}")

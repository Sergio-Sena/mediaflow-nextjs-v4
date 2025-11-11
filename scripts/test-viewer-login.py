import requests
import json

API_URL = "https://api.midiaflow.sstechnologies-cloud.com"

# 1. Login como sergio_sena
print("1. Fazendo login como sergio_sena...")
login_response = requests.post(f"{API_URL}/auth", json={
    "email": "sergio.sena@sstechnologies.com.br",
    "password": "senha123"
})

print(f"Status: {login_response.status_code}")
login_data = login_response.json()
print(f"Success: {login_data.get('success')}")

if login_data.get('success'):
    token = login_data.get('token')
    user = login_data.get('user')
    
    print(f"\nUser: {user}")
    
    # 2. Listar arquivos
    print("\n2. Listando arquivos...")
    files_response = requests.get(
        f"{API_URL}/files",
        headers={"Authorization": f"Bearer {token}"}
    )
    
    print(f"Status: {files_response.status_code}")
    files_data = files_response.json()
    
    if files_data.get('success'):
        files = files_data.get('files', [])
        print(f"\nTotal de arquivos: {len(files)}")
        
        if files:
            print("\nPrimeiros 5 arquivos:")
            for f in files[:5]:
                print(f"  - {f['name']} ({f['folder']})")
        else:
            print("\nNENHUM arquivo retornado!")
            print("\nDEBUG - Token decodificado:")
            import jwt
            decoded = jwt.decode(token, options={"verify_signature": False})
            print(json.dumps(decoded, indent=2))
    else:
        print(f"Erro: {files_data}")
else:
    print(f"Erro no login: {login_data}")

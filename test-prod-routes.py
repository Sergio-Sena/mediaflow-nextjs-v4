import requests
import json

BASE_URL = "https://gdb962d234.execute-api.us-east-1.amazonaws.com/prod"

# Simular login para pegar token
print("1. Testando login...")
login_response = requests.post(
    f"{BASE_URL}/auth/login",
    json={"email": "sergio@midiaflow.com", "password": "admin123"}
)
print(f"   Status: {login_response.status_code}")

if login_response.status_code == 200:
    data = login_response.json()
    token = data.get('token')
    print(f"   Token obtido: {token[:20]}...")
    
    # Testar listagem de arquivos
    print("\n2. Testando listagem de arquivos...")
    headers = {"Authorization": f"Bearer {token}"}
    files_response = requests.get(f"{BASE_URL}/files", headers=headers)
    print(f"   Status: {files_response.status_code}")
    
    if files_response.status_code == 200:
        files = files_response.json()
        print(f"   Arquivos encontrados: {len(files.get('files', []))}")
        
        # Pegar primeiro vídeo para testar
        video_files = [f for f in files.get('files', []) if f.get('key', '').endswith('.mp4')]
        
        if video_files:
            test_video = video_files[0]
            print(f"\n3. Testando URL pré-assinada para: {test_video['key']}")
            
            view_response = requests.get(
                f"{BASE_URL}/view/{test_video['key']}",
                headers=headers
            )
            print(f"   Status: {view_response.status_code}")
            
            if view_response.status_code == 200:
                view_data = view_response.json()
                if view_data.get('success'):
                    print(f"   ✓ URL pré-assinada gerada com sucesso!")
                    print(f"   URL: {view_data['viewUrl'][:80]}...")
                else:
                    print(f"   ✗ Erro: {view_data.get('message')}")
            else:
                print(f"   X Erro HTTP: {view_response.text}")
        else:
            print("   Nenhum vídeo encontrado para testar")
    else:
        print(f"   ✗ Erro ao listar arquivos: {files_response.text}")
else:
    print(f"   ✗ Erro no login: {login_response.text}")

print("\n" + "="*50)
print("Teste concluído!")

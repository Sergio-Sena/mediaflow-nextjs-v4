import requests
import json

# Test API Gateway endpoint
API_URL = "https://gdb962d234.execute-api.us-east-1.amazonaws.com/prod/view"
TEST_KEY = "users/sergio_sena/SergioSenaTeste.mp4"

# Get token from your browser (F12 > Application > Local Storage > token)
TOKEN = input("Cole o token JWT aqui: ").strip()

print(f"\n[TEST] Testando API /view com key: {TEST_KEY}")
print(f"[TEST] URL: {API_URL}/{TEST_KEY}\n")

try:
    response = requests.get(
        f"{API_URL}/{TEST_KEY}",
        headers={
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {TOKEN}'
        }
    )
    
    print(f"[STATUS] {response.status_code}")
    print(f"[HEADERS] {dict(response.headers)}\n")
    
    if response.status_code == 200:
        data = response.json()
        print(f"[SUCCESS] {json.dumps(data, indent=2)}")
        
        if data.get('success') and data.get('viewUrl'):
            print(f"\n[OK] URL presignada gerada com sucesso!")
            print(f"[URL] {data['viewUrl'][:100]}...")
            
            # Test if URL works
            print(f"\n[TEST] Testando se a URL presignada funciona...")
            video_response = requests.head(data['viewUrl'])
            print(f"[VIDEO STATUS] {video_response.status_code}")
            
            if video_response.status_code == 200:
                print(f"[OK] Video acessivel! Tamanho: {video_response.headers.get('Content-Length')} bytes")
            else:
                print(f"[ERRO] Video nao acessivel")
        else:
            print(f"[ERRO] Resposta invalida da API")
    else:
        print(f"[ERRO] {response.text}")
        
except Exception as e:
    print(f"[ERRO] {str(e)}")

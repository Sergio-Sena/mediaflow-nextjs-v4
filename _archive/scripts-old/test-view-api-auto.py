import requests
import json

API_URL = "https://gdb962d234.execute-api.us-east-1.amazonaws.com/prod/view"
TEST_KEY = "users/sergio_sena/SergioSenaTeste.mp4"
TOKEN = "eyJhbGciOiAiSFMyNTYiLCAidHlwIjogIkpXVCJ9.eyJlbWFpbCI6ICJzZXJnaW9AbWlkaWFmbG93LmNvbSIsICJ1c2VyX2lkIjogInNlcmdpb19zZW5hIiwgInMzX3ByZWZpeCI6ICJ1c2Vycy9zZXJnaW9fc2VuYS8iLCAicm9sZSI6ICJ1c2VyIiwgImV4cCI6IDE3NjM1NzQ2MDV9.qunxamUFMvJuuMn3UE2Bl0i2klWdCX3t3KASCTwXjjE"

print(f"[TEST] Testando API /view")
print(f"[URL] {API_URL}/{TEST_KEY}\n")

try:
    response = requests.get(
        f"{API_URL}/{TEST_KEY}",
        headers={
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {TOKEN}'
        }
    )
    
    print(f"[STATUS] {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"[SUCCESS] {json.dumps(data, indent=2)}")
        
        if data.get('success') and data.get('viewUrl'):
            print(f"\n[OK] URL presignada gerada!")
            print(f"[URL] {data['viewUrl'][:100]}...")
            
            print(f"\n[TEST] Testando acesso ao video...")
            video_response = requests.head(data['viewUrl'])
            print(f"[VIDEO] Status {video_response.status_code}")
            
            if video_response.status_code == 200:
                size = int(video_response.headers.get('Content-Length', 0))
                print(f"[OK] Video acessivel! Tamanho: {size / 1024 / 1024:.2f} MB")
                print(f"\n[RESULTADO FINAL] ✅ TUDO FUNCIONANDO!")
            else:
                print(f"[ERRO] Video nao acessivel")
        else:
            print(f"[ERRO] Resposta invalida")
    else:
        print(f"[ERRO] {response.text}")
        print(f"\n[RESULTADO FINAL] ❌ API COM ERRO")
        
except Exception as e:
    print(f"[ERRO] {str(e)}")
    print(f"\n[RESULTADO FINAL] ❌ FALHA NA CONEXAO")

import requests
import time

print("[INFO] Aguardando 10 segundos...")
time.sleep(10)

API_URL = "https://gdb962d234.execute-api.us-east-1.amazonaws.com/prod/view/users/sergio_sena/SergioSenaTeste.mp4"

print(f"[TEST] {API_URL}\n")

response = requests.get(API_URL)

print(f"Status: {response.status_code}")
print(f"Headers: {dict(response.headers)}")
print(f"Response: {response.text[:300]}\n")

if response.status_code == 200:
    data = response.json()
    if data.get('success') and data.get('viewUrl'):
        print("[OK] Lambda funcionando!")
        print(f"[URL] {data['viewUrl'][:100]}...")
    else:
        print("[ERRO] Resposta invalida")
else:
    print("[ERRO] Lambda com problema")

import requests
import time

print("[INFO] Aguardando 10 segundos...")
time.sleep(10)

API_URL = "https://gdb962d234.execute-api.us-east-1.amazonaws.com/prod/view"
TEST_KEY = "users/sergio_sena/SergioSenaTeste.mp4"
TOKEN = "eyJhbGciOiAiSFMyNTYiLCAidHlwIjogIkpXVCJ9.eyJlbWFpbCI6ICJzZXJnaW9AbWlkaWFmbG93LmNvbSIsICJ1c2VyX2lkIjogInNlcmdpb19zZW5hIiwgInMzX3ByZWZpeCI6ICJ1c2Vycy9zZXJnaW9fc2VuYS8iLCAicm9sZSI6ICJ1c2VyIiwgImV4cCI6IDE3NjM1NzQ2MDV9.qunxamUFMvJuuMn3UE2Bl0i2klWdCX3t3KASCTwXjjE"

print(f"[TEST] {API_URL}/{TEST_KEY}\n")

response = requests.get(
    f"{API_URL}/{TEST_KEY}",
    headers={
        'Authorization': f'Bearer {TOKEN}',
        'Content-Type': 'application/json'
    }
)

print(f"Status: {response.status_code}")
print(f"Response: {response.text[:200]}")

if response.status_code == 200:
    print("\n[OK] API FUNCIONANDO!")
else:
    print("\n[ERRO] API COM PROBLEMA")

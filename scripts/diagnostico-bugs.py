"""
Script de Diagnóstico - MidiaFlow v4.8.5
Testa: Upload, Delete, Avatar
"""
import requests
import json

API_BASE = "https://gdb962d234.execute-api.us-east-1.amazonaws.com/prod"

# Obter token (substitua com seu token válido)
TOKEN = input("Cole seu token JWT: ").strip()

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {TOKEN}"
}

print("\n" + "="*60)
print("🔍 DIAGNÓSTICO MIDIAFLOW v4.8.5")
print("="*60)

# 1. Testar Upload Presigned
print("\n1️⃣ Testando Upload Presigned...")
try:
    response = requests.post(
        f"{API_BASE}/upload/presigned",
        headers=headers,
        json={
            "filename": "test_diagnostic.txt",
            "contentType": "text/plain",
            "fileSize": 100
        }
    )
    print(f"   Status: {response.status_code}")
    print(f"   Response: {json.dumps(response.json(), indent=2)}")
    if response.status_code == 200:
        print("   ✅ Upload presigned OK")
    else:
        print("   ❌ Upload presigned FALHOU")
except Exception as e:
    print(f"   ❌ Erro: {e}")

# 2. Testar Delete
print("\n2️⃣ Testando Delete...")
try:
    response = requests.delete(
        f"{API_BASE}/files/delete",
        headers=headers,
        json={"key": "users/sergio_sena/test.txt"}
    )
    print(f"   Status: {response.status_code}")
    print(f"   Response: {response.text}")
    if response.status_code == 200:
        print("   ✅ Delete OK")
    else:
        print("   ❌ Delete FALHOU")
except Exception as e:
    print(f"   ❌ Erro: {e}")

# 3. Testar Avatar
print("\n3️⃣ Testando Avatar...")
try:
    response = requests.get(
        f"{API_BASE}/users/me",
        headers=headers
    )
    print(f"   Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"   Avatar URL: {data.get('avatar_url', 'N/A')}")
        print("   ✅ Avatar endpoint OK")
    else:
        print(f"   Response: {response.text}")
        print("   ❌ Avatar endpoint FALHOU")
except Exception as e:
    print(f"   ❌ Erro: {e}")

print("\n" + "="*60)
print("✅ Diagnóstico concluído")
print("="*60)

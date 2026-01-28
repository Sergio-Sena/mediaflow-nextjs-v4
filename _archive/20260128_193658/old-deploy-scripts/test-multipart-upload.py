#!/usr/bin/env python3
import boto3
import requests
import json

token = "eyJhbGciOiAiSFMyNTYiLCAidHlwIjogIkpXVCJ9.eyJlbWFpbCI6ICJzZXJnaW9AbWlkaWFmbG93LmNvbSIsICJ1c2VyX2lkIjogInNlcmdpb19zZW5hIiwgInMzX3ByZWZpeCI6ICJ1c2Vycy9zZXJnaW9fc2VuYS8iLCAicm9sZSI6ICJ1c2VyIiwgImV4cCI6IDE3NjM2NDQ5Mjh9.gWT_U_mgrS-74hZc7bxgOfbdxIchDvtmjKv2k7VqA5Q"
api_url = "https://gdb962d234.execute-api.us-east-1.amazonaws.com/prod"
headers = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json"
}

print("=== TESTE MULTIPART UPLOAD ===\n")

# 1. INIT
print("1. Chamando /multipart/init...")
init_response = requests.post(
    f"{api_url}/multipart/init",
    json={"filename": "test.mp4", "fileSize": 100000000},
    headers=headers,
    timeout=10
)
print(f"   Status: {init_response.status_code}")
init_data = init_response.json()
print(f"   Response: {init_data}\n")

upload_id = init_data['uploadId']
key = init_data['key']

# 2. GET PART URL
print("2. Chamando /multipart/part para part 1...")
part_response = requests.post(
    f"{api_url}/multipart/part",
    json={"key": key, "uploadId": upload_id, "partNumber": 1},
    headers=headers,
    timeout=10
)
print(f"   Status: {part_response.status_code}")
part_data = part_response.json()
print(f"   Got upload URL: {part_data['uploadUrl'][:80]}...\n")

# 3. UPLOAD CHUNK
print("3. Fazendo upload do chunk...")
chunk = b"x" * 1000000  # 1MB fake data
upload_response = requests.put(
    part_data['uploadUrl'],
    data=chunk,
    timeout=30
)
print(f"   Status: {upload_response.status_code}")
etag = upload_response.headers.get('ETag', '').replace('"', '')
print(f"   ETag: {etag}\n")

# 4. COMPLETE
print("4. Chamando /multipart/complete...")
complete_response = requests.post(
    f"{api_url}/multipart/complete",
    json={
        "key": key,
        "uploadId": upload_id,
        "parts": [{"PartNumber": 1, "ETag": etag}]
    },
    headers=headers,
    timeout=10
)
print(f"   Status: {complete_response.status_code}")
print(f"   Response: {complete_response.json()}\n")

print("✅ Upload multipart completo com sucesso!")

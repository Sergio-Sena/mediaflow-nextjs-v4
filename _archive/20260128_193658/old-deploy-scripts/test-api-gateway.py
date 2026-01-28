#!/usr/bin/env python3
import requests
import json

url = "https://gdb962d234.execute-api.us-east-1.amazonaws.com/prod/multipart/init"
token = "eyJhbGciOiAiSFMyNTYiLCAidHlwIjogIkpXVCJ9.eyJlbWFpbCI6ICJzZXJnaW9AbWlkaWFmbG93LmNvbSIsICJ1c2VyX2lkIjogInNlcmdpb19zZW5hIiwgInMzX3ByZWZpeCI6ICJ1c2Vycy9zZXJnaW9fc2VuYS8iLCAicm9sZSI6ICJ1c2VyIiwgImV4cCI6IDE3NjM2NDQ5Mjh9.gWT_U_mgrS-74hZc7bxgOfbdxIchDvtmjKv2k7VqA5Q"

headers = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json"
}

data = {
    "filename": "Star/kate kuray/test.mp4",
    "fileSize": 1000000000
}

print(f"Testando API Gateway: {url}\n")

try:
    response = requests.post(url, json=data, headers=headers, timeout=10)
    print(f"Status: {response.status_code}")
    print(f"Headers: {dict(response.headers)}")
    print(f"Body: {response.text}")
except Exception as e:
    print(f"Erro: {str(e)}")

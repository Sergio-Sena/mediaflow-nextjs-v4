#!/usr/bin/env python3
import requests

url = "https://gdb962d234.execute-api.us-east-1.amazonaws.com/prod/multipart/init"

headers = {
    "Origin": "https://midiaflow.sstechnologies-cloud.com",
    "Access-Control-Request-Method": "POST",
    "Access-Control-Request-Headers": "content-type,authorization"
}

print("Testando CORS preflight OPTIONS...\n")

try:
    response = requests.options(url, headers=headers, timeout=5)
    print(f"Status: {response.status_code}")
    print(f"Headers: {dict(response.headers)}")
    print(f"Body: {response.text}")
except Exception as e:
    print(f"Erro: {str(e)}")

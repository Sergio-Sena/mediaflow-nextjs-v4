#!/usr/bin/env python3
import requests
import json

ENDPOINT = 'https://gdb962d234.execute-api.us-east-1.amazonaws.com/prod/multipart'

print("=== Teste 1: Iniciar Multipart Upload ===")
response = requests.post(ENDPOINT, json={
    'action': 'initiate',
    'filename': 'test-multipart.txt',
    'contentType': 'text/plain'
})

print(f"Status: {response.status_code}")
print(f"Response: {response.json()}")

if response.status_code == 200:
    data = response.json()
    if data.get('success'):
        upload_id = data['uploadId']
        print(f"\nOK Upload ID: {upload_id}")
        
        print("\n=== Teste 2: Obter Presigned URL ===")
        response2 = requests.post(ENDPOINT, json={
            'action': 'get-url',
            'uploadId': upload_id,
            'key': 'test-multipart.txt',
            'partNumber': 1
        })
        
        print(f"Status: {response2.status_code}")
        data2 = response2.json()
        print(f"Response: {data2}")
        
        if data2.get('success'):
            print(f"\nOK Presigned URL gerada")
            
            print("\n=== Teste 3: Abortar Upload ===")
            response3 = requests.post(ENDPOINT, json={
                'action': 'abort',
                'uploadId': upload_id,
                'key': 'test-multipart.txt'
            })
            
            print(f"Status: {response3.status_code}")
            print(f"Response: {response3.json()}")
            
            if response3.json().get('success'):
                print("\nOK Upload abortado")
                print("\n=== TODOS OS TESTES PASSARAM ===")
            else:
                print("\nERRO: Falha ao abortar")
        else:
            print("\nERRO: Falha ao gerar URL")
    else:
        print("\nERRO: Falha ao iniciar upload")
else:
    print(f"\nERRO: Status {response.status_code}")

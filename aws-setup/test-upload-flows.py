#!/usr/bin/env python3
import requests
import json

print("=" * 60)
print("TESTE DE FLUXOS DE UPLOAD")
print("=" * 60)

# Simular tamanhos
FILE_4GB = 4 * 1024 * 1024 * 1024  # 4GB
FILE_7GB = 7 * 1024 * 1024 * 1024  # 7GB

print("\n[TESTE 1] Arquivo 4GB - Deve usar UPLOAD SIMPLES")
print("-" * 60)

# 1. Upload simples (presigned URL)
print("\n1.1 Solicitar presigned URL...")
response = requests.post(
    'https://gdb962d234.execute-api.us-east-1.amazonaws.com/prod/upload/presigned',
    json={
        'filename': 'test-4gb.mp4',
        'contentType': 'video/mp4',
        'fileSize': FILE_4GB
    }
)

print(f"Status: {response.status_code}")
if response.status_code == 200:
    data = response.json()
    print(f"Success: {data.get('success')}")
    if data.get('success'):
        print(f"Upload URL: {data.get('uploadUrl')[:80]}...")
        print("OK Upload simples funcionando")
    else:
        print(f"ERRO: {data.get('message')}")
else:
    print(f"ERRO: Status {response.status_code}")
    print(response.text)

print("\n" + "=" * 60)
print("[TESTE 2] Arquivo 7GB - Deve usar MULTIPART")
print("-" * 60)

# 2. Multipart upload
print("\n2.1 Iniciar multipart upload...")
response = requests.post(
    'https://gdb962d234.execute-api.us-east-1.amazonaws.com/prod/multipart',
    json={
        'action': 'initiate',
        'filename': 'test-7gb.mp4',
        'contentType': 'video/mp4'
    }
)

print(f"Status: {response.status_code}")
if response.status_code == 200:
    data = response.json()
    print(f"Success: {data.get('success')}")
    
    if data.get('success'):
        upload_id = data.get('uploadId')
        print(f"Upload ID: {upload_id[:50]}...")
        
        print("\n2.2 Obter presigned URL para parte 1...")
        response2 = requests.post(
            'https://gdb962d234.execute-api.us-east-1.amazonaws.com/prod/multipart',
            json={
                'action': 'get-url',
                'uploadId': upload_id,
                'key': 'test-7gb.mp4',
                'partNumber': 1
            }
        )
        
        print(f"Status: {response2.status_code}")
        if response2.status_code == 200:
            data2 = response2.json()
            print(f"Success: {data2.get('success')}")
            if data2.get('success'):
                print(f"Presigned URL: {data2.get('presignedUrl')[:80]}...")
                
                print("\n2.3 Abortar upload (cleanup)...")
                response3 = requests.post(
                    'https://gdb962d234.execute-api.us-east-1.amazonaws.com/prod/multipart',
                    json={
                        'action': 'abort',
                        'uploadId': upload_id,
                        'key': 'test-7gb.mp4'
                    }
                )
                
                print(f"Status: {response3.status_code}")
                if response3.status_code == 200:
                    print("OK Multipart funcionando")
                else:
                    print(f"ERRO ao abortar: {response3.status_code}")
            else:
                print(f"ERRO: {data2.get('message')}")
        else:
            print(f"ERRO: Status {response2.status_code}")
    else:
        print(f"ERRO: {data.get('message')}")
else:
    print(f"ERRO: Status {response.status_code}")
    print(response.text)

print("\n" + "=" * 60)
print("[TESTE 3] Sanitização de Nomes")
print("-" * 60)

test_filenames = [
    'arquivo normal.mp4',
    'arquivo com espaços e acentuação.mp4',
    '../../../etc/passwd',
    'arquivo<script>alert(1)</script>.mp4',
    'arquivo\x00null.mp4'
]

for filename in test_filenames:
    print(f"\nTestando: {repr(filename)}")
    response = requests.post(
        'https://gdb962d234.execute-api.us-east-1.amazonaws.com/prod/multipart',
        json={
            'action': 'initiate',
            'filename': filename,
            'contentType': 'video/mp4'
        }
    )
    
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        if data.get('success'):
            print(f"OK Aceito (uploadId: {data.get('uploadId')[:30]}...)")
            # Cleanup
            requests.post(
                'https://gdb962d234.execute-api.us-east-1.amazonaws.com/prod/multipart',
                json={
                    'action': 'abort',
                    'uploadId': data.get('uploadId'),
                    'key': filename
                }
            )
        else:
            print(f"Rejeitado: {data.get('message')}")
    else:
        print(f"ERRO: {response.status_code}")

print("\n" + "=" * 60)
print("RESUMO DOS TESTES")
print("=" * 60)
print("1. Upload simples (4GB): Verificar se retornou 200")
print("2. Multipart (7GB): Verificar se retornou 200 em todas etapas")
print("3. Sanitizacao: Verificar se nomes perigosos foram tratados")
print("=" * 60)

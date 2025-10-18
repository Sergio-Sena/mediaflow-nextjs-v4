#!/usr/bin/env python3
import requests

print("TESTE: Arquivos dentro de pastas")
print("=" * 60)

test_cases = [
    'pasta/arquivo.mp4',
    'pasta/subpasta/arquivo.mp4',
    'Lid/video-grande.mp4',
    'Sergio Sena/documento.pdf',
    'pasta/../arquivo.mp4',  # Path traversal
]

for filename in test_cases:
    print(f"\nTestando: {filename}")
    response = requests.post(
        'https://gdb962d234.execute-api.us-east-1.amazonaws.com/prod/multipart',
        json={
            'action': 'initiate',
            'filename': filename,
            'contentType': 'video/mp4'
        }
    )
    
    if response.status_code == 200:
        data = response.json()
        if data.get('success'):
            upload_id = data.get('uploadId')
            print(f"  OK Aceito (uploadId: {upload_id[:30]}...)")
            
            # Cleanup
            requests.post(
                'https://gdb962d234.execute-api.us-east-1.amazonaws.com/prod/multipart',
                json={
                    'action': 'abort',
                    'uploadId': upload_id,
                    'key': filename
                }
            )
        else:
            print(f"  ERRO: {data.get('message')}")
    else:
        print(f"  ERRO: Status {response.status_code}")

print("\n" + "=" * 60)
print("RESULTADO: Verificar se pastas foram preservadas")

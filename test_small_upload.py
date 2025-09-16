#!/usr/bin/env python3
import requests
import json
import os

def test_small_upload():
    api_url = "https://gdb962d234.execute-api.us-east-1.amazonaws.com/prod"
    
    # Arquivo menor: PDF (135KB)
    test_file = "teste/Orçamento telhadoAudo3.pdf"
    
    if not os.path.exists(test_file):
        print(f"Arquivo não encontrado: {test_file}")
        return
    
    file_size = os.path.getsize(test_file)
    print(f"TESTE UPLOAD PEQUENO")
    print(f"Arquivo: {test_file}")
    print(f"Tamanho: {file_size} bytes ({file_size/1024:.1f} KB)")
    print("=" * 50)
    
    try:
        # 1. Obter presigned URL
        print("1. Obtendo presigned URL...")
        response = requests.post(
            f"{api_url}/upload",
            json={
                "filename": "test_pdf_pequeno.pdf",
                "contentType": "application/pdf",
                "fileSize": file_size
            },
            headers={"Content-Type": "application/json"}
        )
        
        print(f"Status: {response.status_code}")
        
        if response.status_code != 200:
            print(f"Erro: {response.text}")
            return
            
        data = response.json()
        if not data.get('success'):
            print(f"Erro: {data.get('message')}")
            return
            
        upload_url = data['uploadUrl']
        print(f"✅ Presigned URL obtida")
        
        # 2. Upload do arquivo
        print("2. Fazendo upload...")
        with open(test_file, 'rb') as f:
            upload_response = requests.put(
                upload_url,
                data=f,
                headers={'Content-Type': 'application/pdf'}
            )
        
        print(f"Upload Status: {upload_response.status_code}")
        
        if upload_response.status_code in [200, 204]:
            print("✅ UPLOAD PEQUENO SUCESSO!")
            print("Estratégia SmallFileUpload funcionando!")
        else:
            print(f"❌ Upload falhou: {upload_response.status_code}")
            print(f"Response: {upload_response.text}")
            
    except Exception as e:
        print(f"❌ Erro: {e}")

if __name__ == "__main__":
    test_small_upload()
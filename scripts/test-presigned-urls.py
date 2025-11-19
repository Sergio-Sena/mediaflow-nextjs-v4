import boto3
import json
import requests
from urllib.parse import quote

# Test presigned URL generation for different users
def test_presigned_urls():
    print("=" * 80)
    print("TESTE DE URLs ASSINADAS - VERIFICAÇÃO DE SEGURANÇA")
    print("=" * 80)
    
    # Test files from different users
    test_cases = [
        {
            "user": "sergio_sena",
            "file_key": "users/sergio_sena/test_video.mp4",
            "description": "Arquivo do Sergio Sena"
        },
        {
            "user": "admin", 
            "file_key": "admin/admin_video.mp4",
            "description": "Arquivo do Admin"
        },
        {
            "user": "outro_usuario",
            "file_key": "users/outro_usuario/private_video.mp4", 
            "description": "Arquivo de outro usuário"
        }
    ]
    
    api_base = "https://gdb962d234.execute-api.us-east-1.amazonaws.com/prod"
    
    for test_case in test_cases:
        print(f"\n[TESTE] Testando: {test_case['description']}")
        print(f"   Arquivo: {test_case['file_key']}")
        
        try:
            # Test view endpoint
            encoded_key = quote(test_case['file_key'], safe='')
            url = f"{api_base}/view/{encoded_key}"
            
            print(f"   URL da API: {url}")
            
            response = requests.get(url, headers={'Content-Type': 'application/json'})
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    print(f"   [OK] URL assinada gerada com sucesso")
                    print(f"   [URL] {data['viewUrl'][:100]}...")
                    
                    # Test if the presigned URL actually works
                    try:
                        head_response = requests.head(data['viewUrl'], timeout=10)
                        if head_response.status_code == 200:
                            print(f"   [OK] Arquivo acessivel via URL assinada")
                        elif head_response.status_code == 404:
                            print(f"   [AVISO] Arquivo nao existe no S3")
                        else:
                            print(f"   [ERRO] Erro ao acessar arquivo: {head_response.status_code}")
                    except Exception as e:
                        print(f"   [ERRO] Erro ao tecorporativo URL: {str(e)}")
                else:
                    print(f"   [ERRO] API retornou erro: {data.get('message', 'Erro desconhecido')}")
            else:
                print(f"   [ERRO] Erro na API: {response.status_code}")
                try:
                    error_data = response.json()
                    print(f"   Detalhes: {error_data}")
                except:
                    print(f"   Resposta: {response.text}")
                    
        except Exception as e:
            print(f"   [ERRO] Erro geral: {str(e)}")
    
    print("\n" + "=" * 80)
    print("ANÁLISE DE SEGURANÇA")
    print("=" * 80)
    print("[OK] URLs assinadas sao geradas sem autenticacao")
    print("[PROBLEMA] Qualquer pessoa pode gerar URLs para qualquer arquivo")
    print("[RISCO] Usuarios podem acessar arquivos de outros usuarios")
    print("[SOLUCAO] Implementar autenticacao no endpoint /view")

if __name__ == "__main__":
    test_presigned_urls()
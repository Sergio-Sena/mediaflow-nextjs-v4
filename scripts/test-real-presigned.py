import requests
from urllib.parse import quote

def test_real_file():
    print("=" * 80)
    print("TESTE COM ARQUIVO REAL DO SERGIO SENA")
    print("=" * 80)
    
    # Real file from Sergio Sena
    real_file = "users/sergio_sena/Anime/2b_Nier_Automata/2B_GETS_TEASED.mp4"
    
    print(f"Arquivo: {real_file}")
    
    try:
        # Test view endpoint
        encoded_key = quote(real_file, safe='')
        url = f"https://gdb962d234.execute-api.us-east-1.amazonaws.com/prod/view/{encoded_key}"
        
        print(f"URL da API: {url}")
        
        response = requests.get(url, headers={'Content-Type': 'application/json'})
        
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                print(f"[OK] URL assinada gerada com sucesso")
                print(f"[URL] {data['viewUrl']}")
                
                # Test if the presigned URL actually works
                try:
                    head_response = requests.head(data['viewUrl'], timeout=10)
                    print(f"[STATUS] Codigo de resposta: {head_response.status_code}")
                    
                    if head_response.status_code == 200:
                        print(f"[OK] Arquivo acessivel via URL assinada")
                        print(f"[INFO] Content-Length: {head_response.headers.get('Content-Length', 'N/A')}")
                        print(f"[INFO] Content-Type: {head_response.headers.get('Content-Type', 'N/A')}")
                    elif head_response.status_code == 403:
                        print(f"[ERRO] Acesso negado - problema de permissoes")
                    elif head_response.status_code == 404:
                        print(f"[AVISO] Arquivo nao encontrado")
                    else:
                        print(f"[ERRO] Erro inesperado: {head_response.status_code}")
                        
                except Exception as e:
                    print(f"[ERRO] Erro ao tecorporativo URL: {str(e)}")
            else:
                print(f"[ERRO] API retornou erro: {data.get('message', 'Erro desconhecido')}")
        else:
            print(f"[ERRO] Erro na API: {response.status_code}")
            try:
                error_data = response.json()
                print(f"Detalhes: {error_data}")
            except:
                print(f"Resposta: {response.text}")
                
    except Exception as e:
        print(f"[ERRO] Erro geral: {str(e)}")
    
    print("\n" + "=" * 80)
    print("CONCLUSAO")
    print("=" * 80)
    print("1. Login do Sergio Sena: sergio@midiaflow.com / sergio_sena")
    print("2. URLs assinadas estao sendo geradas SEM autenticacao")
    print("3. Qualquer pessoa pode gerar URLs para arquivos de qualquer usuario")
    print("4. RISCO DE SEGURANCA: Vazamento de conteudo privado")

if __name__ == "__main__":
    test_real_file()
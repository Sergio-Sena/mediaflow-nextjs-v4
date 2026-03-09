import requests
import jwt
from urllib.parse import quote

def test_lid_lima_with_auth():
    print("=" * 60)
    print("TESTE LID LIMA COM AUTENTICACAO")
    print("=" * 60)
    
    # Generate JWT token for lid_lima
    jwt_secret = 'your-secret-key'
    payload = {
        'user_id': 'lid_lima',
        'role': 'user',
        's3_prefix': 'users/lid_lima/'
    }
    
    token = jwt.encode(payload, jwt_secret, algorithm='HS256')
    print(f"[TOKEN] Gerado para lid_lima")
    
    # Test file
    test_file = "users/lid_lima/Moana/Moana.1.Um.Mar.de.Aventuras.2017.mp4"
    print(f"[ARQUIVO] {test_file}")
    
    try:
        encoded_key = quote(test_file, safe='')
        url = f"https://gdb962d234.execute-api.us-east-1.amazonaws.com/prod/view/{encoded_key}"
        
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {token}'
        }
        
        response = requests.get(url, headers=headers)
        
        print(f"[STATUS] {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                print("[OK] URL assinada gerada com autenticacao")
                print(f"[USER] {data.get('user_id', 'N/A')}")
                
                # Test URL access
                try:
                    head_response = requests.head(data['viewUrl'], timeout=10)
                    if head_response.status_code == 200:
                        print("[OK] Video acessivel")
                        print(f"[SIZE] {head_response.headers.get('Content-Length', 'N/A')} bytes")
                    else:
                        print(f"[ERRO] Status: {head_response.status_code}")
                except Exception as e:
                    print(f"[ERRO] Acesso: {str(e)}")
            else:
                print(f"[ERRO] {data.get('message', 'Erro desconhecido')}")
        else:
            print(f"[ERRO] API: {response.status_code}")
            print(f"[RESPOSTA] {response.text}")
            
    except Exception as e:
        print(f"[ERRO] Geral: {str(e)}")

if __name__ == "__main__":
    test_lid_lima_with_auth()
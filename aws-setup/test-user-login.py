import requests
import hashlib
import pyotp

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

users = [
    {'email': 'lid@sstech', 'password': 'lid123', 'totp': 'JLIWGCLA55LWBTC75ADZNBEG6Z3KSVKN'},
    {'email': 'sena@sstech', 'password': 'sena123', 'totp': 'HJQFUX3XEPNJ3TJNARN3M7RTBNBO2JRS'}
]

print("=== TESTANDO LOGIN ===\n")

for user in users:
    print(f"Usuario: {user['email']}")
    
    # 1. Testar login
    login_response = requests.post(
        'https://gdb962d234.execute-api.us-east-1.amazonaws.com/prod/auth/login',
        json={
            'email': user['email'],
            'password': user['password']
        }
    )
    
    print(f"  Login Status: {login_response.status_code}")
    login_data = login_response.json()
    print(f"  Response: {login_data}")
    
    if login_data.get('success'):
        print(f"  Token: {login_data.get('token', 'N/A')[:50]}...")
        
        # 2. Gerar codigo 2FA
        totp = pyotp.TOTP(user['totp'])
        code = totp.now()
        print(f"  2FA Code: {code}")
        
        # 3. Testar 2FA
        twofa_response = requests.post(
            'https://gdb962d234.execute-api.us-east-1.amazonaws.com/prod/verify-2fa',
            json={
                'user_id': login_data.get('user_id'),
                'code': code
            }
        )
        
        print(f"  2FA Status: {twofa_response.status_code}")
        twofa_data = twofa_response.json()
        print(f"  2FA Response: {twofa_data}")
    else:
        print(f"  ERRO: {login_data.get('error', 'Unknown')}")
    
    print()

print("=== TESTE COMPLETO ===")

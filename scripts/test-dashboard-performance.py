import time
import requests

API_URL = 'https://gdb962d234.execute-api.us-east-1.amazonaws.com/prod'

print("=== TESTE DE PERFORMANCE - DASHBOARD ===\n")

# 1. Login
print("[1/4] Login...")
start = time.time()
login_response = requests.post(f'{API_URL}/auth/login', json={
    'email': 'sergio@midiaflow.com',
    'password': 'admin123'
})
login_time = (time.time() - start) * 1000
print(f"  Tempo: {login_time:.0f}ms - Status: {login_response.status_code}")

if login_response.status_code == 200:
    token = login_response.json().get('token')
    headers = {'Authorization': f'Bearer {token}'}
    
    # 2. Listar usuários
    print("\n[2/4] Listar usuarios...")
    start = time.time()
    users_response = requests.get(f'{API_URL}/users', headers=headers)
    users_time = (time.time() - start) * 1000
    print(f"  Tempo: {users_time:.0f}ms - Status: {users_response.status_code}")
    
    # 3. Listar arquivos
    print("\n[3/4] Listar arquivos...")
    start = time.time()
    files_response = requests.get(f'{API_URL}/files', headers=headers)
    files_time = (time.time() - start) * 1000
    print(f"  Tempo: {files_time:.0f}ms - Status: {files_response.status_code}")
    if files_response.status_code == 200:
        files_count = len(files_response.json().get('files', []))
        print(f"  Arquivos: {files_count}")
    
    # 4. Obter presigned URL de um vídeo
    print("\n[4/4] Obter URL de video...")
    start = time.time()
    video_response = requests.post(f'{API_URL}/files/presigned-url', 
                                   headers=headers,
                                   json={'key': 'test.mp4'})
    video_time = (time.time() - start) * 1000
    print(f"  Tempo: {video_time:.0f}ms - Status: {video_response.status_code}")
    
    # Resumo
    total_time = login_time + users_time + files_time + video_time
    print(f"\n{'='*50}")
    print(f"TEMPO TOTAL DASHBOARD: {total_time:.0f}ms ({total_time/1000:.2f}s)")
    print(f"{'='*50}")
    
    print(f"\nDETALHES:")
    print(f"  Login:          {login_time:.0f}ms")
    print(f"  Usuarios:       {users_time:.0f}ms")
    print(f"  Arquivos:       {files_time:.0f}ms")
    print(f"  URL Video:      {video_time:.0f}ms")
    
    print(f"\nDIAGNOSTICO:")
    if total_time < 2000:
        print("  [OK] RAPIDO - Dashboard carrega bem")
    elif total_time < 4000:
        print("  [AVISO] MEDIO - Pode melhorar")
    else:
        print("  [ERRO] LENTO - Precisa otimizar")
else:
    print(f"\nERRO no login: {login_response.text}")

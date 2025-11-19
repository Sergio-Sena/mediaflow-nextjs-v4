import requests
import time
from urllib.parse import urljoin

BASE_URL = 'https://midiaflow.sstechnologies-cloud.com'

PAGES = [
    '/',
    '/login',
    '/register',
    '/dashboard',
    '/admin',
    '/users'
]

def test_page(url):
    try:
        corporativot = time.time()
        response = requests.get(url, timeout=10)
        load_time = round((time.time() - corporativot) * 1000, 2)
        
        return {
            'status': response.status_code,
            'load_time_ms': load_time,
            'size_kb': round(len(response.content) / 1024, 2),
            'ok': response.status_code == 200
        }
    except Exception as e:
        return {
            'status': 'ERROR',
            'load_time_ms': 0,
            'size_kb': 0,
            'ok': False,
            'error': str(e)
        }

print('=' * 70)
print('MONITORAMENTO FRONTEND - Midiaflow')
print('=' * 70)

total_time = 0
total_size = 0
success_count = 0

for page in PAGES:
    url = urljoin(BASE_URL, page)
    print(f'\nTestando: {page}')
    
    result = test_page(url)
    
    if result['ok']:
        status_icon = 'OK'
        success_count += 1
        total_time += result['load_time_ms']
        total_size += result['size_kb']
    else:
        status_icon = 'ERRO'
    
    print(f'  Status: {status_icon} {result["status"]}')
    print(f'  Tempo: {result["load_time_ms"]}ms')
    print(f'  Tamanho: {result["size_kb"]} KB')
    
    if 'error' in result:
        print(f'  Erro: {result["error"]}')

print('\n' + '=' * 70)
print('RESUMO')
print('=' * 70)
print(f'Paginas Testadas: {len(PAGES)}')
print(f'Sucesso: {success_count}/{len(PAGES)} ({round(success_count/len(PAGES)*100, 1)}%)')
print(f'Tempo Medio: {round(total_time/success_count, 2)}ms' if success_count > 0 else 'N/A')
print(f'Tamanho Total: {round(total_size, 2)} KB')
print('=' * 70)

import os
import time

LOCAL_DIR = r'C:\Users\dell 5557\Videos\IDM\Corporativo\Comatozze'
S3_PREFIX = 'users/user_admin/Corporativo/Comatozze/'

def simulate_upload():
    files = []
    for root, dirs, filenames in os.walk(LOCAL_DIR):
        for filename in filenames:
            local_path = os.path.join(root, filename)
            rel_path = os.path.relpath(local_path, LOCAL_DIR)
            s3_key = S3_PREFIX + rel_path.replace('\\', '/')
            
            files.append({
                'local': local_path,
                'key': s3_key,
                'size': os.path.getsize(local_path)
            })
    
    total = len(files)
    total_size = sum(f['size'] for f in files)
    
    print(f'SIMULACAO DE UPLOAD')
    print(f'Total: {total} arquivos ({total_size / (1024**3):.2f} GB)')
    print('=' * 70)
    
    uploaded = 0
    for idx, f in enumerate(files, 1):
        filename = os.path.basename(f['local'])
        size_mb = f['size'] / (1024**2)
        
        # Barra de progresso simples
        progress = int((uploaded / total_size) * 50)
        bar = '#' * progress + '-' * (50 - progress)
        percent = (uploaded / total_size) * 100
        
        print(f'\r[{bar}] {percent:.1f}% | [{idx}/{total}] {filename[:40]}', end='', flush=True)
        
        time.sleep(0.05)  # Simula delay
        uploaded += f['size']
    
    # Barra final completa
    print(f'\r[{"#" * 50}] 100.0% | Concluido!{" " * 30}')
    print('=' * 70)
    print(f'Simulacao concluida: {total} arquivos ({total_size / (1024**3):.2f} GB)')
    print(f'\nDestino S3: s3://mediaflow-uploads-969430605054/{S3_PREFIX}')

if __name__ == '__main__':
    simulate_upload()

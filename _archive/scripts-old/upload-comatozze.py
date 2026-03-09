import os
import boto3
import time
from pathlib import Path
from tqdm import tqdm

DRY_RUN = True  # True = simula, False = upload real

s3 = boto3.client('s3', region_name='us-east-1')
BUCKET = 'mediaflow-uploads-969430605054'
LOCAL_DIR = r'C:\Users\dell 5557\Videos\IDM\Corporativo\Comatozze'
S3_PREFIX = 'users/user_admin/Corporativo/Comatozze/'

def upload_folder():
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
    
    mode = 'SIMULACAO' if DRY_RUN else 'UPLOAD REAL'
    print(f'{mode}: {total} arquivos ({total_size / (1024**3):.2f} GB)\n')
    
    with tqdm(total=total_size, unit='B', unit_scale=True, desc=mode) as pbar:
        for f in files:
            try:
                if DRY_RUN:
                    time.sleep(0.01)  # Simula delay
                else:
                    s3.upload_file(f['local'], BUCKET, f['key'])
                pbar.update(f['size'])
                pbar.set_postfix_str(os.path.basename(f['local'])[:30])
            except Exception as e:
                tqdm.write(f'ERRO: {os.path.basename(f["local"])} - {e}')
    
    print(f'\nConcluido: {total} arquivos')

if __name__ == '__main__':
    upload_folder()

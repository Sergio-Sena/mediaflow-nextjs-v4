import os
import boto3

s3 = boto3.client('s3', region_name='us-east-1')
BUCKET = 'mediaflow-uploads-969430605054'
LOCAL_DIR = r'C:\Users\dell 5557\Videos\IDM\Star\Comatozze'
S3_PREFIX = 'users/user_admin/Star/Comatozze/'

def upload():
    files = []
    for root, dirs, filenames in os.walk(LOCAL_DIR):
        for filename in filenames:
            local_path = os.path.join(root, filename)
            rel_path = os.path.relpath(local_path, LOCAL_DIR)
            s3_key = S3_PREFIX + rel_path.replace('\\', '/')
            files.append({'local': local_path, 'key': s3_key, 'size': os.path.getsize(local_path)})
    
    total = len(files)
    total_size = sum(f['size'] for f in files)
    
    print(f'UPLOAD REAL: {total} arquivos ({total_size / (1024**3):.2f} GB)')
    print('=' * 70)
    
    uploaded = 0
    for idx, f in enumerate(files, 1):
        filename = os.path.basename(f['local'])
        
        # Barra de progresso
        progress = int((uploaded / total_size) * 50)
        bar = '#' * progress + '-' * (50 - progress)
        percent = (uploaded / total_size) * 100
        
        print(f'\r[{bar}] {percent:.1f}% | [{idx}/{total}] Uploading...', end='', flush=True)
        
        try:
            s3.upload_file(f['local'], BUCKET, f['key'])
            uploaded += f['size']
        except Exception as e:
            print(f'\nERRO: {filename} - {e}')
    
    print(f'\r[{"#" * 50}] 100.0% | Concluido!{" " * 30}')
    print('=' * 70)
    print(f'Upload concluido: {total} arquivos ({total_size / (1024**3):.2f} GB)')

if __name__ == '__main__':
    upload()

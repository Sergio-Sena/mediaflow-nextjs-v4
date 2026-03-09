import os
import boto3

s3 = boto3.client('s3', region_name='us-east-1')
BUCKET = 'mediaflow-uploads-969430605054'
FOLDERS = [
    r'C:\Users\dell 5557\Videos\Moana.2',
    r'C:\Users\dell 5557\Videos\Moana.Um.Mar.de.Aventuras'
]
S3_PREFIX = 'users/lid_lima/'

def upload():
    all_files = []
    
    for folder in FOLDERS:
        folder_name = os.path.basename(folder)
        for root, dirs, filenames in os.walk(folder):
            for filename in filenames:
                local_path = os.path.join(root, filename)
                rel_path = os.path.relpath(local_path, folder)
                s3_key = S3_PREFIX + folder_name + '/' + rel_path.replace('\\', '/')
                all_files.append({'local': local_path, 'key': s3_key, 'size': os.path.getsize(local_path)})
    
    total = len(all_files)
    total_size = sum(f['size'] for f in all_files)
    
    print(f'UPLOAD Moana para lid_lima: {total} arquivos ({total_size / (1024**3):.2f} GB)')
    print('=' * 70)
    
    uploaded = 0
    for idx, f in enumerate(all_files, 1):
        progress = int((uploaded / total_size) * 50)
        bar = '#' * progress + '-' * (50 - progress)
        percent = (uploaded / total_size) * 100
        
        print(f'\r[{bar}] {percent:.1f}% | [{idx}/{total}] Uploading...', end='', flush=True)
        
        try:
            s3.upload_file(f['local'], BUCKET, f['key'])
            uploaded += f['size']
        except Exception as e:
            print(f'\nERRO: {os.path.basename(f["local"])} - {e}')
    
    print(f'\r[{"#" * 50}] 100.0% | Concluido!{" " * 30}')
    print('=' * 70)
    print(f'Upload concluido: {total} arquivos ({total_size / (1024**3):.2f} GB)')

if __name__ == '__main__':
    upload()

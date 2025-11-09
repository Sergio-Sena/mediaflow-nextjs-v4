import os
import boto3
import re
from pathlib import Path

s3 = boto3.client('s3', region_name='us-east-1')
BUCKET = 'mediaflow-uploads-969430605054'
LOCAL_DIR = r'C:\Users\dell 5557\Videos\IDM\Star'
S3_PREFIX = 'users/user_admin/Star/'

def sanitize_filename(filename):
    name, ext = os.path.splitext(filename)
    name = name.encode('ascii', 'ignore').decode('ascii')
    name = re.sub(r'[^a-zA-Z0-9_\-\s]', '', name)
    name = re.sub(r'\s+', ' ', name)
    if len(name) > 200:
        name = name[:200]
    name = name.strip()
    return name + ext

def get_files():
    files = []
    for root, dirs, filenames in os.walk(LOCAL_DIR):
        for filename in filenames:
            if filename.lower().endswith(('.mp4', '.mkv', '.avi', '.mov', '.webm', '.ts')):
                local_path = os.path.join(root, filename)
                rel_path = os.path.relpath(local_path, LOCAL_DIR)
                
                parts = rel_path.split(os.sep)
                sanitized_parts = [sanitize_filename(part) for part in parts]
                sanitized_rel_path = '/'.join(sanitized_parts)
                
                s3_key = S3_PREFIX + sanitized_rel_path
                
                files.append({
                    'local': local_path,
                    'key': s3_key,
                    'size': os.path.getsize(local_path)
                })
    return files

def upload():
    files = get_files()
    total = len(files)
    total_size = sum(f['size'] for f in files)
    
    print(f'Total: {total} arquivos ({total_size / (1024**3):.2f} GB)')
    print('=' * 60)
    
    uploaded_size = 0
    
    for idx, file_info in enumerate(files, 1):
        s3.upload_file(file_info['local'], BUCKET, file_info['key'])
        
        uploaded_size += file_info['size']
        progress_gb = int((uploaded_size / total_size) * 100)
        progress_files = int((idx / total) * 100)
        
        bar_gb = '#' * (progress_gb // 2) + '-' * (50 - progress_gb // 2)
        bar_files = '#' * (progress_files // 2) + '-' * (50 - progress_files // 2)
        
        print(f'GB:      [{bar_gb}] {progress_gb}%  ({uploaded_size / (1024**3):.2f}/{total_size / (1024**3):.2f} GB)')
        print(f'Arquivos: [{bar_files}] {progress_files}%  ({idx}/{total})')
        print('\033[2A', end='')
    
    print('\n\n')
    print('=' * 60)
    print(f'Concluido: {total} arquivos ({total_size / (1024**3):.2f} GB)')

if __name__ == '__main__':
    upload()

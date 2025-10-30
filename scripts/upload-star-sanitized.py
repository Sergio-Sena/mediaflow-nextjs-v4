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
    
    # Remove acentos
    name = name.encode('ascii', 'ignore').decode('ascii')
    
    # Remove caracteres especiais (mantém letras, números, _, -, espaços)
    name = re.sub(r'[^a-zA-Z0-9_\-\s]', '', name)
    
    # Remove espaços duplos
    name = re.sub(r'\s+', ' ', name)
    
    # Trunca se muito longo (max 200 chars)
    if len(name) > 200:
        name = name[:200]
    
    # Remove espaços no início/fim
    name = name.strip()
    
    return name + ext

def get_files_to_upload():
    files = []
    for root, dirs, filenames in os.walk(LOCAL_DIR):
        for filename in filenames:
            if filename.lower().endswith(('.mp4', '.mkv', '.avi', '.mov', '.webm')):
                local_path = os.path.join(root, filename)
                rel_path = os.path.relpath(local_path, LOCAL_DIR)
                
                # Sanitiza o caminho completo
                parts = rel_path.split(os.sep)
                sanitized_parts = [sanitize_filename(part) for part in parts]
                sanitized_rel_path = '/'.join(sanitized_parts)
                
                s3_key = S3_PREFIX + sanitized_rel_path
                
                files.append({
                    'local': local_path,
                    'original': rel_path,
                    'sanitized': sanitized_rel_path,
                    's3_key': s3_key,
                    'size': os.path.getsize(local_path)
                })
    return files

def upload_with_progress():
    files = get_files_to_upload()
    
    if not files:
        print('Nenhum arquivo encontrado!')
        return
    
    total_size = sum(f['size'] for f in files)
    total_files = len(files)
    
    print(f'Total: {total_files} arquivos ({total_size / (1024**3):.2f} GB)')
    print('=' * 70)
    
    uploaded_size = 0
    
    for idx, file_info in enumerate(files, 1):
        original = file_info['original']
        sanitized = file_info['sanitized']
        
        if original != sanitized:
            print(f'\n[{idx}/{total_files}] Sanitizando:')
            print(f'  Original: {original}')
            print(f'  Sanitizado: {sanitized}')
        else:
            print(f'\n[{idx}/{total_files}] {sanitized}')
        
        file_size = file_info['size']
        print(f'  Tamanho: {file_size / (1024**2):.2f} MB')
        
        try:
            s3.upload_file(
                file_info['local'],
                BUCKET,
                file_info['s3_key']
            )
            
            uploaded_size += file_size
            progress = (uploaded_size / total_size) * 100
            
            print(f'  Status: OK')
            print(f'  Progresso geral: {progress:.1f}% ({uploaded_size / (1024**3):.2f} GB / {total_size / (1024**3):.2f} GB)')
            
        except Exception as e:
            print(f'  Status: ERRO - {str(e)}')
    
    print('\n' + '=' * 70)
    print(f'Upload concluido: {total_files} arquivos ({total_size / (1024**3):.2f} GB)')

if __name__ == '__main__':
    upload_with_progress()

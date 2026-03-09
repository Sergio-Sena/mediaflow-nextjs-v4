import boto3
import os
import sys

s3 = boto3.client('s3')
BUCKET = 'mediaflow-uploads-969430605054'
LOCAL_PATH = r'C:\Users\dell 5557\Videos\IDM\Star\kate kuray'
S3_PREFIX = 'users/sergio_sena/Star/Kate Kuray/'

def get_local_files():
    files = set()
    if os.path.exists(LOCAL_PATH):
        for root, dirs, filenames in os.walk(LOCAL_PATH):
            for filename in filenames:
                files.add(filename)
    return files

def get_s3_files():
    files = set()
    try:
        paginator = s3.get_paginator('list_objects_v2')
        pages = paginator.paginate(Bucket=BUCKET, Prefix=S3_PREFIX)
        
        for page in pages:
            if 'Contents' in page:
                for obj in page['Contents']:
                    filename = obj['Key'].split('/')[-1]
                    if filename:
                        files.add(filename)
    except Exception as e:
        print(f"Erro S3: {e}")
    
    return files

def get_missing_files():
    local_files = get_local_files()
    s3_files = get_s3_files()
    missing = local_files - s3_files
    
    missing_files = []
    for filename in missing:
        local_file = os.path.join(LOCAL_PATH, filename)
        if os.path.exists(local_file):
            size_mb = round(os.path.getsize(local_file) / (1024*1024), 2)
            missing_files.append({
                'filename': filename,
                'local_path': local_file,
                's3_key': f"{S3_PREFIX}{filename}",
                'size_mb': size_mb
            })
    
    return missing_files

def upload_file_with_progress(file_info):
    try:
        file_size = os.path.getsize(file_info['local_path'])
        
        def progress_callback(bytes_transferred):
            percentage = (bytes_transferred / file_size) * 100
            bar_length = 40
            filled_length = int(bar_length * bytes_transferred // file_size)
            bar = '█' * filled_length + '-' * (bar_length - filled_length)
            mb_transferred = bytes_transferred / (1024*1024)
            sys.stdout.write(f'\r[{bar}] {percentage:.1f}% ({mb_transferred:.1f}/{file_info["size_mb"]} MB)')
            sys.stdout.flush()
        
        s3.upload_file(
            file_info['local_path'],
            BUCKET,
            file_info['s3_key'],
            Callback=progress_callback
        )
        return True
    except Exception as e:
        print(f"\nErro: {e}")
        return False

def main():
    print("Comparando Kate Kuray local vs S3...\n")
    
    missing_files = get_missing_files()
    
    if not missing_files:
        print("[OK] Todos os arquivos ja estao no S3")
        return
    
    print(f"Encontrados {len(missing_files)} arquivos faltando:\n")
    
    for i, file_info in enumerate(missing_files, 1):
        try:
            print(f"{i}. {file_info['filename']} ({file_info['size_mb']} MB)")
        except:
            print(f"{i}. [arquivo com caracteres especiais] ({file_info['size_mb']} MB)")
    
    print(f"\n[AUTO] Iniciando upload de {len(missing_files)} arquivos...\n")
    
    uploaded = 0
    failed = 0
    
    for i, file_info in enumerate(missing_files, 1):
        try:
            print(f"\n[{i}/{len(missing_files)}] {file_info['filename']}")
        except:
            print(f"\n[{i}/{len(missing_files)}] [arquivo com caracteres especiais]")
        
        if upload_file_with_progress(file_info):
            print(" OK")
            uploaded += 1
        else:
            print(" ERRO")
            failed += 1
    
    print(f"\n\nResultado:")
    print(f"   Uploaded: {uploaded}")
    print(f"   Erros: {failed}")
    print(f"   Total: {len(missing_files)}")

if __name__ == '__main__':
    main()
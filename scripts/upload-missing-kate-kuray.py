import boto3
import os
from pathlib import Path

s3 = boto3.client('s3')
BUCKET = 'mediaflow-uploads-969430605054'
LOCAL_PATH = r'C:\Users\dell 5557\Videos\IDM\Star\kate kuray'
S3_PREFIX = 'users/sergio_sena/'

def get_missing_files():
    local_files = set()
    s3_files = set()
    
    # Local files
    if os.path.exists(LOCAL_PATH):
        for root, dirs, filenames in os.walk(LOCAL_PATH):
            for filename in filenames:
                local_files.add(filename)
    
    # S3 files
    try:
        paginator = s3.get_paginator('list_objects_v2')
        pages = paginator.paginate(Bucket=BUCKET, Prefix=S3_PREFIX)
        
        for page in pages:
            if 'Contents' in page:
                for obj in page['Contents']:
                    filename = obj['Key'].split('/')[-1]
                    if filename:
                        s3_files.add(filename)
    except Exception as e:
        print(f"Erro S3: {e}")
        return []
    
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

def upload_file(file_info):
    try:
        s3.upload_file(
            file_info['local_path'],
            BUCKET,
            file_info['s3_key']
        )
        return True
    except Exception as e:
        print(f"Erro: {e}")
        return False

def main():
    print("Fazendo upload dos arquivos faltantes...\n")
    
    missing_files = get_missing_files()
    
    if not missing_files:
        print("[OK] Nenhum arquivo faltante encontrado")
        return
    
    print(f"Encontrados {len(missing_files)} arquivos para upload:\n")
    
    for i, file_info in enumerate(missing_files, 1):
        try:
            print(f"{i}. {file_info['filename']} ({file_info['size_mb']} MB)")
        except:
            print(f"{i}. [arquivo com caracteres especiais] ({file_info['size_mb']} MB)")
    
    confirm = input(f"\nFazer upload de {len(missing_files)} arquivos? (s/N): ").lower()
    if confirm != 's':
        print("[CANCEL] Upload cancelado")
        return
    
    print("\nFazendo upload...\n")
    
    uploaded = 0
    failed = 0
    
    for file_info in missing_files:
        try:
            print(f"Uploading: {file_info['filename']}... ", end="")
        except:
            print(f"Uploading: [caracteres especiais]... ", end="")
        
        if upload_file(file_info):
            print("OK")
            uploaded += 1
        else:
            print("ERRO")
            failed += 1
    
    print(f"\nResultado:")
    print(f"   Uploaded: {uploaded}")
    print(f"   Erros: {failed}")
    print(f"   Total: {len(missing_files)}")

if __name__ == '__main__':
    main()
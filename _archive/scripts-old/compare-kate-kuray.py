import boto3
import os
from pathlib import Path

s3 = boto3.client('s3')
BUCKET = 'mediaflow-uploads-969430605054'
LOCAL_PATH = r'C:\Users\dell 5557\Videos\IDM\Star\kate kuray'
S3_PREFIX = 'users/sergio_sena/'

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

def main():
    print("Comparando kate kuray local vs sergio_sena S3...\n")
    
    local_files = get_local_files()
    s3_files = get_s3_files()
    
    print(f"Local (kate kuray): {len(local_files)} arquivos")
    print(f"S3 (sergio_sena): {len(s3_files)} arquivos\n")
    
    # Arquivos apenas no local
    only_local = local_files - s3_files
    if only_local:
        print(f"Apenas LOCAL ({len(only_local)}):")
        for f in sorted(list(only_local)[:10]):
            print(f"   {f}")
        if len(only_local) > 10:
            print(f"   ... e mais {len(only_local) - 10}")
        print()
    
    # Arquivos apenas no S3
    only_s3 = s3_files - local_files
    if only_s3:
        print(f"Apenas S3 ({len(only_s3)}):")
        for f in sorted(list(only_s3)[:10]):
            print(f"   {f}")
        if len(only_s3) > 10:
            print(f"   ... e mais {len(only_s3) - 10}")
        print()
    
    # Arquivos em comum
    common = local_files & s3_files
    if common:
        print(f"Em AMBOS ({len(common)}):")
        for f in sorted(list(common)[:5]):
            print(f"   {f}")
        if len(common) > 5:
            print(f"   ... e mais {len(common) - 5}")
        print()
    
    print("Resumo:")
    print(f"   Apenas local: {len(only_local)}")
    print(f"   Apenas S3: {len(only_s3)}")
    print(f"   Em ambos: {len(common)}")

if __name__ == '__main__':
    main()
import boto3
import os

s3 = boto3.client('s3')
BUCKET = 'mediaflow-uploads-969430605054'
LOCAL_PATH = r'C:\Users\dell 5557\Videos\IDM\Star\MiaMalkova'
S3_PREFIX = 'users/sergio_sena/'

def get_local_files():
    files = set()
    if os.path.exists(LOCAL_PATH):
        for root, dirs, filenames in os.walk(LOCAL_PATH):
            for filename in filenames:
                try:
                    files.add(filename)
                except:
                    pass
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

def safe_print(text):
    try:
        print(text)
    except:
        print("[arquivo com caracteres especiais]")

def main():
    print("Comparando MiaMalkova local vs sergio_sena S3...\n")
    
    local_files = get_local_files()
    s3_files = get_s3_files()
    
    print(f"Local (MiaMalkova): {len(local_files)} arquivos")
    print(f"S3 (sergio_sena): {len(s3_files)} arquivos\n")
    
    only_local = local_files - s3_files
    only_s3 = s3_files - local_files
    common = local_files & s3_files
    
    print(f"Apenas LOCAL: {len(only_local)} arquivos")
    if only_local:
        count = 0
        for f in sorted(only_local):
            if count < 5:
                safe_print(f"   {f}")
                count += 1
        if len(only_local) > 5:
            print(f"   ... e mais {len(only_local) - 5}")
    
    print(f"\nApenas S3: {len(only_s3)} arquivos")
    print(f"Em AMBOS: {len(common)} arquivos")
    
    if len(only_local) > 0:
        print(f"\n[ACAO] {len(only_local)} arquivos precisam ser enviados do local para S3")
    else:
        print(f"\n[OK] Todos os arquivos locais ja estao no S3")

if __name__ == '__main__':
    main()
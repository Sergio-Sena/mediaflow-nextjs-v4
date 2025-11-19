import boto3
import os
import shutil

s3 = boto3.client('s3')
BUCKET = 'mediaflow-uploads-969430605054'
LOCAL_SOURCE = r'C:\Users\dell 5557\Videos\IDM\Star\kate kuray'
LOCAL_DEST = r'C:\Users\dell 5557\Videos\IDM\Star2'
S3_PREFIX = 'users/sergio_sena/Star/Kate Kuray/'

def get_local_files():
    files = set()
    if os.path.exists(LOCAL_SOURCE):
        for root, dirs, filenames in os.walk(LOCAL_SOURCE):
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
        local_file = os.path.join(LOCAL_SOURCE, filename)
        if os.path.exists(local_file):
            size_mb = round(os.path.getsize(local_file) / (1024*1024), 2)
            missing_files.append({
                'filename': filename,
                'local_path': local_file,
                'size_mb': size_mb
            })
    
    return missing_files

def main():
    print("Copiando videos faltantes de Kate Kuray para Star2...\n")
    
    # Criar pasta Star2 se nao existir
    if not os.path.exists(LOCAL_DEST):
        os.makedirs(LOCAL_DEST)
        print(f"[OK] Pasta criada: {LOCAL_DEST}\n")
    
    missing_files = get_missing_files()
    
    if not missing_files:
        print("[OK] Nenhum arquivo faltando")
        return
    
    print(f"Encontrados {len(missing_files)} arquivos faltando:\n")
    
    for i, file_info in enumerate(missing_files, 1):
        try:
            print(f"{i}. {file_info['filename']} ({file_info['size_mb']} MB)")
        except:
            print(f"{i}. [arquivo com caracteres especiais] ({file_info['size_mb']} MB)")
    
    print(f"\n[AUTO] Copiando {len(missing_files)} arquivos para Star2...\n")
    
    copied = 0
    failed = 0
    
    for i, file_info in enumerate(missing_files, 1):
        try:
            print(f"[{i}/{len(missing_files)}] Copiando: {file_info['filename']}... ", end="", flush=True)
        except:
            print(f"[{i}/{len(missing_files)}] Copiando: [arquivo com caracteres especiais]... ", end="", flush=True)
        
        try:
            dest_path = os.path.join(LOCAL_DEST, file_info['filename'])
            shutil.copy2(file_info['local_path'], dest_path)
            print("OK")
            copied += 1
        except Exception as e:
            print(f"ERRO: {e}")
            failed += 1
    
    print(f"\nResultado:")
    print(f"   Copiados: {copied}")
    print(f"   Erros: {failed}")
    print(f"   Total: {len(missing_files)}")
    print(f"\nArquivos em: {LOCAL_DEST}")

if __name__ == '__main__':
    main()
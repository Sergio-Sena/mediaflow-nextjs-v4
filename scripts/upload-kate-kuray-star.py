import boto3
import os
import sys

s3 = boto3.client('s3')
BUCKET = 'mediaflow-uploads-969430605054'
LOCAL_PATH = r'C:\Users\dell 5557\Videos\IDM\Star\kate kuray'
S3_PREFIX = 'users/sergio_sena/Star/Kate Kuray/'

def get_local_files():
    files = []
    if os.path.exists(LOCAL_PATH):
        for root, dirs, filenames in os.walk(LOCAL_PATH):
            for filename in filenames:
                local_file = os.path.join(root, filename)
                size_mb = round(os.path.getsize(local_file) / (1024*1024), 2)
                files.append({
                    'filename': filename,
                    'local_path': local_file,
                    's3_key': f"{S3_PREFIX}{filename}",
                    'size_mb': size_mb
                })
    return files

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
    print("Upload Kate Kuray para sergio_sena/Star/Kate Kuray/\n")
    
    files_to_upload = get_local_files()
    
    if not files_to_upload:
        print("[OK] Nenhum arquivo encontrado")
        return
    
    print(f"Encontrados {len(files_to_upload)} arquivos:\n")
    
    for i, file_info in enumerate(files_to_upload, 1):
        try:
            print(f"{i}. {file_info['filename']} ({file_info['size_mb']} MB)")
        except:
            print(f"{i}. [arquivo com caracteres especiais] ({file_info['size_mb']} MB)")
    
    print(f"\n[AUTO] Iniciando upload de {len(files_to_upload)} arquivos...\n")
    
    uploaded = 0
    failed = 0
    
    for i, file_info in enumerate(files_to_upload, 1):
        print(f"\n[{i}/{len(files_to_upload)}] {file_info['filename']}")
        
        if upload_file_with_progress(file_info):
            print(" ✓ OK")
            uploaded += 1
        else:
            print(" ✗ ERRO")
            failed += 1
    
    print(f"\n\nResultado:")
    print(f"   Uploaded: {uploaded}")
    print(f"   Erros: {failed}")
    print(f"   Total: {len(files_to_upload)}")

if __name__ == '__main__':
    main()
import boto3
import os
from pathlib import Path

s3 = boto3.client('s3')
BUCKET = 'mediaflow-uploads-969430605054'
LOCAL_PATH = r'C:\Users\dell 5557\Videos\IDM\Star'

def upload_folder():
    print(f"Escaneando: {LOCAL_PATH}\n")
    
    files = []
    for root, dirs, filenames in os.walk(LOCAL_PATH):
        for filename in filenames:
            local_file = os.path.join(root, filename)
            rel_path = os.path.relpath(local_file, LOCAL_PATH)
            s3_key = f"users/user_admin/Star/{rel_path}".replace('\\', '/')
            files.append((local_file, s3_key))
    
    print(f"Total: {len(files)} arquivos\n")
    
    uploaded = 0
    skipped = 0
    
    for local_file, s3_key in files:
        try:
            s3.head_object(Bucket=BUCKET, Key=s3_key)
            print(f"[SKIP] {s3_key.split('/')[-1]}")
            skipped += 1
        except:
            file_size = os.path.getsize(local_file)
            s3.upload_file(local_file, BUCKET, s3_key)
            print(f"[OK] {s3_key.split('/')[-1]} ({file_size / (1024**2):.1f} MB)")
            uploaded += 1
    
    print(f"\nUpload: {uploaded} | Pulados: {skipped}")

if __name__ == '__main__':
    upload_folder()

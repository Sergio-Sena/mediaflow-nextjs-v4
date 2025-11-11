import boto3
import os
from pathlib import Path

s3 = boto3.client('s3', region_name='us-east-1')
BUCKET = 'mediaflow-uploads-969430605054'
LOCAL_PATH = r'C:\Users\dell 5557\Videos\IDM\Star\kate kuray'
S3_PREFIX = 'users/user_admin/Star/kate kuray/'

print("="*60)
print("ADICIONANDO NOVOS ARQUIVOS KATE KURAY")
print("="*60)

local_files = list(Path(LOCAL_PATH).glob('*.mp4'))

print(f"\nArquivos locais: {len(local_files)}")
for f in local_files:
    print(f"  - {f.name}")

print("\n" + "="*60)
resp = input(f"Adicionar {len(local_files)} arquivos ao S3? (s/n): ")

if resp.lower() == 's':
    uploaded = 0
    for file_path in local_files:
        s3_key = S3_PREFIX + file_path.name
        try:
            print(f"[{uploaded+1}/{len(local_files)}] {file_path.name}")
            s3.upload_file(str(file_path), BUCKET, s3_key)
            uploaded += 1
        except Exception as e:
            print(f"  [ERRO] {e}")
    
    print(f"\n{uploaded} arquivos adicionados com sucesso!")
else:
    print("Cancelado")

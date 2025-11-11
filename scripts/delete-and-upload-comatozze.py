import boto3
import os
from pathlib import Path

s3 = boto3.client('s3', region_name='us-east-1')
BUCKET = 'mediaflow-uploads-969430605054'
LOCAL_PATH = r'C:\Users\dell 5557\Videos\IDM\Star\Comatozze'
S3_PREFIX = 'users/user_admin/Star/Comatozze/'

def get_s3_files():
    s3_files = {}
    paginator = s3.get_paginator('list_objects_v2')
    for page in paginator.paginate(Bucket=BUCKET):
        for obj in page.get('Contents', []):
            filename = obj['Key'].split('/')[-1].lower()
            s3_files[filename] = {'key': obj['Key'], 'size': obj['Size']}
    return s3_files

def get_local_files():
    local_files = []
    for root, dirs, files in os.walk(LOCAL_PATH):
        for file in files:
            full_path = os.path.join(root, file)
            size = os.path.getsize(full_path)
            local_files.append({'path': full_path, 'name': file, 'size': size})
    return local_files

print("=" * 80)
print("DELETANDO DUPLICADOS E FAZENDO UPLOAD")
print("=" * 80)

s3_files = get_s3_files()
local_files = get_local_files()

# Identificar duplicados
to_delete = []
to_upload = []

for local in local_files:
    found = False
    
    # Match por nome
    if local['name'].lower() in s3_files:
        if abs(s3_files[local['name'].lower()]['size'] - local['size']) < 1024:
            to_delete.append(local)
            found = True
    
    # Match por tamanho
    if not found:
        for s3_name, s3_data in s3_files.items():
            if abs(s3_data['size'] - local['size']) < 1024:
                to_delete.append(local)
                found = True
                break
    
    if not found:
        to_upload.append(local)

# Deletar duplicados
print(f"\nDeletando {len(to_delete)} duplicados...")
for item in to_delete:
    try:
        os.remove(item['path'])
        print(f"[DELETADO] {item['name']}")
    except Exception as e:
        print(f"[ERRO] {item['name']}: {e}")

# Upload dos restantes
print(f"\nFazendo upload de {len(to_upload)} arquivos para {S3_PREFIX}...")
uploaded = 0

for item in to_upload:
    s3_key = S3_PREFIX + item['name']
    try:
        try:
            print(f"[UPLOADING] {item['name']} ({item['size']/(1024**2):.1f} MB)...")
        except:
            print(f"[UPLOADING] [arquivo com emoji] ({item['size']/(1024**2):.1f} MB)...")
        
        s3.upload_file(
            item['path'],
            BUCKET,
            s3_key,
            Callback=lambda bytes_transferred: None
        )
        uploaded += 1
        try:
            print(f"[OK] {item['name']}")
        except:
            print(f"[OK] [arquivo com emoji]")
    except Exception as e:
        try:
            print(f"[ERRO] {item['name']}: {e}")
        except:
            print(f"[ERRO] [arquivo com emoji]: {e}")

print("\n" + "=" * 80)
print("CONCLUIDO")
print("=" * 80)
print(f"Deletados: {len(to_delete)}")
print(f"Uploadados: {uploaded}/{len(to_upload)}")
print(f"Destino S3: {S3_PREFIX}")

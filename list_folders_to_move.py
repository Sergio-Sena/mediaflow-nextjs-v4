import boto3
import json

# AWS S3 client
s3 = boto3.client('s3')
bucket = 'mediaflow-processed-969430605054'

# Pastas que devem FICAR na raiz (não mover)
keep_in_root = {'Video', 'Seart', 'Captures', 'Star'}

# Listar todas as pastas
def list_all_folders():
    folders = set()
    
    paginator = s3.get_paginator('list_objects_v2')
    for page in paginator.paginate(Bucket=bucket):
        if 'Contents' in page:
            for obj in page['Contents']:
                key = obj['Key']
                if '/' in key:
                    folder = key.split('/')[0]
                    folders.add(folder)
    
    return folders

# Obter pastas para mover
all_folders = list_all_folders()
folders_to_move = [f for f in all_folders if f not in keep_in_root]

print("PASTAS PARA MOVER PARA Star/:")
print("=" * 50)

for i, folder in enumerate(sorted(folders_to_move), 1):
    print(f"{i:2d}. {folder}/ -> Star/{folder}/")

print(f"\nRESUMO:")
print(f"Total de pastas: {len(all_folders)}")
print(f"Ficar na raiz: {len(keep_in_root)} ({', '.join(sorted(keep_in_root))})")
print(f"Mover para Star/: {len(folders_to_move)}")

print(f"\nCOMANDO DE CONFIRMACAO:")
print("python move_folders_to_star.py")
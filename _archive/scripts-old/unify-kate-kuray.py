import boto3
from pathlib import Path

s3 = boto3.client('s3', region_name='us-east-1')
BUCKET = 'mediaflow-uploads-969430605054'
LOCAL_PATH = r'C:\Users\dell 5557\Videos\IDM\Corporativo\kate kuray'
S3_PREFIX_OLD1 = 'users/user_admin/Corporativo/Kate kuray/'
S3_PREFIX_OLD2 = 'users/user_admin/Corporativo/kate kuray/'
S3_PREFIX_NEW = 'users/user_admin/Corporativo/Kate Kuray/'

print("="*80)
print("UNIFICANDO KATE KURAY")
print("="*80)

# 1. Mover arquivos de 'Kate kuray' e 'kate kuray' para 'Kate Kuray'
print("\n1. Movendo arquivos para pasta unificada...")

paginator = s3.get_paginator('list_objects_v2')
moved = 0

for old_prefix in [S3_PREFIX_OLD1, S3_PREFIX_OLD2]:
    for page in paginator.paginate(Bucket=BUCKET, Prefix=old_prefix):
        for obj in page.get('Contents', []):
            old_key = obj['Key']
            filename = old_key.split('/')[-1]
            
            if not filename:
                continue
            
            new_key = S3_PREFIX_NEW + filename
            
            if old_key != new_key:
                try:
                    # Copiar para novo local
                    s3.copy_object(
                        CopySource={'Bucket': BUCKET, 'Key': old_key},
                        Bucket=BUCKET,
                        Key=new_key
                    )
                    # Deletar antigo
                    s3.delete_object(Bucket=BUCKET, Key=old_key)
                    moved += 1
                    print(f"  [{moved}] {filename}")
                except Exception as e:
                    print(f"  [ERRO] {filename}: {e}")

print(f"\n{moved} arquivos movidos para {S3_PREFIX_NEW}")

# 2. Upload arquivos locais
print("\n2. Fazendo upload de arquivos locais...")

local_files = list(Path(LOCAL_PATH).glob('*.mp4'))
uploaded = 0

for file_path in local_files:
    s3_key = S3_PREFIX_NEW + file_path.name
    try:
        print(f"  [{uploaded+1}/{len(local_files)}] {file_path.name}")
        s3.upload_file(str(file_path), BUCKET, s3_key)
        uploaded += 1
    except Exception as e:
        print(f"  [ERRO] {e}")

print(f"\n{uploaded} arquivos locais adicionados")

# 3. Verificar resultado final
print("\n3. Verificando pasta unificada...")
count = 0
for page in paginator.paginate(Bucket=BUCKET, Prefix=S3_PREFIX_NEW):
    count += len(page.get('Contents', []))

print(f"\nTotal em {S3_PREFIX_NEW}: {count} arquivos")

print("\n" + "="*80)
print("CONCLUIDO!")
print("="*80)
print(f"Pasta unificada: {S3_PREFIX_NEW}")
print(f"Arquivos movidos: {moved}")
print(f"Arquivos adicionados: {uploaded}")
print(f"Total final: {count} arquivos")

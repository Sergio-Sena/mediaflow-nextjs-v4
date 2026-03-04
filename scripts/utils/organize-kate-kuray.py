import boto3
import re

s3 = boto3.client('s3')
bucket = 'mediaflow-uploads-969430605054'

print("=" * 80)
print("ORGANIZACAO PASTA ESPECIFICA")
print("=" * 80)

# ETAPA 1: Listar arquivos em users/sergio_sena/FolderA/
print("\n[1/3] Listando users/sergio_sena/FolderA/...")
try:
    response = s3.list_objects_v2(Bucket=bucket, Prefix='users/sergio_sena/FolderA/', MaxKeys=1000)
    kate_root = response.get('Contents', [])
    print(f"[OK] Encontrados {len(kate_root)} arquivos")
except Exception as e:
    print(f"[ERRO] {e}")
    kate_root = []

# ETAPA 2: Listar arquivos em users/sergio_sena/Category/FolderA/
print("\n[2/3] Listando users/sergio_sena/Category/FolderA/...")
try:
    response = s3.list_objects_v2(Bucket=bucket, Prefix='users/sergio_sena/Category/FolderA/', MaxKeys=1000)
    kate_star = response.get('Contents', [])
    print(f"[OK] Encontrados {len(kate_star)} arquivos")
    
    # Criar dicionario de arquivos existentes com qualidade
    existing = {}
    for obj in kate_star:
        filename = obj['Key'].split('/')[-1]
        # Extrair qualidade do nome (1080, 2160, 4K, etc)
        quality_match = re.search(r'\((\d+)\)', filename)
        quality = int(quality_match.group(1)) if quality_match else 0
        
        base_name = re.sub(r'\s*\(\d+\)', '', filename).strip()
        
        if base_name not in existing or quality > existing[base_name]['quality']:
            existing[base_name] = {
                'key': obj['Key'],
                'quality': quality,
                'size': obj['Size']
            }
    
    print(f"[OK] {len(existing)} arquivos unicos em Category/FolderA/"))
    
except Exception as e:
    print(f"[ERRO] {e}")
    existing = {}

# ETAPA 3: Mover/Deduplicar
print("\n[3/3] Movendo e deduplicando...")
moved = 0
skipped = 0
deleted = 0

for obj in kate_root:
    old_key = obj['Key']
    filename = old_key.split('/')[-1]
    
    # Extrair qualidade
    quality_match = re.search(r'\((\d+)\)', filename)
    quality = int(quality_match.group(1)) if quality_match else 0
    
    base_name = re.sub(r'\s*\(\d+\)', '', filename).strip()
    new_key = f'users/sergio_sena/Category/FolderA/{filename}'
    
    # Verificar se ja existe
    if base_name in existing:
        existing_quality = existing[base_name]['quality']
        
        if quality > existing_quality:
            # Nova versao tem maior qualidade - substituir
            print(f"  [UPGRADE] {filename} ({quality}p > {existing_quality}p)")
            
            # Deletar versao antiga
            s3.delete_object(Bucket=bucket, Key=existing[base_name]['key'])
            
            # Copiar nova versao
            s3.copy_object(
                Bucket=bucket,
                CopySource={'Bucket': bucket, 'Key': old_key},
                Key=new_key
            )
            
            # Deletar original
            s3.delete_object(Bucket=bucket, Key=old_key)
            
            moved += 1
            deleted += 1
        else:
            # Versao existente tem maior ou igual qualidade - manter
            print(f"  [SKIP] {filename} ({quality}p <= {existing_quality}p)")
            
            # Deletar versao da raiz
            s3.delete_object(Bucket=bucket, Key=old_key)
            
            skipped += 1
    else:
        # Arquivo nao existe - mover
        print(f"  [MOVE] {filename}")
        
        s3.copy_object(
            Bucket=bucket,
            CopySource={'Bucket': bucket, 'Key': old_key},
            Key=new_key
        )
        
        s3.delete_object(Bucket=bucket, Key=old_key)
        
        moved += 1

print(f"\n[OK] Movidos: {moved}")
print(f"[OK] Ignorados (qualidade menor): {skipped}")
print(f"[OK] Substituidos (qualidade maior): {deleted}")

# ETAPA 4: Deletar pasta vazia FolderA/ da raiz
print("\n[4/4] Verificando pasta vazia...")
try:
    response = s3.list_objects_v2(Bucket=bucket, Prefix='users/sergio_sena/FolderA/', MaxKeys=1)
    if response.get('KeyCount', 0) == 0:
        print("[OK] Pasta FolderA/ vazia e removida")
    else:
        print(f"[ATENCAO] Ainda existem {response['KeyCount']} arquivos em FolderA/")
except Exception as e:
    print(f"[ERRO] {e}")

print("\n" + "=" * 80)
print("ORGANIZACAO CONCLUIDA")
print("=" * 80)

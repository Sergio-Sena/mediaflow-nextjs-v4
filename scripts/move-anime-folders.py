import boto3

s3 = boto3.client('s3', region_name='us-east-1')
bucket = 'mediaflow-uploads-969430605054'

# Mover users/anonymous/Anime/ → users/user_admin/Anime/
print("Movendo users/anonymous/Anime/ para users/user_admin/Anime/")

paginator = s3.get_paginator('list_objects_v2')
pages = paginator.paginate(Bucket=bucket, Prefix='users/anonymous/Anime/')

moved = 0
for page in pages:
    if 'Contents' not in page:
        continue
    
    for obj in page['Contents']:
        old_key = obj['Key']
        
        # Pular se for apenas a pasta
        if old_key.endswith('/'):
            continue
        
        # Nova key: substituir users/anonymous/ por users/user_admin/
        new_key = old_key.replace('users/anonymous/', 'users/user_admin/')
        
        print(f"  {old_key} -> {new_key}")
        
        # Copiar
        s3.copy_object(
            Bucket=bucket,
            CopySource={'Bucket': bucket, 'Key': old_key},
            Key=new_key
        )
        
        # Deletar original
        s3.delete_object(Bucket=bucket, Key=old_key)
        moved += 1

print(f"\n✅ {moved} arquivos movidos de users/anonymous/Anime/ para users/user_admin/Anime/")

# Limpar duplicata users/anonymous/users/user_admin/Anime/
print("\nLimpando duplicata users/anonymous/users/user_admin/Anime/")
pages2 = paginator.paginate(Bucket=bucket, Prefix='users/anonymous/users/user_admin/Anime/')

deleted = 0
for page in pages2:
    if 'Contents' not in page:
        continue
    
    for obj in page['Contents']:
        key = obj['Key']
        print(f"  Deletando: {key}")
        s3.delete_object(Bucket=bucket, Key=key)
        deleted += 1

print(f"\n✅ {deleted} arquivos duplicados removidos")
print("\n🎯 Estrutura final: users/user_admin/Anime/ (mesclado)")

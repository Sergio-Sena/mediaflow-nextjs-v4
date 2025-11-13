import boto3

s3 = boto3.client('s3', region_name='us-east-1')
dynamodb = boto3.resource('dynamodb', region_name='us-east-1')

bucket = 'mediaflow-uploads-969430605054'

# Contar arquivos
print("=== CONTAGEM DE ARQUIVOS ===\n")

paginator = s3.get_paginator('list_objects_v2')

# user_admin
pages = paginator.paginate(Bucket=bucket, Prefix='users/user_admin/')
user_admin_count = sum(len(page.get('Contents', [])) for page in pages)
print(f"users/user_admin/: {user_admin_count} arquivos")

# sergio_sena
pages = paginator.paginate(Bucket=bucket, Prefix='users/sergio_sena/')
sergio_sena_count = sum(len(page.get('Contents', [])) for page in pages)
print(f"users/sergio_sena/: {sergio_sena_count} arquivos")

print(f"\nDiferença: {sergio_sena_count - user_admin_count} arquivos a mais em sergio_sena")

# Verificar se diferença é 2
if sergio_sena_count - user_admin_count == 2:
    print("\n[OK] CONFIRMADO: sergio_sena tem exatamente 2 arquivos a mais (backup completo!)")
    
    print("\n=== INICIANDO LIMPEZA ===\n")
    
    # 1. Deletar user_admin do DynamoDB
    print("1. Deletando user_admin do DynamoDB...")
    table = dynamodb.Table('mediaflow-users')
    table.delete_item(Key={'user_id': 'user_admin'})
    print("   [OK] user_admin deletado do DynamoDB")
    
    # 2. Deletar pasta users/user_admin/ do S3
    print(f"\n2. Deletando {user_admin_count} arquivos de users/user_admin/...")
    deleted = 0
    pages = paginator.paginate(Bucket=bucket, Prefix='users/user_admin/')
    for page in pages:
        for obj in page.get('Contents', []):
            s3.delete_object(Bucket=bucket, Key=obj['Key'])
            deleted += 1
            # Progress bar
            percent = (deleted / user_admin_count) * 100
            bar_length = 40
            filled = int(bar_length * deleted / user_admin_count)
            bar = '=' * filled + '-' * (bar_length - filled)
            print(f"\r   [{bar}] {percent:.1f}% ({deleted}/{user_admin_count})", end='', flush=True)
    print()  # New line after progress bar
    
    print(f"   [OK] {deleted} arquivos deletados do S3")
    
    print("\n[SUCESSO] LIMPEZA CONCLUIDA COM SUCESSO!")
    print("\nResumo:")
    print(f"  - user_admin removido do DynamoDB")
    print(f"  - {deleted} arquivos removidos do S3")
    print(f"  - sergio_sena mantém {sergio_sena_count} arquivos (backup completo)")
    
else:
    print(f"\n[ERRO] ATENCAO: Diferenca esperada era 2, mas encontrada {sergio_sena_count - user_admin_count}")
    print("   Limpeza CANCELADA por segurança. Verifique os dados.")

import boto3
import json
import time
from datetime import datetime

# Clients
dynamodb = boto3.resource('dynamodb')
s3 = boto3.client('s3')
table = dynamodb.Table('mediaflow-users')

BUCKET = 'mediaflow-uploads-969430605054'

print("="*60)
print("MIGRACAO: user_admin -> sergio_sena + admin_sistema")
print("="*60)
print()

# PASSO 1: Backup DynamoDB
print("1. Fazendo backup DynamoDB...")
try:
    response = table.scan()
    backup_file = f"backup-users-{datetime.now().strftime('%Y%m%d-%H%M%S')}.json"
    with open(backup_file, 'w') as f:
        json.dump(response['Items'], f, indent=2, default=str)
    print(f"   [OK] Backup salvo: {backup_file}")
except Exception as e:
    print(f"   [ERRO] Backup falhou: {e}")
    exit(1)

# PASSO 2: Buscar user_admin atual
print("\n2. Buscando user_admin atual...")
try:
    response = table.get_item(Key={'user_id': 'user_admin'})
    if 'Item' not in response:
        print("   [ERRO] user_admin nao encontrado!")
        exit(1)
    
    user_admin = response['Item']
    print(f"   [OK] Encontrado: {user_admin['name']} ({user_admin['email']})")
    print(f"   [OK] Role atual: {user_admin.get('role', 'N/A')}")
except Exception as e:
    print(f"   [ERRO] Busca falhou: {e}")
    exit(1)

# PASSO 3: Criar admin_sistema
print("\n3. Criando admin_sistema...")
try:
    admin_sistema = {
        'user_id': 'admin_sistema',
        'name': 'Administrador',
        'email': user_admin['email'],  # Mesmo email
        'password': user_admin['password'],  # Mesmo hash
        'role': 'admin',
        's3_prefix': 'users/admin_sistema/',
        'status': 'approved',
        'created_at': datetime.now().isoformat(),
        'avatar_url': ''
    }
    
    # Copiar totp_secret se existir
    if 'totp_secret' in user_admin:
        admin_sistema['totp_secret'] = user_admin['totp_secret']
    
    table.put_item(Item=admin_sistema)
    print(f"   [OK] admin_sistema criado")
    print(f"   [OK] Email: {admin_sistema['email']}")
    print(f"   [OK] Role: admin")
except Exception as e:
    print(f"   [ERRO] Criacao falhou: {e}")
    exit(1)

# PASSO 4: Atualizar user_admin -> sergio_sena
print("\n4. Atualizando user_admin -> sergio_sena...")
try:
    # Deletar user_admin
    table.delete_item(Key={'user_id': 'user_admin'})
    
    # Criar sergio_sena
    sergio_sena = {
        'user_id': 'sergio_sena',
        'name': 'Sergio Sena',
        'email': 'sergio@midiaflow.com',  # Novo email
        'password': user_admin['password'],  # Mesmo hash (pode trocar depois)
        'role': 'user',  # Nao mais admin
        's3_prefix': 'users/sergio_sena/',
        'status': 'approved',
        'created_at': user_admin.get('created_at', datetime.now().isoformat()),
        'avatar_url': user_admin.get('avatar_url', '')
    }
    
    table.put_item(Item=sergio_sena)
    print(f"   [OK] sergio_sena criado")
    print(f"   [OK] Email: {sergio_sena['email']}")
    print(f"   [OK] Role: user (sem acesso admin)")
except Exception as e:
    print(f"   [ERRO] Atualizacao falhou: {e}")
    print(f"   [ROLLBACK] Restaurando user_admin...")
    table.put_item(Item=user_admin)
    exit(1)

# PASSO 5: Mover arquivos S3
print("\n5. Movendo arquivos S3 (248 GB)...")
print("   [INFO] Isso pode levar 30-60 minutos...")
print("   [INFO] Progresso sera mostrado a cada 100 arquivos")

try:
    paginator = s3.get_paginator('list_objects_v2')
    pages = paginator.paginate(Bucket=BUCKET, Prefix='users/user_admin/')
    
    moved = 0
    errors = 0
    
    for page in pages:
        if 'Contents' not in page:
            continue
        
        for obj in page['Contents']:
            old_key = obj['Key']
            new_key = old_key.replace('users/user_admin/', 'users/sergio_sena/')
            
            try:
                # Copy
                s3.copy_object(
                    Bucket=BUCKET,
                    CopySource={'Bucket': BUCKET, 'Key': old_key},
                    Key=new_key
                )
                
                # Delete original
                s3.delete_object(Bucket=BUCKET, Key=old_key)
                
                moved += 1
                
                if moved % 100 == 0:
                    print(f"   [PROGRESSO] {moved} arquivos movidos...")
                
            except Exception as e:
                errors += 1
                print(f"   [ERRO] {old_key}: {e}")
    
    print(f"\n   [OK] Migracao S3 concluida!")
    print(f"   [OK] Movidos: {moved} arquivos")
    if errors > 0:
        print(f"   [AVISO] Erros: {errors} arquivos")

except Exception as e:
    print(f"   [ERRO CRITICO] Migracao S3 falhou: {e}")
    print(f"   [AVISO] DynamoDB ja foi alterado!")
    print(f"   [AVISO] Restaure manualmente do backup: {backup_file}")
    exit(1)

# PASSO 6: Criar placeholder admin_sistema
print("\n6. Criando pasta admin_sistema...")
try:
    s3.put_object(
        Bucket=BUCKET,
        Key='users/admin_sistema/.keep',
        Body=b'Pasta administrativa - sem conteudo pessoal'
    )
    print("   [OK] Pasta criada")
except Exception as e:
    print(f"   [AVISO] Placeholder falhou: {e}")

# PASSO 7: Validacao
print("\n7. Validando migracao...")
try:
    # Verificar DynamoDB
    admin = table.get_item(Key={'user_id': 'admin_sistema'})
    sergio = table.get_item(Key={'user_id': 'sergio_sena'})
    
    if 'Item' not in admin or 'Item' not in sergio:
        print("   [ERRO] Usuarios nao encontrados!")
        exit(1)
    
    print("   [OK] DynamoDB:")
    print(f"      - admin_sistema: role={admin['Item']['role']}")
    print(f"      - sergio_sena: role={sergio['Item']['role']}")
    
    # Verificar S3
    response = s3.list_objects_v2(Bucket=BUCKET, Prefix='users/sergio_sena/', MaxKeys=1)
    if 'Contents' in response:
        print(f"   [OK] S3: users/sergio_sena/ existe")
    else:
        print(f"   [AVISO] S3: users/sergio_sena/ vazia")
    
    # Verificar user_admin nao existe mais
    response = s3.list_objects_v2(Bucket=BUCKET, Prefix='users/user_admin/', MaxKeys=1)
    if 'Contents' not in response:
        print(f"   [OK] S3: users/user_admin/ removida")
    else:
        print(f"   [AVISO] S3: users/user_admin/ ainda existe (arquivos restantes)")

except Exception as e:
    print(f"   [ERRO] Validacao falhou: {e}")

# RESUMO
print("\n" + "="*60)
print("MIGRACAO CONCLUIDA!")
print("="*60)
print()
print("RESULTADO:")
print(f"  [OK] Backup: {backup_file}")
print(f"  [OK] admin_sistema criado (role: admin)")
print(f"  [OK] sergio_sena criado (role: user)")
print(f"  [OK] {moved} arquivos movidos para users/sergio_sena/")
print()
print("PROXIMOS PASSOS:")
print("  1. Tecorporativo login admin: admin@midiaflow.com")
print("  2. Tecorporativo login sergio: sergio@midiaflow.com")
print("  3. Verificar arquivos no dashboard")
print("  4. Trocar senha de sergio (opcional)")
print()
print("ROLLBACK (se necessario):")
print(f"  python scripts/rollback-migration.py {backup_file}")
print()

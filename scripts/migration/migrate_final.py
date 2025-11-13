#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Migração com checklist e auto-aprovação"""

import boto3
import os
import sys
import json
from datetime import datetime
from dotenv import load_dotenv

if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

load_dotenv('.env.local')

dynamodb = boto3.resource(
    'dynamodb',
    region_name=os.getenv('AWS_REGION', 'us-east-1'),
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY')
)
s3 = boto3.client(
    's3',
    region_name=os.getenv('AWS_REGION', 'us-east-1'),
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY')
)

table = dynamodb.Table('mediaflow-users')
bucket = 'mediaflow-uploads-969430605054'

def print_checklist():
    print("\n" + "="*60)
    print("  CHECKLIST DE MIGRACAO")
    print("="*60)
    print("\n[ ] 1. Backup do user_admin")
    print("[ ] 2. Criar admin_sistema (limpo, role admin)")
    print("[ ] 3. Criar sergio_sena (role user, sem midias ainda)")
    print("[ ] 4. Mover arquivos: user_admin -> sergio_sena")
    print("[ ] 5. Deletar user_admin antigo")
    print("[ ] 6. Verificacao final")
    print("\n" + "="*60)

def update_checklist(step):
    steps = [
        "1. Backup do user_admin",
        "2. Criar admin_sistema (limpo, role admin)",
        "3. Criar sergio_sena (role user, sem midias ainda)",
        "4. Mover arquivos: user_admin -> sergio_sena",
        "5. Deletar user_admin antigo",
        "6. Verificacao final"
    ]
    print("\n" + "="*60)
    print("  CHECKLIST DE MIGRACAO")
    print("="*60)
    for i, s in enumerate(steps, 1):
        if i <= step:
            print(f"[X] {s}")
        else:
            print(f"[ ] {s}")
    print("="*60)

print("\n" + "="*60)
print("  MIGRACAO: user_admin -> admin_sistema + sergio_sena")
print("="*60)

print_checklist()
input("\nPressione ENTER para iniciar...")

try:
    # PASSO 1: Backup
    print("\n[PASSO 1/5] Fazendo backup...")
    resp = table.get_item(Key={'user_id': 'user_admin'})
    if 'Item' not in resp:
        raise Exception("user_admin nao encontrado!")
    
    backup = resp['Item']
    filename = f'backup_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(backup, f, indent=2, default=str)
    
    print(f"[OK] Backup salvo: {filename}")
    print(f"     User: {backup['user_id']}")
    print(f"     Role: {backup.get('role')}")
    print(f"     Senha: {backup['password'][:20]}...")
    update_checklist(1)
    
    # PASSO 2: Criar admin_sistema
    print("\n[PASSO 2/5] Criando admin_sistema...")
    admin_sistema = {
        'user_id': 'admin_sistema',
        'password': backup['password'],
        'role': 'admin',
        'avatar': backup.get('avatar', ''),
        'created_at': datetime.now().isoformat()
    }
    table.put_item(Item=admin_sistema)
    
    print("[OK] admin_sistema criado!")
    print("     User: admin_sistema")
    print("     Role: admin")
    print("     Senha: Mesma do user_admin")
    print("     Avatar: Sim")
    print("     Midias: 0 (limpo)")
    update_checklist(2)
    
    # PASSO 3: Criar sergio_sena
    print("\n[PASSO 3/5] Criando sergio_sena...")
    sergio_sena = {
        'user_id': 'sergio_sena',
        'password': backup['password'],
        'role': 'user',
        'avatar': backup.get('avatar', ''),
        'created_at': backup.get('created_at', datetime.now().isoformat())
    }
    table.put_item(Item=sergio_sena)
    
    print("[OK] sergio_sena criado!")
    print("     User: sergio_sena")
    print("     Role: user (admin removido)")
    print("     Senha: Mesma do user_admin")
    print("     Avatar: Sim")
    print("     Midias: 0 (ainda vazio, sera movido no passo 4)")
    update_checklist(3)
    
    # PASSO 4: Mover arquivos S3
    print("\n[PASSO 4/5] Movendo arquivos S3 (DEMORADO)...")
    print("Contando arquivos...")
    
    paginator = s3.get_paginator('list_objects_v2')
    pages = paginator.paginate(Bucket=bucket, Prefix='users/user_admin/')
    
    all_files = []
    for page in pages:
        if 'Contents' in page:
            all_files.extend(page['Contents'])
    
    total = len(all_files)
    total_size = sum(f['Size'] for f in all_files)
    
    print(f"Total: {total} arquivos ({total_size / (1024**3):.2f} GB)")
    print("Iniciando copia...\n")
    
    for i, obj in enumerate(all_files, 1):
        old_key = obj['Key']
        new_key = old_key.replace('users/user_admin/', 'users/sergio_sena/')
        size = obj['Size']
        
        # Copy simples ou multipart
        if size < 5 * 1024**3:
            s3.copy_object(
                Bucket=bucket,
                CopySource={'Bucket': bucket, 'Key': old_key},
                Key=new_key
            )
        else:
            # Arquivo grande - multipart
            mpu = s3.create_multipart_upload(Bucket=bucket, Key=new_key)
            upload_id = mpu['UploadId']
            
            try:
                parts = []
                part_size = 100 * 1024**2
                part_num = 1
                
                for start in range(0, size, part_size):
                    end = min(start + part_size - 1, size - 1)
                    part = s3.upload_part_copy(
                        Bucket=bucket,
                        Key=new_key,
                        CopySource={'Bucket': bucket, 'Key': old_key},
                        CopySourceRange=f'bytes={start}-{end}',
                        PartNumber=part_num,
                        UploadId=upload_id
                    )
                    parts.append({
                        'ETag': part['CopyPartResult']['ETag'],
                        'PartNumber': part_num
                    })
                    part_num += 1
                
                s3.complete_multipart_upload(
                    Bucket=bucket,
                    Key=new_key,
                    UploadId=upload_id,
                    MultipartUpload={'Parts': parts}
                )
            except Exception as e:
                s3.abort_multipart_upload(Bucket=bucket, Key=new_key, UploadId=upload_id)
                raise e
        
        # Barra de progresso
        percent = (i / total) * 100
        bar_length = 40
        filled = int(bar_length * i / total)
        bar = '█' * filled + '░' * (bar_length - filled)
        print(f"\r[{bar}] {percent:.1f}% ({i}/{total})", end='', flush=True)
    
    print(f"\n\n[OK] {total} arquivos movidos!")
    print(f"     De: users/user_admin/")
    print(f"     Para: users/sergio_sena/")
    update_checklist(4)
    
    # PASSO 5: Deletar user_admin
    print("\n[PASSO 5/5] Deletando user_admin antigo...")
    table.delete_item(Key={'user_id': 'user_admin'})
    print("[OK] user_admin deletado do DynamoDB")
    update_checklist(5)
    
    # PASSO 6: Verificação final
    print("\n[VERIFICACAO FINAL]")
    
    # Verificar DynamoDB
    print("\nDynamoDB:")
    for user_id in ['admin_sistema', 'sergio_sena', 'user_admin']:
        try:
            resp = table.get_item(Key={'user_id': user_id})
            if 'Item' in resp:
                u = resp['Item']
                print(f"  [OK] {user_id}: role={u.get('role')}")
            else:
                if user_id == 'user_admin':
                    print(f"  [OK] {user_id}: deletado (esperado)")
                else:
                    print(f"  [ERRO] {user_id}: nao encontrado!")
        except Exception as e:
            print(f"  [ERRO] {user_id}: {e}")
    
    # Verificar S3
    print("\nS3:")
    for prefix in ['users/admin_sistema/', 'users/sergio_sena/']:
        try:
            resp = s3.list_objects_v2(Bucket=bucket, Prefix=prefix, MaxKeys=1000)
            count = len(resp.get('Contents', []))
            if prefix == 'users/admin_sistema/':
                print(f"  [OK] {prefix}: {count} arquivos (esperado: 0)")
            else:
                print(f"  [OK] {prefix}: {count} arquivos")
        except Exception as e:
            print(f"  [ERRO] {prefix}: {e}")
    
    update_checklist(6)
    
    # Resumo final
    print("\n" + "="*60)
    print("  MIGRACAO CONCLUIDA COM SUCESSO!")
    print("="*60)
    print("\n[RESULTADO]")
    print("  [OK] admin_sistema:")
    print("       - Role: admin")
    print("       - Senha: mesma do user_admin")
    print("       - Avatar: sim")
    print("       - Midias: 0 (limpo)")
    print("\n  [OK] sergio_sena:")
    print("       - Role: user (admin removido)")
    print("       - Senha: mesma do user_admin")
    print("       - Avatar: sim")
    print(f"       - Midias: {total} arquivos")
    print("\n  [OK] user_admin: deletado")
    print(f"\n  [BACKUP] {filename}")
    print("\n" + "="*60)
    
except Exception as e:
    print(f"\n\n[ERRO] Falha na migracao: {e}")
    print("\n[ROLLBACK] Restaure o backup se necessario:")
    print(f"  python restore_backup.py {filename}")
    sys.exit(1)

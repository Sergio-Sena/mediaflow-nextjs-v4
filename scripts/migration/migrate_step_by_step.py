#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Migração em etapas separadas"""

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

def step1_backup():
    """ETAPA 1: Backup"""
    print("\n" + "="*60)
    print("  [ETAPA 1] BACKUP")
    print("="*60)
    
    resp = table.get_item(Key={'user_id': 'user_admin'})
    if 'Item' not in resp:
        print("[ERRO] user_admin nao encontrado!")
        return None
    
    backup = resp['Item']
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f'backup_step_{timestamp}.json'
    
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(backup, f, indent=2, default=str)
    
    print(f"[OK] Backup salvo: {filename}")
    print(f"    User: {backup['user_id']}")
    print(f"    Role: {backup.get('role')}")
    return backup

def step2_create_admin_sistema(backup):
    """ETAPA 2: Criar admin_sistema (rapido)"""
    print("\n" + "="*60)
    print("  [ETAPA 2] CRIAR admin_sistema (RAPIDO)")
    print("="*60)
    
    admin_sistema = {
        'user_id': 'admin_sistema',
        'password': backup['password'],
        'role': 'admin',
        'avatar': backup.get('avatar', ''),
        'created_at': datetime.now().isoformat()
    }
    
    table.put_item(Item=admin_sistema)
    print(f"[OK] admin_sistema criado!")
    print(f"    Senha: {admin_sistema['password'][:20]}...")
    print(f"    Role: admin")
    print(f"    Avatar: Sim")

def step3_rename_to_sergio(backup):
    """ETAPA 3: Renomear user_admin -> sergio_sena (rapido)"""
    print("\n" + "="*60)
    print("  [ETAPA 3] RENOMEAR user_admin -> sergio_sena (RAPIDO)")
    print("="*60)
    
    sergio_sena = {
        'user_id': 'sergio_sena',
        'password': backup['password'],
        'role': 'user',  # Remove admin
        'avatar': backup.get('avatar', ''),
        'created_at': backup.get('created_at', datetime.now().isoformat())
    }
    
    table.put_item(Item=sergio_sena)
    print(f"[OK] sergio_sena criado!")
    print(f"    Senha: {sergio_sena['password'][:20]}...")
    print(f"    Role: user (admin removido)")
    print(f"    Avatar: Sim")

def step4_move_s3():
    """ETAPA 4: Mover arquivos S3 (DEMORADO)"""
    print("\n" + "="*60)
    print("  [ETAPA 4] MOVER ARQUIVOS S3 (DEMORADO)")
    print("="*60)
    
    # Contar arquivos
    print("Contando arquivos...")
    paginator = s3.get_paginator('list_objects_v2')
    pages = paginator.paginate(Bucket=bucket, Prefix='users/user_admin/')
    
    all_files = []
    for page in pages:
        if 'Contents' in page:
            all_files.extend(page['Contents'])
    
    total = len(all_files)
    print(f"Total: {total} arquivos\n")
    
    # Copiar com progresso
    for i, obj in enumerate(all_files, 1):
        old_key = obj['Key']
        new_key = old_key.replace('users/user_admin/', 'users/sergio_sena/')
        
        # Copy simples ou multipart
        size = obj['Size']
        if size < 5 * 1024**3:
            s3.copy_object(
                Bucket=bucket,
                CopySource={'Bucket': bucket, 'Key': old_key},
                Key=new_key
            )
        else:
            # Multipart para arquivos grandes
            print(f"\n[LARGE] {old_key.split('/')[-1][:40]}... ({size/(1024**3):.2f} GB)")
            mpu = s3.create_multipart_upload(Bucket=bucket, Key=new_key)
            upload_id = mpu['UploadId']
            
            try:
                parts = []
                part_size = 100 * 1024**2
                part_num = 1
                
                for corporativot in range(0, size, part_size):
                    end = min(corporativot + part_size - 1, size - 1)
                    part = s3.upload_part_copy(
                        Bucket=bucket,
                        Key=new_key,
                        CopySource={'Bucket': bucket, 'Key': old_key},
                        CopySourceRange=f'bytes={corporativot}-{end}',
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
        
        # Progresso
        percent = (i / total) * 100
        bar_length = 40
        filled = int(bar_length * i / total)
        bar = '█' * filled + '░' * (bar_length - filled)
        print(f"\r[{bar}] {percent:.1f}% ({i}/{total})", end='', flush=True)
    
    print(f"\n\n[OK] {total} arquivos movidos!")

def step5_cleanup():
    """ETAPA 5: Limpeza (opcional)"""
    print("\n" + "="*60)
    print("  [ETAPA 5] LIMPEZA (OPCIONAL)")
    print("="*60)
    
    print("\n[AVISO] Migracao concluida com sucesso!")
    print("        Agora voce pode deletar os dados antigos\n")
    
    resp = input("Deletar 'user_admin' do DynamoDB? (s/n): ")
    if resp.lower() == 's':
        table.delete_item(Key={'user_id': 'user_admin'})
        print("[OK] user_admin deletado do DynamoDB")
    
    resp = input("Deletar pasta 'users/user_admin/' do S3? (s/n): ")
    if resp.lower() == 's':
        print("Deletando arquivos S3...")
        paginator = s3.get_paginator('list_objects_v2')
        pages = paginator.paginate(Bucket=bucket, Prefix='users/user_admin/')
        
        deleted = 0
        for page in pages:
            if 'Contents' in page:
                for obj in page['Contents']:
                    s3.delete_object(Bucket=bucket, Key=obj['Key'])
                    deleted += 1
        
        print(f"[OK] {deleted} arquivos deletados do S3")

def main():
    print("\n" + "="*60)
    print("  MIGRACAO EM ETAPAS")
    print("="*60)
    print("\n1. Backup (rapido)")
    print("2. Criar admin_sistema (rapido)")
    print("3. Renomear user_admin -> sergio_sena (rapido)")
    print("4. Mover arquivos S3 (DEMORADO)")
    print("5. Limpeza opcional")
    
    resp = input("\nExecutar todas as etapas? (s/n): ")
    if resp.lower() != 's':
        print("Cancelado")
        return
    
    try:
        # Etapa 1
        backup = step1_backup()
        if not backup:
            return
        
        input("\nPressione ENTER para continuar com Etapa 2...")
        
        # Etapa 2
        step2_create_admin_sistema(backup)
        
        input("\nPressione ENTER para continuar com Etapa 3...")
        
        # Etapa 3
        step3_rename_to_sergio(backup)
        
        input("\nPressione ENTER para continuar com Etapa 4 (DEMORADO)...")
        
        # Etapa 4
        step4_move_s3()
        
        # Etapa 5
        step5_cleanup()
        
        print("\n" + "="*60)
        print("  [SUCESSO] MIGRACAO CONCLUIDA!")
        print("="*60)
        print("\n[OK] admin_sistema: criado (role admin, sem midias)")
        print("[OK] sergio_sena: criado (role user, com todas as midias)")
        print("[OK] Mesmas credenciais mantidas")
        
    except Exception as e:
        print(f"\n[ERRO] {e}")
        print("\nVerifique o backup e restaure se necessario")

if __name__ == '__main__':
    main()

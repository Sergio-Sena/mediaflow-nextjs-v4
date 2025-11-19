#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Migracao: user_admin -> admin_sistema + sergio_sena
Com rollback automatico em caso de erro
"""

import boto3
import json
import sys
import os
from datetime import datetime
from botocore.exceptions import ClientError
from dotenv import load_dotenv

# Fix encoding para Windows
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Carregar variáveis de ambiente
load_dotenv('.env.local')

# Configurações AWS
DYNAMODB_TABLE = 'mediaflow-users'
S3_BUCKET = 'mediaflow-uploads-969430605054'
REGION = os.getenv('AWS_REGION', 'us-east-1')
AWS_ACCESS_KEY = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')

# Clientes AWS
dynamodb = boto3.resource(
    'dynamodb',
    region_name=REGION,
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_KEY
)
s3 = boto3.client(
    's3',
    region_name=REGION,
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_KEY
)
table = dynamodb.Table(DYNAMODB_TABLE)

# Variáveis de controle para rollback
backup_data = {}
admin_sistema_created = False
sergio_sena_created = False
s3_files_moved = []

def print_step(msg):
    print(f"\n{'='*60}")
    print(f"  {msg}")
    print(f"{'='*60}")

def backup_user_admin():
    """Faz backup completo do user_admin"""
    print_step("[BACKUP] ETAPA 1: BACKUP")
    
    try:
        response = table.get_item(Key={'user_id': 'user_admin'})
        if 'Item' not in response:
            raise Exception("[ERRO] user_admin nao encontrado no DynamoDB!")
        
        backup_data['user_admin'] = response['Item']
        
        # Salvar backup em arquivo
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_file = f'backup_migration_{timestamp}.json'
        
        with open(backup_file, 'w', encoding='utf-8') as f:
            json.dump(backup_data, f, indent=2, default=str)
        
        print(f"[OK] Backup salvo: {backup_file}")
        print(f"   User: {backup_data['user_admin']['user_id']}")
        print(f"   Role: {backup_data['user_admin'].get('role', 'N/A')}")
        print(f"   Avatar: {backup_data['user_admin'].get('avatar', 'N/A')[:50]}...")
        
        return True
    except Exception as e:
        print(f"[ERRO] ERRO no backup: {e}")
        return False

def create_admin_sistema():
    """Cria admin_sistema (limpo, com avatar e senha do admin)"""
    global admin_sistema_created
    print_step("[ADMIN] ETAPA 2: CRIAR admin_sistema")
    
    try:
        user_admin = backup_data['user_admin']
        
        admin_sistema = {
            'user_id': 'admin_sistema',
            'password': user_admin['password'],  # Mesma senha
            'role': 'admin',
            'avatar': user_admin.get('avatar', ''),  # Mesmo avatar
            'created_at': datetime.now().isoformat()
        }
        
        table.put_item(Item=admin_sistema)
        admin_sistema_created = True
        
        print(f"[OK] admin_sistema criado com sucesso!")
        print(f"   Senha: {admin_sistema['password'][:20]}...")
        print(f"   Role: {admin_sistema['role']}")
        print(f"   Avatar: {'Sim' if admin_sistema['avatar'] else 'Nao'}")
        
        return True
    except Exception as e:
        print(f"[ERRO] ERRO ao criar admin_sistema: {e}")
        return False

def rename_admin_to_sergio():
    """Renomeia user_admin -> sergio_sena (remove role admin)"""
    global sergio_sena_created
    print_step("[RENAME] ETAPA 3: RENOMEAR user_admin -> sergio_sena")
    
    try:
        user_admin = backup_data['user_admin']
        
        sergio_sena = {
            'user_id': 'sergio_sena',
            'password': user_admin['password'],  # Mesma senha
            'role': 'user',  # Remove admin
            'avatar': user_admin.get('avatar', ''),  # Mesmo avatar
            'created_at': user_admin.get('created_at', datetime.now().isoformat())
        }
        
        table.put_item(Item=sergio_sena)
        sergio_sena_created = True
        
        print(f"[OK] sergio_sena criado com sucesso!")
        print(f"   Senha: {sergio_sena['password'][:20]}...")
        print(f"   Role: {sergio_sena['role']} (admin removido)")
        print(f"   Avatar: {'Sim' if sergio_sena['avatar'] else 'Nao'}")
        
        return True
    except Exception as e:
        print(f"[ERRO] ERRO ao criar sergio_sena: {e}")
        return False

def copy_large_file(old_key, new_key):
    """Copia arquivo grande usando multipart copy"""
    # Limite de 5GB para copy simples
    FIVE_GB = 5 * 1024 * 1024 * 1024
    
    # Obter tamanho do arquivo
    head = s3.head_object(Bucket=S3_BUCKET, Key=old_key)
    size = head['ContentLength']
    
    if size < FIVE_GB:
        # Arquivo pequeno - copy simples
        s3.copy_object(
            Bucket=S3_BUCKET,
            CopySource={'Bucket': S3_BUCKET, 'Key': old_key},
            Key=new_key
        )
    else:
        # Arquivo grande - multipart copy
        print(f"   [LARGE] Copiando arquivo grande: {old_key.split('/')[-1][:50]}... ({size / (1024**3):.2f} GB)")
        
        # Iniciar multipart upload
        mpu = s3.create_multipart_upload(Bucket=S3_BUCKET, Key=new_key)
        upload_id = mpu['UploadId']
        
        try:
            # Copiar em partes de 100MB
            part_size = 100 * 1024 * 1024
            parts = []
            part_num = 1
            
            for corporativot in range(0, size, part_size):
                end = min(corporativot + part_size - 1, size - 1)
                
                part = s3.upload_part_copy(
                    Bucket=S3_BUCKET,
                    Key=new_key,
                    CopySource={'Bucket': S3_BUCKET, 'Key': old_key},
                    CopySourceRange=f'bytes={corporativot}-{end}',
                    PartNumber=part_num,
                    UploadId=upload_id
                )
                
                parts.append({
                    'ETag': part['CopyPartResult']['ETag'],
                    'PartNumber': part_num
                })
                part_num += 1
            
            # Completar multipart upload
            s3.complete_multipart_upload(
                Bucket=S3_BUCKET,
                Key=new_key,
                UploadId=upload_id,
                MultipartUpload={'Parts': parts}
            )
        except Exception as e:
            # Abortar multipart em caso de erro
            s3.abort_multipart_upload(
                Bucket=S3_BUCKET,
                Key=new_key,
                UploadId=upload_id
            )
            raise e

def move_s3_files():
    """Move arquivos de users/user_admin/ -> users/sergio_sena/"""
    global s3_files_moved
    print_step("[S3] ETAPA 4: MOVER ARQUIVOS S3")
    
    try:
        prefix = 'users/user_admin/'
        
        # Primeiro, contar total de arquivos
        print("   Contando arquivos...")
        paginator = s3.get_paginator('list_objects_v2')
        pages = paginator.paginate(Bucket=S3_BUCKET, Prefix=prefix)
        
        all_files = []
        for page in pages:
            if 'Contents' in page:
                all_files.extend(page['Contents'])
        
        total_files = len(all_files)
        print(f"   Total: {total_files} arquivos\n")
        
        # Copiar com barra de progresso
        files_count = 0
        for obj in all_files:
            old_key = obj['Key']
            new_key = old_key.replace('users/user_admin/', 'users/sergio_sena/')
            
            # Copiar (suporta arquivos grandes)
            copy_large_file(old_key, new_key)
            
            s3_files_moved.append({'old': old_key, 'new': new_key})
            files_count += 1
            
            # Barra de progresso
            percent = (files_count / total_files) * 100
            bar_length = 40
            filled = int(bar_length * files_count / total_files)
            bar = '█' * filled + '░' * (bar_length - filled)
            print(f"\r   [{bar}] {percent:.1f}% ({files_count}/{total_files})", end='', flush=True)
        
        print()  # Nova linha
        print(f"\n[OK] {files_count} arquivos movidos com sucesso!")
        print(f"   De: users/user_admin/")
        print(f"   Para: users/sergio_sena/")
        
        return True
    except Exception as e:
        print(f"\n[ERRO] ERRO ao mover arquivos S3: {e}")
        return False

def rollback():
    """Reverte todas as mudancas em caso de erro"""
    print_step("[ROLLBACK] ROLLBACK AUTOMATICO")
    
    try:
        # Restaurar user_admin
        if backup_data.get('user_admin'):
            table.put_item(Item=backup_data['user_admin'])
            print("[OK] user_admin restaurado")
        
        # Deletar admin_sistema se foi criado
        if admin_sistema_created:
            table.delete_item(Key={'user_id': 'admin_sistema'})
            print("[OK] admin_sistema deletado")
        
        # Deletar sergio_sena se foi criado
        if sergio_sena_created:
            table.delete_item(Key={'user_id': 'sergio_sena'})
            print("[OK] sergio_sena deletado")
        
        # Reverter arquivos S3
        if s3_files_moved:
            for file_info in s3_files_moved:
                try:
                    s3.delete_object(Bucket=S3_BUCKET, Key=file_info['new'])
                except:
                    pass
            print(f"[OK] {len(s3_files_moved)} arquivos S3 revertidos")
        
        print("\n[OK] ROLLBACK CONCLUIDO - Sistema restaurado ao estado original")
        
    except Exception as e:
        print(f"[ERRO] ERRO no rollback: {e}")
        print("[AVISO] ATENCAO: Restauracao manual pode ser necessaria!")

def cleanup_old_data():
    """Limpa dados antigos apos confirmacao"""
    print_step("[CLEANUP] LIMPEZA (OPCIONAL)")
    
    print("\n[AVISO] Migracao concluida com sucesso!")
    print("   Deseja deletar os dados antigos?\n")
    
    # Deletar user_admin do DynamoDB
    resp = input("   Deletar 'user_admin' do DynamoDB? (s/n): ").lower()
    if resp == 's':
        try:
            table.delete_item(Key={'user_id': 'user_admin'})
            print("   [OK] user_admin deletado do DynamoDB")
        except Exception as e:
            print(f"   [ERRO] Erro ao deletar: {e}")
    
    # Deletar pasta S3
    resp = input("   Deletar pasta 'users/user_admin/' do S3? (s/n): ").lower()
    if resp == 's':
        try:
            prefix = 'users/user_admin/'
            paginator = s3.get_paginator('list_objects_v2')
            pages = paginator.paginate(Bucket=S3_BUCKET, Prefix=prefix)
            
            deleted = 0
            for page in pages:
                if 'Contents' not in page:
                    continue
                for obj in page['Contents']:
                    s3.delete_object(Bucket=S3_BUCKET, Key=obj['Key'])
                    deleted += 1
            
            print(f"   [OK] {deleted} arquivos deletados do S3")
        except Exception as e:
            print(f"   [ERRO] Erro ao deletar: {e}")

def main():
    print("\n" + "="*60)
    print("  [MIGRACAO] user_admin -> admin_sistema + sergio_sena")
    print("="*60)
    
    try:
        # Etapa 1: Backup
        if not backup_user_admin():
            raise Exception("Falha no backup")
        
        # Etapa 2: Criar admin_sistema
        if not create_admin_sistema():
            raise Exception("Falha ao criar admin_sistema")
        
        # Etapa 3: Renomear para sergio_sena
        if not rename_admin_to_sergio():
            raise Exception("Falha ao criar sergio_sena")
        
        # Etapa 4: Mover arquivos S3
        if not move_s3_files():
            raise Exception("Falha ao mover arquivos S3")
        
        # Sucesso!
        print_step("[SUCESSO] MIGRACAO CONCLUIDA COM SUCESSO!")
        print("\n[RESULTADO]:")
        print("   [OK] admin_sistema: criado (role admin, pasta vazia)")
        print("   [OK] sergio_sena: criado (role user, com todos os arquivos)")
        print("   [OK] Ambos mantem senha e avatar originais")
        print("   [OK] Backup salvo localmente")
        
        # Limpeza opcional
        cleanup_old_data()
        
    except Exception as e:
        print(f"\n[ERRO] ERRO NA MIGRACAO: {e}")
        rollback()
        return 1
    
    return 0

if __name__ == '__main__':
    exit(main())

#!/usr/bin/env python3
"""
Rollback rapido para versao anterior
"""
import boto3
import sys

S3_BUCKET = 'midiaflow-frontend-969430605054'
BACKUP_BUCKET = 'midiaflow-backups-969430605054'
CLOUDFRONT_ID = 'E2HZKZ9ZJK18IU'

s3 = boto3.client('s3')
cf = boto3.client('cloudfront')

def list_backups():
    """Lista backups disponiveis"""
    print("Backups disponiveis:")
    print("="*60)
    
    try:
        response = s3.list_objects_v2(Bucket=BACKUP_BUCKET, Delimiter='/')
        
        backups = []
        for prefix in response.get('CommonPrefixes', []):
            backup_name = prefix['Prefix'].replace('backups/', '').strip('/')
            if backup_name:
                backups.append(backup_name)
        
        if not backups:
            print("Nenhum backup encontrado!")
            return None
        
        backups.sort(reverse=True)
        
        for i, backup in enumerate(backups[:10], 1):
            print(f"{i}. {backup}")
        
        return backups
    except Exception as e:
        print(f"Erro ao listar backups: {e}")
        return None

def rollback(backup_name):
    """Restaura backup especifico"""
    print(f"\nRestaurando backup: {backup_name}")
    print("="*60)
    
    backup_prefix = f"backups/{backup_name}/"
    
    try:
        # Limpar bucket atual
        print("Limpando bucket atual...")
        paginator = s3.get_paginator('list_objects_v2')
        deleted = 0
        
        for page in paginator.paginate(Bucket=S3_BUCKET):
            for obj in page.get('Contents', []):
                s3.delete_object(Bucket=S3_BUCKET, Key=obj['Key'])
                deleted += 1
        
        print(f"✓ {deleted} arquivos removidos")
        
        # Restaurar backup
        print("\nRestaurando arquivos...")
        restored = 0
        
        for page in paginator.paginate(Bucket=BACKUP_BUCKET, Prefix=backup_prefix):
            for obj in page.get('Contents', []):
                new_key = obj['Key'].replace(backup_prefix, '')
                if not new_key:
                    continue
                
                copy_source = {'Bucket': BACKUP_BUCKET, 'Key': obj['Key']}
                s3.copy_object(
                    CopySource=copy_source,
                    Bucket=S3_BUCKET,
                    Key=new_key
                )
                restored += 1
                
                if restored % 20 == 0:
                    print(f"  {restored} arquivos...")
        
        print(f"✓ {restored} arquivos restaurados")
        
        # Invalidar CloudFront
        print("\nInvalidando CloudFront...")
        import time
        cf.create_invalidation(
            DistributionId=CLOUDFRONT_ID,
            InvalidationBatch={
                'Paths': {'Quantity': 1, 'Items': ['/*']},
                'CallerReference': str(int(time.time()))
            }
        )
        print("✓ Cache invalidado")
        
        print("\n" + "="*60)
        print("ROLLBACK COMPLETO!")
        print("URL: https://midiaflow.sstechnologies-cloud.com")
        print("="*60)
        
        return True
    except Exception as e:
        print(f"\n✗ Erro no rollback: {e}")
        return False

def main():
    print("\n" + "="*60)
    print("MIDIAFLOW ROLLBACK RAPIDO")
    print("="*60 + "\n")
    
    backups = list_backups()
    if not backups:
        return
    
    print("\n" + "="*60)
    choice = input("Escolha o backup (numero) ou 'q' para sair: ").strip()
    
    if choice.lower() == 'q':
        print("Cancelado")
        return
    
    try:
        index = int(choice) - 1
        if 0 <= index < len(backups):
            backup_name = backups[index]
            
            confirm = input(f"\nConfirmar rollback para {backup_name}? (s/n): ")
            if confirm.lower() == 's':
                rollback(backup_name)
            else:
                print("Cancelado")
        else:
            print("Opcao invalida!")
    except ValueError:
        print("Opcao invalida!")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nCancelado")

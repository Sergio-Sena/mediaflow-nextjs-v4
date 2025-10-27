#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para limpar uploads multipart incompletos no S3
Remove uploads parados, com erro ou abandonados
"""

import boto3
import sys
from datetime import datetime, timedelta

# Fix encoding para Windows
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

BUCKET = 'mediaflow-uploads-969430605054'

def cleanup_incomplete_multipart():
    s3 = boto3.client('s3')
    
    print(f"[BUSCA] Uploads multipart incompletos em {BUCKET}...\n")
    
    # Listar todos os uploads multipart em progresso
    response = s3.list_multipart_uploads(Bucket=BUCKET)
    
    uploads = response.get('Uploads', [])
    
    if not uploads:
        print("[OK] Nenhum upload multipart incompleto encontrado!")
        return
    
    print(f"[INFO] Encontrados {len(uploads)} uploads incompletos:\n")
    
    for upload in uploads:
        key = upload['Key']
        upload_id = upload['UploadId']
        initiated = upload['Initiated']
        age = datetime.now(initiated.tzinfo) - initiated
        
        print(f"  Arquivo: {key}")
        print(f"  ID: {upload_id}")
        print(f"  Iniciado: {initiated}")
        print(f"  Idade: {age.days} dias, {age.seconds // 3600} horas")
        
        # Abortar TODOS os uploads incompletos
        if True:
            try:
                s3.abort_multipart_upload(
                    Bucket=BUCKET,
                    Key=key,
                    UploadId=upload_id
                )
                print(f"  [ABORTADO] Upload muito antigo")
            except Exception as e:
                print(f"  [ERRO] Falha ao abortar: {e}")
        else:
            print(f"  [MANTIDO] Menos de 1 dia")
        
        print()
    
    print(f"\n[CONCLUIDO] Limpeza finalizada!")

if __name__ == '__main__':
    cleanup_incomplete_multipart()

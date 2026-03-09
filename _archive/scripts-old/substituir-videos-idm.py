#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Substitui vídeos: Deleta atuais e faz upload dos vídeos do IDM
"""

import boto3
import sys
import io
from pathlib import Path
from tqdm import tqdm

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

s3 = boto3.client('s3', region_name='us-east-1',
    aws_access_key_id='AKIA6DNURDT7MO5EXHLQ',
    aws_secret_access_key='9wmyrw4365OTX+hwZ2ZZXjE+lbEUxn3INY4tu0Ir')

BUCKET = 'mediaflow-uploads-969430605054'
USER = 'lid_lima'

def deletar_pasta_s3(pasta):
    """Deleta pasta do S3"""
    print(f"\n[DELETE S3] {pasta}")
    
    resp = s3.list_objects_v2(Bucket=BUCKET, Prefix=f"users/{USER}/{pasta}/")
    
    if 'Contents' not in resp:
        print("  -> Pasta vazia")
        return
    
    print(f"  -> {len(resp['Contents'])} arquivos")
    
    for obj in resp['Contents']:
        s3.delete_object(Bucket=BUCKET, Key=obj['Key'])
    
    print("  -> Deletado!")

def upload_pasta(local_path, s3_folder):
    """Upload com barra de progresso"""
    pasta = Path(local_path)
    
    if not pasta.exists():
        print(f"  -> Pasta nao encontrada: {local_path}")
        return
    
    arquivos = [f for f in pasta.rglob('*.mp4') if f.is_file()]
    
    print(f"\n[UPLOAD] {s3_folder}")
    print(f"  -> {len(arquivos)} arquivos MP4")
    
    with tqdm(total=len(arquivos), desc=s3_folder, unit="video") as pbar:
        for file_path in arquivos:
            s3_key = f"users/{USER}/{s3_folder}/{file_path.name}"
            
            try:
                s3.upload_file(str(file_path), BUCKET, s3_key)
                pbar.update(1)
            except Exception as e:
                pbar.write(f"ERRO: {file_path.name} - {e}")
                pbar.update(1)

def main():
    print("=" * 60)
    print("SUBSTITUIR VIDEOS - LID LIMA")
    print("=" * 60)
    
    idm_path = r"C:\Users\dell 5557\Videos\IDM"
    
    # Carros
    print("\n>>> CARROS")
    deletar_pasta_s3("Carros")
    upload_pasta(f"{idm_path}/Carros", "Carros")
    
    # Lilo & Stitch
    print("\n>>> LILO & STITCH")
    deletar_pasta_s3("Lilo & Stitch")
    upload_pasta(f"{idm_path}/Lilo & Stitch", "Lilo & Stitch")
    
    print("\n" + "=" * 60)
    print("CONCLUIDO!")
    print("=" * 60)

if __name__ == "__main__":
    main()

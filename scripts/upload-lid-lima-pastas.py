#!/usr/bin/env python3
"""
Upload das pastas Carros e Lilo & Stitch para o usuário lid lima
"""

import boto3
import os
from pathlib import Path
from tqdm import tqdm

# Configuração AWS
s3_client = boto3.client(
    's3',
    region_name='us-east-1',
    aws_access_key_id='AKIA6DNURDT7MO5EXHLQ',
    aws_secret_access_key='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'
)

BUCKET = 'mediaflow-uploads-969430605054'
USER_ID = 'lid-lima'

def upload_folder(local_path, folder_name):
    """Upload de uma pasta completa"""
    local_path = Path(local_path)
    
    if not local_path.exists():
        print(f"❌ Pasta não encontrada: {local_path}")
        return
    
    print(f"\n📁 Uploading: {folder_name}")
    print(f"   Local: {local_path}")
    print(f"   Destino: users/{USER_ID}/{folder_name}/")
    
    files = [f for f in local_path.rglob('*') if f.is_file()]
    total_files = len(files)
    total_size = sum(f.stat().st_size for f in files)
    
    print(f"   Arquivos: {total_files}")
    print(f"   Tamanho: {total_size / (1024**3):.2f} GB")
    print("-" * 60)
    
    uploaded = 0
    skipped = 0
    errors = 0
    
    for i, file_path in enumerate(files, 1):
        # Caminho relativo dentro da pasta
        relative_path = file_path.relative_to(local_path)
        
        # Chave S3
        s3_key = f"users/{USER_ID}/{folder_name}/{relative_path}".replace('\\', '/')
        
        try:
            # Verificar se já existe
            try:
                s3_client.head_object(Bucket=BUCKET, Key=s3_key)
                skipped += 1
                print(f"⏭️  [{i}/{total_files}] Já existe: {relative_path}")
                continue
            except:
                pass
            
            # Upload
            file_size = file_path.stat().st_size / (1024**2)  # MB
            print(f"📤 [{i}/{total_files}] {relative_path} ({file_size:.1f} MB)")
            
            s3_client.upload_file(
                str(file_path),
                BUCKET,
                s3_key
            )
            
            uploaded += 1
            print(f"✅ Enviado!")
            
        except KeyboardInterrupt:
            print(f"\n\n⚠️  Upload cancelado pelo usuário")
            print(f"✅ Enviados: {uploaded} | ⏭️  Pulados: {skipped} | ❌ Erros: {errors}")
            raise
        except Exception as e:
            errors += 1
            print(f"❌ Erro: {e}")
    
    print(f"\n✅ {folder_name}: {uploaded} enviados | {skipped} já existiam | {errors} erros")

def main():
    print("=" * 60)
    print("🚀 UPLOAD PARA LID LIMA")
    print("=" * 60)
    
    base_path = r"C:\Users\dell 5557\Videos"
    
    # Upload Carros
    upload_folder(
        os.path.join(base_path, "Carros"),
        "Carros"
    )
    
    # Upload Lilo & Stitch
    upload_folder(
        os.path.join(base_path, "Lilo & Stitch"),
        "Lilo & Stitch"
    )
    
    print("\n" + "=" * 60)
    print("✅ UPLOAD CONCLUÍDO!")
    print("=" * 60)

if __name__ == "__main__":
    main()

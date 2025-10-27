#!/usr/bin/env python3
"""
Upload com sanitizacao de nomes - Anasta_angel
"""

import boto3
import os
from pathlib import Path
import unicodedata
import re

def sanitize_filename(filename):
    """Sanitizar nome do arquivo (remover acentos e caracteres especiais)"""
    # Normalizar unicode (remover acentos)
    nfkd = unicodedata.normalize('NFKD', filename)
    filename = ''.join([c for c in nfkd if not unicodedata.combining(c)])
    
    # Remover caracteres especiais (manter apenas letras, numeros, espacos, pontos, hifens, underscores)
    filename = re.sub(r'[^\w\s\.\-]', '', filename)
    
    # Substituir multiplos espacos por um unico
    filename = re.sub(r'\s+', ' ', filename)
    
    # Limitar tamanho (max 200 caracteres)
    name, ext = os.path.splitext(filename)
    if len(name) > 200:
        name = name[:200]
    
    return name + ext

def upload_with_sanitization():
    """Upload com sanitizacao de nomes"""
    try:
        local_path = Path(r"C:\Users\dell 5557\Videos\IDM\Star\Anasta_angel")
        
        s3 = boto3.client('s3', region_name='us-east-1')
        bucket = 'mediaflow-uploads-969430605054'
        prefix = 'users/user_admin/Star/Anasta_angel/'
        
        print("Upload com sanitizacao de nomes")
        print("=" * 50)
        print(f"Origem: {local_path}")
        print(f"Destino: s3://{bucket}/{prefix}")
        print(f"Storage: INTELLIGENT_TIERING")
        print()
        
        if not local_path.exists():
            print("Erro: Pasta local nao encontrada!")
            return False
        
        # Listar arquivos locais
        files_to_upload = []
        for file_path in local_path.rglob('*'):
            if file_path.is_file():
                files_to_upload.append(file_path)
        
        print(f"Total de arquivos: {len(files_to_upload)}")
        print()
        
        # Upload cada arquivo
        uploaded = 0
        skipped = 0
        
        for file_path in files_to_upload:
            try:
                # Nome original e sanitizado
                original_name = file_path.name
                sanitized_name = sanitize_filename(original_name)
                
                # Caminho relativo
                rel_path = file_path.relative_to(local_path)
                rel_dir = rel_path.parent
                
                # Key S3 com nome sanitizado
                if str(rel_dir) != '.':
                    s3_key = f"{prefix}{rel_dir}/{sanitized_name}".replace('\\', '/')
                else:
                    s3_key = f"{prefix}{sanitized_name}"
                
                # Verificar se ja existe no S3
                try:
                    s3.head_object(Bucket=bucket, Key=s3_key)
                    print(f"[SKIP] {original_name}")
                    if original_name != sanitized_name:
                        print(f"       -> {sanitized_name}")
                    skipped += 1
                    continue
                except:
                    pass  # Arquivo nao existe, fazer upload
                
                # Upload
                file_size = file_path.stat().st_size
                file_size_mb = file_size / (1024**2)
                
                print(f"[UP] {original_name} ({file_size_mb:.1f} MB)")
                if original_name != sanitized_name:
                    print(f"     -> {sanitized_name}")
                
                s3.upload_file(
                    str(file_path),
                    bucket,
                    s3_key,
                    ExtraArgs={
                        'StorageClass': 'INTELLIGENT_TIERING',
                        'ContentType': 'video/mp4' if file_path.suffix.lower() == '.mp4' else 'application/octet-stream'
                    }
                )
                
                uploaded += 1
                
            except Exception as e:
                print(f"[ERRO] {file_path.name}: {e}")
        
        print()
        print("=" * 50)
        print(f"Upload concluido!")
        print(f"Enviados: {uploaded}")
        print(f"Pulados: {skipped}")
        print(f"Total: {len(files_to_upload)}")
        
        return True
        
    except Exception as e:
        print(f"Erro: {e}")
        return False

if __name__ == "__main__":
    upload_with_sanitization()

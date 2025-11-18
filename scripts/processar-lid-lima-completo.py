#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script completo: Converte MKV -> MP4, faz upload e limpa arquivos não-MP4
"""

import boto3
import os
import subprocess
import sys
import io
from pathlib import Path

# Fix encoding Windows
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

# Configuração AWS
s3_client = boto3.client(
    's3',
    region_name='us-east-1',
    aws_access_key_id='AKIA6DNURDT7MO5EXHLQ',
    aws_secret_access_key='9wmyrw4365OTX+hwZ2ZZXjE+lbEUxn3INY4tu0Ir'
)

BUCKET = 'mediaflow-uploads-969430605054'
USER_ID = 'lid-lima'
FFMPEG = r"C:\ffmpeg\bin\ffmpeg.exe"

def converter_mkv(pasta_base, pasta_nome):
    """Converte MKV para MP4"""
    print(f"\n🎬 ETAPA 1: Convertendo {pasta_nome}")
    print("-" * 60)
    
    pasta = Path(pasta_base)
    arquivos_mkv = list(pasta.rglob('*.mkv'))
    
    if not arquivos_mkv:
        print(f"✅ Nenhum MKV encontrado")
        return
    
    print(f"Encontrados: {len(arquivos_mkv)} arquivos MKV")
    
    for i, mkv_path in enumerate(arquivos_mkv, 1):
        mp4_path = mkv_path.with_suffix('.mp4')
        
        if mp4_path.exists():
            print(f"⏭️  [{i}/{len(arquivos_mkv)}] Já existe: {mkv_path.name}")
            continue
        
        print(f"\n🔄 [{i}/{len(arquivos_mkv)}] {mkv_path.name}")
        
        try:
            subprocess.run(
                [FFMPEG, '-i', str(mkv_path), '-c', 'copy', '-y', str(mp4_path)],
                capture_output=True,
                timeout=3600
            )
            print(f"✅ Convertido!")
        except Exception as e:
            print(f"❌ Erro: {e}")

def upload_pasta(pasta_base, pasta_nome):
    """Faz upload da pasta para S3"""
    print(f"\n📤 ETAPA 2: Upload {pasta_nome}")
    print("-" * 60)
    
    pasta = Path(pasta_base)
    arquivos = [f for f in pasta.rglob('*') if f.is_file()]
    
    print(f"Total de arquivos: {len(arquivos)}")
    
    for i, file_path in enumerate(arquivos, 1):
        relative_path = file_path.relative_to(pasta)
        s3_key = f"users/{USER_ID}/{pasta_nome}/{relative_path}".replace('\\', '/')
        
        try:
            # Verificar se já existe
            try:
                s3_client.head_object(Bucket=BUCKET, Key=s3_key)
                print(f"⏭️  [{i}/{len(arquivos)}] Já existe: {relative_path}")
                continue
            except:
                pass
            
            print(f"📤 [{i}/{len(arquivos)}] {relative_path}")
            s3_client.upload_file(str(file_path), BUCKET, s3_key)
            print(f"✅ Enviado!")
            
        except Exception as e:
            print(f"❌ Erro: {e}")

def limpar_nao_mp4(pasta_base, pasta_nome):
    """Remove arquivos não-MP4 (local e S3)"""
    print(f"\n🗑️  ETAPA 3: Limpando {pasta_nome}")
    print("-" * 60)
    
    # Limpar local
    pasta = Path(pasta_base)
    nao_mp4 = [f for f in pasta.rglob('*') if f.is_file() and f.suffix.lower() != '.mp4']
    
    print(f"Local: {len(nao_mp4)} arquivos não-MP4")
    for arquivo in nao_mp4:
        try:
            print(f"🗑️  {arquivo.name}")
            arquivo.unlink()
        except Exception as e:
            print(f"❌ Erro: {e}")
    
    # Limpar S3
    try:
        response = s3_client.list_objects_v2(
            Bucket=BUCKET,
            Prefix=f"users/{USER_ID}/{pasta_nome}/"
        )
        
        if 'Contents' in response:
            nao_mp4_s3 = [obj for obj in response['Contents'] if not obj['Key'].lower().endswith('.mp4')]
            
            print(f"S3: {len(nao_mp4_s3)} arquivos não-MP4")
            for obj in nao_mp4_s3:
                try:
                    nome = obj['Key'].split('/')[-1]
                    print(f"🗑️  {nome}")
                    s3_client.delete_object(Bucket=BUCKET, Key=obj['Key'])
                except Exception as e:
                    print(f"❌ Erro: {e}")
    except Exception as e:
        print(f"❌ Erro S3: {e}")

def processar_pasta(pasta_base, pasta_nome):
    """Processa uma pasta completa"""
    print(f"\n{'='*60}")
    print(f"📁 PROCESSANDO: {pasta_nome}")
    print(f"{'='*60}")
    
    # converter_mkv(pasta_base, pasta_nome)  # JÁ CONVERTIDO
    upload_pasta(pasta_base, pasta_nome)
    limpar_nao_mp4(pasta_base, pasta_nome)
    
    print(f"\n✅ {pasta_nome} concluído!")

def main():
    print("=" * 60)
    print("🚀 UPLOAD E LIMPEZA - LID LIMA")
    print("=" * 60)
    print("\nEtapas:")
    print("1. Upload para S3")
    print("2. Limpar arquivos MKV (local + S3)")
    
    confirmar = input("\nDigite 'CONFIRMO' para iniciar: ")
    
    if confirmar != 'CONFIRMO':
        print("❌ Operação cancelada")
        return
    
    base_path = r"C:\Users\dell 5557\Videos"
    
    # Processar Carros
    processar_pasta(os.path.join(base_path, "Carros"), "Carros")
    
    # Processar Lilo & Stitch
    processar_pasta(os.path.join(base_path, "Lilo & Stitch"), "Lilo & Stitch")
    
    print("\n" + "=" * 60)
    print("✅ PROCESSAMENTO COMPLETO CONCLUÍDO!")
    print("=" * 60)

if __name__ == "__main__":
    main()

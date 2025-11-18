#!/usr/bin/env python3
"""
Remove arquivos que não são MP4 (local e S3) das pastas Carros e Lilo & Stitch
"""

import boto3
import os
from pathlib import Path

# Configuração AWS
s3_client = boto3.client(
    's3',
    region_name='us-east-1',
    aws_access_key_id='AKIA6DNURDT7MO5EXHLQ',
    aws_secret_access_key='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'
)

BUCKET = 'mediaflow-uploads-969430605054'
USER_ID = 'lid-lima'

def limpar_local(pasta_base, pasta_nome):
    """Remove arquivos não-MP4 localmente"""
    pasta = Path(pasta_base)
    
    if not pasta.exists():
        print(f"❌ Pasta não encontrada: {pasta}")
        return
    
    print(f"\n🗑️  Limpando local: {pasta_nome}")
    
    # Encontrar todos os arquivos que NÃO são MP4
    todos_arquivos = list(pasta.rglob('*'))
    nao_mp4 = [f for f in todos_arquivos if f.is_file() and f.suffix.lower() != '.mp4']
    
    if not nao_mp4:
        print(f"✅ Nenhum arquivo não-MP4 encontrado")
        return
    
    print(f"   Encontrados: {len(nao_mp4)} arquivos não-MP4")
    
    removidos = 0
    for arquivo in nao_mp4:
        try:
            tamanho = arquivo.stat().st_size / (1024**2)  # MB
            print(f"🗑️  Removendo: {arquivo.name} ({tamanho:.1f} MB)")
            arquivo.unlink()
            removidos += 1
        except Exception as e:
            print(f"❌ Erro ao remover {arquivo.name}: {e}")
    
    print(f"✅ Local: {removidos} arquivos removidos")

def limpar_s3(pasta_nome):
    """Remove arquivos não-MP4 do S3"""
    print(f"\n🗑️  Limpando S3: {pasta_nome}")
    
    prefix = f"users/{USER_ID}/{pasta_nome}/"
    
    try:
        # Listar objetos
        response = s3_client.list_objects_v2(
            Bucket=BUCKET,
            Prefix=prefix
        )
        
        if 'Contents' not in response:
            print(f"✅ Nenhum arquivo encontrado no S3")
            return
        
        # Filtrar não-MP4
        nao_mp4 = [
            obj for obj in response['Contents'] 
            if not obj['Key'].lower().endswith('.mp4')
        ]
        
        if not nao_mp4:
            print(f"✅ Nenhum arquivo não-MP4 encontrado no S3")
            return
        
        print(f"   Encontrados: {len(nao_mp4)} arquivos não-MP4")
        
        removidos = 0
        for obj in nao_mp4:
            try:
                tamanho = obj['Size'] / (1024**2)  # MB
                nome = obj['Key'].split('/')[-1]
                print(f"🗑️  Removendo: {nome} ({tamanho:.1f} MB)")
                
                s3_client.delete_object(
                    Bucket=BUCKET,
                    Key=obj['Key']
                )
                removidos += 1
            except Exception as e:
                print(f"❌ Erro ao remover {nome}: {e}")
        
        print(f"✅ S3: {removidos} arquivos removidos")
        
    except Exception as e:
        print(f"❌ Erro ao listar S3: {e}")

def main():
    print("=" * 60)
    print("🗑️  LIMPEZA DE ARQUIVOS NÃO-MP4")
    print("=" * 60)
    
    base_path = r"C:\Users\dell 5557\Videos"
    
    # Limpar Carros
    print("\n📁 CARROS")
    print("-" * 60)
    limpar_local(os.path.join(base_path, "Carros"), "Carros")
    limpar_s3("Carros")
    
    # Limpar Lilo & Stitch
    print("\n📁 LILO & STITCH")
    print("-" * 60)
    limpar_local(os.path.join(base_path, "Lilo & Stitch"), "Lilo & Stitch")
    limpar_s3("Lilo & Stitch")
    
    print("\n" + "=" * 60)
    print("✅ LIMPEZA CONCLUÍDA!")
    print("=" * 60)

if __name__ == "__main__":
    confirmar = input("\n⚠️  Isso vai DELETAR arquivos MKV e outros não-MP4!\nDigite 'CONFIRMO' para continuar: ")
    
    if confirmar == 'CONFIRMO':
        main()
    else:
        print("❌ Operação cancelada")

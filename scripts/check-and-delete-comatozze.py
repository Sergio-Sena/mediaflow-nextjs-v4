import boto3
import os
from pathlib import Path

s3 = boto3.client('s3', region_name='us-east-1')
BUCKET = 'mediaflow-uploads-969430605054'
LOCAL_PATH = r'C:\Users\dell 5557\Videos\IDM\Corporativo\Comatozze'

def get_s3_files():
    """Pega todos os arquivos do S3 com tamanho"""
    s3_files = {}
    paginator = s3.get_paginator('list_objects_v2')
    
    for page in paginator.paginate(Bucket=BUCKET):
        for obj in page.get('Contents', []):
            key = obj['Key']
            size = obj['Size']
            # Extrair apenas o nome do arquivo
            filename = key.split('/')[-1].lower()
            s3_files[filename] = {'key': key, 'size': size}
    
    return s3_files

def get_local_files():
    """Pega todos os arquivos locais com tamanho"""
    local_files = []
    for root, dirs, files in os.walk(LOCAL_PATH):
        for file in files:
            full_path = os.path.join(root, file)
            size = os.path.getsize(full_path)
            local_files.append({
                'path': full_path,
                'name': file,
                'size': size
            })
    return local_files

def sanitize_for_comparison(filename):
    """Simula sanitização do upload"""
    import re
    # Remove emojis
    clean = re.sub(r'[^\x00-\x7F]+', '_', filename)
    # Remove caracteres especiais
    clean = re.sub(r'[^a-zA-Z0-9._-]', '_', clean)
    # Remove underscores duplicados
    clean = re.sub(r'_+', '_', clean)
    clean = clean.strip('_').lower()
    return clean

print("=" * 80)
print("VERIFICANDO ARQUIVOS COMATOZZE")
print("=" * 80)
print(f"Local: {LOCAL_PATH}")
print()

# Buscar arquivos
print("Buscando arquivos no S3...")
s3_files = get_s3_files()
print(f"Total S3: {len(s3_files)} arquivos")

print("\nBuscando arquivos locais...")
local_files = get_local_files()
print(f"Total Local: {len(local_files)} arquivos")

print("\n" + "=" * 80)
print("COMPARANDO ARQUIVOS")
print("=" * 80)

to_delete = []
not_found = []

for local in local_files:
    local_name = local['name']
    local_size = local['size']
    local_path = local['path']
    
    # Tentar match por nome original
    found = False
    if local_name.lower() in s3_files:
        s3_size = s3_files[local_name.lower()]['size']
        if abs(s3_size - local_size) < 1024:  # Tolerância de 1KB
            to_delete.append(local_path)
            found = True
            print(f"[MATCH] {local_name} ({local_size} bytes)")
    
    # Tentar match por nome sanitizado
    if not found:
        sanitized = sanitize_for_comparison(local_name)
        if sanitized in s3_files:
            s3_size = s3_files[sanitized]['size']
            if abs(s3_size - local_size) < 1024:
                to_delete.append(local_path)
                found = True
                print(f"[MATCH SANITIZADO] {local_name} -> {sanitized} ({local_size} bytes)")
    
    # Tentar match apenas por tamanho
    if not found:
        for s3_name, s3_data in s3_files.items():
            if abs(s3_data['size'] - local_size) < 1024:
                to_delete.append(local_path)
                found = True
                print(f"[MATCH TAMANHO] {local_name} = {s3_name} ({local_size} bytes)")
                break
    
    if not found:
        not_found.append(local_name)

print("\n" + "=" * 80)
print("RESUMO")
print("=" * 80)
print(f"Arquivos locais: {len(local_files)}")
print(f"Encontrados no S3: {len(to_delete)}")
print(f"Nao encontrados: {len(not_found)}")

if not_found:
    print("\nARQUIVOS NAO ENCONTRADOS NO S3:")
    for name in not_found[:10]:
        try:
            print(f"  - {name}")
        except:
            print(f"  - [nome com caracteres especiais]")
    if len(not_found) > 10:
        print(f"  ... e mais {len(not_found) - 10}")

if to_delete:
    print("\n" + "=" * 80)
    print("DELETAR ARQUIVOS LOCAIS?")
    print("=" * 80)
    print(f"Serao deletados {len(to_delete)} arquivos")
    resp = input("\nDigite 'SIM' para confirmar: ")
    
    if resp.upper() == 'SIM':
        deleted = 0
        for path in to_delete:
            try:
                os.remove(path)
                deleted += 1
                print(f"[DELETADO] {os.path.basename(path)}")
            except Exception as e:
                print(f"[ERRO] {os.path.basename(path)}: {e}")
        
        print(f"\n{deleted} arquivos deletados com sucesso!")
    else:
        print("\nOperacao cancelada")
else:
    print("\nNenhum arquivo para deletar")

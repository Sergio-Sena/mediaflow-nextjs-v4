# -*- coding: utf-8 -*-
import boto3
import os
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

s3 = boto3.client('s3', region_name='us-east-1')
bucket = 'mediaflow-uploads-969430605054'
paginator = s3.get_paginator('list_objects_v2')
local_path = r'C:\Users\dell 5557\Videos\IDM'
VIDEO_EXTS = ('.mp4', '.ts', '.mkv', '.avi', '.mov', '.webm')

# 1. Coletar todos os nomes de arquivos no S3
print('1. Coletando arquivos do S3...')
s3_names_exact = set()
s3_names_sanitized = set()

for page in paginator.paginate(Bucket=bucket):
    for obj in page.get('Contents', []):
        key = obj['Key']
        filename = key.split('/')[-1]
        s3_names_exact.add(filename.lower())
        # Versao sanitizada (apenas alfanumerico)
        base = filename.rsplit('.', 1)[0] if '.' in filename else filename
        sanitized = re.sub(r'[^a-z0-9]', '', base.lower())
        if sanitized:
            s3_names_sanitized.add(sanitized)

# Coletar tamanhos dos arquivos no S3
s3_sizes = set()
for page in paginator.paginate(Bucket=bucket):
    for obj in page.get('Contents', []):
        if obj['Key'].endswith(VIDEO_EXTS):
            s3_sizes.add(obj['Size'])

print(f'   S3: {len(s3_names_exact)} arquivos encontrados ({len(s3_sizes)} tamanhos unicos)')

# 2. Varrer pastas locais e comparar
print('\n2. Comparando com arquivos locais...')
total_local = 0
total_match = 0
total_pending = 0
folders_ok = []
folders_pending = []

for folder in sorted(os.listdir(local_path)):
    folder_path = os.path.join(local_path, folder)
    if not os.path.isdir(folder_path):
        continue

    local_files = []
    matched = []
    pending = []

    for root, dirs, files in os.walk(folder_path):
        for f in files:
            if f.lower().endswith(VIDEO_EXTS):
                local_files.append(os.path.join(root, f))
                
                # Comparar nome exato
                if f.lower() in s3_names_exact:
                    matched.append(os.path.join(root, f))
                    continue
                
                # Comparar com extensao .mp4 (caso .ts ja foi convertido)
                base = f.rsplit('.', 1)[0] if '.' in f else f
                mp4_name = base + '.mp4'
                if mp4_name.lower() in s3_names_exact:
                    matched.append(os.path.join(root, f))
                    continue
                
                # Comparar sanitizado
                san = re.sub(r'[^a-z0-9]', '', base.lower())
                if san and san in s3_names_sanitized:
                    matched.append(os.path.join(root, f))
                    continue
                
                # Comparar por tamanho exato
                file_size = os.path.getsize(os.path.join(root, f))
                if file_size in s3_sizes:
                    matched.append(os.path.join(root, f))
                    continue
                
                pending.append(os.path.join(root, f))

    if local_files:
        total_local += len(local_files)
        total_match += len(matched)
        total_pending += len(pending)
        
        if not pending:
            folders_ok.append((folder, len(local_files), matched))
        else:
            folders_pending.append((folder, len(local_files), len(matched), pending))

# 3. Relatorio
print(f'\n{"="*60}')
print(f'RELATORIO')
print(f'{"="*60}')
print(f'Total local:    {total_local} videos')
print(f'Ja no S3:       {total_match} (podem ser removidos)')
print(f'Pendentes:      {total_pending} (precisam tratar)')
print(f'Pastas prontas: {len(folders_ok)} (100% no S3)')
print(f'Pastas pendentes: {len(folders_pending)}')

# Pastas que podem ser deletadas inteiras
print(f'\n{"="*60}')
print(f'PASTAS 100% NO S3 (podem ser removidas):')
print(f'{"="*60}')
for folder, count, _ in folders_ok:
    print(f'  [{count:>3} arquivos] {folder}')

# Pastas com pendencias
print(f'\n{"="*60}')
print(f'PASTAS COM PENDENCIAS:')
print(f'{"="*60}')
for folder, total, matched, pending in folders_pending:
    print(f'\n  {folder} ({matched}/{total} no S3, faltam {len(pending)}):')
    for p in pending[:5]:
        print(f'    - {os.path.basename(p)}')
    if len(pending) > 5:
        print(f'    ... +{len(pending)-5} arquivos')

# 4. Perguntar se deseja remover
print(f'\n{"="*60}')
print(f'Para remover os {total_match} arquivos ja no S3, execute:')
print(f'  python scripts/compare-local-s3.py --delete')
print(f'{"="*60}')

if '--delete' in sys.argv:
    print('\n REMOVENDO arquivos ja presentes no S3...')
    removed = 0
    freed_bytes = 0
    
    for folder, count, matched_files in folders_ok:
        for f in matched_files:
            try:
                size = os.path.getsize(f)
                os.remove(f)
                removed += 1
                freed_bytes += size
            except Exception as e:
                print(f'  ERRO: {f} - {e}')
    
    for folder, total, matched_count, pending in folders_pending:
        # Re-identificar matched files nesta pasta
        folder_path = os.path.join(local_path, folder)
        for root, dirs, files in os.walk(folder_path):
            for f in files:
                full = os.path.join(root, f)
                if full in pending:
                    continue
                if f.lower().endswith(VIDEO_EXTS):
                    try:
                        size = os.path.getsize(full)
                        os.remove(full)
                        removed += 1
                        freed_bytes += size
                    except:
                        pass
    
    gb = freed_bytes / (1024**3)
    print(f'\n  Removidos: {removed} arquivos')
    print(f'  Espaco liberado: {gb:.2f} GB')
    
    # Remover pastas vazias
    empty_removed = 0
    for root, dirs, files in os.walk(local_path, topdown=False):
        if not os.listdir(root) and root != local_path:
            os.rmdir(root)
            empty_removed += 1
    print(f'  Pastas vazias removidas: {empty_removed}')

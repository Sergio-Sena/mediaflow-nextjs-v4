# -*- coding: utf-8 -*-
"""
Compara arquivos locais vs S3 e remove duplicados.
Roda direto de scripts/media/ sem precisar de cd.

Uso:
  python "c:\Projetos Git\MidiaFlow\scripts\media\compare-local-s3.py"
  python "c:\Projetos Git\MidiaFlow\scripts\media\compare-local-s3.py" --delete
"""
import boto3
import os
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

s3 = boto3.client('s3', region_name='us-east-1')
BUCKET = 'mediaflow-uploads-969430605054'
LOCAL_PATH = r'C:\Users\dell 5557\Videos\IDM'
VIDEO_EXTS = ('.mp4', '.ts', '.mkv', '.avi', '.mov', '.webm')

paginator = s3.get_paginator('list_objects_v2')
print(f'Pasta base: {LOCAL_PATH}\n')

# 1. Coletar nomes e tamanhos do S3
print('1. Coletando arquivos do S3...')
s3_names_exact = set()
s3_names_sanitized = set()
s3_sizes = set()

for page in paginator.paginate(Bucket=BUCKET):
    for obj in page.get('Contents', []):
        key = obj['Key']
        filename = key.split('/')[-1]
        s3_names_exact.add(filename.lower())
        base = filename.rsplit('.', 1)[0] if '.' in filename else filename
        sanitized = re.sub(r'[^a-z0-9]', '', base.lower())
        if sanitized:
            s3_names_sanitized.add(sanitized)
        if key.endswith(VIDEO_EXTS):
            s3_sizes.add(obj['Size'])

print(f'   S3: {len(s3_names_exact)} arquivos ({len(s3_sizes)} tamanhos unicos)')

# 2. Varrer pastas locais e comparar
print('\n2. Comparando com arquivos locais...')
total_local = 0
total_match = 0
total_pending = 0
folders_ok = []
folders_pending = []

for folder in sorted(os.listdir(LOCAL_PATH)):
    folder_path = os.path.join(LOCAL_PATH, folder)
    if not os.path.isdir(folder_path):
        continue

    local_files = []
    matched = []
    pending = []

    for root, dirs, files in os.walk(folder_path):
        for f in files:
            if f.lower().endswith(VIDEO_EXTS):
                full_path = os.path.join(root, f)
                local_files.append(full_path)

                if f.lower() in s3_names_exact:
                    matched.append(full_path)
                    continue

                base = f.rsplit('.', 1)[0] if '.' in f else f
                if (base + '.mp4').lower() in s3_names_exact:
                    matched.append(full_path)
                    continue

                san = re.sub(r'[^a-z0-9]', '', base.lower())
                if san and san in s3_names_sanitized:
                    matched.append(full_path)
                    continue

                file_size = os.path.getsize(full_path)
                if file_size in s3_sizes:
                    matched.append(full_path)
                    continue

                pending.append(full_path)

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

print(f'\n{"="*60}')
print(f'PASTAS 100% NO S3 (podem ser removidas):')
print(f'{"="*60}')
for folder, count, _ in folders_ok:
    print(f'  [{count:>3} arquivos] {folder}')

print(f'\n{"="*60}')
print(f'PASTAS COM PENDENCIAS:')
print(f'{"="*60}')
for folder, total, matched, pending in folders_pending:
    print(f'\n  {folder} ({matched}/{total} no S3, faltam {len(pending)}):')
    for p in pending[:5]:
        print(f'    - {os.path.basename(p)}')
    if len(pending) > 5:
        print(f'    ... +{len(pending)-5} arquivos')

print(f'\n{"="*60}')
print(f'Para remover os {total_match} arquivos ja no S3, execute com --delete')
print(f'{"="*60}')

if '--delete' in sys.argv:
    print('\nREMOVENDO arquivos ja presentes no S3...')
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
        folder_path = os.path.join(LOCAL_PATH, folder)
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

    empty_removed = 0
    for root, dirs, files in os.walk(LOCAL_PATH, topdown=False):
        if not os.listdir(root) and root != LOCAL_PATH:
            os.rmdir(root)
            empty_removed += 1
    print(f'  Pastas vazias removidas: {empty_removed}')

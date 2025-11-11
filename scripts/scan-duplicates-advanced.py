import boto3
from collections import defaultdict
from difflib import SequenceMatcher
import json
import re

s3 = boto3.client('s3', region_name='us-east-1')
BUCKETS = [
    'mediaflow-uploads-969430605054',
    'mediaflow-processed-969430605054'
]

def sanitize_name(name):
    """Sanitiza nome para comparacao"""
    # Remove extensao
    name_no_ext = name.rsplit('.', 1)[0] if '.' in name else name
    # Lowercase
    clean = name_no_ext.lower()
    # Remove caracteres especiais, pontuacao
    clean = re.sub(r'[^a-z0-9]', '', clean)
    return clean

def similar(a, b):
    return SequenceMatcher(None, a.lower(), b.lower()).ratio()

def get_all_files():
    """Lista TODOS os arquivos de TODOS os buckets"""
    files = []
    paginator = s3.get_paginator('list_objects_v2')
    
    for bucket in BUCKETS:
        print(f"\nEscaneando bucket: {bucket}")
        count = 0
        
        try:
            for page in paginator.paginate(Bucket=bucket):
                for obj in page.get('Contents', []):
                    if obj['Key'].endswith('/'):
                        continue
                    
                    name = obj['Key'].split('/')[-1]
                    files.append({
                        'bucket': bucket,
                        'key': obj['Key'],
                        'name': name,
                        'sanitized': sanitize_name(name),
                        'size': obj['Size'],
                        'modified': obj['LastModified']
                    })
                    count += 1
                    if count % 100 == 0:
                        print(f"  {count} arquivos...")
            print(f"  Total: {count} arquivos")
        except Exception as e:
            print(f"  Erro: {e}")
    
    return files

print("="*80)
print("ESCANEAMENTO AVANCADO DE DUPLICADOS")
print("="*80)

files = get_all_files()
print(f"\nTotal de arquivos: {len(files)}")

# 1. Duplicados por nome EXATO
print("\n1. Buscando nomes exatos...")
by_name = defaultdict(list)
for f in files:
    by_name[f['name'].lower()].append(f)

duplicates_exact = []
for name, file_list in by_name.items():
    if len(file_list) > 1:
        for i, f1 in enumerate(file_list):
            for f2 in file_list[i+1:]:
                duplicates_exact.append({
                    'file1': f1,
                    'file2': f2,
                    'type': 'exact_name',
                    'match': 'Nome exato'
                })

# 2. Duplicados por nome SANITIZADO
print("2. Buscando nomes sanitizados...")
by_sanitized = defaultdict(list)
for f in files:
    if f['sanitized']:  # Ignorar vazios
        by_sanitized[f['sanitized']].append(f)

duplicates_sanitized = []
checked = set()
for sanitized, file_list in by_sanitized.items():
    if len(file_list) > 1:
        for i, f1 in enumerate(file_list):
            for f2 in file_list[i+1:]:
                pair = tuple(sorted([f1['key'], f2['key']]))
                if pair not in checked:
                    checked.add(pair)
                    # Nao adicionar se ja esta em exact
                    if f1['name'].lower() != f2['name'].lower():
                        duplicates_sanitized.append({
                            'file1': f1,
                            'file2': f2,
                            'type': 'sanitized_name',
                            'match': 'Nome sanitizado'
                        })

# 3. Duplicados por TAMANHO exato
print("3. Buscando tamanhos exatos...")
by_size = defaultdict(list)
for f in files:
    by_size[f['size']].append(f)

duplicates_size = []
checked = set()
for size, file_list in by_size.items():
    if len(file_list) > 1 and size > 1024*1024:  # Apenas > 1MB
        for i, f1 in enumerate(file_list):
            for f2 in file_list[i+1:]:
                pair = tuple(sorted([f1['key'], f2['key']]))
                if pair not in checked:
                    checked.add(pair)
                    similarity = similar(f1['name'], f2['name'])
                    if similarity > 0.7:
                        duplicates_size.append({
                            'file1': f1,
                            'file2': f2,
                            'similarity': similarity,
                            'type': 'same_size_similar_name',
                            'match': f'Tamanho igual + {similarity*100:.0f}% similar'
                        })

duplicates = duplicates_exact + duplicates_sanitized + duplicates_size

print(f"\nDuplicados por nome exato: {len(duplicates_exact)}")
print(f"Duplicados por nome sanitizado: {len(duplicates_sanitized)}")
print(f"Duplicados por tamanho + nome similar: {len(duplicates_size)}")
print(f"Total: {len(duplicates)}")

# Salvar relatorios
with open('duplicados_avancado.json', 'w', encoding='utf-8') as f:
    json.dump(duplicates, f, indent=2, default=str)

with open('duplicados_avancado.txt', 'w', encoding='utf-8') as f:
    f.write("RELATORIO AVANCADO DE DUPLICADOS\n")
    f.write("="*80 + "\n\n")
    f.write(f"Total de arquivos: {len(files)}\n")
    f.write(f"Duplicados nome exato: {len(duplicates_exact)}\n")
    f.write(f"Duplicados nome sanitizado: {len(duplicates_sanitized)}\n")
    f.write(f"Duplicados tamanho + similar: {len(duplicates_size)}\n")
    f.write(f"Total: {len(duplicates)}\n\n")
    f.write("="*80 + "\n\n")
    
    if duplicates_exact:
        f.write("### 1. NOME EXATO ###\n\n")
        for i, dup in enumerate(duplicates_exact, 1):
            s1 = dup['file1']['size']/(1024**2)
            s2 = dup['file2']['size']/(1024**2)
            f.write(f"[{i}] {dup['file1']['name']}\n")
            f.write(f"  1: {dup['file1']['key']} ({s1:.1f} MB)\n")
            f.write(f"  2: {dup['file2']['key']} ({s2:.1f} MB)\n")
            if abs(s1 - s2) > 0.1:
                f.write(f"  TAMANHOS DIFERENTES: {abs(s1-s2):.1f} MB\n")
            f.write("\n")
    
    if duplicates_sanitized:
        f.write("\n### 2. NOME SANITIZADO (sem acentos/espacos) ###\n\n")
        for i, dup in enumerate(duplicates_sanitized, 1):
            s1 = dup['file1']['size']/(1024**2)
            s2 = dup['file2']['size']/(1024**2)
            f.write(f"[{i}] Sanitizado: {dup['file1']['sanitized']}\n")
            f.write(f"  1: {dup['file1']['name']} ({s1:.1f} MB)\n")
            f.write(f"     {dup['file1']['key']}\n")
            f.write(f"  2: {dup['file2']['name']} ({s2:.1f} MB)\n")
            f.write(f"     {dup['file2']['key']}\n")
            if abs(s1 - s2) > 0.1:
                f.write(f"  TAMANHOS DIFERENTES: {abs(s1-s2):.1f} MB\n")
            f.write("\n")
    
    if duplicates_size:
        f.write("\n### 3. TAMANHO IGUAL + NOME SIMILAR ###\n\n")
        for i, dup in enumerate(duplicates_size, 1):
            s = dup['file1']['size']/(1024**2)
            sim = dup.get('similarity', 0) * 100
            f.write(f"[{i}] Tamanho: {s:.1f} MB | Similaridade: {sim:.0f}%\n")
            f.write(f"  1: {dup['file1']['name']}\n")
            f.write(f"     {dup['file1']['key']}\n")
            f.write(f"  2: {dup['file2']['name']}\n")
            f.write(f"     {dup['file2']['key']}\n\n")

# Estatisticas
total_size = sum(f['size'] for f in files)
duplicate_size = sum(max(d['file1']['size'], d['file2']['size']) for d in duplicates)

print("\n" + "="*80)
print("ESTATISTICAS")
print("="*80)
print(f"Total de arquivos: {len(files)}")
print(f"Tamanho total: {total_size/(1024**3):.2f} GB")
print(f"Duplicados: {len(duplicates)}")
print(f"Espaco desperdicado: {duplicate_size/(1024**3):.2f} GB")
print(f"\nRelatorios salvos:")
print(f"  - duplicados_avancado.txt")
print(f"  - duplicados_avancado.json")
print("="*80)

import boto3
from collections import defaultdict
from difflib import SequenceMatcher
import json

s3 = boto3.client('s3', region_name='us-east-1')
BUCKETS = [
    'mediaflow-uploads-969430605054',
    'mediaflow-processed-969430605054'
]

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
                    
                    files.append({
                        'bucket': bucket,
                        'key': obj['Key'],
                        'name': obj['Key'].split('/')[-1],
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
print("ESCANEAMENTO COMPLETO DE DUPLICADOS")
print("="*80)

files = get_all_files()
print(f"\nTotal de arquivos: {len(files)}")

# Agrupar por tamanho
by_size = defaultdict(list)
for f in files:
    by_size[f['size']].append(f)

# Encontrar duplicados por nome exato
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
                    'similarity': 100.0,
                    'type': 'exact_name'
                })

# Encontrar duplicados por tamanho + nome similar
duplicates_similar = []
checked = set()

for size, file_list in by_size.items():
    if len(file_list) > 1:
        for i, f1 in enumerate(file_list):
            for f2 in file_list[i+1:]:
                pair_key = tuple(sorted([f1['key'], f2['key']]))
                if pair_key in checked:
                    continue
                checked.add(pair_key)
                
                similarity = similar(f1['name'], f2['name'])
                if similarity > 0.7 and similarity < 1.0:  # 70-99% similar
                    duplicates_similar.append({
                        'file1': f1,
                        'file2': f2,
                        'similarity': similarity,
                        'type': 'similar_name_same_size'
                    })

duplicates = duplicates_exact + duplicates_similar

print(f"\nDuplicados por nome exato: {len(duplicates_exact)}")
print(f"Duplicados por nome similar + tamanho: {len(duplicates_similar)}")
print(f"Total de duplicados: {len(duplicates)}")

# Salvar relatorio completo
with open('duplicados_completo.json', 'w', encoding='utf-8') as f:
    json.dump(duplicates, f, indent=2, default=str)

with open('duplicados_completo.txt', 'w', encoding='utf-8') as f:
    f.write("RELATORIO COMPLETO DE DUPLICADOS\n")
    f.write("="*80 + "\n\n")
    f.write(f"Total de arquivos escaneados: {len(files)}\n")
    f.write(f"Duplicados por nome exato: {len(duplicates_exact)}\n")
    f.write(f"Duplicados por nome similar: {len(duplicates_similar)}\n")
    f.write(f"Total: {len(duplicates)}\n\n")
    f.write("="*80 + "\n\n")
    
    if duplicates_exact:
        f.write("### DUPLICADOS POR NOME EXATO (100%) ###\n\n")
        for i, dup in enumerate(duplicates_exact, 1):
            size1 = dup['file1']['size']/(1024**2)
            size2 = dup['file2']['size']/(1024**2)
            f.write(f"[{i}] Nome: {dup['file1']['name']}\n")
            f.write(f"  1: [{dup['file1']['bucket']}] {dup['file1']['key']} ({size1:.1f} MB)\n")
            f.write(f"  2: [{dup['file2']['bucket']}] {dup['file2']['key']} ({size2:.1f} MB)\n")
            if size1 != size2:
                f.write(f"  ⚠️  TAMANHOS DIFERENTES! Diferenca: {abs(size1-size2):.1f} MB\n")
            f.write("\n")
    
    if duplicates_similar:
        f.write("\n### DUPLICADOS POR NOME SIMILAR (70-99%) ###\n\n")
        for i, dup in enumerate(duplicates_similar, 1):
            f.write(f"[{i}] Similaridade: {dup['similarity']*100:.1f}% | Tamanho: {dup['file1']['size']/(1024**2):.1f} MB\n")
            f.write(f"  1: [{dup['file1']['bucket']}] {dup['file1']['key']}\n")
            f.write(f"  2: [{dup['file2']['bucket']}] {dup['file2']['key']}\n\n")

# Estatisticas
total_size = sum(f['size'] for f in files)
duplicate_size_exact = sum(max(dup['file1']['size'], dup['file2']['size']) for dup in duplicates_exact)
duplicate_size_similar = sum(dup['file1']['size'] for dup in duplicates_similar)
duplicate_size = duplicate_size_exact + duplicate_size_similar

print("\n" + "="*80)
print("ESTATISTICAS")
print("="*80)
print(f"Total de arquivos: {len(files)}")
print(f"Tamanho total: {total_size/(1024**3):.2f} GB")
print(f"Duplicados nome exato: {len(duplicates_exact)}")
print(f"Duplicados nome similar: {len(duplicates_similar)}")
print(f"Total duplicados: {len(duplicates)}")
print(f"Espaco desperdicado: {duplicate_size/(1024**3):.2f} GB")
print(f"\nRelatorios salvos:")
print(f"  - duplicados_completo.txt (legivel)")
print(f"  - duplicados_completo.json (processavel)")
print("="*80)

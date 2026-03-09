import boto3
from collections import defaultdict
from difflib import SequenceMatcher

s3 = boto3.client('s3', region_name='us-east-1')
BUCKET = 'mediaflow-uploads-969430605054'
PREFIX = 'users/user_admin/'

def similar(a, b):
    """Verifica similaridade entre nomes"""
    return SequenceMatcher(None, a.lower(), b.lower()).ratio()

def get_all_files():
    """Lista todos os arquivos do admin com metadados"""
    files = []
    paginator = s3.get_paginator('list_objects_v2')
    
    print("Buscando arquivos no S3...")
    for page in paginator.paginate(Bucket=BUCKET, Prefix=PREFIX):
        for obj in page.get('Contents', []):
            if obj['Key'].endswith('/'):
                continue
            
            files.append({
                'key': obj['Key'],
                'name': obj['Key'].split('/')[-1],
                'size': obj['Size'],
                'modified': obj['LastModified']
            })
    
    return files

print("="*80)
print("BUSCANDO DUPLICADOS EM users/user_admin/")
print("="*80)

files = get_all_files()
print(f"\nTotal de arquivos: {len(files)}")

# Agrupar por tamanho
by_size = defaultdict(list)
for f in files:
    by_size[f['size']].append(f)

# Encontrar duplicados exatos (mesmo tamanho)
duplicates_exact = []
for size, file_list in by_size.items():
    if len(file_list) > 1:
        duplicates_exact.append((size, file_list))

print(f"\nArquivos com mesmo tamanho: {len(duplicates_exact)} grupos")

# Encontrar duplicados similares (nome parecido + mesmo tamanho)
duplicates_similar = []
for size, file_list in duplicates_exact:
    for i, f1 in enumerate(file_list):
        for f2 in file_list[i+1:]:
            similarity = similar(f1['name'], f2['name'])
            if similarity > 0.7:  # 70% similar
                duplicates_similar.append({
                    'file1': f1,
                    'file2': f2,
                    'similarity': similarity,
                    'size': size
                })

print(f"Duplicados similares encontrados: {len(duplicates_similar)}")

if duplicates_similar:
    print("\n" + "="*80)
    print("DUPLICADOS ENCONTRADOS")
    print("="*80)
    
    for i, dup in enumerate(duplicates_similar[:50], 1):  # Mostrar primeiros 50
        print(f"\n[{i}] Similaridade: {dup['similarity']*100:.1f}% | Tamanho: {dup['size']/(1024**2):.1f} MB")
        print(f"  1: {dup['file1']['name']}")
        print(f"     {dup['file1']['key']}")
        print(f"  2: {dup['file2']['name']}")
        print(f"     {dup['file2']['key']}")
    
    if len(duplicates_similar) > 50:
        print(f"\n... e mais {len(duplicates_similar) - 50} duplicados")
    
    # Salvar relatorio
    with open('duplicados_admin.txt', 'w', encoding='utf-8') as f:
        f.write("DUPLICADOS EM users/user_admin/\n")
        f.write("="*80 + "\n\n")
        
        for i, dup in enumerate(duplicates_similar, 1):
            f.write(f"[{i}] Similaridade: {dup['similarity']*100:.1f}% | Tamanho: {dup['size']/(1024**2):.1f} MB\n")
            f.write(f"  1: {dup['file1']['key']}\n")
            f.write(f"  2: {dup['file2']['key']}\n\n")
    
    print("\n" + "="*80)
    print(f"Relatorio salvo em: duplicados_admin.txt")
    print("="*80)
else:
    print("\nNenhum duplicado encontrado!")

# Estatisticas
total_size = sum(f['size'] for f in files)
duplicate_size = sum(dup['size'] for dup in duplicates_similar)

print(f"\nEstatisticas:")
print(f"  Total de arquivos: {len(files)}")
print(f"  Tamanho total: {total_size/(1024**3):.2f} GB")
print(f"  Duplicados: {len(duplicates_similar)}")
print(f"  Espaco desperdicado: {duplicate_size/(1024**3):.2f} GB")

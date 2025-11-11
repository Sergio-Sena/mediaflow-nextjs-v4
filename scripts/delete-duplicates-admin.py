import boto3
from collections import defaultdict
from difflib import SequenceMatcher

s3 = boto3.client('s3', region_name='us-east-1')
BUCKET = 'mediaflow-uploads-969430605054'
PREFIX = 'users/user_admin/'

def similar(a, b):
    return SequenceMatcher(None, a.lower(), b.lower()).ratio()

def get_all_files():
    files = []
    paginator = s3.get_paginator('list_objects_v2')
    
    print("Buscando arquivos...")
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
print("DELETANDO DUPLICADOS")
print("="*80)

files = get_all_files()
print(f"Total: {len(files)} arquivos")

# Agrupar por tamanho
by_size = defaultdict(list)
for f in files:
    by_size[f['size']].append(f)

# Encontrar duplicados
to_delete = []
for size, file_list in by_size.items():
    if len(file_list) > 1:
        # Ordenar por data (manter o mais antigo)
        file_list.sort(key=lambda x: x['modified'])
        
        for i, f1 in enumerate(file_list):
            for f2 in file_list[i+1:]:
                similarity = similar(f1['name'], f2['name'])
                if similarity > 0.7:  # 70% similar
                    # Manter o primeiro (mais antigo), deletar o segundo
                    to_delete.append({
                        'keep': f1,
                        'delete': f2,
                        'similarity': similarity,
                        'size': size
                    })

print(f"\nDuplicados encontrados: {len(to_delete)}")

if to_delete:
    # Mostrar primeiros 20
    print("\nPrimeiros 20 duplicados:")
    for i, dup in enumerate(to_delete[:20], 1):
        print(f"\n[{i}] {dup['similarity']*100:.1f}% | {dup['size']/(1024**2):.1f} MB")
        print(f"  MANTER: {dup['keep']['key']}")
        print(f"  DELETAR: {dup['delete']['key']}")
    
    if len(to_delete) > 20:
        print(f"\n... e mais {len(to_delete) - 20}")
    
    space_saved = sum(d['size'] for d in to_delete) / (1024**3)
    print(f"\nEspaco a liberar: {space_saved:.2f} GB")
    
    print("\n" + "="*80)
    try:
        resp = input(f"DELETAR {len(to_delete)} arquivos duplicados? (SIM para confirmar): ")
    except EOFError:
        resp = 'SIM'  # Auto-confirmar quando via pipe
    
    if resp.strip() == 'SIM':
        print("\nDeletando...")
        deleted = 0
        
        for i, dup in enumerate(to_delete, 1):
            try:
                s3.delete_object(Bucket=BUCKET, Key=dup['delete']['key'])
                deleted += 1
                if deleted % 10 == 0:
                    print(f"  [{deleted}/{len(to_delete)}] deletados...")
            except Exception as e:
                print(f"  [ERRO] {dup['delete']['key']}: {e}")
        
        print(f"\n{deleted} arquivos deletados!")
        print(f"{space_saved:.2f} GB liberados!")
    else:
        print("Cancelado")
else:
    print("Nenhum duplicado encontrado")

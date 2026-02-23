import boto3
from collections import defaultdict

s3 = boto3.client('s3')
bucket = 'mediaflow-uploads-969430605054'

print("=" * 80)
print("MAPEAMENTO COMPLETO DO BUCKET")
print("=" * 80)

# Listar TODAS as pastas de primeiro nível
print("\n[1/2] Listando estrutura raiz...")
response = s3.list_objects_v2(Bucket=bucket, Delimiter='/', MaxKeys=1000)

root_folders = []
if 'CommonPrefixes' in response:
    for prefix in response['CommonPrefixes']:
        folder = prefix['Prefix'].rstrip('/')
        root_folders.append(folder)
        print(f"  - {folder}/")

print(f"\n[OK] Total de pastas na raiz: {len(root_folders)}")

# Contar arquivos em cada pasta
print("\n[2/2] Contando arquivos por pasta...")
for folder in root_folders:
    try:
        response = s3.list_objects_v2(Bucket=bucket, Prefix=f'{folder}/', MaxKeys=1000)
        count = response.get('KeyCount', 0)
        
        # Calcular tamanho
        total_size = sum(obj['Size'] for obj in response.get('Contents', []))
        size_gb = total_size / (1024 * 1024 * 1024)
        
        print(f"\n{folder}/")
        print(f"  Arquivos: {count}")
        print(f"  Tamanho: {size_gb:.2f} GB")
        
        # Listar subpastas
        if count > 0:
            subfolders = set()
            for obj in response.get('Contents', [])[:100]:
                parts = obj['Key'].replace(f'{folder}/', '').split('/')
                if len(parts) > 1:
                    subfolders.add(parts[0])
            
            if subfolders:
                print(f"  Subpastas: {', '.join(sorted(list(subfolders))[:10])}")
                if len(subfolders) > 10:
                    print(f"             ... e mais {len(subfolders) - 10}")
        
    except Exception as e:
        print(f"  [ERRO] {e}")

print("\n" + "=" * 80)
print("MAPEAMENTO CONCLUIDO")
print("=" * 80)

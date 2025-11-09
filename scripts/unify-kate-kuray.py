import boto3

s3 = boto3.client('s3', region_name='us-east-1')
BUCKET = 'mediaflow-uploads-969430605054'

# Listar todas as pastas kate kuray
folders = [
    'users/user_admin/Star/Kate kuray/',
    'users/user_admin/Star/kate kuray/',
    'users/user_admin/Star/kate_kuray/'
]

dest_folder = 'users/user_admin/Star/Kate kuray/'

# Coletar todos os arquivos
all_files = {}
for folder in folders:
    paginator = s3.get_paginator('list_objects_v2')
    for page in paginator.paginate(Bucket=BUCKET, Prefix=folder):
        for obj in page.get('Contents', []):
            key = obj['Key']
            filename = key.split('/')[-1]
            size = obj['Size']
            
            # Usar nome + tamanho como chave unica
            unique_key = f"{filename}_{size}"
            
            if unique_key not in all_files:
                all_files[unique_key] = {
                    'filename': filename,
                    'size': size,
                    'source': key,
                    'folder': folder
                }

print(f'Total de arquivos unicos: {len(all_files)}')
print('=' * 70)

# Mover/copiar para Kate kuray/ e deletar duplicados
moved = 0
deleted = 0

for unique_key, file_info in all_files.items():
    source = file_info['source']
    dest = dest_folder + file_info['filename']
    
    # Se ja esta na pasta correta, pular
    if source == dest:
        print(f'[SKIP] {file_info["filename"]} (ja na pasta correta)')
        continue
    
    # Verificar se destino ja existe
    try:
        s3.head_object(Bucket=BUCKET, Key=dest)
        # Destino existe, deletar source
        s3.delete_object(Bucket=BUCKET, Key=source)
        deleted += 1
        print(f'[DEL] {file_info["filename"]} (duplicado)')
    except:
        # Destino nao existe, copiar e deletar source
        s3.copy_object(
            Bucket=BUCKET,
            CopySource={'Bucket': BUCKET, 'Key': source},
            Key=dest
        )
        s3.delete_object(Bucket=BUCKET, Key=source)
        moved += 1
        print(f'[MOVE] {file_info["filename"]}')

print('=' * 70)
print(f'Arquivos movidos: {moved}')
print(f'Duplicados deletados: {deleted}')
print(f'Total unificado em Kate kuray/: {len(all_files)}')

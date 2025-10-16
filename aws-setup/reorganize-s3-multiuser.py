import boto3
import time
import sys

s3 = boto3.client('s3')
BUCKET = 'mediaflow-uploads-969430605054'

print('Iniciando reorganizacao S3 para multi-usuario...\n')

# Criar estrutura users/
print('Criando estrutura users/')
s3.put_object(Bucket=BUCKET, Key='users/')
s3.put_object(Bucket=BUCKET, Key='users/user_admin/')
s3.put_object(Bucket=BUCKET, Key='users/user_joao/')
s3.put_object(Bucket=BUCKET, Key='users/user_maria/')
print('OK - Estrutura criada\n')

# Pastas a mover para user_admin
folders = ['Anime', 'Star', 'Lara_Croft', 'Seart', 'Video', 'Fotos', 'Documentos', 'raiz']

total_moved = 0

for folder in folders:
    print(f'\nMovendo {folder}/ para users/user_admin/{folder}/')
    
    try:
        # Contar total primeiro
        paginator = s3.get_paginator('list_objects_v2')
        pages = paginator.paginate(Bucket=BUCKET, Prefix=f'{folder}/')
        
        total_files = 0
        for page in pages:
            if 'Contents' in page:
                for obj in page['Contents']:
                    if not obj['Key'].startswith('users/'):
                        total_files += 1
        
        if total_files == 0:
            print(f'  Nenhum arquivo em {folder}/')
            continue
        
        print(f'  Total: {total_files} arquivos')
        
        # Mover com porcentagem
        paginator = s3.get_paginator('list_objects_v2')
        pages = paginator.paginate(Bucket=BUCKET, Prefix=f'{folder}/')
        
        folder_count = 0
        for page in pages:
            if 'Contents' not in page:
                continue
                
            for obj in page['Contents']:
                key = obj['Key']
                
                # Pular se ja esta em users/
                if key.startswith('users/'):
                    continue
                
                new_key = f"users/user_admin/{key}"
                
                # Copiar
                s3.copy_object(
                    Bucket=BUCKET,
                    CopySource={'Bucket': BUCKET, 'Key': key},
                    Key=new_key
                )
                
                # Deletar original
                s3.delete_object(Bucket=BUCKET, Key=key)
                
                folder_count += 1
                total_moved += 1
                
                # Mostrar porcentagem
                percent = int((folder_count / total_files) * 100)
                sys.stdout.write(f'\r  Progresso: {percent}% ({folder_count}/{total_files})')
                sys.stdout.flush()
        
        print(f'\n  OK - {folder_count} arquivos movidos')
        
    except Exception as e:
        print(f'\n  ERRO em {folder}: {str(e)}')

print(f'\nReorganizacao concluida!')
print(f'Total: {total_moved} arquivos movidos para users/user_admin/')
print(f'\nEstrutura final:')
print(f'   users/user_admin/ - Todo conteúdo atual')
print(f'   users/user_joao/  - Vazio (pronto para uso)')
print(f'   users/user_maria/ - Vazio (pronto para uso)')

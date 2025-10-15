import boto3
import os

s3 = boto3.client('s3')
bucket = 'mediaflow-uploads-969430605054'
local_path = r"C:\Users\dell 5557\Videos\IDM\Anime"

print("RENOMEANDO ARQUIVOS TRUNCADOS NO S3")
print("=" * 40)

# Mapear arquivos locais
local_files = {}
for root, dirs, files in os.walk(local_path):
    folder = os.path.basename(root)
    if folder != "Anime":
        for file in files:
            if file.endswith('.mp4'):
                local_files[folder] = local_files.get(folder, [])
                local_files[folder].append(file)

# Listar arquivos S3
response = s3.list_objects_v2(Bucket=bucket, Prefix='Anime/')
s3_files = []

if 'Contents' in response:
    for obj in response['Contents']:
        if obj['Key'].endswith('.mp4'):
            s3_files.append({
                'key': obj['Key'],
                'size': obj['Size']
            })

# Encontrar e renomear truncados
renamed = 0
for s3_file in s3_files:
    if '....' in s3_file['key']:
        parts = s3_file['key'].split('/')
        if len(parts) >= 3:
            folder = parts[1]
            truncated_name = parts[2]
            
            # Procurar arquivo local correspondente por tamanho
            if folder in local_files:
                for local_file in local_files[folder]:
                    local_full_path = None
                    for root, dirs, files in os.walk(local_path):
                        if os.path.basename(root) == folder and local_file in files:
                            local_full_path = os.path.join(root, local_file)
                            break
                    
                    if local_full_path and os.path.getsize(local_full_path) == s3_file['size']:
                        new_key = f"Anime/{folder}/{local_file}"
                        
                        # Verificar se já existe
                        try:
                            s3.head_object(Bucket=bucket, Key=new_key)
                            print(f"JA EXISTE: {new_key}")
                            continue
                        except:
                            pass
                        
                        print(f"RENOMEAR:")
                        print(f"  De: {s3_file['key']}")
                        print(f"  Para: {new_key}")
                        
                        # Copiar com novo nome
                        s3.copy_object(
                            Bucket=bucket,
                            CopySource={'Bucket': bucket, 'Key': s3_file['key']},
                            Key=new_key
                        )
                        
                        # Deletar antigo
                        s3.delete_object(Bucket=bucket, Key=s3_file['key'])
                        
                        renamed += 1
                        break

print(f"\nCONCLUIDO: {renamed} arquivos renomeados")
import boto3
import os
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm

s3 = boto3.client('s3')
bucket = 'mediaflow-uploads-969430605054'
local_path = r'C:\Users\dell 5557\Videos\Star'
s3_prefix = 'users/sergio_sena/Star'

def upload_file(file_path, s3_key):
    try:
        s3.upload_file(file_path, bucket, s3_key)
        return True
    except Exception as e:
        return False

# Listar arquivos
files_to_upload = []
for root, dirs, files in os.walk(local_path):
    for file in files:
        if file.endswith('.mp4'):
            file_path = os.path.join(root, file)
            rel_path = os.path.relpath(file_path, local_path)
            s3_key = f'{s3_prefix}/{rel_path}'.replace('\\', '/')
            files_to_upload.append((file_path, s3_key))

print(f'Iniciando upload de {len(files_to_upload)} arquivos...')

# Upload paralelo (10 threads)
with ThreadPoolExecutor(max_workers=10) as executor:
    futures = [executor.submit(upload_file, fp, sk) for fp, sk in files_to_upload]
    for _ in tqdm(as_completed(futures), total=len(files_to_upload), desc='Upload'):
        pass

print('Upload concluido!')

# Renomear pasta emillya_Bunny para Emillya_Bunny
print('Renomeando pasta emillya_Bunny para Emillya_Bunny...')

response = s3.list_objects_v2(Bucket=bucket, Prefix=f'{s3_prefix}/emillya_Bunny/')

if 'Contents' in response:
    for obj in tqdm(response['Contents'], desc='Renomeando'):
        old_key = obj['Key']
        new_key = old_key.replace('/emillya_Bunny/', '/Emillya_Bunny/')
        
        s3.copy_object(
            Bucket=bucket,
            CopySource={'Bucket': bucket, 'Key': old_key},
            Key=new_key
        )
        s3.delete_object(Bucket=bucket, Key=old_key)

print('Concluido!')

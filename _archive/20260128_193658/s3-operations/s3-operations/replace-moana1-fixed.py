import boto3
import os
from tqdm import tqdm

s3 = boto3.client('s3', region_name='us-east-1')
bucket = 'mediaflow-uploads-969430605054'

local_file = r'C:\Users\dell 5557\Videos\Moana.Um.Mar.de.Aventuras\Moana.1.Um.Mar.de.Aventuras.2017.mp4'
s3_key = 'users/lid_lima/Moana/Moana.1.Um.Mar.de.Aventuras.2017.mp4'

if not os.path.exists(local_file):
    print(f"ERRO: Arquivo nao encontrado: {local_file}")
    exit(1)

file_size = os.path.getsize(local_file)
print(f"Arquivo: {local_file}")
print(f"Tamanho: {file_size / (1024**3):.2f} GB")
print(f"Destino S3: {s3_key}")
print("\nDeletando arquivo antigo...")

s3.delete_object(Bucket=bucket, Key=s3_key)
print("Deletado!")

print("\nUpload do arquivo corrigido...")
with tqdm(total=file_size, unit='B', unit_scale=True) as pbar:
    s3.upload_file(
        local_file,
        bucket,
        s3_key,
        Callback=lambda bytes: pbar.update(bytes)
    )

print("\nConcluido! Arquivo substituido com sucesso.")

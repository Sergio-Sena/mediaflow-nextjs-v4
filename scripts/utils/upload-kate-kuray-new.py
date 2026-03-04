import boto3
import os
from pathlib import Path

s3 = boto3.client('s3')
bucket = 'mediaflow-uploads-969430605054'
s3_prefix = 'users/sergio_sena/Star/Kate Kuray/'
local_folder = r"C:\Users\dell 5557\Videos\IDM\Star\Kate Kuray"

print("=" * 80)
print("UPLOAD DE ARQUIVOS NOVOS")
print("=" * 80)

arquivos_novos = [
    "delicious busty swallowing cock (1080).mp4",
    "fucks her pussy with a dildo (1080).mp4",
    "gogo dancer sat on a hard cock (1080).mp4",
    "k4te kur4y amateur sex 5 (1080).mp4",
    "kate kuray - ahegao (1080).mp4",
    "kate kuray - foxy (1080).mp4",
    "kate kuray fuck 10 (1080).mp4",
    "kate kuray halloween video (1080).mp4",
    "kate kuray, a creampie a day keeps boredom at bay (1080).mp4",
    "kinky fun under mask (1080).mp4",
    "pop your balloons in my mouth, 4k (onlythe top) (1080).mp4"
]

uploaded = 0
errors = 0

for i, filename in enumerate(arquivos_novos, 1):
    local_path = os.path.join(local_folder, filename)
    s3_key = s3_prefix + filename
    
    if not os.path.exists(local_path):
        print(f"\n[{i}/11] [ERRO] Arquivo nao encontrado: {filename}")
        errors += 1
        continue
    
    file_size = os.path.getsize(local_path) / (1024 * 1024)
    print(f"\n[{i}/11] Uploading: {filename} ({file_size:.2f} MB)")
    
    try:
        s3.upload_file(
            local_path,
            bucket,
            s3_key,
            Callback=lambda bytes_transferred: None
        )
        uploaded += 1
        print(f"  [OK] Upload concluido")
    except Exception as e:
        print(f"  [ERRO] {e}")
        errors += 1

print("\n" + "=" * 80)
print(f"CONCLUIDO: {uploaded} uploads, {errors} erros")
print("=" * 80)

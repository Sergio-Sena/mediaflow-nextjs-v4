import boto3
import os

s3 = boto3.client('s3')
bucket = 'mediaflow-uploads-969430605054'
s3_prefix = 'users/sergio_sena/Star/Kate Kuray/'
local_folder = r"C:\Users\dell 5557\Videos\IDM\Star\Kate Kuray"

print("=" * 80)
print("COMPARANDO ARQUIVOS LOCAIS vs S3")
print("=" * 80)

# Listar arquivos no S3
print("\n[1/3] Listando arquivos no S3...")
try:
    response = s3.list_objects_v2(Bucket=bucket, Prefix=s3_prefix, MaxKeys=1000)
    s3_files = {}
    for obj in response.get('Contents', []):
        filename = obj['Key'].split('/')[-1]
        s3_files[filename.lower()] = obj['Size']
    
    print(f"[OK] {len(s3_files)} arquivos no S3")
except Exception as e:
    print(f"[ERRO] {e}")
    s3_files = {}

# Listar arquivos locais
print("\n[2/3] Listando arquivos locais...")
local_files = {}
for filename in os.listdir(local_folder):
    if filename.endswith('.mp4'):
        filepath = os.path.join(local_folder, filename)
        size = os.path.getsize(filepath)
        local_files[filename.lower()] = size

print(f"[OK] {len(local_files)} arquivos locais")

# Comparar
print("\n[3/3] Comparando...")

print("\n--- ARQUIVOS NOVOS (nao estao no S3) ---")
novos = []
for filename in local_files:
    if filename not in s3_files:
        novos.append(filename)
        print(f"  [NOVO] {filename}")

if not novos:
    print("  Nenhum arquivo novo")

print("\n--- ARQUIVOS JA EXISTENTES ---")
existentes = []
for filename in local_files:
    if filename in s3_files:
        existentes.append(filename)
        print(f"  [OK] {filename}")

print("\n" + "=" * 80)
print(f"RESUMO: {len(novos)} novos, {len(existentes)} ja existem")
print("=" * 80)

import boto3
import os
from pathlib import Path

s3 = boto3.client('s3', region_name='us-east-1')
BUCKET = 'mediaflow-uploads-969430605054'
DOWNLOAD_DIR = r'C:\Users\dell 5557\Videos\IDM\arquivos TS'

# Lista de arquivos .ts para download
TS_FILES = [
    'users/sergio_sena/Corporativo/Creamy_Spot/Voc_Pode_Ver_Dentro_Da_Minh....ts',
    'users/sergio_sena/Corporativo/Lisinha/BRANQUINHA_AMADORA_ABRE_a_BUCET....ts',
    'users/sergio_sena/Corporativo/Lisinha/Brincando_com_a_Bucetinha_Apert....ts',
    'users/sergio_sena/Corporativo/Lisinha/Cindel_Sozinha_Em_Casa_Fodendo_....ts',
    'users/sergio_sena/Corporativo/Lisinha/Garota_De_18_Anos_que_Nunca_Tra....ts',
    'users/sergio_sena/Corporativo/Lisinha/Que_Tal_Voc_Pagar_o_Aluguel_com....ts',
    'users/sergio_sena/Corporativo/Lisinha/Universit_ria_Gostosa_com_Uma_B....ts',
    'users/sergio_sena/Corporativo/Lisinha/cindel_Voce_Quer_Chupar_Essa_Bu....ts',
    'users/sergio_sena/Corporativo/angel/Garota_Perfeita_Fodida_no_Ho....ts'
]

# Criar diretório se não existir
Path(DOWNLOAD_DIR).mkdir(parents=True, exist_ok=True)

print(f"[INFO] Baixando {len(TS_FILES)} arquivos .ts")
print(f"[INFO] Destino: {DOWNLOAD_DIR}\n")

downloaded = 0
failed = 0

def progress_callback(bytes_transferred):
    mb_transferred = bytes_transferred / (1024 * 1024)
    print(f"\r  Progresso: {mb_transferred:.2f} MB", end='', flush=True)

for s3_key in TS_FILES:
    try:
        filename = s3_key.split('/')[-1]
        local_path = os.path.join(DOWNLOAD_DIR, filename)
        
        print(f"[{downloaded+1}/{len(TS_FILES)}] Baixando: {filename}")
        
        s3.download_file(
            BUCKET, 
            s3_key, 
            local_path,
            Callback=progress_callback
        )
        
        file_size = os.path.getsize(local_path) / (1024 * 1024)
        print(f"\r  OK - {file_size:.2f} MB baixados\n")
        
        downloaded += 1
        
    except Exception as e:
        print(f"\r  ERRO: {str(e)}\n")
        failed += 1

print(f"\n[RESUMO]")
print(f"  Sucesso: {downloaded}")
print(f"  Falhas: {failed}")
print(f"  Total: {len(TS_FILES)}")

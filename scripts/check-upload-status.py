import boto3
import os

s3 = boto3.client('s3')
BUCKET = 'mediaflow-uploads-969430605054'
LOCAL_KATE = r'C:\Users\dell 5557\Videos\IDM\Star\kate kuray'
S3_PREFIX = 'users/sergio_sena/'

def check_kate_kuray_status():
    print("Verificando status do upload kate kuray...\n")
    
    # Arquivos que estavam faltando
    missing_files = [
        'EPORNER.COM - [2NArHQyVzYf] Kate Kuray  Fucked (1440).mp4',
        'EPORNER.COM - [8zoDtJiJljb] Kate Kuray - Penny Tease Down Here It Gets Wet (2160).mp4',
        'EPORNER.COM - [XCtzYN9c7Vq] Kate Kuray She  Fuck Her Ass (1080).mp4'
    ]
    
    # Verificar no S3
    s3_files = set()
    try:
        paginator = s3.get_paginator('list_objects_v2')
        pages = paginator.paginate(Bucket=BUCKET, Prefix=S3_PREFIX)
        
        for page in pages:
            if 'Contents' in page:
                for obj in page['Contents']:
                    filename = obj['Key'].split('/')[-1]
                    if filename:
                        s3_files.add(filename)
    except Exception as e:
        print(f"Erro S3: {e}")
        return
    
    print("Status dos arquivos que estavam faltando:")
    uploaded = 0
    
    for filename in missing_files:
        if filename in s3_files:
            print(f"[OK] {filename}")
            uploaded += 1
        else:
            print(f"[PENDING] {filename}")
    
    print(f"\nProgresso: {uploaded}/{len(missing_files)} arquivos")
    
    if uploaded == len(missing_files):
        print("[COMPLETO] Upload kate kuray finalizado!")
    else:
        print("[EM ANDAMENTO] Upload ainda em progresso...")

if __name__ == '__main__':
    check_kate_kuray_status()
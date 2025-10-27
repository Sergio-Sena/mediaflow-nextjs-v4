#!/usr/bin/env python3
import boto3
import os

s3 = boto3.client('s3', region_name='us-east-1')
bucket = 'mediaflow-uploads-969430605054'
local_dir = r'C:\Users\dell 5557\Videos\IDM\Star\MIRARI HUB'
s3_prefix = 'users/user_admin/Star/MIRARI HUB/'

missing = [
    "A Acompanhante De 18 Anos Veio Pedir Pela Primeira Vez. Eu Promise Ser Um Bom Primeiro Cliente - MIRARI - Pornhub.com.mp4",
    "A Amiga Da Minha Meia-irmã Não Se Importa Em Provar Minha Porra - Sexo Apaixonado - MIRARI - Pornhub.com.mp4",
    "A Amiga Da Minha Meia-irmã Não Se Importa Em Provar Minha Porra - Sexo Apaixonado - MIRARI - Pornhub.com~1.mp4",
    "Andorinhas Cum com Boca e Buceta - COMPILAÇÃO CUM - Pornhub.com.mp4",
    "Boa Garota Se Deu Mal. Foda áspera com Uma Garota Em Cintos De Couro - MIRARI - Pornhub.com.mp4",
    "Garota Inocente é Cheia De Depravação - MIRARI - Pornhub.com.mp4",
    "Lifeselector - Petite GF Mirari Hub Espalha Seus Lábios De Buceta - Pornhub.com.mp4",
    "Minha Nova Secretária MIRARI - Pornhub.com.mp4",
    "Sexo Rápido com Meia-irmã Enquanto Ninguém Está Em Casa - MIRARI - Pornhub.com.mp4"
]

print("Enviando 9 arquivos faltantes de MIRARI HUB")
print("=" * 60)

for idx, filename in enumerate(missing, 1):
    local_path = os.path.join(local_dir, filename)
    s3_key = s3_prefix + filename
    
    if os.path.exists(local_path):
        size_mb = os.path.getsize(local_path) / (1024**2)
        print(f"[{idx}/9] {filename[:60]}... ({size_mb:.1f} MB)")
        s3.upload_file(local_path, bucket, s3_key)
    else:
        print(f"[{idx}/9] ERRO: Arquivo nao encontrado localmente")

print("\nConcluido!")

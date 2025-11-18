#!/usr/bin/env python3
"""
Upload seletivo dos 23 arquivos faltantes para sergio_sena
"""

import boto3
import os
from pathlib import Path

def get_missing_files():
    """Lista dos 23 arquivos faltantes identificados"""
    missing_files = [
        # Aidra Fox (6 arquivos)
        "Aidra Fox/NubileFilms - Intensamente Ardente Trindade Sexual - Pornhub.com.mp4",
        "Aidra Fox/TUSHY - Primeira Dupla Penetração De Riley Reid - Pornhub.com.mp4", 
        "Aidra Fox/Tushy Sendo Reiley Capitulo 2 - Pornhub.com.mp4",
        "Aidra Fox/VIXEN Eu Fiquei Pelada Para o Meu Meio-Irmão e Ele Não Resistiu - Pornhub.com.mp4",
        "Aidra Fox/Vídeo completo - PORNPROS Meu melhor amigo montou seu pau enquanto eu emprestava seu rosto.mp4",
        "Aidra Fox/Vídeo completo - Twistys - Duas colegas de quarto sexy Aidra Fox e Tru Kait têm um momento íntimo juntos.mp4",
        
        # Asian (2 arquivos)
        "Asian/Cute Menina Asiática Ao Lado me Deixa Gozar Em Todos Os Três Buracos - Lucy Mochi - Anal - Pornhub.com.mp4",
        "Asian/Pequena Asiática Lucy Mochi Adora Anal Demais - Compilação - Pornhub.com.mp4",
        
        # Comatozze (2 arquivos) 
        "Comatozze/Virgin Step Sister Quer Aprender a Foder ... - Pornhub.com.mp4",
        
        # Diana Rider (5 arquivos)
        "Diana Rider/Babe Candidata Massagem, Acaba Em Salão Handjob! Gozada Facial! - Pornhub.com.mp4",
        "Diana Rider/Black Mirror- Sweetie Fox Pegou O Corpo Da Diana Rider E Fodeu Comigo - Pornhub.com.mp4",
        "Diana Rider/Creampied a Buceta Da Minha Ex no Seu Casamento! Ela Gozou Tanto Que Esqueceu Do Marido! - Pornhub.com.mp4",
        "Diana Rider/Mana, Roubaste Meu Dinheiro Pra Labubu. Vou Foder Tua Buceta Como Castigo! - Pornhub.com.mp4",
        "Diana Rider/Ovulação Transforma Minha Mana De Tímida Em Máquina De Sexo Horny! Pede Foda Dura E CumShot! - Pornhub.com.mp4",
        
        # Little Caprice (3 arquivos)
        "Little Caprice/EPORNER.COM - [BoN3COJE2ub] Caprice and angelica are sharing a cock (1080).mp4",
        "Little Caprice/EPORNER.COM - [Iv79yOPySOm] Xa C Rf Hot (1080).mp4",
        "Little Caprice/EPORNER.COM - [lmGr9vokhQ1] Hqcollect 1814 (1440).mp4",
        
        # Megan Rain (1 arquivo)
        "Megan Rain/TUSHY Megan Rain Namorada Traidora Faz Dupla Penetração com Outros Caras - Pornhub.com.mp4",
        
        # sweetfox (1 arquivo)
        "sweetfox/Eu Transei com a Meia-Irmã Da Minha Esposa no Banheiro Enquanto Minha Esposa Foi À Loja. - Pornhub.com.mp4",
        
        # kate kuray (3 arquivos)
        "kate kuray/EPORNER.COM - [2NArHQyVzYf] Kate Kuray  Fucked (1440).mp4",
        "kate kuray/EPORNER.COM - [8zoDtJiJljb] Kate Kuray - Penny Tease Down Her Panties (1080).mp4",
        "kate kuray/EPORNER.COM - [XCtzYN9c7Vq] Kate Kuray She  Fuck Her Ass (1080).mp4"
    ]
    return missing_files

class ProgressPercentage:
    def __init__(self, filename, filesize):
        self._filename = filename
        self._size = filesize
        self._seen_so_far = 0
        
    def __call__(self, bytes_amount):
        self._seen_so_far += bytes_amount
        percentage = (self._seen_so_far / self._size) * 100
        print(f"\r  Progress: {percentage:.1f}% ({self._seen_so_far / (1024*1024):.1f}/{self._size / (1024*1024):.1f} MB)", end='', flush=True)

def upload_file_to_s3(local_path, s3_key, bucket_name):
    """Upload arquivo para S3 com progresso"""
    s3_client = boto3.client('s3')
    
    try:
        file_size = os.path.getsize(local_path)
        progress = ProgressPercentage(os.path.basename(local_path), file_size)
        
        print(f"  Iniciando upload...")
        s3_client.upload_file(
            local_path, 
            bucket_name, 
            s3_key,
            ExtraArgs={'ContentType': 'video/mp4'},
            Callback=progress
        )
        print()  # Nova linha após progresso
        return True
    except Exception as e:
        print(f"\n  Erro: {e}")
        return False

def main():
    print("Upload seletivo - 23 arquivos faltantes para sergio_sena")
    print("=" * 60)
    print("ACOMPANHAMENTO EM TEMPO REAL:")
    print("- Progresso individual por arquivo")
    print("- Velocidade de upload (MB/s)")
    print("- Tempo decorrido por arquivo")
    print("- Progresso geral da operacao")
    print("=" * 60)
    
    star_path = r"C:\Users\dell 5557\Videos\IDM\Star"
    bucket_name = 'mediaflow-uploads-969430605054'
    s3_prefix = 'users/sergio_sena/Star'
    
    missing_files = get_missing_files()
    
    print(f"Arquivos para upload: {len(missing_files)}")
    print()
    
    uploaded = 0
    errors = 0
    total_size = 0
    
    for i, relative_path in enumerate(missing_files, 1):
        local_file = os.path.join(star_path, relative_path)
        
        # Verificar se arquivo existe
        if not os.path.exists(local_file):
            print(f"[{i:2d}/{len(missing_files)}] SKIP - Arquivo não encontrado: {relative_path}")
            errors += 1
            continue
        
        # Calcular tamanho
        size_mb = os.path.getsize(local_file) / (1024 * 1024)
        total_size += size_mb
        
        # Definir chave S3
        s3_key = f"{s3_prefix}/{relative_path}"
        
        print(f"[{i:2d}/{len(missing_files)}] {os.path.basename(relative_path)} ({size_mb:.1f} MB)")
        print(f"  Pasta: {os.path.dirname(relative_path)}")
        
        # Upload com tempo
        import time
        start_time = time.time()
        
        if upload_file_to_s3(local_file, s3_key, bucket_name):
            elapsed = time.time() - start_time
            speed = size_mb / elapsed if elapsed > 0 else 0
            uploaded += 1
            print(f"  OK - {elapsed:.1f}s ({speed:.1f} MB/s)")
        else:
            errors += 1
            print(f"  ERRO")
        
        # Progresso geral
        progress_pct = (i / len(missing_files)) * 100
        print(f"  Progresso geral: {progress_pct:.1f}% ({i}/{len(missing_files)} arquivos)")
        print("-" * 50)
    
    print("=" * 60)
    print(f"RESULTADO:")
    print(f"Uploaded: {uploaded}")
    print(f"Errors: {errors}")
    print(f"Total size: {total_size:.1f} MB ({total_size/1024:.2f} GB)")

if __name__ == "__main__":
    main()
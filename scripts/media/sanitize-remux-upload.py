# -*- coding: utf-8 -*-
"""
Sanitiza nomes, remux .ts->.mp4 e upload para S3.
Processa os arquivos pendentes.
"""
import boto3
import os
import re
import subprocess
import sys

sys.stdout.reconfigure(encoding='utf-8')

s3 = boto3.client('s3', region_name='us-east-1')
BUCKET = 'mediaflow-uploads-969430605054'
LOCAL_PATH = r'C:\Users\dell 5557\Videos\IDM'
FFMPEG = r'C:\ffmpeg\bin\ffmpeg.exe'
VIDEO_EXTS = ('.mp4', '.ts', '.mkv', '.avi', '.mov', '.webm')

# Mapeamento pasta local -> pasta S3
S3_PREFIX = 'users/sergio_sena'


def sanitize_filename(filename):
    """Remove sites, resolucoes, codecs, caracteres especiais."""
    name, ext = os.path.splitext(filename)
    
    # Remove sites
    name = re.sub(r'\s*-?\s*(Pornhub\.com|Pornhub|EPORNER\.COM|xvideos)', '', name, flags=re.IGNORECASE)
    
    # Remove sufixos tipo _2, _3
    name = re.sub(r'_(\d)$', r' \1', name)
    
    # Remove tags [H69], [4K60FPS], [4K 120FPS], [R2 Studio], [NO WM]
    name = re.sub(r'\[H69\]', '', name, flags=re.IGNORECASE)
    name = re.sub(r'\[4K\s*\d*FPS\]', '', name, flags=re.IGNORECASE)
    name = re.sub(r'\[R2\s*Studio\]', '', name, flags=re.IGNORECASE)
    name = re.sub(r'\[NO\s*WM\.?\]', '', name, flags=re.IGNORECASE)
    name = re.sub(r'\[[^\]]*\]', '', name)  # Remove qualquer outro []
    
    # Remove resolucoes
    name = re.sub(r'\s*(4K|1080p?|720p?|480p?|60FPS|120FPS)\s*', ' ', name, flags=re.IGNORECASE)
    
    # Remove prefixos de produtoras
    name = re.sub(r'^(BLACKEDRAW|GIRLSWAY|HouseHumpers|TUSHY)\s*-?\s*', '', name, flags=re.IGNORECASE)
    
    # Normalizar caracteres
    name = name.strip(' -_.')
    name = re.sub(r'[^\w\s.-]', '_', name)
    name = re.sub(r'\s+', '_', name)
    name = re.sub(r'_+', '_', name)
    name = name.strip('_')
    
    # Truncar a 60 chars
    if len(name) > 60:
        name = name[:60]
        last_underscore = name.rfind('_')
        if last_underscore > 50:
            name = name[:last_underscore]
    
    return (name or 'video') + '.mp4'


def remux_to_mp4(input_file, output_file):
    """Remux sem re-encode (rapido)."""
    cmd = [
        FFMPEG,
        '-i', input_file,
        '-c', 'copy',
        '-movflags', '+faststart',
        '-y',
        output_file
    ]
    result = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8', errors='ignore')
    return result.returncode == 0


def upload_to_s3(local_file, s3_key):
    """Upload com progress."""
    file_size = os.path.getsize(local_file)
    uploaded = [0]
    
    def callback(bytes_transferred):
        uploaded[0] += bytes_transferred
        mb = uploaded[0] / (1024 * 1024)
        pct = (uploaded[0] / file_size) * 100
        print(f'\r    Upload: {mb:.0f}/{file_size/(1024*1024):.0f} MB ({pct:.0f}%)', end='', flush=True)
    
    s3.upload_file(local_file, BUCKET, s3_key, Callback=callback)
    print()


def main():
    # Verificar ffmpeg
    if not os.path.exists(FFMPEG):
        print(f'ERRO: ffmpeg nao encontrado em {FFMPEG}')
        sys.exit(1)
    
    # Coletar arquivos pendentes
    print('Coletando arquivos pendentes...\n')
    
    pending = []
    for folder in sorted(os.listdir(LOCAL_PATH)):
        folder_path = os.path.join(LOCAL_PATH, folder)
        if not os.path.isdir(folder_path):
            continue
        for root, dirs, files in os.walk(folder_path):
            for f in files:
                if f.lower().endswith(VIDEO_EXTS):
                    pending.append((os.path.join(root, f), folder))
    
    if not pending:
        print('Nenhum arquivo pendente encontrado!')
        return
    
    print(f'Total: {len(pending)} arquivos para processar\n')
    print('=' * 60)
    
    processed = 0
    uploaded_count = 0
    errors = []
    
    for idx, (filepath, folder) in enumerate(pending, 1):
        filename = os.path.basename(filepath)
        print(f'\n[{idx}/{len(pending)}] {filename[:70]}')
        print(f'  Pasta: {folder}')
        
        # Sanitizar nome
        sanitized_name = sanitize_filename(filename)
        print(f'  Nome sanitizado: {sanitized_name}')
        
        # Definir S3 key
        s3_folder = f'{S3_PREFIX}/{folder}'
        s3_key = f'{s3_folder}/{sanitized_name}'
        print(f'  S3: {s3_key}')
        
        # Verificar se ja existe no S3
        try:
            s3.head_object(Bucket=BUCKET, Key=s3_key)
            print(f'  SKIP - ja existe no S3')
            # Remover local
            os.remove(filepath)
            print(f'  Removido local')
            continue
        except:
            pass
        
        # Se ja e .mp4, upload direto
        if filepath.lower().endswith('.mp4'):
            print(f'  Enviando .mp4 direto...')
            try:
                upload_to_s3(filepath, s3_key)
                uploaded_count += 1
                os.remove(filepath)
                print(f'  OK - removido local')
            except Exception as e:
                print(f'  ERRO upload: {e}')
                errors.append((filename, str(e)))
        else:
            # Remux .ts -> .mp4
            temp_mp4 = os.path.join(os.path.dirname(filepath), f'_temp_{sanitized_name}')
            print(f'  Remuxing...')
            
            if remux_to_mp4(filepath, temp_mp4):
                processed += 1
                print(f'  Enviando...')
                try:
                    upload_to_s3(temp_mp4, s3_key)
                    uploaded_count += 1
                    # Remover ambos
                    os.remove(filepath)
                    os.remove(temp_mp4)
                    print(f'  OK - removido local')
                except Exception as e:
                    print(f'  ERRO upload: {e}')
                    errors.append((filename, str(e)))
                    if os.path.exists(temp_mp4):
                        os.remove(temp_mp4)
            else:
                print(f'  ERRO remux')
                errors.append((filename, 'remux failed'))
                if os.path.exists(temp_mp4):
                    os.remove(temp_mp4)
    
    # Limpar pastas vazias
    empty_removed = 0
    for root, dirs, files in os.walk(LOCAL_PATH, topdown=False):
        if not os.listdir(root) and root != LOCAL_PATH:
            os.rmdir(root)
            empty_removed += 1
    
    # Resumo
    print(f'\n{"="*60}')
    print(f'RESUMO')
    print(f'{"="*60}')
    print(f'  Processados:  {len(pending)}')
    print(f'  Remuxados:    {processed}')
    print(f'  Enviados:     {uploaded_count}')
    print(f'  Erros:        {len(errors)}')
    print(f'  Pastas vazias removidas: {empty_removed}')
    
    if errors:
        print(f'\n  ERROS:')
        for name, err in errors:
            print(f'    - {name[:50]}: {err}')


if __name__ == '__main__':
    main()

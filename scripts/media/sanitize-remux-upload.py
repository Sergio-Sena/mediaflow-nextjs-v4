# -*- coding: utf-8 -*-
"""
Sanitiza nomes, remux .ts->.mp4 e upload para S3.
Roda direto de scripts/media/ sem precisar de cd.
Preserva estrutura de pastas local -> S3.

Uso:
  python scripts/media/sanitize-remux-upload.py

Mapeamento:
  IDM/Star/AniButler/video.ts  -> users/sergio_sena/Star/AniButler/video_sanitizado.mp4
  IDM/Anime/Kimetsu/video.mp4  -> users/sergio_sena/Anime/Kimetsu/video_sanitizado.mp4
"""
import boto3
from boto3.s3.transfer import TransferConfig
import os
import re
import subprocess
import sys
import unicodedata

sys.stdout.reconfigure(encoding='utf-8')

session = boto3.Session(profile_name='default')
s3 = session.client('s3', region_name='us-east-1')
BUCKET = 'mediaflow-uploads-969430605054'
LOCAL_PATH = r'C:\Users\dell 5557\Videos\IDM'
FFMPEG = r'C:\ffmpeg\bin\ffmpeg.exe'
VIDEO_EXTS = ('.mp4', '.ts', '.mkv', '.avi', '.mov', '.webm')
S3_USER = 'users/sergio_sena'

def get_transfer_config():
    """Mede velocidade de upload e configura multipart otimizado."""
    try:
        import speedtest
        print('Medindo velocidade de internet...')
        st = speedtest.Speedtest()
        st.get_best_server()
        upload_speed = st.upload() / 1_000_000  # Mbps
        print(f'  Upload: {upload_speed:.0f} Mbps')

        if upload_speed > 150:
            config = TransferConfig(multipart_threshold=8*1024*1024, multipart_chunksize=64*1024*1024, max_concurrency=10, use_threads=True)
            print(f'  Config: 64MB chunks, 10 threads (banda alta)\n')
        elif upload_speed > 50:
            config = TransferConfig(multipart_threshold=8*1024*1024, multipart_chunksize=32*1024*1024, max_concurrency=8, use_threads=True)
            print(f'  Config: 32MB chunks, 8 threads (banda media)\n')
        else:
            config = TransferConfig(multipart_threshold=8*1024*1024, multipart_chunksize=8*1024*1024, max_concurrency=5, use_threads=True)
            print(f'  Config: 8MB chunks, 5 threads (banda baixa)\n')
        return config
    except Exception:
        print('  Speedtest indisponivel, usando config padrao (64MB, 10 threads)\n')
        return TransferConfig(multipart_threshold=8*1024*1024, multipart_chunksize=64*1024*1024, max_concurrency=10, use_threads=True)


TRANSFER_CONFIG = None  # inicializado no main()

# Transliteração cirílico -> latin
CYRILLIC_MAP = {
    'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e', 'ё': 'yo',
    'ж': 'zh', 'з': 'z', 'и': 'i', 'й': 'y', 'к': 'k', 'л': 'l', 'м': 'm',
    'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r', 'с': 's', 'т': 't', 'у': 'u',
    'ф': 'f', 'х': 'kh', 'ц': 'ts', 'ч': 'ch', 'ш': 'sh', 'щ': 'shch',
    'ъ': '', 'ы': 'y', 'ь': '', 'э': 'e', 'ю': 'yu', 'я': 'ya',
}

# Produtoras a remover
PRODUTORAS = [
    'BLACKEDRAW', 'BLACKED RAW', 'BLACKED', 'GIRLSWAY', 'HouseHumpers',
    'TUSHY', 'XPERVO', 'LETSDOEIT', 'VIXEN', 'BRAZZERS', 'SWEET SINNER',
    'ADULT TIME', 'CUM4K', 'JULES JORDAN', 'Jules Jordan', 'NEW SENSATIONS',
    'PORNPROS', '404HotFound'
]

print(f'Pasta base: {LOCAL_PATH}\n')


def sanitize_filename(filename):
    """Sanitiza nomes em qualquer idioma."""
    name, ext = os.path.splitext(filename)

    # Remove sites
    name = re.sub(r'\s*-?\s*(Pornhub\.com|Pornhub|EPORNER\.COM|xvideos|PornHD)', '', name, flags=re.IGNORECASE)

    # Remove sufixos _2, _3
    name = re.sub(r'_(\d)$', r'_\1', name)

    # Remove tags entre colchetes/chaves
    name = re.sub(r'\[H69\]', '', name, flags=re.IGNORECASE)
    name = re.sub(r'\[4K\s*\d*FPS\]', '', name, flags=re.IGNORECASE)
    name = re.sub(r'\[R2\s*Studio\]', '', name, flags=re.IGNORECASE)
    name = re.sub(r'\[NO\s*WM\.?\]', '', name, flags=re.IGNORECASE)
    name = re.sub(r'\[[^\]]*\]', '', name)
    name = re.sub(r'\{[^\}]*\}', '', name)

    # Remove resolucoes
    name = re.sub(r'\s*(4K|1080p?|720p?|480p?|60FPS|120FPS)\s*', ' ', name, flags=re.IGNORECASE)

    # Remove produtoras
    for prod in PRODUTORAS:
        name = re.sub(rf'^\s*{re.escape(prod)}\s*-?\s*', '', name, flags=re.IGNORECASE)
        name = re.sub(rf'\s*-?\s*{re.escape(prod)}\s*-?\s*', ' ', name, flags=re.IGNORECASE)

    # Remove "Video completo - "
    name = re.sub(r'^V[ií]deo\s+completo\s*-?\s*', '', name, flags=re.IGNORECASE)

    # Transliterar cirílico
    result = []
    for char in name:
        lower = char.lower()
        if lower in CYRILLIC_MAP:
            mapped = CYRILLIC_MAP[lower]
            result.append(mapped.upper() if char.isupper() else mapped)
        else:
            result.append(char)
    name = ''.join(result)

    # Remover acentos
    name = unicodedata.normalize('NFD', name)
    name = ''.join(c for c in name if unicodedata.category(c) != 'Mn')

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
    cmd = [FFMPEG, '-i', input_file, '-c', 'copy', '-movflags', '+faststart', '-y', output_file]
    result = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8', errors='ignore')
    return result.returncode == 0


def upload_to_s3(local_file, s3_key):
    """Upload otimizado com multipart (64MB chunks, 10 threads)."""
    file_size = os.path.getsize(local_file)
    uploaded = [0]

    def callback(bytes_transferred):
        uploaded[0] += bytes_transferred
        pct = (uploaded[0] / file_size) * 100
        print(f'\r    Upload: {uploaded[0]/(1024*1024):.0f}/{file_size/(1024*1024):.0f} MB ({pct:.0f}%)', end='', flush=True)

    s3.upload_file(local_file, BUCKET, s3_key, Config=TRANSFER_CONFIG, Callback=callback)
    print()


def get_s3_folder(filepath):
    """Mapeia path local para pasta S3 preservando estrutura."""
    rel_path = os.path.relpath(filepath, LOCAL_PATH)
    parts = rel_path.replace('\\', '/').split('/')
    return '/'.join(parts[:-1]) if len(parts) > 1 else ''


def main():
    global TRANSFER_CONFIG

    if not os.path.exists(FFMPEG):
        print(f'ERRO: ffmpeg nao encontrado em {FFMPEG}')
        sys.exit(1)

    TRANSFER_CONFIG = get_transfer_config()

    print('Coletando arquivos pendentes...\n')

    pending = []
    for root, dirs, files in os.walk(LOCAL_PATH):
        for f in files:
            if f.lower().endswith(VIDEO_EXTS):
                pending.append(os.path.join(root, f))

    if not pending:
        print('Nenhum arquivo pendente encontrado!')
        return

    print(f'Total: {len(pending)} arquivos para processar\n')
    print('=' * 60)

    processed = 0
    uploaded_count = 0
    errors = []

    for idx, filepath in enumerate(pending, 1):
        filename = os.path.basename(filepath)
        s3_folder = get_s3_folder(filepath)
        print(f'\n[{idx}/{len(pending)}] {filename[:70]}')
        print(f'  Pasta S3: {S3_USER}/{s3_folder}/')

        sanitized_name = sanitize_filename(filename)
        print(f'  Nome sanitizado: {sanitized_name}')

        s3_key = f'{S3_USER}/{s3_folder}/{sanitized_name}' if s3_folder else f'{S3_USER}/{sanitized_name}'
        print(f'  S3 key: {s3_key}')

        # Verificar se ja existe
        try:
            s3.head_object(Bucket=BUCKET, Key=s3_key)
            print(f'  SKIP - ja existe no S3')
            os.remove(filepath)
            print(f'  Removido local')
            continue
        except:
            pass

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
            temp_mp4 = os.path.join(os.path.dirname(filepath), f'_temp_{sanitized_name}')
            print(f'  Remuxing...')

            if remux_to_mp4(filepath, temp_mp4):
                processed += 1
                print(f'  Enviando...')
                try:
                    upload_to_s3(temp_mp4, s3_key)
                    uploaded_count += 1
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

    print(f'\n{"="*60}')
    print(f'RESUMO')
    print(f'{"="*60}')
    print(f'  Processados:  {len(pending)}')
    print(f'  Remuxados:    {processed}')
    print(f'  Enviados:     {uploaded_count}')
    print(f'  Erros:        {len(errors)}')

    if errors:
        print(f'\n  ERROS:')
        for name, err in errors:
            print(f'    - {name[:50]}: {err}')


if __name__ == '__main__':
    main()

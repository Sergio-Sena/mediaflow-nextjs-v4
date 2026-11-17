# -*- coding: utf-8 -*-
"""
Sanitiza nomes, remux .ts->.mp4 e upload para S3 via AWS CLI.
Preserva estrutura de pastas local -> S3.

Mapeamento:
  IDM/Star/AniButler/video.ts  -> users/sergio_sena/Star/AniButler/video_sanitizado.mp4
  IDM/Anime/Kimetsu/video.mp4  -> users/sergio_sena/Anime/Kimetsu/video_sanitizado.mp4
"""
import os
import re
import subprocess
import sys
import unicodedata

sys.stdout.reconfigure(encoding='utf-8')

BUCKET    = 'mediaflow-uploads-969430605054'
BASE_PATH  = r'C:\Users\dell 5557\Videos\IDM'

# Suporte a múltiplos --path
_paths = []
_i = 1
while _i < len(sys.argv):
    if sys.argv[_i] == '--path' and _i + 1 < len(sys.argv):
        _paths.append(sys.argv[_i + 1])
        _i += 2
    else:
        _i += 1
LOCAL_PATHS = _paths if _paths else [BASE_PATH]
FFMPEG    = r'C:\ffmpeg\bin\ffmpeg.exe'
FFPROBE   = r'C:\ffmpeg\bin\ffprobe.exe'
CODEC_RANK = {'hevc': 3, 'h265': 3, 'av1': 4, 'vp9': 2, 'h264': 1, 'avc': 1}
AWS       = 'aws'
PROFILE   = 'default'
VIDEO_EXTS = ('.mp4', '.ts', '.mkv', '.avi', '.mov', '.webm')
S3_USER   = 'users/sergio_sena'

CYRILLIC_MAP = {
    'а':'a','б':'b','в':'v','г':'g','д':'d','е':'e','ё':'yo','ж':'zh','з':'z',
    'и':'i','й':'y','к':'k','л':'l','м':'m','н':'n','о':'o','п':'p','р':'r',
    'с':'s','т':'t','у':'u','ф':'f','х':'kh','ц':'ts','ч':'ch','ш':'sh',
    'щ':'shch','ъ':'','ы':'y','ь':'','э':'e','ю':'yu','я':'ya',
}

PRODUTORAS = [
    'BLACKEDRAW','BLACKED RAW','BLACKED','GIRLSWAY','HouseHumpers','TUSHY',
    'XPERVO','LETSDOEIT','VIXEN','BRAZZERS','SWEET SINNER','ADULT TIME','CUM4K',
    'JULES JORDAN','Jules Jordan','NEW SENSATIONS','PORNPROS','404HotFound'
]


LANG_TAGS = re.compile(r'\[(LEGENDADO?\s+[A-Z]{2}(?:-[A-Z]{2})?|[A-Z]{2}-[A-Z]{2}|DUBBED|SUBBED|LEGENDA(?:DO)?)\]', re.IGNORECASE)


def sanitize_filename(filename):
    name, _ = os.path.splitext(filename)
    # Preservar sufixo de idioma antes de remover colchetes
    lang_match = LANG_TAGS.search(name)
    lang_suffix = '_' + lang_match.group(1).replace(' ', '-').upper() if lang_match else ''
    name = re.sub(r'\s*-?\s*(Pornhub\.com|Pornhub|EPORNER\.COM|xvideos|PornHD)', '', name, flags=re.IGNORECASE)
    name = re.sub(r'\[H69\]', '', name, flags=re.IGNORECASE)
    name = re.sub(r'\[4K\s*\d*FPS\]', '', name, flags=re.IGNORECASE)
    name = re.sub(r'\[R2\s*Studio\]', '', name, flags=re.IGNORECASE)
    name = re.sub(r'\[NO\s*WM\.?\]', '', name, flags=re.IGNORECASE)
    name = re.sub(r'\[[^\]]*\]', '', name)
    name = re.sub(r'\{[^\}]*\}', '', name)
    name = re.sub(r'\s*(4K|1080p?|720p?|480p?|60FPS|120FPS)\s*', ' ', name, flags=re.IGNORECASE)
    for prod in PRODUTORAS:
        name = re.sub(rf'^\s*{re.escape(prod)}\s*-?\s*', '', name, flags=re.IGNORECASE)
        name = re.sub(rf'\s*-?\s*{re.escape(prod)}\s*-?\s*', ' ', name, flags=re.IGNORECASE)
    name = re.sub(r'^V[ií]deo\s+completo\s*-?\s*', '', name, flags=re.IGNORECASE)
    result = []
    for char in name:
        lower = char.lower()
        if lower in CYRILLIC_MAP:
            mapped = CYRILLIC_MAP[lower]
            result.append(mapped.upper() if char.isupper() else mapped)
        else:
            result.append(char)
    name = ''.join(result)
    name = unicodedata.normalize('NFD', name)
    name = ''.join(c for c in name if unicodedata.category(c) != 'Mn')
    name = name.strip(' -_.')
    name = re.sub(r'[^\w\s.-]', '_', name)
    name = re.sub(r'\s+', '_', name)
    name = re.sub(r'_+', '_', name)
    name = name.strip('_')
    if len(name) > 60:
        name = name[:60]
        last = name.rfind('_')
        if last > 50:
            name = name[:last]
    return (name or 'video') + lang_suffix + '.mp4'


def get_video_meta(filepath):
    """Retorna dict com width, height, bitrate, codec, duration via ffprobe."""
    cmd = [
        FFPROBE, '-v', 'quiet', '-select_streams', 'v:0',
        '-show_entries', 'stream=width,height,bit_rate,codec_name',
        '-show_entries', 'format=duration',
        '-of', 'csv=p=0', filepath
    ]
    result = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8', errors='ignore')
    if result.returncode != 0 or not result.stdout.strip():
        return None
    lines = [l.strip() for l in result.stdout.strip().splitlines() if l.strip()]
    # linha 0: codec,width,height,bitrate  linha 1: duration
    if len(lines) < 1:
        return None
    try:
        parts = lines[0].split(',')
        duration = 0
        for line in lines[1:]:
            try:
                duration = int(float(line))
                break
            except:
                pass
        return {
            'codec':    parts[0].lower(),
            'width':    int(parts[1]),
            'height':   int(parts[2]),
            'bitrate':  int(parts[3]) if len(parts) > 3 and parts[3].isdigit() else 0,
            'duration': duration,
        }
    except:
        return None


def meta_to_s3_tags(meta):
    """Converte meta dict para string de metadata S3."""
    return (
        f'resolution={meta["width"]}x{meta["height"]}'
        f',bitrate={meta["bitrate"]}'
        f',codec={meta["codec"]}'
        f',duration={meta.get("duration", 0)}'
    )


def s3_get_meta(s3_key):
    """Lê metadata de qualidade do S3 via head-object. Custo zero."""
    result = subprocess.run(
        [AWS, 's3api', 'head-object',
         '--bucket', BUCKET, '--key', s3_key,
         '--profile', PROFILE, '--query', 'Metadata'],
        capture_output=True, text=True, encoding='utf-8'
    )
    if result.returncode != 0 or not result.stdout.strip():
        return None
    import json
    try:
        data = json.loads(result.stdout)
        return {
            'codec':   data.get('codec', ''),
            'width':   int(data.get('resolution', '0x0').split('x')[0]),
            'height':  int(data.get('resolution', '0x0').split('x')[1]),
            'bitrate': int(data.get('bitrate', 0)),
        }
    except:
        return None


def is_local_better(local_meta, s3_meta):
    """Retorna True se local tem qualidade superior ao S3."""
    if not s3_meta:
        return True  # S3 sem metadata = arquivo antigo, substitui
    local_res  = local_meta['width'] * local_meta['height']
    s3_res     = s3_meta['width']    * s3_meta['height']
    if local_res != s3_res:
        return local_res > s3_res
    if local_meta['bitrate'] != s3_meta['bitrate']:
        return local_meta['bitrate'] > s3_meta['bitrate']
    return CODEC_RANK.get(local_meta['codec'], 0) > CODEC_RANK.get(s3_meta['codec'], 0)


def s3_get_size(s3_key):
    """Retorna tamanho do arquivo no S3 em bytes, ou -1 se não existir."""
    result = subprocess.run(
        [AWS, 's3', 'ls', f's3://{BUCKET}/{s3_key}', '--profile', PROFILE],
        capture_output=True, text=True
    )
    if result.returncode != 0 or not result.stdout.strip():
        return -1
    try:
        return int(result.stdout.split()[2])
    except:
        return -1


def s3_exists(s3_key):
    """Verifica se arquivo já existe no S3 via CLI."""
    return s3_get_size(s3_key) >= 0


def upload_to_s3(local_file, s3_key, meta=None):
    """Upload via AWS CLI com metadata de qualidade."""
    cmd = [AWS, 's3', 'cp', local_file, f's3://{BUCKET}/{s3_key}',
           '--profile', PROFILE, '--no-progress']
    if meta:
        cmd += ['--metadata', meta_to_s3_tags(meta)]
    result = subprocess.run(cmd, text=True, encoding='utf-8', errors='ignore')
    return result.returncode == 0


def remux_to_mp4(input_file, output_file):
    """Remux sem re-encode."""
    cmd = [FFMPEG, '-i', input_file, '-c', 'copy', '-movflags', '+faststart', '-y', output_file]
    result = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8', errors='ignore')
    return result.returncode == 0


def get_s3_folder(filepath):
    """Mapeia path local para pasta S3 preservando estrutura a partir de BASE_PATH."""
    rel_path = os.path.relpath(filepath, BASE_PATH)
    parts = rel_path.replace('\\', '/').split('/')
    return '/'.join(parts[:-1]) if len(parts) > 1 else ''


def get_upload_speed():
    """Mede velocidade e retorna config de multipart."""
    try:
        import speedtest
        print('Medindo velocidade...')
        st = speedtest.Speedtest()
        st.get_best_server()
        speed = st.upload() / 1_000_000
        print(f'  Upload: {speed:.0f} Mbps\n')
        return speed
    except:
        print('  Speedtest indisponivel\n')
        return 50


def main():
    force = '--force' in sys.argv
    if force:
        print('MODO FORCE: sobrescrevendo arquivos existentes no S3\n')
    print(f'Pastas: {LOCAL_PATHS}\n')

    if not os.path.exists(FFMPEG):
        print(f'ERRO: ffmpeg nao encontrado em {FFMPEG}')
        sys.exit(1)

    # Medir velocidade e configurar multipart via env var para AWS CLI
    speed = get_upload_speed()
    if speed > 150:
        chunk = '64MB'; concurrency = '10'
    elif speed > 50:
        chunk = '32MB'; concurrency = '8'
    else:
        chunk = '8MB';  concurrency = '5'

    os.environ['AWS_DEFAULT_REGION'] = 'us-east-1'
    subprocess.run([AWS, 'configure', 'set', 'default.s3.multipart_chunksize', chunk, '--profile', PROFILE])
    subprocess.run([AWS, 'configure', 'set', 'default.s3.max_concurrent_requests', concurrency, '--profile', PROFILE])
    print(f'Config: {chunk} chunks, {concurrency} threads\n')

    print('Coletando arquivos...\n')

    pending = []
    for local_path in LOCAL_PATHS:
        for root, _, files in os.walk(local_path):
            for f in files:
                if f.lower().endswith(VIDEO_EXTS):
                    pending.append(os.path.join(root, f))

    if not pending:
        print('Nenhum arquivo encontrado!')
        return

    print(f'Total: {len(pending)} arquivos\n')
    print('=' * 60)

    uploaded_count = 0
    remuxed = 0
    errors = []

    for idx, filepath in enumerate(pending, 1):
        filename = os.path.basename(filepath)
        s3_folder = get_s3_folder(filepath)
        sanitized = sanitize_filename(filename)
        s3_key = f'{S3_USER}/{s3_folder}/{sanitized}' if s3_folder else f'{S3_USER}/{sanitized}'

        print(f'\n[{idx}/{len(pending)}] {filename[:70]}')
        print(f'  → {sanitized}')
        print(f'  S3: {s3_key}')

        # Arquivo a processar (pode ser remuxado)
        upload_file = filepath
        temp = None

        if not filepath.lower().endswith('.mp4'):
            temp = os.path.join(os.path.dirname(filepath), f'_temp_{sanitized}')
            print(f'  Remuxing...')
            if remux_to_mp4(filepath, temp):
                remuxed += 1
                upload_file = temp
            else:
                print(f'  ERRO remux - arquivo LOCAL MANTIDO')
                errors.append((filename, 'remux failed'))
                if os.path.exists(temp): os.remove(temp)
                continue

        # Ler metadados locais
        local_meta = get_video_meta(upload_file)
        if local_meta:
            print(f'  Qualidade local: {local_meta["width"]}x{local_meta["height"]} | {local_meta["bitrate"]}bps | {local_meta["codec"]}')

        # Verificar se já existe no S3
        if not force and s3_exists(s3_key):
            s3_meta = s3_get_meta(s3_key)
            if s3_meta:
                print(f'  Qualidade S3:    {s3_meta["width"]}x{s3_meta["height"]} | {s3_meta["bitrate"]}bps | {s3_meta["codec"]}')
            if local_meta and not is_local_better(local_meta, s3_meta):
                print(f'  SKIP - S3 tem qualidade igual ou superior')
                os.remove(upload_file if upload_file != filepath else filepath)
                if upload_file != filepath and os.path.exists(filepath): os.remove(filepath)
                continue
            else:
                print(f'  SUBSTITUINDO - local tem qualidade superior')

        # Upload
        local_size = os.path.getsize(upload_file)
        print(f'  Enviando... ({local_size/1024/1024:.1f} MB)')
        if upload_to_s3(upload_file, s3_key, meta=local_meta):
            s3_size = s3_get_size(s3_key)
            if s3_size == local_size:
                uploaded_count += 1
                if upload_file != filepath: os.remove(filepath)
                os.remove(upload_file)
                print(f'  OK - removido local ({s3_size/1024/1024:.1f} MB confirmado no S3)')
            else:
                print(f'  ERRO verificacao: local={local_size} s3={s3_size} - arquivo LOCAL MANTIDO')
                errors.append((filename, f'size mismatch local={local_size} s3={s3_size}'))
                if temp and os.path.exists(temp): os.remove(temp)
        else:
            print(f'  ERRO upload - arquivo LOCAL MANTIDO')
            errors.append((filename, 'upload failed'))
            if temp and os.path.exists(temp): os.remove(temp)

    print(f'\n{"="*60}')
    print(f'RESUMO')
    print(f'{"="*60}')
    print(f'  Processados: {len(pending)}')
    print(f'  Remuxados:   {remuxed}')
    print(f'  Enviados:    {uploaded_count}')
    print(f'  Erros:       {len(errors)}')
    if errors:
        print(f'\n  ERROS:')
        for name, err in errors:
            print(f'    - {name[:50]}: {err}')


if __name__ == '__main__':
    main()

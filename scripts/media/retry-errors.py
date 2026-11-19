# -*- coding: utf-8 -*-
import os, re, sys, unicodedata, subprocess
sys.stdout.reconfigure(encoding='utf-8')

BUCKET = 'mediaflow-uploads-969430605054'
LOCAL_PATH = r'C:\Users\dell 5557\Videos\IDM'
FFMPEG = r'C:\ffmpeg\bin\ffmpeg.exe'
AWS = 'aws'
PROFILE = 'default'
S3_USER = 'users/sergio_sena'

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

def sanitize_filename(filename):
    name, _ = os.path.splitext(filename)
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
    return (name or 'video') + '.mp4'

def get_s3_folder(filepath):
    rel_path = os.path.relpath(filepath, LOCAL_PATH)
    parts = rel_path.replace('\\', '/').split('/')
    return '/'.join(parts[:-1]) if len(parts) > 1 else ''

# Encontrar os arquivos com erro
targets = ['Furinas New Starring Role', 'D-VIRUS']
errors = []

for root, _, files in os.walk(LOCAL_PATH):
    for f in files:
        if any(t.lower() in f.lower() for t in targets):
            filepath = os.path.join(root, f)
            sanitized = sanitize_filename(f)
            s3_folder = get_s3_folder(filepath)
            s3_key = f'{S3_USER}/{s3_folder}/{sanitized}' if s3_folder else f'{S3_USER}/{sanitized}'

            print(f'Arquivo: {f}')
            print(f'  → {sanitized}')
            print(f'  S3: {s3_key}')
            print(f'  Enviando...')

            result = subprocess.run(
                [AWS, 's3', 'cp', filepath, f's3://{BUCKET}/{s3_key}',
                 '--profile', PROFILE, '--no-progress'],
                text=True, encoding='utf-8', errors='ignore', capture_output=True
            )

            if result.returncode == 0:
                os.remove(filepath)
                print(f'  OK - removido local\n')
            else:
                print(f'  ERRO: {result.stderr[:200]}\n')
                errors.append(f)

if errors:
    print(f'Ainda com erro: {errors}')
else:
    print('Todos enviados com sucesso!')

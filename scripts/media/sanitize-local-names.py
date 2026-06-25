# -*- coding: utf-8 -*-
"""
Sanitiza nomes de arquivos locais.
- Remove sites (Pornhub, etc)
- Remove produtoras (BLACKED, TUSHY, VIXEN, etc)
- Remove sufixos _2, _3
- Converte caracteres especiais para underscore
- Trunca a 60 chars
- Mantém palavras-chave que identificam o conteudo
"""
import os
import re
import sys
import unicodedata
sys.stdout.reconfigure(encoding='utf-8')

LOCAL_PATH = r'C:\Users\dell 5557\Videos\IDM'
VIDEO_EXTS = ('.mp4', '.ts', '.mkv', '.avi', '.mov', '.webm')


def sanitize_filename(filename):
    name, ext = os.path.splitext(filename)

    # Remove sites
    name = re.sub(r'\s*-?\s*(Pornhub\.com|Pornhub|EPORNER\.COM|xvideos|PornHD)', '', name, flags=re.IGNORECASE)

    # Remove sufixos _2, _3, _4
    name = re.sub(r'_(\d)$', r'_\1', name)

    # Remove tags entre colchetes
    name = re.sub(r'\[H69\]', '', name, flags=re.IGNORECASE)
    name = re.sub(r'\[4K\s*\d*FPS\]', '', name, flags=re.IGNORECASE)
    name = re.sub(r'\[R2\s*Studio\]', '', name, flags=re.IGNORECASE)
    name = re.sub(r'\[NO\s*WM\.?\]', '', name, flags=re.IGNORECASE)
    name = re.sub(r'\[[^\]]*\]', '', name)
    name = re.sub(r'\{[^\}]*\}', '', name)

    # Remove resolucoes
    name = re.sub(r'\s*(4K|1080p?|720p?|480p?|60FPS|120FPS)\s*', ' ', name, flags=re.IGNORECASE)

    # Remove produtoras no inicio
    produtoras = [
        'BLACKEDRAW', 'BLACKED RAW', 'BLACKED', 'GIRLSWAY', 'HouseHumpers',
        'TUSHY', 'XPERVO', 'LETSDOEIT', 'VIXEN', 'BRAZZERS', 'SWEET SINNER',
        'ADULT TIME', 'CUM4K', 'JULES JORDAN', 'Jules Jordan', 'NEW SENSATIONS',
        'PORNPROS', '404HotFound'
    ]
    for prod in produtoras:
        name = re.sub(rf'^\s*{re.escape(prod)}\s*-?\s*', '', name, flags=re.IGNORECASE)
        # Tambem no meio se seguido de " - "
        name = re.sub(rf'\s*-?\s*{re.escape(prod)}\s*-?\s*', ' ', name, flags=re.IGNORECASE)

    # Remove "Video completo - " no inicio
    name = re.sub(r'^V[ií]deo\s+completo\s*-?\s*', '', name, flags=re.IGNORECASE)

    # Remove " - Pornhub.com" residual
    name = re.sub(r'\s*-\s*$', '', name)

    # Transliterar cirílico para latin
    cyrillic_map = {
        'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e', 'ё': 'yo',
        'ж': 'zh', 'з': 'z', 'и': 'i', 'й': 'y', 'к': 'k', 'л': 'l', 'м': 'm',
        'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r', 'с': 's', 'т': 't', 'у': 'u',
        'ф': 'f', 'х': 'kh', 'ц': 'ts', 'ч': 'ch', 'ш': 'sh', 'щ': 'shch',
        'ъ': '', 'ы': 'y', 'ь': '', 'э': 'e', 'ю': 'yu', 'я': 'ya',
    }
    transliterated = []
    for char in name:
        lower = char.lower()
        if lower in cyrillic_map:
            mapped = cyrillic_map[lower]
            transliterated.append(mapped.upper() if char.isupper() else mapped)
        else:
            transliterated.append(char)
    name = ''.join(transliterated)

    # Normalizar: remover acentos
    name = unicodedata.normalize('NFD', name)
    name = ''.join(c for c in name if unicodedata.category(c) != 'Mn')

    # Substituir caracteres especiais por underscore
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

    return (name or 'video') + ext


# Executar
renamed = 0
skipped = 0

for root, dirs, files in os.walk(LOCAL_PATH):
    for f in files:
        if not f.lower().endswith(VIDEO_EXTS):
            continue

        old_path = os.path.join(root, f)
        new_name = sanitize_filename(f)

        if new_name == f:
            skipped += 1
            continue

        new_path = os.path.join(root, new_name)

        # Evitar conflito
        if os.path.exists(new_path):
            base, ext = os.path.splitext(new_name)
            counter = 2
            while os.path.exists(new_path):
                new_name = f'{base}_{counter}{ext}'
                new_path = os.path.join(root, new_name)
                counter += 1

        os.rename(old_path, new_path)
        rel_old = os.path.relpath(old_path, LOCAL_PATH)
        print(f'  {rel_old}')
        print(f'    -> {new_name}')
        print()
        renamed += 1

print(f'{"="*60}')
print(f'Renomeados: {renamed}')
print(f'Ja estavam OK: {skipped}')
print(f'Total: {renamed + skipped}')

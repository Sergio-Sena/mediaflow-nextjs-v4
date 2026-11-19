# -*- coding: utf-8 -*-
import os, re, sys, unicodedata
sys.stdout.reconfigure(encoding='utf-8')

PRODUTORAS = [
    'BLACKEDRAW','BLACKED RAW','BLACKED','GIRLSWAY','HouseHumpers','TUSHY',
    'XPERVO','LETSDOEIT','VIXEN','BRAZZERS','SWEET SINNER','ADULT TIME','CUM4K',
    'JULES JORDAN','Jules Jordan','NEW SENSATIONS','PORNPROS','404HotFound'
]
CYRILLIC_MAP = {
    'а':'a','б':'b','в':'v','г':'g','д':'d','е':'e','ё':'yo','ж':'zh','з':'z',
    'и':'i','й':'y','к':'k','л':'l','м':'m','н':'n','о':'o','п':'p','р':'r',
    'с':'s','т':'t','у':'u','ф':'f','х':'kh','ц':'ts','ч':'ch','ш':'sh',
    'щ':'shch','ъ':'','ы':'y','ь':'','э':'e','ю':'yu','я':'ya',
}

def sanitize(filename):
    name, _ = os.path.splitext(filename)
    name = re.sub(r'\s*-?\s*(Pornhub\.com|Pornhub|EPORNER\.COM|xvideos|PornHD)', '', name, flags=re.IGNORECASE)
    name = re.sub(r'\[H69\]', '', name, flags=re.IGNORECASE)
    name = re.sub(r'\[4K\s*\d*FPS\]', '', name, flags=re.IGNORECASE)
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

files = [
    'Daki Fuck Living Room.mp4',
    'Infinitys Pleasure Castle - Part 4 [ENG][H69][4K60FPS].mp4',
    'Mitsuri Infinitys Pleasure Castle [LEGENDADO PT-BR]_2.mp4',
]

for f in files:
    print(f'  {f}')
    print(f'  → {sanitize(f)}\n')

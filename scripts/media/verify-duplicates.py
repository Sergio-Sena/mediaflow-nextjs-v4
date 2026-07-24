# -*- coding: utf-8 -*-
import hashlib
import sys

sys.stdout.reconfigure(encoding='utf-8')

PAIRS = [
    (
        r'C:\Users\dell 5557\Videos\IDM\Star\Kate_Kuray\Kate_Kuray_Football_Practice.mp4',
        r'C:\Users\dell 5557\Videos\IDM\Star\Kate_Kuray\Kate_Kuray_Football_Practice_2.mp4',
    ),
    (
        r'C:\Users\dell 5557\Videos\IDM\Star\Kate_Kuray\KK_-_100424_Deepthroat_And_Cowgirl.mp4',
        r'C:\Users\dell 5557\Videos\IDM\Star\Kate_Kuray\KK_-_100424_Deepthroat_And_Cowgirl_2.mp4',
    ),
]

def partial_hash(path, chunk=8*1024*1024):
    """Hash dos primeiros + últimos 8MB."""
    h = hashlib.md5()
    with open(path, 'rb') as f:
        h.update(f.read(chunk))
        f.seek(-min(chunk, f.seek(0, 2)), 2)
        h.update(f.read(chunk))
    return h.hexdigest()

for a, b in PAIRS:
    ha, hb = partial_hash(a), partial_hash(b)
    identical = ha == hb
    print(f'{"IDÊNTICOS" if identical else "DIFERENTES"}: {a.split(chr(92))[-1]} vs {b.split(chr(92))[-1]}')
    if not identical:
        print(f'  hash A: {ha}')
        print(f'  hash B: {hb}')

# -*- coding: utf-8 -*-
import os
import sys
from collections import defaultdict

sys.stdout.reconfigure(encoding='utf-8')

path = r'C:\Users\dell 5557\Videos\IDM'
exts = ('.mp4', '.ts', '.mkv', '.avi', '.mov', '.webm')

by_name = defaultdict(list)
by_size = defaultdict(list)

for root, _, files in os.walk(path):
    for f in files:
        if f.lower().endswith(exts):
            fp = os.path.join(root, f)
            size = os.path.getsize(fp)
            by_name[f.lower()].append((fp, size))
            by_size[size].append((fp, f))

print('=== DUPLICATAS POR NOME ===')
dups_name = {k: v for k, v in by_name.items() if len(v) > 1}
if dups_name:
    for name, items in dups_name.items():
        print(f'  {name}')
        for fp, size in items:
            print(f'    {fp} ({size/1024**2:.1f} MB)')
else:
    print('  Nenhuma.')

print()
print('=== DUPLICATAS POR TAMANHO ===')
dups_size = {k: v for k, v in by_size.items() if len(v) > 1}
if dups_size:
    for size, items in dups_size.items():
        print(f'  {size/1024**2:.1f} MB')
        for fp, name in items:
            print(f'    {fp}')
else:
    print('  Nenhuma.')

total = sum(len(v) for v in by_name.values())
print(f'\nTotal de arquivos: {total}')

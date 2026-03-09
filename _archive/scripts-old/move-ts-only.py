# -*- coding: utf-8 -*-
import os
import sys
import io
import shutil
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

TS_DIR = r'C:\Users\dell 5557\Videos\IDM\Corporativo\arquivos TS'
STAR_DIR = r'C:\Users\dell 5557\Videos\IDM\Corporativo'

Path(TS_DIR).mkdir(parents=True, exist_ok=True)
moved = 0

print("=" * 60)
print("MOVER ARQUIVOS .TS")
print("=" * 60 + "\n")

for root, dirs, files in os.walk(STAR_DIR):
    if 'arquivos TS' in root:
        continue
    for file in files:
        if file.lower().endswith('.ts'):
            source = os.path.join(root, file)
            dest = os.path.join(TS_DIR, file)
            if source != dest:
                try:
                    shutil.move(source, dest)
                    print(f"  [OK] {file}")
                    moved += 1
                except Exception as e:
                    print(f"  [ERRO] {file}")

print(f"\nTotal: {moved} arquivos .ts movidos")
print("=" * 60)

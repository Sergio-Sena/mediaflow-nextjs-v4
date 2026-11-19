# -*- coding: utf-8 -*-
import shutil, os, sys
sys.stdout.reconfigure(encoding='utf-8')

base = r'C:\Users\dell 5557\Videos\IDM\Anime'
dst  = os.path.join(base, 'Spy_x_Family')
os.makedirs(dst, exist_ok=True)

moved = 0
for f in os.listdir(base):
    full = os.path.join(base, f)
    if os.path.isfile(full) and f.lower().endswith(('.mp4','.ts','.mkv','.avi','.mov','.webm')):
        shutil.move(full, os.path.join(dst, f))
        print(f'Movido: {f}')
        moved += 1

print(f'Total: {moved}')

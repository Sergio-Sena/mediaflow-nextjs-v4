# -*- coding: utf-8 -*-
import os
import subprocess
import sys

sys.stdout.reconfigure(encoding='utf-8')

FFMPEG = r'C:\ffmpeg\bin\ffmpeg.exe'
src = r'C:\Users\dell 5557\Videos\IDM\Star\TUSHY\PRETTY_AND_PETITE_Top_Petite_Model_Compilation_-_Anastasia.ts'
dst = r'C:\Users\dell 5557\Videos\IDM\Star\TUSHY\PRETTY_AND_PETITE_Top_Petite_Model_Compilation_-_Anastasia.mp4'

print(f'Remuxando...')
cmd = [FFMPEG, '-i', src, '-c', 'copy', '-movflags', '+faststart', '-y', dst]
result = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8', errors='ignore')

if result.returncode == 0:
    os.remove(src)
    print(f'OK - {os.path.basename(dst)} ({os.path.getsize(dst)/1024**2:.1f} MB)')
    print(f'Removido: {os.path.basename(src)}')
else:
    print(f'ERRO: {result.stderr[-300:]}')

# -*- coding: utf-8 -*-
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

TO_DELETE = [
    r'C:\Users\dell 5557\Videos\IDM\Star\Kate_Kuray\Kate_Kuray_Football_Practice_2.mp4',
    r'C:\Users\dell 5557\Videos\IDM\Star\Kate_Kuray\KK_-_100424_Deepthroat_And_Cowgirl_2.mp4',
]

for f in TO_DELETE:
    size = os.path.getsize(f) / 1024**2
    os.remove(f)
    print(f'Removido: {os.path.basename(f)} ({size:.1f} MB)')

total = sum(os.path.getsize(f) for f in TO_DELETE if os.path.exists(f))
print(f'\nTotal liberado: ~{(723.7 + 562.6):.1f} MB')

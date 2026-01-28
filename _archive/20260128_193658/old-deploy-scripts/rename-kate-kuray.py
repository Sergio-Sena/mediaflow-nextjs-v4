import os
import re

DIR = r'C:\Users\dell 5557\Videos\IDM\Star\Kate Kuray'

files = os.listdir(DIR)

for filename in files:
    if filename.startswith('EPORNER.COM - '):
        # Remove "EPORNER.COM - [ID] " pattern
        new_name = re.sub(r'^EPORNER\.COM - \[[^\]]+\] ', '', filename)
        
        old_path = os.path.join(DIR, filename)
        new_path = os.path.join(DIR, new_name)
        
        os.rename(old_path, new_path)
        print(f'{filename} -> {new_name}')

print('Renomeacao concluida!')

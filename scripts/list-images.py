import os
from pathlib import Path

folder_path = r"C:\Users\dell 5557\Pictures\imagens devagram"

if not os.path.exists(folder_path):
    print(f"[ERRO] Pasta não encontrada: {folder_path}")
else:
    images = list(Path(folder_path).glob('*.[jJ][pP][gG]')) + \
             list(Path(folder_path).glob('*.[pP][nN][gG]')) + \
             list(Path(folder_path).glob('*.[gG][iI][fF]'))
    
    if not images:
        print(f"Nenhuma imagem encontrada em: {folder_path}")
    else:
        print(f"#SouVoluntario - {len(images)} imagens encontradas:\n")
        for img in sorted(images):
            print(f"  ✓ {img.name}")

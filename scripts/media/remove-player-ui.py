"""
Remove player UI elements from thumbnail using OpenCV inpainting.
Elements to remove: h69 logo, 2 play buttons, volume, time, progress bar, speed, expand, settings
"""
import cv2
import numpy as np

INPUT = r'c:\Projetos Git\MidiaFlow\public\trumbnail.jpg'
OUTPUT = r'c:\Projetos Git\MidiaFlow\public\trumbnail_clean.jpg'
PREVIEW = r'c:\Projetos Git\MidiaFlow\public\trumbnail_preview.jpg'

img = cv2.imread(INPUT)
h, w = img.shape[:2]
print(f"Imagem: {w}x{h}")

# Criar mascara (branco = areas a remover)
mask = np.zeros((h, w), dtype=np.uint8)

# --- Definir regioes dos elementos do player ---

# 1. Logo h69 - canto superior direito (quadrado 125x125)
mask[50:175, w-165:w-40] = 255

# 2. Play central (botao grande no meio da tela)
cx, cy = w // 2, h // 2
mask[cy-45:cy+45, cx-45:cx+45] = 255

# 3. Barra inferior completa (controles: play pequeno, volume, tempo, progress bar, velocidade, config, expand)
# Geralmente ocupa os ultimos ~50-70px da imagem
mask[h-70:h, 0:w] = 255

# --- Preview: mostrar areas marcadas em vermelho ---
preview = img.copy()
preview[mask == 255] = [0, 0, 255]  # vermelho nas areas
cv2.imwrite(PREVIEW, preview)
print(f"Preview salva em: {PREVIEW}")
print("Verifique se as areas vermelhas cobrem os elementos corretos.")
print("Se OK, execute novamente com --apply")

import sys
if '--apply' in sys.argv:
    # Aplicar inpainting
    result = cv2.inpaint(img, mask, inpaintRadius=12, flags=cv2.INPAINT_TELEA)
    cv2.imwrite(OUTPUT, result, [cv2.IMWRITE_JPEG_QUALITY, 95])
    print(f"\nImagem limpa salva em: {OUTPUT}")
else:
    print("\nPara aplicar: python scripts/remove-player-ui.py --apply")

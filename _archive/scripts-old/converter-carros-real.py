#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Conversão REAL com recodificação de áudio para AAC
"""

import subprocess
import sys
import io
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

FFMPEG = r"C:\ffmpeg\bin\ffmpeg.exe"
pasta = Path(r"C:\Users\dell 5557\Videos\Carros")

arquivos = [
    "Carros..mp4",      # Carros 1
    "Carros.3..mp4"     # Carros 3
]

print("=== CONVERSAO REAL (Video copy + Audio AAC) ===\n")

for arquivo in arquivos:
    input_file = pasta / arquivo
    output_file = pasta / f"{arquivo.replace('..', '_fixed.')}"
    
    if not input_file.exists():
        print(f"Nao encontrado: {arquivo}\n")
        continue
    
    print(f"Convertendo: {arquivo}")
    print(f"  -> Video: copy (sem recodificar)")
    print(f"  -> Audio: AAC (compativel web)")
    
    try:
        subprocess.run([
            FFMPEG,
            '-i', str(input_file),
            '-c:v', 'copy',           # Video: copia (rapido)
            '-c:a', 'aac',            # Audio: converte para AAC
            '-b:a', '192k',           # Bitrate audio
            '-y',
            str(output_file)
        ], check=True, capture_output=True)
        
        print(f"  -> OK: {output_file.name}\n")
        
    except Exception as e:
        print(f"  -> ERRO: {e}\n")

print("=== CONCLUIDO ===")
print("\nArquivos gerados:")
print("  - Carros_fixed.mp4")
print("  - Carros.3_fixed.mp4")

# -*- coding: utf-8 -*-
import os
import shutil
from pathlib import Path

TS_DIR = r'C:\Users\dell 5557\Videos\IDM\Corporativo\arquivos TS'
MP4_DIR = r'C:\Users\dell 5557\Videos\IDM\Corporativo\MP4'
STAR_DIR = r'C:\Users\dell 5557\Videos\IDM\Corporativo'

def move_ts_files():
    """Move todos os arquivos .ts de subpastas para arquivos TS"""
    print("[MOVENDO .TS] Procurando arquivos .ts em subpastas...\n")
    
    moved = 0
    
    for root, dirs, files in os.walk(STAR_DIR):
        # Pula a pasta arquivos TS
        if 'arquivos TS' in root:
            continue
        
        for file in files:
            if file.lower().endswith('.ts'):
                source = os.path.join(root, file)
                dest = os.path.join(TS_DIR, file)
                
                try:
                    shutil.move(source, dest)
                    print(f"  ✓ Movido: {file}")
                    moved += 1
                except Exception as e:
                    print(f"  ✗ Erro ao mover {file}: {e}")
    
    print(f"\n[OK] {moved} arquivos .ts movidos para {TS_DIR}\n")
    return moved

def move_mp4_files():
    """Move todos os arquivos .mp4 de subpastas para MP4"""
    print("[MOVENDO .MP4] Procurando arquivos .mp4 em subpastas...\n")
    
    moved = 0
    
    for root, dirs, files in os.walk(STAR_DIR):
        # Pula a pasta MP4
        if 'MP4' in root:
            continue
        
        for file in files:
            if file.lower().endswith('.mp4'):
                source = os.path.join(root, file)
                dest = os.path.join(MP4_DIR, file)
                
                # Se arquivo já existe, adiciona número
                if os.path.exists(dest):
                    name, ext = os.path.splitext(file)
                    counter = 1
                    while os.path.exists(os.path.join(MP4_DIR, f"{name}_{counter}{ext}")):
                        counter += 1
                    dest = os.path.join(MP4_DIR, f"{name}_{counter}{ext}")
                
                try:
                    shutil.move(source, dest)
                    print(f"  ✓ Movido: {file}")
                    moved += 1
                except Exception as e:
                    print(f"  ✗ Erro ao mover {file}: {e}")
    
    print(f"\n[OK] {moved} arquivos .mp4 movidos para {MP4_DIR}\n")
    return moved

def cleanup_empty_dirs():
    """Remove pastas vazias"""
    print("[LIMPEZA] Removendo pastas vazias...\n")
    
    removed = 0
    
    for root, dirs, files in os.walk(STAR_DIR, topdown=False):
        for dir_name in dirs:
            dir_path = os.path.join(root, dir_name)
            
            # Pula pastas importantes
            if 'arquivos TS' in dir_path or 'MP4' in dir_path:
                continue
            
            try:
                if not os.listdir(dir_path):  # Se vazia
                    os.rmdir(dir_path)
                    print(f"  ✓ Removida: {dir_path}")
                    removed += 1
            except Exception as e:
                pass
    
    print(f"\n[OK] {removed} pastas vazias removidas\n")
    return removed

if __name__ == "__main__":
    print("=" * 70)
    print("ORGANIZAÇÃO DE ARQUIVOS")
    print("=" * 70 + "\n")
    
    # Criar pastas se não existirem
    Path(TS_DIR).mkdir(parents=True, exist_ok=True)
    Path(MP4_DIR).mkdir(parents=True, exist_ok=True)
    
    # Mover arquivos
    ts_moved = move_ts_files()
    mp4_moved = move_mp4_files()
    dirs_removed = cleanup_empty_dirs()
    
    # Resumo
    print("=" * 70)
    print("[RESUMO]")
    print(f"  Arquivos .ts movidos: {ts_moved}")
    print(f"  Arquivos .mp4 movidos: {mp4_moved}")
    print(f"  Pastas vazias removidas: {dirs_removed}")
    print("=" * 70)

#!/usr/bin/env python3
"""
Mover todos os arquivos .ts para uma pasta de backup
"""

import os
import shutil
import sys

def mover_arquivos_ts(source_folder):
    """Move todos os arquivos .ts para pasta de backup"""
    
    if not os.path.exists(source_folder):
        print(f"Erro: Pasta nao encontrada: {source_folder}")
        return
    
    # Criar pasta de backup
    backup_folder = os.path.join(source_folder, "_backup_ts_files")
    if not os.path.exists(backup_folder):
        os.makedirs(backup_folder)
        print(f"Pasta de backup criada: {backup_folder}")
    
    print(f"Procurando arquivos .ts em: {source_folder}")
    print("=" * 60)
    
    ts_files = []
    
    # Encontrar todos os arquivos .ts
    for dirpath, dirnames, filenames in os.walk(source_folder):
        # Pular a pasta de backup
        if "_backup_ts_files" in dirpath:
            continue
            
        for filename in filenames:
            if filename.lower().endswith('.ts'):
                full_path = os.path.join(dirpath, filename)
                ts_files.append(full_path)
    
    if not ts_files:
        print("Nenhum arquivo .ts encontrado")
        return
    
    print(f"Encontrados {len(ts_files)} arquivos .ts")
    print()
    
    moved = 0
    errors = 0
    
    for i, ts_file in enumerate(ts_files, 1):
        relative_path = os.path.relpath(ts_file, source_folder)
        filename = os.path.basename(ts_file)
        
        print(f"[{i}/{len(ts_files)}] {relative_path}")
        
        try:
            # Criar estrutura de pastas no backup se necessario
            source_dir = os.path.dirname(ts_file)
            relative_dir = os.path.relpath(source_dir, source_folder)
            
            if relative_dir != ".":
                backup_subdir = os.path.join(backup_folder, relative_dir)
                if not os.path.exists(backup_subdir):
                    os.makedirs(backup_subdir)
                
                destination = os.path.join(backup_subdir, filename)
            else:
                destination = os.path.join(backup_folder, filename)
            
            # Mover arquivo
            shutil.move(ts_file, destination)
            print(f"  Movido para: {os.path.relpath(destination, source_folder)}")
            moved += 1
            
        except Exception as e:
            print(f"  Erro: {e}")
            errors += 1
    
    print()
    print("=" * 60)
    print(f"Operacao concluida!")
    print(f"Movidos: {moved} | Erros: {errors}")
    print(f"Backup em: {backup_folder}")

if __name__ == "__main__":
    folder = r"C:\Users\dell 5557\Videos\IDM"
    
    print("ATENCAO: Esta operacao ira mover todos os arquivos .ts")
    print(f"Da pasta: {folder}")
    print(f"Para: {folder}\\_backup_ts_files\\")
    print()
    
    confirm = input("Deseja continuar? (s/N): ").strip().lower()
    
    if confirm in ['s', 'sim', 'y', 'yes']:
        mover_arquivos_ts(folder)
    else:
        print("Operacao cancelada.")
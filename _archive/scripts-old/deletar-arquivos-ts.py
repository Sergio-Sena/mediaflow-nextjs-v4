#!/usr/bin/env python3
"""
Deletar todos os arquivos .ts
"""

import os
import sys

def deletar_arquivos_ts(source_folder):
    """Deleta todos os arquivos .ts"""
    
    if not os.path.exists(source_folder):
        print(f"Erro: Pasta nao encontrada: {source_folder}")
        return
    
    print(f"Procurando arquivos .ts em: {source_folder}")
    print("=" * 60)
    
    ts_files = []
    
    # Encontrar todos os arquivos .ts
    for dirpath, dirnames, filenames in os.walk(source_folder):
        for filename in filenames:
            if filename.lower().endswith('.ts'):
                full_path = os.path.join(dirpath, filename)
                ts_files.append(full_path)
    
    if not ts_files:
        print("Nenhum arquivo .ts encontrado")
        return
    
    print(f"Encontrados {len(ts_files)} arquivos .ts")
    print()
    
    deleted = 0
    errors = 0
    total_size = 0
    
    for i, ts_file in enumerate(ts_files, 1):
        relative_path = os.path.relpath(ts_file, source_folder)
        
        try:
            # Obter tamanho antes de deletar
            size_mb = os.path.getsize(ts_file) / (1024 * 1024)
            total_size += size_mb
            
            print(f"[{i}/{len(ts_files)}] {relative_path} ({size_mb:.1f} MB)")
            
            # Deletar arquivo
            os.remove(ts_file)
            print(f"  Deletado")
            deleted += 1
            
        except Exception as e:
            print(f"  Erro: {e}")
            errors += 1
    
    print()
    print("=" * 60)
    print(f"Operacao concluida!")
    print(f"Deletados: {deleted} | Erros: {errors}")
    print(f"Espaco liberado: {total_size:.1f} MB ({total_size/1024:.2f} GB)")

if __name__ == "__main__":
    folder = r"C:\Users\dell 5557\Videos\IDM"
    deletar_arquivos_ts(folder)
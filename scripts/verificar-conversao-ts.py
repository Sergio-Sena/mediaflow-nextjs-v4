#!/usr/bin/env python3
"""
Verificar arquivos .ts convertidos para .mp4
"""

import os
import sys

def verificar_conversao(folder_path):
    """Verifica se todos os .ts foram convertidos para .mp4"""
    
    if not os.path.exists(folder_path):
        print(f"Erro: Pasta nao encontrada: {folder_path}")
        return
    
    print(f"Verificando conversoes em: {folder_path}")
    print("=" * 60)
    
    ts_files = []
    mp4_files = []
    
    # Encontrar todos os arquivos .ts e .mp4
    for dirpath, dirnames, filenames in os.walk(folder_path):
        for filename in filenames:
            full_path = os.path.join(dirpath, filename)
            if filename.lower().endswith('.ts'):
                ts_files.append(full_path)
            elif filename.lower().endswith('.mp4'):
                mp4_files.append(full_path)
    
    print(f"Arquivos .ts encontrados: {len(ts_files)}")
    print(f"Arquivos .mp4 encontrados: {len(mp4_files)}")
    print()
    
    # Verificar conversoes
    converted_pairs = []
    missing_mp4 = []
    
    for ts_file in ts_files:
        mp4_file = ts_file.replace('.ts', '.mp4')
        if os.path.exists(mp4_file):
            # Obter tamanhos
            ts_size = os.path.getsize(ts_file) / (1024 * 1024)  # MB
            mp4_size = os.path.getsize(mp4_file) / (1024 * 1024)  # MB
            
            converted_pairs.append({
                'ts': ts_file,
                'mp4': mp4_file,
                'ts_size': ts_size,
                'mp4_size': mp4_size
            })
        else:
            missing_mp4.append(ts_file)
    
    # Relatorio
    if converted_pairs:
        print("ARQUIVOS CONVERTIDOS COM SUCESSO:")
        print("-" * 50)
        for pair in converted_pairs:
            relative_path = os.path.relpath(pair['ts'], folder_path)
            folder_name = os.path.dirname(relative_path)
            filename = os.path.basename(relative_path).replace('.ts', '')
            
            print(f"Pasta: {folder_name}")
            print(f"Arquivo: {filename}")
            print(f"  .ts:  {pair['ts_size']:.1f} MB")
            print(f"  .mp4: {pair['mp4_size']:.1f} MB")
            print()
    
    if missing_mp4:
        print("ARQUIVOS .TS SEM CONVERSAO:")
        print("-" * 50)
        for ts_file in missing_mp4:
            relative_path = os.path.relpath(ts_file, folder_path)
            print(f"  {relative_path}")
        print()
    
    # Resumo final
    print("RESUMO:")
    print("-" * 30)
    print(f"Total .ts: {len(ts_files)}")
    print(f"Convertidos: {len(converted_pairs)}")
    print(f"Pendentes: {len(missing_mp4)}")
    print(f"Taxa de sucesso: {len(converted_pairs)/len(ts_files)*100:.1f}%" if ts_files else "N/A")
    
    # Calcular espaco total
    if converted_pairs:
        total_ts_size = sum(pair['ts_size'] for pair in converted_pairs)
        total_mp4_size = sum(pair['mp4_size'] for pair in converted_pairs)
        
        print(f"\nESPACO UTILIZADO:")
        print(f"Total .ts:  {total_ts_size:.1f} MB")
        print(f"Total .mp4: {total_mp4_size:.1f} MB")
        print(f"Diferenca:  {total_mp4_size - total_ts_size:+.1f} MB")

if __name__ == "__main__":
    folder = r"C:\Users\dell 5557\Videos\IDM"
    verificar_conversao(folder)
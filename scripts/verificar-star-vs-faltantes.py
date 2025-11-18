#!/usr/bin/env python3
"""
Verificar se arquivos faltantes estao na pasta Star
"""

import os
from collections import defaultdict

def get_files_from_folder(folder_path):
    """Obter arquivos de uma pasta"""
    files = []
    
    if not os.path.exists(folder_path):
        return files
    
    for dirpath, dirnames, filenames in os.walk(folder_path):
        for filename in filenames:
            if filename.lower().endswith(('.mp4', '.avi', '.mkv', '.mov')):
                full_path = os.path.join(dirpath, filename)
                relative_path = os.path.relpath(full_path, folder_path)
                
                try:
                    normalized_name = filename.lower().replace(' ', '').replace('_', '').replace('-', '')
                    normalized_name = ''.join(c for c in normalized_name if c.isalnum() or c == '.')
                    
                    files.append({
                        'path': relative_path,
                        'filename': filename,
                        'normalized': normalized_name,
                        'size': os.path.getsize(full_path) / (1024 * 1024)
                    })
                except:
                    continue
    
    return files

def main():
    print("Verificando se arquivos faltantes estao na pasta Star")
    print("=" * 60)
    
    # Pastas
    idm_path = r"C:\Users\dell 5557\Videos\IDM"
    star_path = r"C:\Users\dell 5557\Videos\IDM\Star"
    
    # Obter arquivos
    print("Carregando arquivos IDM (exceto Star)...")
    idm_files = []
    
    for dirpath, dirnames, filenames in os.walk(idm_path):
        # Pular pasta Star
        if "Star" in dirpath:
            continue
            
        for filename in filenames:
            if filename.lower().endswith(('.mp4', '.avi', '.mkv', '.mov')):
                full_path = os.path.join(dirpath, filename)
                relative_path = os.path.relpath(full_path, idm_path)
                
                try:
                    normalized_name = filename.lower().replace(' ', '').replace('_', '').replace('-', '')
                    normalized_name = ''.join(c for c in normalized_name if c.isalnum() or c == '.')
                    
                    idm_files.append({
                        'path': relative_path,
                        'filename': filename,
                        'normalized': normalized_name,
                        'size': os.path.getsize(full_path) / (1024 * 1024)
                    })
                except:
                    continue
    
    print("Carregando arquivos da pasta Star...")
    star_files = get_files_from_folder(star_path)
    
    print(f"Arquivos IDM (sem Star): {len(idm_files)}")
    print(f"Arquivos Star: {len(star_files)}")
    print()
    
    # Criar indices
    star_normalized = {f['normalized'] for f in star_files}
    idm_normalized = {f['normalized'] for f in idm_files}
    
    # Verificar sobreposicao
    overlap = idm_normalized.intersection(star_normalized)
    only_idm = idm_normalized - star_normalized
    only_star = star_normalized - idm_normalized
    
    print("ANALISE DE SOBREPOSICAO:")
    print("-" * 40)
    print(f"Arquivos em ambas as pastas: {len(overlap)}")
    print(f"Apenas em IDM (sem Star): {len(only_idm)}")
    print(f"Apenas em Star: {len(only_star)}")
    print()
    
    # Mostrar arquivos apenas em Star (candidatos para upload)
    if only_star:
        print("ARQUIVOS APENAS EM STAR (CANDIDATOS PARA UPLOAD):")
        print("-" * 50)
        
        # Agrupar por pasta
        star_by_folder = defaultdict(list)
        for file in star_files:
            if file['normalized'] in only_star:
                folder = os.path.dirname(file['path'])
                if not folder:
                    folder = 'root'
                star_by_folder[folder].append(file)
        
        total_size = 0
        total_count = 0
        
        for folder, files in star_by_folder.items():
            print(f"\nPasta Star/{folder} ({len(files)} arquivos)")
            folder_size = 0
            
            for file in files:
                safe_name = file['filename'][:50] + "..." if len(file['filename']) > 50 else file['filename']
                try:
                    print(f"  {safe_name} ({file['size']:.1f} MB)")
                except:
                    print(f"  [arquivo com caracteres especiais] ({file['size']:.1f} MB)")
                
                folder_size += file['size']
                total_size += file['size']
                total_count += 1
            
            print(f"  Subtotal: {folder_size:.1f} MB")
        
        print(f"\nTOTAL STAR EXCLUSIVOS: {total_count} arquivos ({total_size:.1f} MB / {total_size/1024:.2f} GB)")
    
    # Resumo final
    print(f"\nRESUMO:")
    print(f"IDM tem {len(idm_files)} arquivos unicos")
    print(f"Star tem {len(star_files)} arquivos ({len(only_star)} exclusivos)")
    print(f"Sobreposicao: {len(overlap)} arquivos")
    
    if len(only_star) > 0:
        print(f"\nRECOMENDACAO:")
        print(f"Fazer upload dos {len(only_star)} arquivos exclusivos da pasta Star")
        print(f"para completar a colecao do sergio_sena")

if __name__ == "__main__":
    main()
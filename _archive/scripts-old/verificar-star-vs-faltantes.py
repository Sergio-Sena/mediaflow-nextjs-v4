#!/usr/bin/env python3
"""
Verificar se arquivos faltantes estao na pasta Corporativo
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
    print("Verificando se arquivos faltantes estao na pasta Corporativo")
    print("=" * 60)
    
    # Pastas
    idm_path = r"C:\Users\dell 5557\Videos\IDM"
    corporativo_path = r"C:\Users\dell 5557\Videos\IDM\Corporativo"
    
    # Obter arquivos
    print("Carregando arquivos IDM (exceto Corporativo)...")
    idm_files = []
    
    for dirpath, dirnames, filenames in os.walk(idm_path):
        # Pular pasta Corporativo
        if "Corporativo" in dirpath:
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
    
    print("Carregando arquivos da pasta Corporativo...")
    corporativo_files = get_files_from_folder(corporativo_path)
    
    print(f"Arquivos IDM (sem Corporativo): {len(idm_files)}")
    print(f"Arquivos Corporativo: {len(corporativo_files)}")
    print()
    
    # Criar indices
    corporativo_normalized = {f['normalized'] for f in corporativo_files}
    idm_normalized = {f['normalized'] for f in idm_files}
    
    # Verificar sobreposicao
    overlap = idm_normalized.intersection(corporativo_normalized)
    only_idm = idm_normalized - corporativo_normalized
    only_corporativo = corporativo_normalized - idm_normalized
    
    print("ANALISE DE SOBREPOSICAO:")
    print("-" * 40)
    print(f"Arquivos em ambas as pastas: {len(overlap)}")
    print(f"Apenas em IDM (sem Corporativo): {len(only_idm)}")
    print(f"Apenas em Corporativo: {len(only_corporativo)}")
    print()
    
    # Mostrar arquivos apenas em Corporativo (candidatos para upload)
    if only_corporativo:
        print("ARQUIVOS APENAS EM STAR (CANDIDATOS PARA UPLOAD):")
        print("-" * 50)
        
        # Agrupar por pasta
        corporativo_by_folder = defaultdict(list)
        for file in corporativo_files:
            if file['normalized'] in only_corporativo:
                folder = os.path.dirname(file['path'])
                if not folder:
                    folder = 'root'
                corporativo_by_folder[folder].append(file)
        
        total_size = 0
        total_count = 0
        
        for folder, files in corporativo_by_folder.items():
            print(f"\nPasta Corporativo/{folder} ({len(files)} arquivos)")
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
    print(f"Corporativo tem {len(corporativo_files)} arquivos ({len(only_corporativo)} exclusivos)")
    print(f"Sobreposicao: {len(overlap)} arquivos")
    
    if len(only_corporativo) > 0:
        print(f"\nRECOMENDACAO:")
        print(f"Fazer upload dos {len(only_corporativo)} arquivos exclusivos da pasta Corporativo")
        print(f"para completar a colecao do sergio_sena")

if __name__ == "__main__":
    main()
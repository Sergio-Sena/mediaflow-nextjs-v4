import os
import re
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

def sanitize_filename(filename):
    """Remove caracteres especiais e sanitiza nome do arquivo"""
    # Remove emojis e caracteres especiais
    filename = re.sub(r'[^\w\s\-\.]', '', filename)
    # Remove espaços múltiplos
    filename = re.sub(r'\s+', ' ', filename)
    # Remove espaços no início e fim
    filename = filename.strip()
    return filename

def find_files(root_path):
    """Encontra todos os arquivos .ts e .mp4"""
    files = {'ts': [], 'mp4': []}
    for dirpath, dirnames, filenames in os.walk(root_path):
        for filename in filenames:
            full_path = os.path.join(dirpath, filename)
            if filename.lower().endswith('.ts'):
                files['ts'].append(full_path)
            elif filename.lower().endswith('.mp4'):
                files['mp4'].append(full_path)
    return files

def sanitize_and_remove(folder_path):
    """Sanitiza nomes e remove .mp4 convertidos"""
    
    if not os.path.exists(folder_path):
        print(f"Erro: Pasta não encontrada: {folder_path}")
        return
    
    print(f"Analisando pasta: {folder_path}\n")
    print("=" * 80)
    
    files = find_files(folder_path)
    
    print(f"\nArquivos encontrados:")
    print(f"  .ts: {len(files['ts'])}")
    print(f"  .mp4: {len(files['mp4'])}")
    print("\n" + "=" * 80)
    
    # 1. Sanitizar nomes dos arquivos .ts
    print("\n[ETAPA 1] Sanitizando nomes dos arquivos .ts...")
    renamed_ts = 0
    
    for ts_file in files['ts']:
        dir_path = os.path.dirname(ts_file)
        old_name = os.path.basename(ts_file)
        new_name = sanitize_filename(old_name)
        
        if old_name != new_name:
            new_path = os.path.join(dir_path, new_name)
            try:
                os.rename(ts_file, new_path)
                print(f"  Renomeado: {old_name[:50]}... -> {new_name[:50]}...")
                renamed_ts += 1
            except Exception as e:
                print(f"  Erro ao renomear: {e}")
    
    print(f"\nArquivos .ts renomeados: {renamed_ts}")
    
    # 2. Identificar e remover .mp4 convertidos
    print("\n" + "=" * 80)
    print("[ETAPA 2] Identificando .mp4 convertidos...")
    
    # Recarregar lista após renomeação
    files = find_files(folder_path)
    
    ts_basenames = set()
    for ts_file in files['ts']:
        basename = os.path.splitext(os.path.basename(ts_file))[0]
        ts_basenames.add(basename)
    
    mp4_to_remove = []
    mp4_native = []
    
    for mp4_file in files['mp4']:
        basename = os.path.splitext(os.path.basename(mp4_file))[0]
        if basename in ts_basenames:
            mp4_to_remove.append(mp4_file)
        else:
            mp4_native.append(mp4_file)
    
    print(f"\n.mp4 convertidos (serão removidos): {len(mp4_to_remove)}")
    print(f".mp4 nativos (serão mantidos): {len(mp4_native)}")
    
    if mp4_native:
        print("\nArquivos .mp4 nativos que serão MANTIDOS:")
        for mp4 in mp4_native:
            print(f"  ✓ {os.path.basename(mp4)}")
    
    # 3. Remover .mp4 convertidos
    print("\n" + "=" * 80)
    print("[ETAPA 3] Removendo .mp4 convertidos...")
    
    removed = 0
    for mp4_file in mp4_to_remove:
        try:
            os.remove(mp4_file)
            print(f"  Removido: {os.path.basename(mp4_file)[:60]}...")
            removed += 1
        except Exception as e:
            print(f"  Erro ao remover: {e}")
    
    print("\n" + "=" * 80)
    print(f"\nRESUMO:")
    print(f"  Arquivos .ts renomeados: {renamed_ts}")
    print(f"  Arquivos .mp4 removidos: {removed}")
    print(f"  Arquivos .mp4 nativos mantidos: {len(mp4_native)}")
    print("\nPronto para conversão!")

if __name__ == "__main__":
    folder = r"C:\Users\dell 5557\Videos\IDM"
    sanitize_and_remove(folder)

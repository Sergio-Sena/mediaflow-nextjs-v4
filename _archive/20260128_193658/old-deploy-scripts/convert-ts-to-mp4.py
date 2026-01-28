import os
import subprocess
import sys
import io

# Fix encoding for Windows console
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

def find_ts_files(root_path):
    """Encontra todos os arquivos .ts recursivamente"""
    ts_files = []
    for dirpath, dirnames, filenames in os.walk(root_path):
        for filename in filenames:
            if filename.lower().endswith('.ts'):
                full_path = os.path.join(dirpath, filename)
                ts_files.append(full_path)
    return ts_files

def convert_ts_to_mp4(folder_path):
    """Converte todos os arquivos .ts de uma pasta (incluindo subpastas) para .mp4"""
    
    if not os.path.exists(folder_path):
        print(f"Erro: Pasta nao encontrada: {folder_path}")
        return
    
    print(f"Procurando arquivos .ts em: {folder_path}")
    print("Incluindo subpastas...\n")
    
    ts_files = find_ts_files(folder_path)
    
    if not ts_files:
        print("Nenhum arquivo .ts encontrado")
        return
    
    print(f"Encontrados {len(ts_files)} arquivos .ts")
    print("=" * 60)
    
    ffmpeg_path = r"C:\ffmpeg\bin\ffmpeg.exe"
    converted = 0
    skipped = 0
    errors = 0
    
    for i, input_path in enumerate(ts_files, 1):
        output_path = input_path.replace('.ts', '.mp4')
        relative_path = os.path.relpath(input_path, folder_path)
        
        print(f"\n[{i}/{len(ts_files)}] {relative_path}")
        
        if os.path.exists(output_path):
            print(f"  Pulando (ja existe)")
            skipped += 1
            continue
        
        try:
            result = subprocess.run(
                [ffmpeg_path, '-i', input_path, '-c', 'copy', output_path],
                capture_output=True,
                text=True,
                timeout=60
            )
            
            if result.returncode == 0:
                print(f"  Concluido")
                converted += 1
            else:
                print(f"  Erro ao converter")
                errors += 1
                
        except Exception as e:
            print(f"  Erro: {e}")
            errors += 1
    
    print("\n" + "=" * 60)
    print(f"Conversao concluida!")
    print(f"Convertidos: {converted} | Pulados: {skipped} | Erros: {errors}")

if __name__ == "__main__":
    # Caminho padrao
    default_path = r"C:\Users\dell 5557\Videos\IDM"
    
    if len(sys.argv) > 1:
        folder = sys.argv[1]
    else:
        folder = default_path
        print(f"Usando caminho padrao: {folder}")
    
    convert_ts_to_mp4(folder)

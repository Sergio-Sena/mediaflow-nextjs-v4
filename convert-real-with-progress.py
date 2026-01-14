import os
import subprocess
import sys
import io
import re

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

def get_video_duration(file_path, ffmpeg_path):
    """Obtém duração do vídeo em segundos"""
    try:
        result = subprocess.run(
            [ffmpeg_path, '-i', file_path],
            capture_output=True,
            text=True,
            timeout=10
        )
        duration_match = re.search(r'Duration: (\d{2}):(\d{2}):(\d{2})', result.stderr)
        if duration_match:
            h, m, s = map(int, duration_match.groups())
            return h * 3600 + m * 60 + s
    except:
        pass
    return 0

def find_ts_files(root_path):
    """Encontra todos os arquivos .ts recursivamente"""
    ts_files = []
    for dirpath, dirnames, filenames in os.walk(root_path):
        for filename in filenames:
            if filename.lower().endswith('.ts'):
                full_path = os.path.join(dirpath, filename)
                ts_files.append(full_path)
    return ts_files

def convert_with_progress(input_path, output_path, ffmpeg_path, file_num, total_files):
    """Converte com barra de progresso"""
    duration = get_video_duration(input_path, ffmpeg_path)
    
    print(f"\n[{file_num}/{total_files}] Convertendo...")
    print(f"Arquivo: {os.path.basename(input_path)}")
    
    process = subprocess.Popen(
        [ffmpeg_path, '-i', input_path, '-c:v', 'libx264', '-crf', '23', 
         '-preset', 'medium', '-c:a', 'aac', '-b:a', '128k', output_path, '-y'],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        universal_newlines=True,
        encoding='utf-8',
        errors='replace'
    )
    
    for line in process.stdout:
        if 'time=' in line:
            time_match = re.search(r'time=(\d{2}):(\d{2}):(\d{2})', line)
            if time_match and duration > 0:
                h, m, s = map(int, time_match.groups())
                current_time = h * 3600 + m * 60 + s
                progress = min(int((current_time / duration) * 100), 100)
                bar_length = 40
                filled = int(bar_length * progress / 100)
                bar = '█' * filled + '░' * (bar_length - filled)
                print(f'\r  Progresso: [{bar}] {progress}%', end='', flush=True)
    
    process.wait()
    print(f'\r  Progresso: [{"█" * 40}] 100% - Concluído!')
    return process.returncode == 0

def convert_ts_to_mp4(folder_path):
    """Converte todos os arquivos .ts com conversão real"""
    
    if not os.path.exists(folder_path):
        print(f"Erro: Pasta não encontrada: {folder_path}")
        return
    
    print(f"Procurando arquivos .ts em: {folder_path}\n")
    
    ts_files = find_ts_files(folder_path)
    
    if not ts_files:
        print("Nenhum arquivo .ts encontrado")
        return
    
    print(f"Encontrados {len(ts_files)} arquivos .ts")
    print("=" * 60)
    
    ffmpeg_path = r"C:\ffmpeg\bin\ffmpeg.exe"
    converted = 0
    errors = 0
    
    for i, input_path in enumerate(ts_files, 1):
        output_path = input_path.replace('.ts', '.mp4')
        
        try:
            if convert_with_progress(input_path, output_path, ffmpeg_path, i, len(ts_files)):
                converted += 1
            else:
                print(f"  Erro ao converter")
                errors += 1
        except Exception as e:
            print(f"  Erro: {e}")
            errors += 1
    
    print("\n" + "=" * 60)
    print(f"Conversão concluída!")
    print(f"Convertidos: {converted} | Erros: {errors}")

if __name__ == "__main__":
    folder = r"C:\Users\dell 5557\Videos\IDM"
    print(f"Usando caminho: {folder}\n")
    convert_ts_to_mp4(folder)

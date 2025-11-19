# -*- coding: utf-8 -*-
import os
import subprocess
from pathlib import Path

MP4_DIR = r'C:\Users\dell 5557\Videos\IDM\Corporativo\MP4'

def get_video_duration(file_path):
    """Obtém duração do vídeo usando ffprobe"""
    try:
        result = subprocess.run(
            [r'C:\ffmpeg\bin\ffprobe.exe', '-v', 'error', '-show_entries',
             'format=duration', '-of', 'default=noprint_wrappers=1:nokey=1:noprint_wrappers=1',
             file_path],
            capture_output=True,
            text=True,
            timeout=10
        )
        return float(result.stdout.strip())
    except:
        return None

def verify_mp4_integrity(file_path):
    """Verifica integridade do arquivo MP4"""
    try:
        result = subprocess.run(
            [r'C:\ffmpeg\bin\ffmpeg.exe', '-v', 'error', '-i', file_path, '-f', 'null', '-'],
            capture_output=True,
            text=True,
            timeout=30
        )
        return result.returncode == 0
    except:
        return False

def verify_conversions():
    """Verifica todas as conversões"""
    print("=" * 70)
    print("VERIFICAÇÃO DE CONVERSÕES")
    print("=" * 70 + "\n")
    
    mp4_files = sorted(Path(MP4_DIR).glob('*.mp4'))
    
    if not mp4_files:
        print("[ERRO] Nenhum arquivo .mp4 encontrado!")
        return
    
    print(f"Verificando {len(mp4_files)} arquivos .mp4\n")
    
    valid = 0
    invalid = 0
    corrupted = 0
    details = []
    
    for idx, mp4_file in enumerate(mp4_files, 1):
        file_size_mb = mp4_file.stat().st_size / (1024 * 1024)
        duration = get_video_duration(str(mp4_file))
        is_valid = verify_mp4_integrity(str(mp4_file))
        
        status = "✓ OK" if is_valid else "✗ ERRO"
        
        print(f"[{idx}/{len(mp4_files)}] {mp4_file.name}")
        print(f"  Tamanho: {file_size_mb:.2f} MB")
        
        if duration:
            minutes = int(duration // 60)
            seconds = int(duration % 60)
            print(f"  Duração: {minutes}m {seconds}s")
        else:
            print(f"  Duração: Não detectada")
        
        print(f"  Status: {status}\n")
        
        if is_valid:
            valid += 1
            details.append({
                'name': mp4_file.name,
                'size': file_size_mb,
                'duration': duration,
                'status': 'OK'
            })
        else:
            invalid += 1
            details.append({
                'name': mp4_file.name,
                'size': file_size_mb,
                'duration': duration,
                'status': 'ERRO'
            })
    
    # Resumo
    print("=" * 70)
    print("[RESUMO]")
    print(f"  Total de arquivos: {len(mp4_files)}")
    print(f"  Válidos: {valid} ✓")
    print(f"  Inválidos: {invalid} ✗")
    print(f"  Taxa de sucesso: {(valid/len(mp4_files)*100):.1f}%")
    print("=" * 70)
    
    # Detalhes dos inválidos
    if invalid > 0:
        print("\n[ARQUIVOS COM ERRO]")
        for detail in details:
            if detail['status'] == 'ERRO':
                print(f"  - {detail['name']}")
    
    return valid, invalid

if __name__ == "__main__":
    verify_conversions()

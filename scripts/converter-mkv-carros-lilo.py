#!/usr/bin/env python3
"""
Converte arquivos MKV para MP4 nas pastas Carros e Lilo & Stitch
"""

import os
import subprocess
from pathlib import Path

def converter_mkv_para_mp4(pasta_base):
    """Converte todos os MKV de uma pasta para MP4"""
    
    pasta = Path(pasta_base)
    
    if not pasta.exists():
        print(f"❌ Pasta não encontrada: {pasta}")
        return
    
    # Encontrar todos os MKV
    arquivos_mkv = list(pasta.rglob('*.mkv'))
    
    if not arquivos_mkv:
        print(f"✅ Nenhum arquivo MKV encontrado em {pasta.name}")
        return
    
    print(f"\n📁 {pasta.name}")
    print(f"   Encontrados: {len(arquivos_mkv)} arquivos MKV")
    print("-" * 60)
    
    ffmpeg_path = r"C:\ffmpeg\bin\ffmpeg.exe"
    convertidos = 0
    pulados = 0
    erros = 0
    
    for i, mkv_path in enumerate(arquivos_mkv, 1):
        mp4_path = mkv_path.with_suffix('.mp4')
        
        # Verificar se já existe
        if mp4_path.exists():
            print(f"⏭️  [{i}/{len(arquivos_mkv)}] Já existe: {mkv_path.name}")
            pulados += 1
            continue
        
        print(f"\n🔄 [{i}/{len(arquivos_mkv)}] Convertendo: {mkv_path.name}")
        print(f"   Tamanho: {mkv_path.stat().st_size / (1024**3):.2f} GB")
        
        try:
            # Converter com ffmpeg (copia streams, rápido)
            resultado = subprocess.run(
                [
                    ffmpeg_path,
                    '-i', str(mkv_path),
                    '-c', 'copy',  # Copia sem recodificar (rápido)
                    '-y',  # Sobrescrever se existir
                    str(mp4_path)
                ],
                capture_output=True,
                text=True,
                timeout=3600  # 1 hora timeout
            )
            
            if resultado.returncode == 0:
                print(f"✅ Convertido: {mp4_path.name}")
                convertidos += 1
            else:
                print(f"❌ Erro na conversão")
                erros += 1
                
        except subprocess.TimeoutExpired:
            print(f"⏱️ Timeout - arquivo muito grande")
            erros += 1
        except Exception as e:
            print(f"❌ Erro: {e}")
            erros += 1
    
    print(f"\n✅ {pasta.name}: {convertidos} convertidos | {pulados} já existiam | {erros} erros")

def main():
    print("=" * 60)
    print("🎬 CONVERSÃO MKV → MP4")
    print("=" * 60)
    
    base_path = r"C:\Users\dell 5557\Videos"
    
    # Converter Carros
    converter_mkv_para_mp4(os.path.join(base_path, "Carros"))
    
    # Converter Lilo & Stitch
    converter_mkv_para_mp4(os.path.join(base_path, "Lilo & Stitch"))
    
    print("\n" + "=" * 60)
    print("✅ CONVERSÃO CONCLUÍDA!")
    print("=" * 60)
    print("\nAgora execute: python scripts\\upload-lid-lima-pastas.py")

if __name__ == "__main__":
    main()

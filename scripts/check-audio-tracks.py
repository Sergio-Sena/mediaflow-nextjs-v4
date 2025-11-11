import subprocess
import json
from pathlib import Path

VIDEO_PATH = r'C:\Users\dell 5557\Downloads\Video'

def check_audio_tracks(video_file):
    """Verifica quantas faixas de audio tem o video"""
    try:
        result = subprocess.run([
            'ffprobe',
            '-v', 'quiet',
            '-print_format', 'json',
            '-show_streams',
            str(video_file)
        ], capture_output=True, text=True)
        
        data = json.loads(result.stdout)
        audio_streams = [s for s in data.get('streams', []) if s['codec_type'] == 'audio']
        
        return len(audio_streams), audio_streams
    except:
        return 0, []

print("="*80)
print("VERIFICANDO FAIXAS DE AUDIO")
print("="*80)

# Verificar alguns videos
videos = list(Path(VIDEO_PATH).rglob('*.mp4'))[:10]

for video in videos:
    count, streams = check_audio_tracks(video)
    
    if count > 1:
        print(f"\n[MULTIPLAS FAIXAS] {video.name}")
        print(f"  Total: {count} faixas de audio")
        for i, stream in enumerate(streams, 1):
            lang = stream.get('tags', {}).get('language', 'unknown')
            print(f"    {i}. Idioma: {lang}")
    elif count == 1:
        print(f"\n[1 FAIXA] {video.name}")
    else:
        print(f"\n[SEM AUDIO] {video.name}")

print("\n" + "="*80)
print("Se encontrou videos com MULTIPLAS FAIXAS:")
print("  -> Player ja funciona automaticamente!")
print("\nSe todos tem 1 FAIXA:")
print("  -> Precisa implementar seletor manual")

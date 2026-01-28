import subprocess
import os

input_file = r'C:\Users\dell 5557\Videos\Moana.Um.Mar.de.Aventuras\Moana.Um.Mar.de.Aventuras.2017.1080p.BluRay.DD5.1.x264.DUAL-TDF.mp4'
output_file = r'C:\Users\dell 5557\Videos\Moana.Um.Mar.de.Aventuras\Moana.1.Um.Mar.de.Aventuras.2017.mp4'

if not os.path.exists(input_file):
    print(f"ERRO: Arquivo nao encontrado: {input_file}")
    exit(1)

print("Tentando usar ffmpeg...")
cmd = [
    'ffmpeg',
    '-i', input_file,
    '-c:v', 'copy',
    '-c:a', 'aac',
    '-b:a', '192k',
    '-movflags', '+fastcorporativot',
    output_file
]

try:
    subprocess.run(cmd, check=True)
    print(f"\nConversao concluida: {output_file}")
except FileNotFoundError:
    print("\nERRO: ffmpeg nao encontrado.")
    print("Baixe em: https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip")
    print("Extraia e adicione ao PATH do Windows")
except Exception as e:
    print(f"ERRO: {e}")

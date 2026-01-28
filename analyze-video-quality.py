import boto3
import re

S3_BUCKET = "mediaflow-uploads-969430605054"
S3_PREFIX = "users/sergio_sena/"

s3 = boto3.client('s3')

# Bitrate esperado por resolução (Mbps)
EXPECTED_BITRATE = {
    '480': 2.5,
    '720': 5.0,
    '1080': 8.0,
    '1440': 16.0,
    '2160': 35.0  # 4K
}

def extract_resolution(filename):
    """Extrai resolução do nome do arquivo"""
    match = re.search(r'\((\d+)p?\)', filename, re.IGNORECASE)
    if match:
        return match.group(1)
    if '4K' in filename.upper():
        return '2160'
    return None

def calculate_bitrate(file_size, duration_estimate=300):
    """Calcula bitrate aproximado (assumindo 5min de vídeo)"""
    # file_size em bytes, duration em segundos
    bitrate_bps = (file_size * 8) / duration_estimate
    bitrate_mbps = bitrate_bps / 1_000_000
    return bitrate_mbps

def analyze_quality(filename, file_size, resolution):
    """Analisa se qualidade está suspeita"""
    if not resolution or resolution not in EXPECTED_BITRATE:
        return None, None
    
    expected = EXPECTED_BITRATE[resolution]
    actual = calculate_bitrate(file_size)
    
    # Se bitrate real é < 60% do esperado, qualidade suspeita
    threshold = expected * 0.6
    
    if actual < threshold:
        return 'RUIM', f'{actual:.1f} Mbps (esperado: {expected} Mbps)'
    elif actual < expected * 0.8:
        return 'BAIXA', f'{actual:.1f} Mbps (esperado: {expected} Mbps)'
    else:
        return 'BOA', f'{actual:.1f} Mbps'

print("=" * 100)
print("ANALISE DE QUALIDADE DE VIDEOS - S3")
print("=" * 100)
print(f"\nBucket: {S3_BUCKET}")
print(f"Prefix: {S3_PREFIX}")
print("\nAnalisando videos...\n")

videos_ruins = []
videos_baixa = []
videos_bons = []
sem_resolucao = []

try:
    paginator = s3.get_paginator('list_objects_v2')
    for page in paginator.paginate(Bucket=S3_BUCKET, Prefix=S3_PREFIX):
        if 'Contents' in page:
            for obj in page['Contents']:
                key = obj['Key']
                filename = key.split('/')[-1]
                
                # Apenas vídeos
                if not filename.lower().endswith(('.mp4', '.webm', '.mov', '.avi', '.mkv')):
                    continue
                
                file_size = obj['Size']
                resolution = extract_resolution(filename)
                
                if not resolution:
                    sem_resolucao.append({
                        'file': filename,
                        'size': file_size,
                        'size_mb': file_size / (1024**2)
                    })
                    continue
                
                quality, details = analyze_quality(filename, file_size, resolution)
                
                video_info = {
                    'file': filename,
                    'resolution': resolution + 'p',
                    'size': file_size,
                    'size_mb': file_size / (1024**2),
                    'details': details,
                    'key': key
                }
                
                if quality == 'RUIM':
                    videos_ruins.append(video_info)
                elif quality == 'BAIXA':
                    videos_baixa.append(video_info)
                elif quality == 'BOA':
                    videos_bons.append(video_info)

except Exception as e:
    print(f"ERRO: {e}")
    exit(1)

# Ordenar por tamanho (menores primeiro = mais suspeitos)
videos_ruins.sort(key=lambda x: x['size'])
videos_baixa.sort(key=lambda x: x['size'])

print("=" * 100)
print("RESULTADOS DA ANALISE")
print("=" * 100)

# Vídeos com qualidade RUIM
if videos_ruins:
    print(f"\n[CRITICO] VIDEOS COM QUALIDADE RUIM: {len(videos_ruins)}")
    print("-" * 100)
    print("Estes videos tem bitrate muito abaixo do esperado. RECOMENDADO: Re-upload do original\n")
    
    for i, v in enumerate(videos_ruins[:20], 1):  # Mostrar top 20
        print(f"[{i}] {v['resolution']} - {v['size_mb']:.1f} MB")
        print(f"    {v['file'][:80]}")
        print(f"    Bitrate: {v['details']}")
        print()

# Vídeos com qualidade BAIXA
if videos_baixa:
    print(f"\n[ATENCAO] VIDEOS COM QUALIDADE BAIXA: {len(videos_baixa)}")
    print("-" * 100)
    print("Estes videos tem bitrate abaixo do ideal. CONSIDERE: Re-upload se tiver original melhor\n")
    
    for i, v in enumerate(videos_baixa[:10], 1):  # Mostrar top 10
        print(f"[{i}] {v['resolution']} - {v['size_mb']:.1f} MB")
        print(f"    {v['file'][:80]}")
        print(f"    Bitrate: {v['details']}")
        print()

# Vídeos sem resolução no nome
if sem_resolucao:
    print(f"\n[INFO] VIDEOS SEM RESOLUCAO NO NOME: {len(sem_resolucao)}")
    print("-" * 100)
    print("Nao foi possivel determinar qualidade (sem resolucao no nome)\n")
    
    for i, v in enumerate(sem_resolucao[:10], 1):
        print(f"[{i}] {v['size_mb']:.1f} MB - {v['file'][:80]}")

print("\n" + "=" * 100)
print("RESUMO")
print("=" * 100)
print(f"\nQualidade RUIM (re-upload recomendado): {len(videos_ruins)}")
print(f"Qualidade BAIXA (considerar re-upload): {len(videos_baixa)}")
print(f"Qualidade BOA: {len(videos_bons)}")
print(f"Sem resolucao no nome: {len(sem_resolucao)}")
print(f"\nTotal de videos analisados: {len(videos_ruins) + len(videos_baixa) + len(videos_bons) + len(sem_resolucao)}")

# Salvar lista completa em arquivo
if videos_ruins or videos_baixa:
    with open('videos-qualidade-suspeita.txt', 'w', encoding='utf-8') as f:
        f.write("VIDEOS COM QUALIDADE SUSPEITA - RE-UPLOAD RECOMENDADO\n")
        f.write("=" * 100 + "\n\n")
        
        if videos_ruins:
            f.write(f"QUALIDADE RUIM ({len(videos_ruins)} videos):\n")
            f.write("-" * 100 + "\n")
            for v in videos_ruins:
                f.write(f"{v['resolution']} - {v['size_mb']:.1f} MB - {v['details']}\n")
                f.write(f"  {v['file']}\n")
                f.write(f"  S3: {v['key']}\n\n")
        
        if videos_baixa:
            f.write(f"\nQUALIDADE BAIXA ({len(videos_baixa)} videos):\n")
            f.write("-" * 100 + "\n")
            for v in videos_baixa:
                f.write(f"{v['resolution']} - {v['size_mb']:.1f} MB - {v['details']}\n")
                f.write(f"  {v['file']}\n")
                f.write(f"  S3: {v['key']}\n\n")
    
    print(f"\nLista completa salva em: videos-qualidade-suspeita.txt")

print("\n" + "=" * 100)

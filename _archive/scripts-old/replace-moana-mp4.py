import os
import boto3

s3 = boto3.client('s3', region_name='us-east-1')
BUCKET = 'mediaflow-uploads-969430605054'

files = [
    {
        'local': r'C:\Users\dell 5557\Videos\Moana.2\Moana.Um.Mar.de.Aventuras.2017.1080p.BluRay.DD5.1.x264.DUAL-TDF.mp4',
        's3_key': 'users/lid_lima/Moana.2/Moana.Um.Mar.de.Aventuras.2017.1080p.BluRay.DD5.1.x264.DUAL-TDF.mp4',
        'old_key': 'users/lid_lima/Moana.2/Moana.2.2024.1080p.WEB-DL.DUAL.5.1.mkv'
    },
    {
        'local': r'C:\Users\dell 5557\Videos\Moana.Um.Mar.de.Aventuras\Moana.2.2024.1080p.WEB-DL.DUAL.5.1.mp4',
        's3_key': 'users/lid_lima/Moana.Um.Mar.de.Aventuras/Moana.2.2024.1080p.WEB-DL.DUAL.5.1.mp4',
        'old_key': 'users/lid_lima/Moana.Um.Mar.de.Aventuras/Moana.Um.Mar.de.Aventuras.2017.1080p.BluRay.DD5.1.x264.DUAL-TDF.mkv'
    }
]

print('Substituindo MKV por MP4 convertidos...')
print('=' * 70)

for f in files:
    size_gb = os.path.getsize(f['local']) / (1024**3)
    print(f'\n[1/3] Deletando MKV antigo: {f["old_key"]}')
    
    try:
        s3.delete_object(Bucket=BUCKET, Key=f['old_key'])
        print('  [OK] Deletado')
    except Exception as e:
        print(f'  [AVISO] {e}')
    
    print(f'[2/3] Uploading MP4 novo ({size_gb:.2f} GB): {os.path.basename(f["local"])}')
    
    try:
        s3.upload_file(f['local'], BUCKET, f['s3_key'])
        print('  [OK] Upload concluido')
    except Exception as e:
        print(f'  [ERRO] {e}')
        continue

print('\n' + '=' * 70)
print('Substituicao concluida!')

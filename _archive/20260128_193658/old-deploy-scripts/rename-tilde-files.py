import boto3

s3 = boto3.client('s3', region_name='us-east-1')
bucket = 'mediaflow-uploads-969430605054'

files_with_tilde = [
    'users/lid_lima/Lilo & Stitch/Lilo & Stitch 2025 WEB-DL 1080p x264 DUAL 5.1~1.mp4',
    'users/sergio_sena/Carros 2~1.mp4',
    'users/sergio_sena/Carros.3.~1.mp4',
    'users/sergio_sena/Carros.~1.mp4',
    'users/sergio_sena/Lilo & Stitch 2 - Stitch Deu Defeito 2005 WEB-DL 1080p x264 DUAL 5.1~1.mp4',
    'users/sergio_sena/Lilo & Stitch 2002 WEB-DL 1080p x264 DUAL 5.1~1.mp4',
    'users/sergio_sena/Lilo & Stitch 2025 WEB-DL 1080p x264 DUAL 5.1~1.mp4',
    'users/sergio_sena/Star/Lil Karina/Gata Asiatica Fofa e Pau Branco - Pornhub.com~1.mp4',
    'users/sergio_sena/Star/MIRARI HUB/Seduction of a Cute Tutor - MIRARI - Pornhub.com~1.mp4',
    'users/sergio_sena/Star/anastangel/Busty Step Sis Suga e e Fodida com Forca - Anastangel - Family Fun - Pornhub.com~1.mp4'
]

print(f"Renomeando {len(files_with_tilde)} arquivos...\n")

for i, old_key in enumerate(files_with_tilde, 1):
    new_key = old_key.replace('~1', '')
    
    try:
        # Copiar para novo nome
        s3.copy_object(
            Bucket=bucket,
            CopySource={'Bucket': bucket, 'Key': old_key},
            Key=new_key
        )
        
        # Deletar arquivo antigo
        s3.delete_object(Bucket=bucket, Key=old_key)
        
        print(f"[{i}/{len(files_with_tilde)}] OK: {old_key.split('/')[-1]}")
        print(f"         -> {new_key.split('/')[-1]}\n")
        
    except Exception as e:
        print(f"ERRO: {old_key}")
        print(f"   {str(e)}\n")

print("Concluído!")

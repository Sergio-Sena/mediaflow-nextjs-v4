# -*- coding: utf-8 -*-
import boto3
import sys
sys.stdout.reconfigure(encoding='utf-8')

s3 = boto3.client('s3', region_name='us-east-1')
bucket = 'mediaflow-uploads-969430605054'
paginator = s3.get_paginator('list_objects_v2')

print('=' * 60)
print('ETAPA 1: Mover Mitsuri para Kimetsu_No_Yaba')
print('=' * 60)

old_key = 'users/sergio_sena/Anime/Mitsuri_Infinitys_Pleasure_Castle.mp4'
new_key = 'users/sergio_sena/Anime/Kimetsu_No_Yaba/Mitsuri_Infinitys_Pleasure_Castle.mp4'

print(f'  Copiando: {old_key}')
print(f'       ->   {new_key}')
s3.copy_object(
    Bucket=bucket,
    CopySource={'Bucket': bucket, 'Key': old_key},
    Key=new_key
)
s3.delete_object(Bucket=bucket, Key=old_key)
print('  OK\n')

print('=' * 60)
print('ETAPA 2: Colocar thumbnail como capa (path correto)')
print('=' * 60)

# A thumbnail deve ficar em public/thumbnails/{user}/{path}/{filename}.jpg
thumb_src = r'C:\Users\dell 5557\Videos\IDM\Anime\Kimetsu_No_Yaba\Mitsuri_Infinitys_Pleasure_Castle_thumbnail.jpg'
thumb_s3_key = 'public/thumbnails/sergio_sena/Anime/Kimetsu_No_Yaba/Mitsuri_Infinitys_Pleasure_Castle.jpg'

print(f'  Enviando thumbnail para: {thumb_s3_key}')
s3.upload_file(thumb_src, bucket, thumb_s3_key, ExtraArgs={'ContentType': 'image/jpeg'})
print('  OK')

# Remover thumbnail antiga na pasta errada
old_thumb = 'users/sergio_sena/Anime/thumbnails/Mitsuri_Infinitys_Pleasure_Castle_thumbnail.jpg'
try:
    s3.delete_object(Bucket=bucket, Key=old_thumb)
    print(f'  Removida thumb antiga: {old_thumb}')
except:
    pass
print()

print('=' * 60)
print('ETAPA 3: Mover AniButler -> Star/AniButler')
print('=' * 60)

anibutler_files = []
for page in paginator.paginate(Bucket=bucket, Prefix='users/sergio_sena/AniButler/'):
    for obj in page.get('Contents', []):
        anibutler_files.append(obj['Key'])

print(f'  {len(anibutler_files)} arquivos para mover')
for old in anibutler_files:
    filename = old.split('/')[-1]
    new = f'users/sergio_sena/Star/AniButler/{filename}'
    print(f'  {filename} -> Star/AniButler/')
    s3.copy_object(Bucket=bucket, CopySource={'Bucket': bucket, 'Key': old}, Key=new)
    s3.delete_object(Bucket=bucket, Key=old)

print('  OK\n')

print('=' * 60)
print('TUDO PRONTO!')
print('=' * 60)
print(f'\nVideo: {new_key}')
print(f'Thumbnail (capa): {thumb_s3_key}')
print(f'AniButler movido para Star/AniButler/')

import boto3
import sys

s3 = boto3.client('s3')
BUCKET = 'mediaflow-uploads-969430605054'

# Arquivos para deletar
DELETE_FILES = [
    'users/user_admin/Corporativo/Captures/V_deo_de_show_musical_na_cidade.mp4',
    'users/user_admin/Video/SergioSenaTeste.mp4',
    'users/user_admin/Anime/Street_Fighter/....mp4',
    'users/user_admin/Corporativo/angelica/WOWGIRLS.COM_Two_horny_h....mp4',
    'users/user_admin/Anime/Jiggly Girls [Hentai on Brasil]/Imagem (3).jpg',
    'users/user_admin/Anime/Jiggly Girls [Hentai on Brasil]/Imagem (4).jpg',
    'users/user_admin/Anime/Jiggly Girls [Hentai on Brasil]/Imagem (5).jpg',
    'users/user_admin/Anime/Jiggly Girls [Hentai on Brasil]/Imagem (6).jpg',
    'users/user_admin/Anime/Jiggly Girls [Hentai on Brasil]/Imagem (7).jpg',
]

# Renomear
RENAME = {
    'users/user_admin/Anime/Monster_Hunter/....mp4': 'users/user_admin/Anime/Monster_Hunter/double_toys.mp4'
}

# Verificar fotos de perfil
CHECK_PROFILE = [
    'users/lid_lima/Fotos_Lid/IMG_20190210_162038.jpg',
    'users/lid_lima/IMG_20190210_162038.jpg'
]

print("Verificando fotos de perfil...")
for key in CHECK_PROFILE:
    try:
        response = s3.head_object(Bucket=BUCKET, Key=key)
        print(f"[OK] Existe: {key} ({response['ContentLength']} bytes)")
    except:
        print(f"[X] Nao existe: {key}")

# Verificar se é avatar
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('mediaflow-users')
response = table.get_item(Key={'user_id': 'lid_lima'})
avatar = response.get('Item', {}).get('avatar_url', '')
print(f"\nAvatar lid_lima: {avatar}")

if 'IMG_20190210_162038.jpg' in avatar:
    print("[!] FOTO E AVATAR! Nao deletar.")
else:
    print("[OK] Foto NAO e avatar. Pode deletar ambas.")
    DELETE_FILES.extend(CHECK_PROFILE)

print(f"\nDeletando {len(DELETE_FILES)} arquivos...")
for key in DELETE_FILES:
    try:
        s3.delete_object(Bucket=BUCKET, Key=key)
        print(f"[OK] Deletado: {key}")
    except Exception as e:
        print(f"[X] Erro ao deletar {key}: {e}")

print(f"\nRenomeando {len(RENAME)} arquivo(s)...")
for old_key, new_key in RENAME.items():
    try:
        s3.copy_object(Bucket=BUCKET, CopySource={'Bucket': BUCKET, 'Key': old_key}, Key=new_key)
        s3.delete_object(Bucket=BUCKET, Key=old_key)
        print(f"[OK] Renomeado: {old_key} -> {new_key}")
    except Exception as e:
        print(f"[X] Erro ao renomear {old_key}: {e}")

print("\n[OK] Limpeza concluida!")

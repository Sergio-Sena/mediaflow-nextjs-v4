import os
import re
import unicodedata
import boto3
from concurrent.futures import ThreadPoolExecutor, as_completed

# Config
SOURCE_BUCKET = 'smarthophone'
DEST_BUCKET = 'mediaflow-uploads-969430605054'
SOURCE_REGION = 'sa-east-1'
DEST_REGION = 'us-east-1'
MAX_WORKERS = 10
LOCAL_DOWNLOAD_DIR = r'C:\Users\dell 5557\Videos\IDM\Wattsup'

s3_source = boto3.client('s3', region_name=SOURCE_REGION)
s3_dest = boto3.client('s3', region_name=DEST_REGION)

# Mapping: (source_prefix, dest_prefix)
MIGRATIONS = [
    # VideoDownloader
    ('backup_xioami_redmi_note_8/VideoDownloader/Anime/MMD/', 'users/sergio_sena/Anime/Outros/'),
    ('backup_xioami_redmi_note_8/VideoDownloader/Anime/Vídeos/', 'users/sergio_sena/Anime/Outros/'),
    ('backup_xioami_redmi_note_8/VideoDownloader/kate kuray/', 'users/sergio_sena/Star/Kate_Kuray/'),
    ('backup_xioami_redmi_note_8/VideoDownloader/Mia Malkova/', 'users/sergio_sena/Star/MiaMalkova/'),
    ('backup_xioami_redmi_note_8/VideoDownloader/megan/', 'users/sergio_sena/Star/megan/'),
    ('backup_xioami_redmi_note_8/VideoDownloader/Lana compilation/', 'users/sergio_sena/Star/Lana/'),
    ('backup_xioami_redmi_note_8/VideoDownloader/angelica/', 'users/sergio_sena/Star/angelica/'),
    ('backup_xioami_redmi_note_8/VideoDownloader/Asa akira/', 'users/sergio_sena/Star/Asa_akira/'),
    ('backup_xioami_redmi_note_8/VideoDownloader/compilation/', 'users/sergio_sena/Star/compilation/'),
    ('backup_xioami_redmi_note_8/VideoDownloader/Outros/', 'users/sergio_sena/Star/Outros/'),
    ('backup_xioami_redmi_note_8/VideoDownloader/Deeper/', 'users/sergio_sena/Star/Outros/'),
    ('backup_xioami_redmi_note_8/VideoDownloader/maior/', 'users/sergio_sena/Star/Outros/'),
    ('backup_xioami_redmi_note_8/VideoDownloader/pos converter/', 'users/sergio_sena/Star/Outros/'),
    ('backup_xioami_redmi_note_8/VideoDownloader/google fotos/', 'users/sergio_sena/Star/Outros/'),
    ('backup_xioami_redmi_note_8/VideoDownloader/BelleDelphine/', 'users/sergio_sena/Star/BelleDelphine/'),
    ('backup_xioami_redmi_note_8/VideoDownloader/Gia Paig/', 'users/sergio_sena/Star/Gia_Paige/'),
    ('backup_xioami_redmi_note_8/VideoDownloader/meru/', 'users/sergio_sena/Anime/Meru_Succubus/'),
    # Xiaomi
    ('Xiaomi/xiaomi media/videos/FinalFantasy/', 'users/sergio_sena/Anime/Final_Fantasy/'),
    ('Xiaomi/xiaomi media/videos/Nier/', 'users/sergio_sena/Anime/2b_Nier_Automata/'),
    ('Xiaomi/xiaomi media/videos/Othes/', 'users/sergio_sena/Anime/Outros/'),
    # Videos v2
    ('Videos/Videos/Vidoes v2/Anime/', 'users/sergio_sena/Anime/Outros/'),
    ('Videos/Videos/Vidoes v2/Blacked/', 'users/sergio_sena/Star/blacked/'),
    ('Videos/Videos/Vidoes v2/DP/', 'users/sergio_sena/Star/Outros/'),
    ('Videos/Videos/Vidoes v2/Star/', 'users/sergio_sena/Star/Outros/'),
]

# Skip these (already migrated or not video)
SKIP_PREFIXES = [
    'backup_xioami_redmi_note_8/VideoDownloader/Charming/',
    'backup_xioami_redmi_note_8/VideoDownloader/EmillyaBunny/',
]

# Download locally instead of S3->S3
LOCAL_DOWNLOADS = [
    'backup_xioami_redmi_note_8/VideoDownloader/Pequenos/',
]

VIDEO_EXTENSIONS = ('.mp4', '.mkv', '.avi', '.mov', '.ts')

def sanitize(name):
    n = os.path.splitext(name)[0]
    ext = os.path.splitext(name)[1].lower()
    # Normalize and remove accents
    n = unicodedata.normalize('NFD', n)
    n = re.sub(r'[\u0300-\u036f]', '', n)
    # Remove emojis and non-ASCII
    n = re.sub(r'[^\x20-\x7E]', '', n)
    # Remove common junk
    n = re.sub(r'\s*-?\s*Pornhub\.com', '', n, flags=re.IGNORECASE)
    n = re.sub(r'\(\d+_P\)', '', n)
    n = re.sub(r'\(\d+P\)', '', n)
    n = re.sub(r"[&?!,#':;\"^()\[\]]", '', n)
    n = re.sub(r'\.+', '_', n)
    n = re.sub(r'[\s\-]+', '_', n)
    n = re.sub(r'_+', '_', n)
    n = n.strip('_')
    if len(n) > 60:
        n = n[:60].rstrip('_')
    if not n:
        n = 'unnamed'
    return n + (ext if ext in VIDEO_EXTENSIONS else '.mp4')

def dest_exists(key):
    try:
        s3_dest.head_object(Bucket=DEST_BUCKET, Key=key)
        return True
    except:
        return False

def copy_s3_to_s3(source_key, dest_key):
    copy_source = {'Bucket': SOURCE_BUCKET, 'Key': source_key}
    s3_dest.copy(copy_source, DEST_BUCKET, dest_key,
                 SourceClient=s3_source)

def process_migration(source_key, dest_prefix):
    filename = source_key.split('/')[-1]
    if not filename.lower().endswith(VIDEO_EXTENSIONS):
        return 'skip_ext'
    
    sanitized = sanitize(filename)
    dest_key = dest_prefix + sanitized
    
    if dest_exists(dest_key):
        return 'exists'
    
    try:
        copy_s3_to_s3(source_key, dest_key)
        return 'ok'
    except Exception as e:
        print(f"  [ERR] {source_key}: {str(e)[:80]}")
        return 'error'

def download_local(source_key, local_dir):
    filename = source_key.split('/')[-1]
    local_path = os.path.join(local_dir, filename)
    if os.path.exists(local_path):
        return 'exists'
    try:
        s3_source.download_file(SOURCE_BUCKET, source_key, local_path)
        return 'ok'
    except Exception as e:
        print(f"  [ERR] Download {filename}: {str(e)[:80]}")
        return 'error'

def list_objects(prefix):
    paginator = s3_source.get_paginator('list_objects_v2')
    objects = []
    for page in paginator.paginate(Bucket=SOURCE_BUCKET, Prefix=prefix):
        for obj in page.get('Contents', []):
            objects.append(obj['Key'])
    return objects

def main():
    print("=" * 60)
    print("MIGRACAO S3 -> MidiaFlow")
    print(f"Origem: {SOURCE_BUCKET} ({SOURCE_REGION})")
    print(f"Destino: {DEST_BUCKET} ({DEST_REGION})")
    print("=" * 60)

    total_stats = {'ok': 0, 'exists': 0, 'error': 0, 'skip_ext': 0}

    # S3 -> S3 migrations
    for source_prefix, dest_prefix in MIGRATIONS:
        print(f"\n[MIGRATING] {source_prefix}")
        print(f"         -> {dest_prefix}")
        
        objects = list_objects(source_prefix)
        videos = [o for o in objects if o.lower().endswith(VIDEO_EXTENSIONS)]
        print(f"  Videos encontrados: {len(videos)}")
        
        if not videos:
            continue

        with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
            futures = {executor.submit(process_migration, key, dest_prefix): key for key in videos}
            for i, future in enumerate(as_completed(futures), 1):
                result = future.result()
                total_stats[result] += 1
                key = futures[future]
                name = key.split('/')[-1][:40]
                if result == 'ok':
                    print(f"  [{i}/{len(videos)}] [OK] {name}")
                elif result == 'error':
                    print(f"  [{i}/{len(videos)}] [ERR] {name}")

    # Local downloads
    print(f"\n{'=' * 60}")
    print("DOWNLOADS LOCAIS")
    os.makedirs(LOCAL_DOWNLOAD_DIR, exist_ok=True)

    for prefix in LOCAL_DOWNLOADS:
        print(f"\n[DOWNLOAD] {prefix}")
        print(f"        -> {LOCAL_DOWNLOAD_DIR}")
        
        objects = list_objects(prefix)
        videos = [o for o in objects if o.lower().endswith(VIDEO_EXTENSIONS)]
        print(f"  Videos: {len(videos)}")

        for i, key in enumerate(videos, 1):
            result = download_local(key, LOCAL_DOWNLOAD_DIR)
            total_stats[result] += 1
            name = key.split('/')[-1][:40]
            if result == 'ok':
                print(f"  [{i}/{len(videos)}] [OK] {name}")

    # Summary
    print(f"\n{'=' * 60}")
    print("RESULTADO FINAL")
    print(f"  Copiados:    {total_stats['ok']}")
    print(f"  Ja existiam: {total_stats['exists']}")
    print(f"  Erros:       {total_stats['error']}")
    print(f"  Ignorados:   {total_stats['skip_ext']}")
    print("=" * 60)

if __name__ == '__main__':
    main()

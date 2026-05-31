import boto3
from concurrent.futures import ThreadPoolExecutor, as_completed

SOURCE_REGION = 'sa-east-1'
DEST_BUCKET = 'backup-midia-smartphone'
MAX_WORKERS = 15

s3 = boto3.client('s3', region_name=SOURCE_REGION)

# Mapping: (source_bucket, source_prefix, dest_prefix)
MIGRATIONS = [
    # === Apps ===
    ('smarthophone', 'Apps/Apps/', 'Apps/'),

    # === Fotos ===
    ('smarthophone', 'Fotos/Fotos/', 'Fotos/redmi-note-8/'),
    ('smarthophone', 'Xiaomi/xiaomi media/Fotos/', 'Fotos/redmi-note-8/xiaomi-media/'),
    ('pics-notebackup', 'Jiggly Girls [Hentai on Brasil]/', 'Fotos/anime-art/Jiggly_Girls/'),
    ('smarthophone', 'backup_xioami_redmi_note_8/VideoDownloader/Anime/Seart/', 'Fotos/anime-art/Seart/'),
    ('smarthophone', 'backup_xioami_redmi_note_8/VideoDownloader/Anime/Jiggly Girls [Hentai on Brasil]/', 'Fotos/anime-art/Jiggly_Girls_v2/'),

    # === Videos ===
    ('smarthophone', 'backup_xioami_redmi_note_8/VideoDownloader/Anime/MMD/', 'Videos/redmi-note-8/Anime_MMD/'),
    ('smarthophone', 'backup_xioami_redmi_note_8/VideoDownloader/Anime/Vídeos/', 'Videos/redmi-note-8/Anime/'),
    ('smarthophone', 'backup_xioami_redmi_note_8/VideoDownloader/Charming/', 'Videos/redmi-note-8/Charming/'),
    ('smarthophone', 'backup_xioami_redmi_note_8/VideoDownloader/EmillyaBunny/', 'Videos/redmi-note-8/EmillyaBunny/'),
    ('smarthophone', 'backup_xioami_redmi_note_8/VideoDownloader/kate kuray/', 'Videos/redmi-note-8/Kate_Kuray/'),
    ('smarthophone', 'backup_xioami_redmi_note_8/VideoDownloader/Mia Malkova/', 'Videos/redmi-note-8/MiaMalkova/'),
    ('smarthophone', 'backup_xioami_redmi_note_8/VideoDownloader/megan/', 'Videos/redmi-note-8/megan/'),
    ('smarthophone', 'backup_xioami_redmi_note_8/VideoDownloader/Lana compilation/', 'Videos/redmi-note-8/Lana/'),
    ('smarthophone', 'backup_xioami_redmi_note_8/VideoDownloader/angelica/', 'Videos/redmi-note-8/angelica/'),
    ('smarthophone', 'backup_xioami_redmi_note_8/VideoDownloader/Asa akira/', 'Videos/redmi-note-8/Asa_akira/'),
    ('smarthophone', 'backup_xioami_redmi_note_8/VideoDownloader/compilation/', 'Videos/redmi-note-8/compilation/'),
    ('smarthophone', 'backup_xioami_redmi_note_8/VideoDownloader/Outros/', 'Videos/redmi-note-8/Outros/'),
    ('smarthophone', 'backup_xioami_redmi_note_8/VideoDownloader/Deeper/', 'Videos/redmi-note-8/Deeper/'),
    ('smarthophone', 'backup_xioami_redmi_note_8/VideoDownloader/maior/', 'Videos/redmi-note-8/maior/'),
    ('smarthophone', 'backup_xioami_redmi_note_8/VideoDownloader/pos converter/', 'Videos/redmi-note-8/pos_converter/'),
    ('smarthophone', 'backup_xioami_redmi_note_8/VideoDownloader/google fotos/', 'Videos/redmi-note-8/google_fotos/'),
    ('smarthophone', 'backup_xioami_redmi_note_8/VideoDownloader/BelleDelphine/', 'Videos/redmi-note-8/BelleDelphine/'),
    ('smarthophone', 'backup_xioami_redmi_note_8/VideoDownloader/Gia Paig/', 'Videos/redmi-note-8/Gia_Paige/'),
    ('smarthophone', 'backup_xioami_redmi_note_8/VideoDownloader/meru/', 'Videos/redmi-note-8/meru/'),
    ('smarthophone', 'backup_xioami_redmi_note_8/VideoDownloader/Pequenos/', 'Videos/redmi-note-8/WhatsApp_Pequenos/'),
    ('smarthophone', 'Xiaomi/xiaomi media/videos/FinalFantasy/', 'Videos/xiaomi-mi6/FinalFantasy/'),
    ('smarthophone', 'Xiaomi/xiaomi media/videos/Nier/', 'Videos/xiaomi-mi6/Nier/'),
    ('smarthophone', 'Xiaomi/xiaomi media/videos/Othes/', 'Videos/xiaomi-mi6/Outros/'),
    ('smarthophone', 'Videos/Videos/Vidoes v2/Anime/', 'Videos/redmi-note-8/Anime_v2/'),
    ('smarthophone', 'Videos/Videos/Vidoes v2/Blacked/', 'Videos/redmi-note-8/Blacked/'),
    ('smarthophone', 'Videos/Videos/Vidoes v2/DP/', 'Videos/redmi-note-8/DP/'),
    ('smarthophone', 'Videos/Videos/Vidoes v2/Star/', 'Videos/redmi-note-8/Star/'),

    # === WhatsApp (xioami-mi6) ===
    ('xioami-mi6', 'MI6/Media/WhatsApp Animated Gifs/', 'WhatsApp/gifs/'),
    ('xioami-mi6', 'MI6/Media/WhatsApp Audio/', 'WhatsApp/audio/'),
    ('xioami-mi6', 'MI6/Media/WhatsApp Documents/', 'WhatsApp/documents/'),
    ('xioami-mi6', 'MI6/Media/WhatsApp Stickers/', 'WhatsApp/stickers/'),
    ('xioami-mi6', 'MI6/Media/WhatsApp Video Notes/', 'WhatsApp/video-notes/'),
    ('xioami-mi6', 'MI6/Media/WhatsApp Voice Notes/', 'WhatsApp/voice-notes/'),
]

# Large files to copy individually (zips)
LARGE_FILES = [
    ('xioami-mi6', 'MI6/Media/WhatsApp Images.zip', 'WhatsApp/WhatsApp_Images.zip'),
    ('xioami-mi6', 'MI6/Media/WhatsApp Video.zip', 'WhatsApp/WhatsApp_Video.zip'),
]

def list_objects(bucket, prefix):
    paginator = s3.get_paginator('list_objects_v2')
    objects = []
    for page in paginator.paginate(Bucket=bucket, Prefix=prefix):
        for obj in page.get('Contents', []):
            objects.append(obj['Key'])
    return objects

def copy_file(source_bucket, source_key, dest_key):
    try:
        s3.copy({'Bucket': source_bucket, 'Key': source_key}, DEST_BUCKET, dest_key)
        return 'ok'
    except Exception as e:
        print(f"  [ERR] {source_key[:50]}: {str(e)[:60]}")
        return 'error'

def process_batch(source_bucket, source_prefix, dest_prefix):
    objects = list_objects(source_bucket, source_prefix)
    if not objects:
        print(f"  Vazio, pulando.")
        return 0, 0

    ok = 0
    err = 0
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = {}
        for key in objects:
            # Remove source prefix, keep relative path
            relative = key[len(source_prefix):]
            dest_key = dest_prefix + relative
            futures[executor.submit(copy_file, source_bucket, key, dest_key)] = key

        for i, future in enumerate(as_completed(futures), 1):
            result = future.result()
            if result == 'ok':
                ok += 1
            else:
                err += 1
            if i % 50 == 0 or i == len(futures):
                print(f"  Progresso: {i}/{len(futures)} (OK: {ok}, ERR: {err})")

    return ok, err

def main():
    print("=" * 60)
    print("UNIFICACAO DE BUCKETS")
    print(f"Destino: {DEST_BUCKET} ({SOURCE_REGION})")
    print("=" * 60)

    total_ok = 0
    total_err = 0

    for source_bucket, source_prefix, dest_prefix in MIGRATIONS:
        print(f"\n[{source_bucket}] {source_prefix}")
        print(f"  -> {dest_prefix}")
        ok, err = process_batch(source_bucket, source_prefix, dest_prefix)
        total_ok += ok
        total_err += err

    # Large files
    print(f"\n[LARGE FILES]")
    for source_bucket, source_key, dest_key in LARGE_FILES:
        print(f"  Copiando {source_key} -> {dest_key}...")
        result = copy_file(source_bucket, source_key, dest_key)
        if result == 'ok':
            total_ok += 1
            print(f"  [OK]")
        else:
            total_err += 1

    print(f"\n{'=' * 60}")
    print("RESULTADO FINAL")
    print(f"  Copiados: {total_ok}")
    print(f"  Erros:    {total_err}")
    print("=" * 60)
    print("\nApos verificar, pode deletar os buckets antigos com:")
    print("  aws s3 rb s3://pics-notebackup --force --region sa-east-1")
    print("  aws s3 rb s3://smarthophone --force --region sa-east-1")
    print("  aws s3 rb s3://xioami-mi6 --force --region sa-east-1")

if __name__ == '__main__':
    main()

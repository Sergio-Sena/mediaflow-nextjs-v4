import boto3
import re
from concurrent.futures import ThreadPoolExecutor, as_completed

BUCKET = 'mediaflow-uploads-969430605054'
REGION = 'us-east-1'
BASE = 'users/sergio_sena/'
MAX_WORKERS = 10

s3 = boto3.client('s3', region_name=REGION)

# Keywords -> destination folder (relative to BASE)
RULES = [
    # Anime - Final Fantasy
    (r'(?i)(tifa|aerith|yuffie|cloud|jessie|final.?fantasy|ff.?vii|lockhart|7th.?heaven)', 'Anime/Final_Fantasy/'),
    # Anime - Nier
    (r'(?i)(2b|nier|yorha|a2.*nier|automata)', 'Anime/2b_Nier_Automata/'),
    # Anime - Zelda
    (r'(?i)(zelda|link.*zelda|midna|ganon|linkle|botw)', 'Anime/Zelda/'),
    # Anime - RE
    (r'(?i)(resident.?evil|leon.*ada|ashley.*leon|ada.*wong|jill.*valentine|claire.*redfield|re4|re.?village|cassandra.*re)', 'Anime/RE4/'),
    # Anime - Dead or Alive
    (r'(?i)(dead.?or.?alive|doa|marie.?rose|honoka|nyotengu|kasumi)', 'Anime/Dead_or_Alive/'),
    # Anime - Stellar Blade
    (r'(?i)(stellar.?blade|eve.*stellar)', 'Anime/Stellar_Blade/'),
    # Anime - Lara Croft
    (r'(?i)(lara.?croft|lara.*trouble|tomb.?raider)', 'Anime/Lara_Croft/'),
    # Anime - Overwatch
    (r'(?i)(overwatch|d\.?va|mercy|tracer)', 'Anime/Outros/'),
    # Anime - Derpixon/Studio FOW
    (r'(?i)(derpixon|fandeltales|mime.?and.?dash|party.?games|fow.?\d{3}|studio.?fow|kunoichi)', 'Anime/Dexpirion/'),
    # Anime - Meru
    (r'(?i)(meru.*succubus)', 'Anime/Meru_Succubus/'),
    # Star - Kate Kuray
    (r'(?i)(kate.?kuray|katekuray|k4t3.?kur4y)', 'Star/Kate_Kuray/'),
    # Star - Megan Rain
    (r'(?i)(megan.?rain)', 'Star/megan/'),
    # Star - Lana Rhoades
    (r'(?i)(lana.?rhoade)', 'Star/Lana/'),
    # Star - Mia Malkova
    (r'(?i)(mia.?malkova)', 'Star/MiaMalkova/'),
]

# Only scan these folders for reorganization
SCAN_FOLDERS = [
    'users/sergio_sena/Star/Outros/',
    'users/sergio_sena/Anime/Outros/',
]

def get_dest_folder(filename):
    for pattern, dest in RULES:
        if re.search(pattern, filename):
            return BASE + dest
    return None

def move_file(source_key, dest_key):
    try:
        s3.copy_object(Bucket=BUCKET, CopySource={'Bucket': BUCKET, 'Key': source_key}, Key=dest_key)
        s3.delete_object(Bucket=BUCKET, Key=source_key)
        return 'moved'
    except Exception as e:
        print(f"  [ERR] {source_key}: {str(e)[:80]}")
        return 'error'

def process_file(key):
    filename = key.split('/')[-1]
    dest_folder = get_dest_folder(filename)
    
    if not dest_folder:
        return 'no_match'
    
    # Already in correct folder?
    if key.startswith(dest_folder):
        return 'already_correct'
    
    dest_key = dest_folder + filename
    
    # Check if dest already exists
    try:
        s3.head_object(Bucket=BUCKET, Key=dest_key)
        # Already exists at destination, just delete source
        s3.delete_object(Bucket=BUCKET, Key=key)
        return 'dedup'
    except:
        pass
    
    return move_file(key, dest_key)

def main():
    print("=" * 60)
    print("REORGANIZACAO POR KEYWORDS")
    print("=" * 60)

    stats = {'moved': 0, 'no_match': 0, 'already_correct': 0, 'error': 0, 'dedup': 0}

    for folder in SCAN_FOLDERS:
        print(f"\n[SCANNING] {folder}")
        
        paginator = s3.get_paginator('list_objects_v2')
        files = []
        for page in paginator.paginate(Bucket=BUCKET, Prefix=folder):
            for obj in page.get('Contents', []):
                if obj['Key'].lower().endswith(('.mp4', '.mkv', '.avi', '.mov')):
                    files.append(obj['Key'])
        
        print(f"  Arquivos: {len(files)}")

        with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
            futures = {executor.submit(process_file, key): key for key in files}
            for i, future in enumerate(as_completed(futures), 1):
                result = future.result()
                stats[result] += 1
                if result == 'moved':
                    key = futures[future]
                    name = key.split('/')[-1][:45]
                    dest = get_dest_folder(key.split('/')[-1])
                    print(f"  [{i}/{len(files)}] [MOVED] {name} -> {dest.split('sergio_sena/')[1]}")
                elif result == 'dedup':
                    print(f"  [{i}/{len(files)}] [DEDUP] {futures[future].split('/')[-1][:45]}")

    print(f"\n{'=' * 60}")
    print("RESULTADO")
    print(f"  Movidos:     {stats['moved']}")
    print(f"  Sem match:   {stats['no_match']}")
    print(f"  Ja corretos: {stats['already_correct']}")
    print(f"  Duplicados:  {stats['dedup']}")
    print(f"  Erros:       {stats['error']}")
    print("=" * 60)

if __name__ == '__main__':
    main()

import os
import boto3
import re

s3 = boto3.client('s3', region_name='us-east-1')
BUCKET = 'mediaflow-uploads-969430605054'
LOCAL_DIR = r'C:\Users\dell 5557\Videos\IDM\Corporativo\ShyBlanche'
S3_PREFIX = 'users/user_admin/Corporativo/ShyBlanche/'

def sanitize(name):
    name, ext = os.path.splitext(name)
    name = name.encode('ascii', 'ignore').decode('ascii')
    name = re.sub(r'[^a-zA-Z0-9_\-\s]', '', name)
    name = re.sub(r'\s+', ' ', name).strip()
    return (name[:200] + ext) if len(name) > 200 else (name + ext)

files = []
for f in os.listdir(LOCAL_DIR):
    path = os.path.join(LOCAL_DIR, f)
    if os.path.isfile(path) and f.lower().endswith(('.mp4', '.mkv', '.avi', '.mov', '.webm')):
        files.append({'local': path, 'key': S3_PREFIX + sanitize(f), 'size': os.path.getsize(path)})

total = len(files)
total_size = sum(f['size'] for f in files)
uploaded = 0

print(f'Pasta: ShyBlanche - {total} arquivos ({total_size / (1024**3):.2f} GB)')
print('=' * 60)

for idx, f in enumerate(files, 1):
    s3.upload_file(f['local'], BUCKET, f['key'])
    uploaded += f['size']
    progress = int((uploaded / total_size) * 100)
    bar = '#' * (progress // 2) + '-' * (50 - progress // 2)
    print(f'\r[{bar}] {progress}% ({idx}/{total})', end='', flush=True)

print(f'\n\nConcluido: {total} arquivos ({total_size / (1024**3):.2f} GB)')

import os
import re
import boto3
from difflib import SequenceMatcher

LOCAL_FOLDER = r"C:\Users\dell 5557\Videos\IDM\Star\Kate Kuray"
S3_BUCKET = "mediaflow-uploads-969430605054"
S3_PREFIX = "users/sergio_sena/Star/Kate Kuray/"

s3 = boto3.client('s3')

def extract_quality(filename):
    """Extrai qualidade do nome (1080, 1440, 4K, etc)"""
    match = re.search(r'\((\d+)p?\)', filename, re.IGNORECASE)
    if match:
        return int(match.group(1))
    if '4K' in filename.upper():
        return 2160
    return 720  # default

def normalize_name(filename):
    """Normaliza nome para comparação"""
    name = os.path.splitext(filename)[0]
    # Remove qualidade
    name = re.sub(r'\((\d+)p?\)', '', name, flags=re.IGNORECASE)
    name = re.sub(r'4K', '', name, flags=re.IGNORECASE)
    # Remove espaços extras
    name = re.sub(r'\s+', ' ', name).strip().lower()
    return name

def similar(a, b):
    """Calcula similaridade entre dois nomes"""
    return SequenceMatcher(None, a, b).ratio()

print("=" * 80)
print("ANÁLISE DE UPLOAD - Kate Kuray")
print("=" * 80)
print(f"\nOrigem: {LOCAL_FOLDER}")
print(f"Destino: s3://{S3_BUCKET}/{S3_PREFIX}")
print("\n" + "=" * 80)

# Listar arquivos locais
local_files = {}
for filename in os.listdir(LOCAL_FOLDER):
    if filename.endswith('.mp4'):
        filepath = os.path.join(LOCAL_FOLDER, filename)
        size = os.path.getsize(filepath)
        quality = extract_quality(filename)
        normalized = normalize_name(filename)
        
        local_files[filename] = {
            'path': filepath,
            'size': size,
            'quality': quality,
            'normalized': normalized
        }

print(f"\nArquivos locais encontrados: {len(local_files)}")

# Listar arquivos no S3
print(f"\nVerificando arquivos no S3...")
s3_files = {}
try:
    paginator = s3.get_paginator('list_objects_v2')
    for page in paginator.paginate(Bucket=S3_BUCKET, Prefix=S3_PREFIX):
        if 'Contents' in page:
            for obj in page['Contents']:
                key = obj['Key']
                filename = key.replace(S3_PREFIX, '')
                if filename and filename.endswith('.mp4'):
                    s3_files[filename] = {
                        'key': key,
                        'size': obj['Size'],
                        'quality': extract_quality(filename),
                        'normalized': normalize_name(filename)
                    }
except Exception as e:
    print(f"⚠️  Erro ao listar S3: {e}")

print(f"Arquivos no S3: {len(s3_files)}")

# Análise de upload
print("\n" + "=" * 80)
print("PLANO DE UPLOAD")
print("=" * 80)

to_upload = []
to_skip = []
conflicts = []

for local_name, local_info in local_files.items():
    # Verificar se já existe exatamente
    if local_name in s3_files:
        s3_info = s3_files[local_name]
        if local_info['quality'] > s3_info['quality']:
            to_upload.append({
                'file': local_name,
                'reason': f"Maior qualidade ({local_info['quality']}p vs {s3_info['quality']}p)",
                'action': 'SUBSTITUIR',
                'local_quality': local_info['quality'],
                's3_quality': s3_info['quality']
            })
        elif local_info['quality'] == s3_info['quality']:
            to_skip.append({
                'file': local_name,
                'reason': f"Mesma qualidade ({local_info['quality']}p) - EMPATE"
            })
        else:
            to_skip.append({
                'file': local_name,
                'reason': f"Qualidade inferior ({local_info['quality']}p vs {s3_info['quality']}p)"
            })
        continue
    
    # Verificar arquivos similares
    similar_found = False
    for s3_name, s3_info in s3_files.items():
        similarity = similar(local_info['normalized'], s3_info['normalized'])
        
        if similarity > 0.8:  # 80% similar
            similar_found = True
            if local_info['quality'] > s3_info['quality']:
                to_upload.append({
                    'file': local_name,
                    'reason': f"Similar a '{s3_name}' mas maior qualidade ({local_info['quality']}p vs {s3_info['quality']}p)",
                    'action': 'UPLOAD NOVO',
                    'local_quality': local_info['quality'],
                    's3_quality': s3_info['quality'],
                    'similar_to': s3_name
                })
            elif local_info['quality'] == s3_info['quality']:
                to_skip.append({
                    'file': local_name,
                    'reason': f"Similar a '{s3_name}' com mesma qualidade ({local_info['quality']}p) - EMPATE"
                })
            else:
                to_skip.append({
                    'file': local_name,
                    'reason': f"Similar a '{s3_name}' mas qualidade inferior ({local_info['quality']}p vs {s3_info['quality']}p)"
                })
            break
    
    if not similar_found:
        to_upload.append({
            'file': local_name,
            'reason': "Arquivo novo",
            'action': 'UPLOAD NOVO',
            'local_quality': local_info['quality']
        })

# Mostrar plano
print(f"\nARQUIVOS PARA UPLOAD: {len(to_upload)}")
if to_upload:
    for i, item in enumerate(to_upload, 1):
        print(f"\n  [{i}] {item['file']}")
        print(f"      Ação: {item['action']}")
        print(f"      Motivo: {item['reason']}")
        print(f"      Destino: s3://{S3_BUCKET}/{S3_PREFIX}{item['file']}")

print(f"\nARQUIVOS IGNORADOS: {len(to_skip)}")
if to_skip:
    for i, item in enumerate(to_skip, 1):
        print(f"\n  [{i}] {item['file']}")
        print(f"      Motivo: {item['reason']}")

print("\n" + "=" * 80)
print(f"RESUMO: {len(to_upload)} uploads | {len(to_skip)} ignorados")
print("=" * 80)

# Perguntar confirmação
if to_upload:
    print("\nATENCAO: Revise o plano acima antes de continuar!")
    resposta = input("\nDeseja executar o upload? (sim/não): ").strip().lower()
    
    if resposta == 'sim':
        print("\n" + "=" * 80)
        print("EXECUTANDO UPLOADS")
        print("=" * 80)
        
        for i, item in enumerate(to_upload, 1):
            filename = item['file']
            local_path = local_files[filename]['path']
            s3_key = S3_PREFIX + filename
            
            print(f"\n[{i}/{len(to_upload)}] Uploading: {filename}")
            try:
                s3.upload_file(
                    local_path,
                    S3_BUCKET,
                    s3_key,
                    Callback=lambda bytes_transferred: print('.', end='', flush=True)
                )
                print(f"\nOK: {filename}")
            except Exception as e:
                print(f"\nERRO: {e}")
        
        print("\n" + "=" * 80)
        print("UPLOAD CONCLUÍDO!")
        print("=" * 80)
    else:
        print("\nUpload cancelado pelo usuario")
else:
    print("\nNenhum arquivo para upload!")

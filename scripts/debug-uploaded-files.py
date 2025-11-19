#!/usr/bin/env python3
import boto3

s3 = boto3.client('s3', region_name='us-east-1')
bucket = 'mediaflow-uploads-969430605054'
prefix = 'users/user_admin/Corporativo/'

print("=" * 60)
print("DEBUG: Arquivos enviados recentemente")
print("=" * 60)

# Licorporativo arquivos das pastas enviadas
test_folders = ['Anasta_angel', 'arina fox', 'Lil Karina', 'litle dragon', 'Little Angel', 'MIRARI HUB']

for folder in test_folders:
    print(f"\n{folder}/:")
    print("-" * 60)
    
    paginator = s3.get_paginator('list_objects_v2')
    pages = paginator.paginate(Bucket=bucket, Prefix=f'{prefix}{folder}/')
    
    count = 0
    for page in pages:
        for obj in page.get('Contents', []):
            key = obj['Key']
            filename = key.split('/')[-1]
            size_mb = obj['Size'] / (1024**2)
            
            # Verificar problemas
            issues = []
            if len(filename) > 100:
                issues.append(f"NOME LONGO ({len(filename)} chars)")
            if any(c in filename for c in ['á', 'é', 'í', 'ó', 'ú', 'ã', 'õ', 'ç']):
                issues.append("ACENTOS")
            if '  ' in filename:
                issues.append("ESPACOS DUPLOS")
            
            status = " | ".join(issues) if issues else "OK"
            print(f"  [{status}] {filename[:80]}... ({size_mb:.1f} MB)")
            count += 1
    
    print(f"  Total: {count} arquivos")

print("\n" + "=" * 60)

import boto3

s3 = boto3.client('s3', region_name='us-east-1')
BUCKET = 'mediaflow-uploads-969430605054'

def check_users():
    paginator = s3.get_paginator('list_objects_v2')
    
    admin_files = []
    sergio_files = []
    
    # user_admin
    for page in paginator.paginate(Bucket=BUCKET, Prefix='users/user_admin/'):
        for obj in page.get('Contents', []):
            admin_files.append(obj['Key'])
    
    # sergio_sena
    for page in paginator.paginate(Bucket=BUCKET, Prefix='users/sergio_sena/'):
        for obj in page.get('Contents', []):
            sergio_files.append(obj['Key'])
    
    print("=" * 80)
    print(f"ARQUIVOS EM users/user_admin/: {len(admin_files)}")
    print("=" * 80)
    if admin_files:
        for f in admin_files[:20]:
            print(f"  {f}")
        if len(admin_files) > 20:
            print(f"  ... e mais {len(admin_files) - 20} arquivos")
    else:
        print("  [VAZIO]")
    
    print("\n" + "=" * 80)
    print(f"ARQUIVOS EM users/sergio_sena/: {len(sergio_files)}")
    print("=" * 80)
    if sergio_files:
        for f in sergio_files[:20]:
            print(f"  {f}")
        if len(sergio_files) > 20:
            print(f"  ... e mais {len(sergio_files) - 20} arquivos")
    else:
        print("  [VAZIO]")
    
    print("\n" + "=" * 80)
    print("RECOMENDACAO:")
    print("=" * 80)
    if admin_files and sergio_files:
        print("  [!] BAGUNCA DETECTADA - Arquivos em ambas as pastas")
        print("  Solucao: Mover tudo para users/sergio_sena/")
    elif admin_files and not sergio_files:
        print("  [OK] Todos em user_admin - Pode continuar usando admin")
    elif sergio_files and not admin_files:
        print("  [OK] Todos em sergio_sena - Continue usando sergio_sena")
    else:
        print("  [OK] Ambos vazios - Comece do zero")

if __name__ == '__main__':
    check_users()

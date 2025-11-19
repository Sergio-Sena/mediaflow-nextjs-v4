import boto3

s3 = boto3.client('s3')
BUCKET = 'mediaflow-uploads-969430605054'
PREFIX = 'users/sergio_sena/Video/'

def check_video_folders():
    print("Verificando pastas em users/sergio_sena/Video/\n")
    
    try:
        paginator = s3.get_paginator('list_objects_v2')
        pages = paginator.paginate(Bucket=BUCKET, Prefix=PREFIX, Delimiter='/')
        
        folders = set()
        
        for page in pages:
            if 'CommonPrefixes' in page:
                for prefix in page['CommonPrefixes']:
                    folder_path = prefix['Prefix']
                    folder_name = folder_path.replace(PREFIX, '').rstrip('/')
                    folders.add(folder_name)
        
        folders = sorted(folders)
        
        print(f"Pastas encontradas em Video/: {len(folders)}")
        for folder in folders:
            print(f"  - {folder}/")
        
        # Verificar especificamente carros, moana, lilo
        expected = ['carros', 'moana', 'lilo']
        found_expected = []
        
        for folder in folders:
            if folder.lower() in [e.lower() for e in expected]:
                found_expected.append(folder)
        
        print(f"\nPastas esperadas encontradas: {len(found_expected)}/3")
        for folder in found_expected:
            print(f"  [OK] {folder}/")
        
        missing = [e for e in expected if e.lower() not in [f.lower() for f in folders]]
        if missing:
            print(f"\nPastas nao encontradas:")
            for folder in missing:
                print(f"  [MISSING] {folder}/")
        
    except Exception as e:
        print(f"Erro: {e}")

if __name__ == '__main__':
    check_video_folders()
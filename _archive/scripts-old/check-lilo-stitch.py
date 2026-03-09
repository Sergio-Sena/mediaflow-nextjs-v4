import boto3

s3 = boto3.client('s3')
BUCKET = 'mediaflow-uploads-969430605054'
PREFIX = 'users/sergio_sena/Video/'

def check_lilo_stitch():
    print("Procurando pasta 'Lilo & Stitch' em users/sergio_sena/Video/\n")
    
    try:
        paginator = s3.get_paginator('list_objects_v2')
        pages = paginator.paginate(Bucket=BUCKET, Prefix=PREFIX, Delimiter='/')
        
        folders = []
        
        for page in pages:
            if 'CommonPrefixes' in page:
                for prefix in page['CommonPrefixes']:
                    folder_path = prefix['Prefix']
                    folder_name = folder_path.replace(PREFIX, '').rstrip('/')
                    folders.append(folder_name)
        
        print("Todas as pastas em Video/:")
        for folder in sorted(folders):
            print(f"  - {folder}/")
        
        # Procurar por Lilo
        lilo_folders = [f for f in folders if 'lilo' in f.lower() or 'stitch' in f.lower()]
        
        if lilo_folders:
            print(f"\nPastas relacionadas a Lilo encontradas:")
            for folder in lilo_folders:
                print(f"  [FOUND] {folder}/")
        else:
            print(f"\n[NOT FOUND] Nenhuma pasta com 'Lilo' ou 'Stitch' encontrada")
        
    except Exception as e:
        print(f"Erro: {e}")

if __name__ == '__main__':
    check_lilo_stitch()
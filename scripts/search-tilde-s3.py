import boto3

s3 = boto3.client('s3')
BUCKET = 'mediaflow-uploads-969430605054'

def search_tilde_files():
    print("Procurando arquivos com '~1' no S3...\n")
    
    try:
        paginator = s3.get_paginator('list_objects_v2')
        pages = paginator.paginate(Bucket=BUCKET)
        
        tilde_files = []
        
        for page in pages:
            if 'Contents' in page:
                for obj in page['Contents']:
                    key = obj['Key']
                    filename = key.split('/')[-1]
                    
                    if '~1' in filename:
                        size_mb = round(obj['Size'] / (1024*1024), 2)
                        tilde_files.append({
                            'key': key,
                            'filename': filename,
                            'size_mb': size_mb
                        })
        
        if not tilde_files:
            print("[OK] Nenhum arquivo com '~1' encontrado")
            return
        
        print(f"Encontrados {len(tilde_files)} arquivos com '~1':\n")
        
        for i, file_info in enumerate(tilde_files, 1):
            try:
                print(f"{i}. {file_info['key']}")
                print(f"   Tamanho: {file_info['size_mb']} MB\n")
            except:
                print(f"{i}. [arquivo com caracteres especiais]")
                print(f"   Tamanho: {file_info['size_mb']} MB\n")
        
        print(f"Total: {len(tilde_files)} arquivos")
        
    except Exception as e:
        print(f"Erro: {e}")

if __name__ == '__main__':
    search_tilde_files()
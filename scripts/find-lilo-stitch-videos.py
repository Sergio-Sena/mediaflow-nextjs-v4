import boto3

s3 = boto3.client('s3')
BUCKET = 'mediaflow-uploads-969430605054'

def find_lilo_stitch_videos():
    print("Procurando 'Lilo & Stitch 2 - Stitch Deu Defeito'...\n")
    
    try:
        paginator = s3.get_paginator('list_objects_v2')
        pages = paginator.paginate(Bucket=BUCKET, Prefix='users/sergio_sena/')
        
        lilo_videos = []
        target_folder = None
        
        for page in pages:
            if 'Contents' in page:
                for obj in page['Contents']:
                    key = obj['Key']
                    filename = key.split('/')[-1]
                    
                    # Procurar arquivo específico
                    if 'Lilo' in filename and 'Stitch' in filename and 'Defeito' in filename:
                        size_mb = round(obj['Size'] / (1024*1024), 2)
                        folder_path = '/'.join(key.split('/')[:-1]) + '/'
                        
                        print(f"[FOUND TARGET] {key}")
                        print(f"               Tamanho: {size_mb} MB")
                        print(f"               Pasta: {folder_path}")
                        
                        target_folder = folder_path
                        lilo_videos.append({
                            'key': key,
                            'filename': filename,
                            'size_mb': size_mb
                        })
        
        if target_folder:
            print(f"\nProcurando outros videos na mesma pasta: {target_folder}\n")
            
            # Procurar outros videos na mesma pasta
            pages = paginator.paginate(Bucket=BUCKET, Prefix=target_folder)
            
            for page in pages:
                if 'Contents' in page:
                    for obj in page['Contents']:
                        key = obj['Key']
                        filename = key.split('/')[-1]
                        
                        if filename.lower().endswith(('.mp4', '.avi', '.mkv', '.mov')):
                            size_mb = round(obj['Size'] / (1024*1024), 2)
                            
                            # Verificar se já não está na lista
                            if not any(v['key'] == key for v in lilo_videos):
                                lilo_videos.append({
                                    'key': key,
                                    'filename': filename,
                                    'size_mb': size_mb
                                })
            
            print(f"Total de videos encontrados na pasta: {len(lilo_videos)}")
            for i, video in enumerate(lilo_videos, 1):
                print(f"{i}. {video['filename']} ({video['size_mb']} MB)")
        
        else:
            print("[NOT FOUND] Arquivo 'Lilo & Stitch 2 - Stitch Deu Defeito' nao encontrado")
        
        return lilo_videos, target_folder
        
    except Exception as e:
        print(f"Erro: {e}")
        return [], None

if __name__ == '__main__':
    find_lilo_stitch_videos()
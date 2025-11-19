import boto3

s3 = boto3.client('s3')
BUCKET = 'mediaflow-uploads-969430605054'

def find_carros_video():
    print("Procurando 'Carros 2~1.mp4'...\n")
    
    try:
        paginator = s3.get_paginator('list_objects_v2')
        pages = paginator.paginate(Bucket=BUCKET, Prefix='users/sergio_sena/')
        
        for page in pages:
            if 'Contents' in page:
                for obj in page['Contents']:
                    key = obj['Key']
                    filename = key.split('/')[-1]
                    
                    if 'Carros' in filename and '2' in filename:
                        size_mb = round(obj['Size'] / (1024*1024), 2)
                        print(f"[FOUND] {key}")
                        print(f"        Tamanho: {size_mb} MB")
                        print(f"        Nome: {filename}")
                        return key
        
        print("[NOT FOUND] Carros 2~1.mp4 nao encontrado")
        return None
        
    except Exception as e:
        print(f"Erro: {e}")
        return None

if __name__ == '__main__':
    find_carros_video()
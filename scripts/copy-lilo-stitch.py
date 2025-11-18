import boto3
from botocore.exceptions import ClientError

s3 = boto3.client('s3', region_name='us-east-1')
BUCKET = 'mediaflow-uploads-969430605054'

SOURCE_PREFIX = 'users/lid_lima/Lilo & Stitch/'
DEST_PREFIX = 'users/sergio_sena/video/Lilo & Stitch/'

def copy_folder():
    print(f"Copiando de: {SOURCE_PREFIX}")
    print(f"Para: {DEST_PREFIX}\n")
    
    try:
        paginator = s3.get_paginator('list_objects_v2')
        pages = paginator.paginate(Bucket=BUCKET, Prefix=SOURCE_PREFIX)
        
        count = 0
        for page in pages:
            if 'Contents' not in page:
                print("Pasta origem não encontrada ou vazia")
                return
            
            for obj in page['Contents']:
                source_key = obj['Key']
                
                if source_key == SOURCE_PREFIX:
                    continue
                
                relative_path = source_key[len(SOURCE_PREFIX):]
                dest_key = DEST_PREFIX + relative_path
                
                print(f"Copiando: {relative_path}")
                
                s3.copy_object(
                    Bucket=BUCKET,
                    CopySource={'Bucket': BUCKET, 'Key': source_key},
                    Key=dest_key
                )
                
                count += 1
        
        print(f"\n[OK] {count} arquivos copiados com sucesso!")
        
    except ClientError as e:
        print(f"[ERRO] {e}")

if __name__ == '__main__':
    copy_folder()

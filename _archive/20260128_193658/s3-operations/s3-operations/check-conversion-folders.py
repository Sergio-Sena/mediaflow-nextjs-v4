import boto3

s3 = boto3.client('s3', region_name='us-east-1')
bucket = 'mediaflow-uploads-969430605054'

folders = ['temp/', 'converted/']

for folder in folders:
    print(f"\nVerificando: {folder}")
    response = s3.list_objects_v2(Bucket=bucket, Prefix=folder)
    
    if 'Contents' in response:
        print(f"  Arquivos: {len(response['Contents'])}")
        for obj in response['Contents']:
            size_gb = obj['Size'] / (1024**3)
            print(f"    - {obj['Key']} ({size_gb:.2f} GB)")
    else:
        print(f"  Vazio")

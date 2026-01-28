import boto3

s3 = boto3.client('s3', region_name='us-east-1')
bucket = 'mediaflow-uploads-969430605054'

# Contar arquivos por usuário
users = ['admin/', 'users/lid_lima/', 'users/sergio_sena/', 'users/gabriel/', 'users/user_admin/']

for user_prefix in users:
    paginator = s3.get_paginator('list_objects_v2')
    pages = paginator.paginate(Bucket=bucket, Prefix=user_prefix)
    
    count = 0
    for page in pages:
        count += len(page.get('Contents', []))
    
    print(f"{user_prefix:30} -> {count} arquivos")

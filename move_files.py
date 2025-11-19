import boto3
import re


s3 = boto3.client('s3')
bucket = 'mediaflow-uploads-969430605054'
prefix = 'users/sergio_sena/Star/'

# Listar objetos
response = s3.list_objects_v2(Bucket=bucket, Prefix=prefix, Delimiter='/')

if 'Contents' in response:
    for obj in response['Contents']:
        key = obj['Key']
        if 'EmiliaBunny' in key and key.endswith('.mp4'):
            # Extrair nome do arquivo
            filename = key.split('/')[-1]
            new_key = f'{prefix}emillya_Bunny/{filename}'
            
            # Copiar e deletar
            s3.copy_object(
                Bucket=bucket,
                CopySource={'Bucket': bucket, 'Key': key},
                Key=new_key
            )
            s3.delete_object(Bucket=bucket, Key=key)
            print(f'Movido: {filename}')

print('Concluido!')

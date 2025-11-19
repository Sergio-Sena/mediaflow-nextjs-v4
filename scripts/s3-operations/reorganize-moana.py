import boto3
from botocore.exceptions import ClientError

s3 = boto3.client('s3', region_name='us-east-1')
bucket = 'mediaflow-uploads-969430605054'

print("Reorganizando pastas Moana...")
print("=" * 60)

# Licorporativo arquivos atuais
print("\nEstrutura atual:")
response = s3.list_objects_v2(Bucket=bucket, Prefix='users/lid_lima/Moana')
if 'Contents' in response:
    for obj in response['Contents']:
        print(f"  - {obj['Key']}")

# Mover/Copiar arquivos para nova estrutura
operations = [
    {
        'source': 'users/lid_lima/Moana.2/Moana.Um.Mar.de.Aventuras.2017.1080p.BluRay.DD5.1.x264.DUAL-TDF.mp4',
        'dest': 'users/lid_lima/Moana/Moana.Um.Mar.de.Aventuras.2017.1080p.BluRay.DD5.1.x264.DUAL-TDF.mp4'
    },
    {
        'source': 'users/lid_lima/Moana.Um.Mar.de.Aventuras/Moana.2.2024.1080p.WEB-DL.DUAL.5.1.mp4',
        'dest': 'users/lid_lima/Moana/Moana.2.2024.1080p.WEB-DL.DUAL.5.1.mp4'
    }
]

print("\nMovendo arquivos...")
for op in operations:
    try:
        # Copiar arquivo
        print(f"  Copiando: {op['source']} -> {op['dest']}")
        s3.copy_object(
            Bucket=bucket,
            CopySource={'Bucket': bucket, 'Key': op['source']},
            Key=op['dest']
        )
        
        # Deletar original
        print(f"  Deletando: {op['source']}")
        s3.delete_object(Bucket=bucket, Key=op['source'])
        
    except ClientError as e:
        print(f"  Erro: {e}")

# Deletar pastas vazias (S3 não tem pastas reais, mas vamos tentar deletar os "marcadores")
print("\nLimpando pastas antigas...")
old_folders = [
    'users/lid_lima/Moana.2/',
    'users/lid_lima/Moana.Um.Mar.de.Aventuras/'
]

for folder in old_folders:
    try:
        s3.delete_object(Bucket=bucket, Key=folder)
        print(f"  Deletado: {folder}")
    except:
        pass  # Pasta pode não existir como objeto

# Verificar resultado final
print("\nEstrutura final:")
response = s3.list_objects_v2(Bucket=bucket, Prefix='users/lid_lima/Moana')
if 'Contents' in response:
    for obj in response['Contents']:
        size_gb = obj['Size'] / (1024**3)
        print(f"  - {obj['Key']} ({size_gb:.2f} GB)")

print("\nReorganizacao concluida!")
print("=" * 60)

import boto3

s3 = boto3.client('s3', region_name='us-east-1')
BUCKET = 'mediaflow-uploads-969430605054'

source = 'users/anonymous/Star/kate_kuray/EPORNER.COM_-_Katekura....mp4'
dest = 'users/user_admin/Star/Kate kuray/EPORNER.COM_-_Katekura....mp4'

# Copiar
s3.copy_object(
    Bucket=BUCKET,
    CopySource={'Bucket': BUCKET, 'Key': source},
    Key=dest
)
print(f'[OK] Copiado para: {dest}')

# Deletar original
s3.delete_object(Bucket=BUCKET, Key=source)
print(f'[OK] Deletado: {source}')

print('\nMovimentacao concluida!')

import boto3
import json

s3 = boto3.client('s3', region_name='us-east-1')
bucket = 'mediaflow-uploads-969430605054'

print("Tornando QR codes publicos...")

# Obter policy atual
current_policy = s3.get_bucket_policy(Bucket=bucket)
policy = json.loads(current_policy['Policy'])

# Adicionar statement para qrcodes
qr_statement = {
    'Sid': 'PublicReadQRCodes',
    'Effect': 'Allow',
    'Principal': '*',
    'Action': 's3:GetObject',
    'Resource': f'arn:aws:s3:::{bucket}/qrcodes/*'
}

# Adicionar ao policy
policy['Statement'].append(qr_statement)

s3.put_bucket_policy(Bucket=bucket, Policy=json.dumps(policy))
print("QR codes agora sao publicos!")

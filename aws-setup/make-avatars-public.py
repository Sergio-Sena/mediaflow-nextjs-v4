import boto3
import json

s3 = boto3.client('s3', region_name='us-east-1')
bucket = 'mediaflow-uploads-969430605054'

print("Configurando acesso publico para avatars...")

# Obter policy atual
try:
    current_policy = s3.get_bucket_policy(Bucket=bucket)
    policy = json.loads(current_policy['Policy'])
    statements = policy.get('Statement', [])
except:
    policy = {'Version': '2012-10-17', 'Statement': []}
    statements = []

# Adicionar statement para avatars
avatar_statement = {
    'Sid': 'PublicReadAvatars',
    'Effect': 'Allow',
    'Principal': '*',
    'Action': 's3:GetObject',
    'Resource': f'arn:aws:s3:::{bucket}/avatars/*'
}

# Remover statement antigo se existir
statements = [s for s in statements if s.get('Sid') != 'PublicReadAvatars']
statements.append(avatar_statement)

policy['Statement'] = statements

# Aplicar policy
s3.put_bucket_policy(Bucket=bucket, Policy=json.dumps(policy))
print("Avatars agora sao publicos!")

# Testar acesso
import requests
test_url = f"https://{bucket}.s3.amazonaws.com/avatars/avatar_Lid.jpg"
response = requests.head(test_url)
print(f"\nTeste de acesso: {response.status_code}")
if response.status_code == 200:
    print("OK - Avatar acessivel!")
else:
    print(f"ERRO - Status {response.status_code}")

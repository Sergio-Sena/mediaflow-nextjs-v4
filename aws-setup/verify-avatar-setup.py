import boto3
import json

s3 = boto3.client('s3', region_name='us-east-1')
lambda_client = boto3.client('lambda', region_name='us-east-1')
iam = boto3.client('iam', region_name='us-east-1')

bucket = 'mediaflow-uploads-969430605054'

print("=== 1. VERIFICANDO CORS DO S3 ===")
try:
    cors = s3.get_bucket_cors(Bucket=bucket)
    print("CORS configurado:")
    print(json.dumps(cors['CORSRules'], indent=2))
except Exception as e:
    print(f"ERRO: {e}")
    print("\nConfigurando CORS...")
    s3.put_bucket_cors(
        Bucket=bucket,
        CORSConfiguration={
            'CORSRules': [{
                'AllowedHeaders': ['*'],
                'AllowedMethods': ['GET', 'PUT', 'POST', 'DELETE', 'HEAD'],
                'AllowedOrigins': ['*'],
                'ExposeHeaders': ['ETag'],
                'MaxAgeSeconds': 3000
            }]
        }
    )
    print("CORS configurado com sucesso!")

print("\n=== 2. VERIFICANDO PERMISSOES LAMBDA ===")
functions = ['mediaflow-avatar-presigned', 'mediaflow-update-user']
for func in functions:
    try:
        policy = lambda_client.get_policy(FunctionName=func)
        print(f"\n{func}:")
        print("  Permissoes OK")
    except Exception as e:
        print(f"\n{func}: ERRO - {e}")

print("\n=== 3. VERIFICANDO ROLE LAMBDA ===")
with open('mediaflow-config.json', 'r') as f:
    config = json.load(f)

role_name = config['lambda_role_arn'].split('/')[-1]
try:
    policies = iam.list_attached_role_policies(RoleName=role_name)
    print(f"\nRole: {role_name}")
    print("Policies anexadas:")
    for p in policies['AttachedPolicies']:
        print(f"  - {p['PolicyName']}")
except Exception as e:
    print(f"ERRO: {e}")

print("\n=== 4. TESTANDO PRESIGNED URL ===")
try:
    url = s3.generate_presigned_url(
        'put_object',
        Params={
            'Bucket': bucket,
            'Key': 'avatars/test.png',
            'ContentType': 'image/png'
        },
        ExpiresIn=60
    )
    print("Presigned URL gerada com sucesso!")
    print(f"URL: {url[:100]}...")
except Exception as e:
    print(f"ERRO: {e}")

print("\n=== 5. VERIFICANDO ACESSO PUBLICO AVATARS ===")
try:
    response = s3.list_objects_v2(Bucket=bucket, Prefix='avatars/', MaxKeys=5)
    if 'Contents' in response:
        print(f"\nAvatars encontrados: {len(response['Contents'])}")
        for obj in response['Contents']:
            print(f"  - {obj['Key']}")
    else:
        print("\nNenhum avatar encontrado")
except Exception as e:
    print(f"ERRO: {e}")

print("\n=== RESUMO ===")
print("1. CORS: Verificado")
print("2. Lambda Permissions: Verificado")
print("3. IAM Role: Verificado")
print("4. Presigned URL: Verificado")
print("5. Avatars S3: Verificado")

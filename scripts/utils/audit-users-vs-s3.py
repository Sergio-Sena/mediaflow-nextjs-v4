import boto3

dynamodb = boto3.resource('dynamodb')
s3 = boto3.client('s3')

print("=" * 80)
print("AUDITORIA: USUARIOS vs PASTAS S3")
print("=" * 80)

# ETAPA 1: Listar usuários do DynamoDB
print("\n[1/3] Usuarios cadastrados no DynamoDB...")
try:
    table = dynamodb.Table('mediaflow-users')
    response = table.scan()
    users = response.get('Items', [])
    
    print(f"[OK] Total de usuarios: {len(users)}\n")
    
    for user in users:
        username = user.get('username', 'N/A')
        email = user.get('email', 'N/A')
        role = user.get('role', 'N/A')
        print(f"  - {username} ({email}) - Role: {role}")
    
except Exception as e:
    print(f"[ERRO] {e}")
    users = []

# ETAPA 2: Listar pastas em users/ no S3
print("\n[2/3] Pastas em S3 (users/)...")
bucket = 'mediaflow-uploads-969430605054'

try:
    response = s3.list_objects_v2(Bucket=bucket, Prefix='users/', Delimiter='/')
    
    s3_users = []
    if 'CommonPrefixes' in response:
        for prefix in response['CommonPrefixes']:
            folder = prefix['Prefix'].replace('users/', '').rstrip('/')
            s3_users.append(folder)
    
    print(f"[OK] Total de pastas: {len(s3_users)}\n")
    
    for folder in s3_users:
        # Contar arquivos
        resp = s3.list_objects_v2(Bucket=bucket, Prefix=f'users/{folder}/', MaxKeys=1000)
        count = resp.get('KeyCount', 0)
        size = sum(obj['Size'] for obj in resp.get('Contents', [])) / (1024**3)
        
        print(f"  - users/{folder}/ ({count} arquivos, {size:.2f} GB)")
    
except Exception as e:
    print(f"[ERRO] {e}")
    s3_users = []

# ETAPA 3: Comparar
print("\n[3/3] Comparacao...")

db_usernames = [u.get('username') for u in users]

print("\nUsuarios no DB mas SEM pasta no S3:")
for username in db_usernames:
    if username not in s3_users:
        print(f"  - {username} (VAZIO)")

print("\nPastas no S3 mas SEM usuario no DB:")
for folder in s3_users:
    if folder not in db_usernames:
        print(f"  - {folder} (ORFAO)")

print("\n" + "=" * 80)
print("AUDITORIA CONCLUIDA")
print("=" * 80)

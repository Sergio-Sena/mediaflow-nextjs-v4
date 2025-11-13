import boto3
import json
import sys

if len(sys.argv) < 2:
    print("Uso: python rollback-migration.py <backup-file.json>")
    exit(1)

backup_file = sys.argv[1]

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('mediaflow-users')

print("="*60)
print("ROLLBACK: Restaurando usuarios do backup")
print("="*60)
print()

# Carregar backup
print(f"1. Carregando backup: {backup_file}")
try:
    with open(backup_file, 'r') as f:
        users = json.load(f)
    print(f"   [OK] {len(users)} usuarios no backup")
except Exception as e:
    print(f"   [ERRO] Falha ao carregar: {e}")
    exit(1)

# Deletar usuarios atuais
print("\n2. Deletando usuarios atuais...")
try:
    table.delete_item(Key={'user_id': 'admin_sistema'})
    print("   [OK] admin_sistema deletado")
except:
    print("   [SKIP] admin_sistema nao existe")

try:
    table.delete_item(Key={'user_id': 'sergio_sena'})
    print("   [OK] sergio_sena deletado")
except:
    print("   [SKIP] sergio_sena nao existe")

# Restaurar backup
print("\n3. Restaurando usuarios do backup...")
for user in users:
    try:
        table.put_item(Item=user)
        print(f"   [OK] {user['user_id']} restaurado")
    except Exception as e:
        print(f"   [ERRO] {user['user_id']}: {e}")

print("\n" + "="*60)
print("ROLLBACK CONCLUIDO!")
print("="*60)
print("\nNOTA: Arquivos S3 NAO foram revertidos.")
print("Se necessario, mova manualmente:")
print("  users/sergio_sena/ -> users/user_admin/")

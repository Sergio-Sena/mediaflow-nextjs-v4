#!/usr/bin/env python3
"""
Script para adicionar s3_prefix aos usuários existentes no DynamoDB
"""
import boto3

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
table = dynamodb.Table('mediaflow-users')

# Mapeamento de usuários para suas pastas S3
USER_PREFIXES = {
    'user_admin': '',  # Admin vê tudo (sem prefixo)
    'Lid': 'Lid/',
    'Sergio_sena': 'Sergio Sena/'
}

def update_users():
    print("Atualizando usuarios com s3_prefix...")
    
    # Listar todos os usuários
    response = table.scan()
    users = response.get('Items', [])
    
    for user in users:
        user_id = user['user_id']
        s3_prefix = USER_PREFIXES.get(user_id, f"{user_id}/")
        
        # Atualizar role também (admin para user_admin)
        role = 'admin' if user_id == 'user_admin' else 'user'
        
        print(f"  Atualizando {user_id}: s3_prefix='{s3_prefix}', role='{role}'")
        
        table.update_item(
            Key={'user_id': user_id},
            UpdateExpression='SET s3_prefix = :prefix, #r = :role',
            ExpressionAttributeNames={'#r': 'role'},
            ExpressionAttributeValues={
                ':prefix': s3_prefix,
                ':role': role
            }
        )
    
    print("Usuarios atualizados com sucesso!")
    print("\nResumo:")
    for user_id, prefix in USER_PREFIXES.items():
        role = 'admin' if user_id == 'user_admin' else 'user'
        print(f"  - {user_id}: s3_prefix='{prefix}' role='{role}'")
    
    # Adicionar email ao user_admin se não existir
    admin = table.get_item(Key={'user_id': 'user_admin'})
    if 'Item' in admin and not admin['Item'].get('email'):
        print("\nAdicionando email ao user_admin...")
        table.update_item(
            Key={'user_id': 'user_admin'},
            UpdateExpression='SET email = :email',
            ExpressionAttributeValues={':email': 'sergiosenaadmin@sstech'}
        )
        print("  Email adicionado: sergiosenaadmin@sstech")

if __name__ == '__main__':
    update_users()

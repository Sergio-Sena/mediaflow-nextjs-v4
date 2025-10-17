#!/usr/bin/env python3
import boto3
import hashlib

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
table = dynamodb.Table('mediaflow-users')

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Adicionar senha ao user_admin
password_hash = hash_password('admin123')

table.update_item(
    Key={'user_id': 'user_admin'},
    UpdateExpression='SET password = :pwd',
    ExpressionAttributeValues={':pwd': password_hash}
)

print("Senha admin123 adicionada ao user_admin no DynamoDB")
print(f"Hash: {password_hash}")

import json
import boto3
import hashlib

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('mediaflow-users')

def lambda_handler(event, context):
    try:
        if event['httpMethod'] == 'OPTIONS':
            return cors_response(200, {})
        
        if isinstance(event.get('body'), str):
            body = json.loads(event['body'])
        else:
            body = event.get('body', {})
        
        user_id = body.get('user_id')
        
        if not user_id:
            return cors_response(400, {'success': False, 'message': 'user_id obrigatório'})
        
        # Verificar se usuário existe
        user = table.get_item(Key={'user_id': user_id})
        if 'Item' not in user:
            return cors_response(404, {'success': False, 'message': 'Usuário não encontrado'})
        
        # Construir UpdateExpression dinamicamente
        update_expr = []
        expr_values = {}
        
        if 'email' in body:
            update_expr.append('email = :email')
            expr_values[':email'] = body['email']
        
        if 'password' in body:
            password_hash = hashlib.sha256(body['password'].encode()).hexdigest()
            update_expr.append('password = :password')
            expr_values[':password'] = password_hash
        
        if 'role' in body:
            update_expr.append('#r = :role')
            expr_values[':role'] = body['role']
        
        if 'avatar_url' in body:
            update_expr.append('avatar_url = :avatar_url')
            expr_values[':avatar_url'] = body['avatar_url']
        
        if not update_expr:
            return cors_response(400, {'success': False, 'message': 'Nenhum campo para atualizar'})
        
        # Atualizar usuário
        update_params = {
            'Key': {'user_id': user_id},
            'UpdateExpression': 'SET ' + ', '.join(update_expr),
            'ExpressionAttributeValues': expr_values
        }
        
        # Adicionar ExpressionAttributeNames se role estiver sendo atualizado
        if 'role' in body:
            update_params['ExpressionAttributeNames'] = {'#r': 'role'}
        
        table.update_item(**update_params)
        
        return cors_response(200, {'success': True, 'message': 'Usuário atualizado'})
        
    except Exception as e:
        return cors_response(500, {'success': False, 'message': str(e)})

def cors_response(status_code, body):
    return {
        'statusCode': status_code,
        'headers': {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Headers': 'Content-Type,Authorization',
            'Access-Control-Allow-Methods': 'GET,POST,PUT,PATCH,DELETE,OPTIONS'
        },
        'body': json.dumps(body)
    }

import json
import boto3

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('mediaflow-users')

def lambda_handler(event, context):
    try:
        if event['httpMethod'] == 'OPTIONS':
            return cors_response(200, {})
        
        # Extrair user_id do path
        user_id = event.get('pathParameters', {}).get('user_id')
        
        if not user_id:
            return cors_response(400, {'success': False, 'message': 'user_id obrigatório'})
        
        # Verificar se usuário existe
        user = table.get_item(Key={'user_id': user_id})
        if 'Item' not in user:
            return cors_response(404, {'success': False, 'message': 'Usuário não encontrado'})
        
        # Deletar usuário
        table.delete_item(Key={'user_id': user_id})
        
        return cors_response(200, {'success': True, 'message': 'Usuário deletado'})
        
    except Exception as e:
        return cors_response(500, {'success': False, 'message': str(e)})

def cors_response(status_code, body):
    return {
        'statusCode': status_code,
        'headers': {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Headers': 'Content-Type,Authorization',
            'Access-Control-Allow-Methods': 'DELETE,OPTIONS'
        },
        'body': json.dumps(body)
    }
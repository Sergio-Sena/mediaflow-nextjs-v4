import json
import boto3

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('mediaflow-users')

def lambda_handler(event, context):
    try:
        if event['httpMethod'] == 'OPTIONS':
            return cors_response(200, {})
        
        # Listar todos os usuários
        response = table.scan()
        users = response['Items']
        
        # Remover secrets da resposta (segurança)
        for user in users:
            user.pop('totp_secret', None)
            # Manter avatar_url se existir
        
        return cors_response(200, {
            'success': True,
            'users': users
        })
        
    except Exception as e:
        return cors_response(500, {
            'success': False,
            'message': str(e)
        })

def cors_response(status_code, body):
    return {
        'statusCode': status_code,
        'headers': {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Headers': 'Content-Type,Authorization',
            'Access-Control-Allow-Methods': 'GET,OPTIONS'
        },
        'body': json.dumps(body)
    }

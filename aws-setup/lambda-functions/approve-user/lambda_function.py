import json
import boto3
from datetime import datetime

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('mediaflow-users')

def lambda_handler(event, context):
    try:
        if event['httpMethod'] == 'OPTIONS':
            return cors_response(200, {})
        
        if event['httpMethod'] == 'POST':
            body = json.loads(event['body'])
            user_id = body.get('user_id')
            action = body.get('action')
            
            if not user_id or action not in ['approve', 'reject']:
                return cors_response(400, {
                    'success': False,
                    'message': 'user_id e action (approve/reject) são obrigatórios'
                })
            
            response = table.get_item(Key={'user_id': user_id})
            if 'Item' not in response:
                return cors_response(404, {
                    'success': False,
                    'message': 'Usuário não encontrado'
                })
            
            new_status = 'approved' if action == 'approve' else 'rejected'
            table.update_item(
                Key={'user_id': user_id},
                UpdateExpression='SET #status = :status, approved_at = :timestamp',
                ExpressionAttributeNames={'#status': 'status'},
                ExpressionAttributeValues={
                    ':status': new_status,
                    ':timestamp': datetime.utcnow().isoformat()
                }
            )
            
            return cors_response(200, {
                'success': True,
                'message': f'Usuário {action}d com sucesso'
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
            'Access-Control-Allow-Methods': 'POST,OPTIONS'
        },
        'body': json.dumps(body)
    }

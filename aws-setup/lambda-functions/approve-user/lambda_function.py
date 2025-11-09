import json
import boto3
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../lib'))
from logger import Logger
from datetime import datetime

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('mediaflow-users')

def lambda_handler(event, context):
    correlation_id = event.get('headers', {}).get('x-correlation-id', None)
    logger = Logger('approve-user', correlation_id)
    
    try:
        logger.info("Approve user request", method=event['httpMethod'])
        
        if event['httpMethod'] == 'OPTIONS':
            return cors_response(200, {})
        
        if event['httpMethod'] == 'POST':
            body = json.loads(event['body'])
            user_id = body.get('user_id')
            action = body.get('action')
            
            if not user_id or action not in ['approve', 'reject']:
                logger.warn("Invalid request", user_id=user_id, action=action)
                return cors_response(400, {
                    'success': False,
                    'message': 'user_id e action (approve/reject) são obrigatórios'
                })
            
            response = table.get_item(Key={'user_id': user_id})
            if 'Item' not in response:
                logger.warn("User not found", user_id=user_id)
                return cors_response(404, {
                    'success': False,
                    'message': 'Usuário não encontrado'
                })
            
            if action == 'approve':
                table.update_item(
                    Key={'user_id': user_id},
                    UpdateExpression='SET #status = :status, approved_at = :timestamp',
                    ExpressionAttributeNames={'#status': 'status'},
                    ExpressionAttributeValues={
                        ':status': 'approved',
                        ':timestamp': datetime.utcnow().isoformat()
                    }
                )
                logger.info("User approved", user_id=user_id)
                logger.metric("user_approved", 1)
                return cors_response(200, {
                    'success': True,
                    'message': 'Usuário aprovado com sucesso'
                })
            else:
                # Rejeitar = deletar usuário
                table.delete_item(Key={'user_id': user_id})
                logger.info("User rejected and deleted", user_id=user_id)
                logger.metric("user_rejected", 1)
                return cors_response(200, {
                    'success': True,
                    'message': 'Usuário rejeitado e removido com sucesso'
                })
            
    except Exception as e:
        logger.error("Approve user error", error=str(e))
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

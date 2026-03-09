import json
import boto3

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
users_table = dynamodb.Table('mediaflow-users')

def lambda_handler(event, context):
    try:
        # Suportar GET /users/{user_id}
        user_id = event.get('pathParameters', {}).get('user_id') or event.get('pathParameters', {}).get('userId')
        
        if not user_id:
            return cors_response(400, {'success': False, 'message': 'userId required'})
        
        response = users_table.get_item(Key={'user_id': user_id})
        
        if 'Item' not in response:
            return cors_response(404, {'success': False, 'message': 'User not found'})
        
        user = response['Item']
        user.pop('password', None)
        
        return cors_response(200, {'success': True, 'user': user})
        
    except Exception as e:
        return cors_response(500, {'success': False, 'message': str(e)})

def cors_response(status_code, body):
    return {
        'statusCode': status_code,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Headers': 'Content-Type,Authorization',
            'Access-Control-Allow-Methods': 'GET,OPTIONS'
        },
        'body': json.dumps(body, default=str)
    }

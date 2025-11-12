import boto3
import json
from datetime import datetime
from decimal import Decimal

dynamodb = boto3.resource('dynamodb')

def lambda_handler(event, context):
    try:
        user_id = event.get('user_id')
        action = event.get('action')
        
        if not user_id or not action:
            return {
                'allowed': False,
                'reason': 'invalid_request',
                'message': 'user_id e action são obrigatórios'
            }
        
        table = dynamodb.Table('mediaflow-users')
        response = table.get_item(Key={'user_id': user_id})
        
        if 'Item' not in response:
            return {
                'allowed': False,
                'reason': 'user_not_found',
                'message': 'Usuário não encontrado'
            }
        
        user = response['Item']
        
        # Verificar trial expirado
        if user.get('plan') == 'trial' and user.get('trial_end'):
            trial_end = datetime.fromisoformat(user['trial_end'])
            if datetime.utcnow() > trial_end:
                return {
                    'allowed': False,
                    'reason': 'trial_expired',
                    'message': 'Seu trial de 15 dias expirou. Faça upgrade para continuar.'
                }
        
        # Verificar storage
        if action == 'upload':
            file_size_bytes = event.get('file_size', 0)
            file_size_gb = file_size_bytes / (1024**3)
            
            limits = user.get('limits', {})
            usage = user.get('usage', {})
            
            storage_used = float(usage.get('storage_used_gb', 0))
            storage_limit = float(limits.get('storage_gb', 10))
            
            if storage_used + file_size_gb > storage_limit:
                # Marcar flag para email
                mark_alert_flag(user_id, 'alert_storage')
                
                return {
                    'allowed': False,
                    'reason': 'storage_limit',
                    'message': f'Limite de {storage_limit} GB atingido. Faça upgrade.'
                }
            
            upload_max = float(limits.get('upload_max_gb', 1))
            if file_size_gb > upload_max:
                return {
                    'allowed': False,
                    'reason': 'file_too_large',
                    'message': f'Arquivo maior que {upload_max} GB. Limite do plano.'
                }
        
        # Verificar bandwidth
        if action == 'bandwidth':
            usage = user.get('usage', {})
            limits = user.get('limits', {})
            
            bandwidth_used = float(usage.get('bandwidth_used_gb', 0))
            bandwidth_limit = float(limits.get('bandwidth_gb', 20))
            
            if bandwidth_used > bandwidth_limit:
                # Marcar flag para email
                mark_alert_flag(user_id, 'alert_bandwidth')
                
                return {
                    'allowed': False,
                    'reason': 'bandwidth_limit',
                    'message': f'Limite de {bandwidth_limit} GB/mês atingido.'
                }
        
        return {'allowed': True}
        
    except Exception as e:
        return {
            'allowed': False,
            'reason': 'error',
            'message': str(e)
        }

def mark_alert_flag(user_id, flag_name):
    try:
        table = dynamodb.Table('mediaflow-users')
        table.update_item(
            Key={'user_id': user_id},
            UpdateExpression=f'SET {flag_name} = :true, alert_date = :date',
            ExpressionAttributeValues={
                ':true': True,
                ':date': datetime.utcnow().isoformat()
            }
        )
    except Exception as e:
        print(f'Erro ao marcar flag: {str(e)}')

import boto3
from datetime import datetime, timedelta

ses = boto3.client('ses')
dynamodb = boto3.resource('dynamodb')

def lambda_handler(event, context):
    table = dynamodb.Table('mediaflow-users')
    
    # Buscar todos os usuários trial
    response = table.scan(
        FilterExpression='plan = :trial',
        ExpressionAttributeValues={':trial': 'trial'}
    )
    
    emails_sent = 0
    
    for user in response['Items']:
        # Verificar alertas de limite
        if user.get('alert_storage') and not_sent_today(user, 'storage'):
            send_email(user, 'storage_limit')
            clear_flag(user['user_id'], 'alert_storage', 'storage')
            emails_sent += 1
        
        if user.get('alert_bandwidth') and not_sent_today(user, 'bandwidth'):
            send_email(user, 'bandwidth_limit')
            clear_flag(user['user_id'], 'alert_bandwidth', 'bandwidth')
            emails_sent += 1
        
        # Verificar trial
        if not user.get('trial_end'):
            continue
            
        trial_end = datetime.fromisoformat(user['trial_end'])
        days_since_trial = (datetime.utcnow() - trial_end).days
        
        # Email D+0 (trial expirou hoje)
        if days_since_trial == 0:
            send_email(user, 'trial_expired')
            emails_sent += 1
        
        # Email D+7 (50% OFF)
        elif days_since_trial == 7:
            send_email(user, 'last_chance')
            emails_sent += 1
        
        # Email D+30 (3 meses)
        elif days_since_trial == 30:
            send_email(user, 'comeback')
            emails_sent += 1
        
        # Email D+90 (aviso exclusão)
        elif days_since_trial == 90:
            send_email(user, 'deletion_warning')
            emails_sent += 1
    
    return {
        'statusCode': 200,
        'body': f'{emails_sent} emails enviados'
    }

def not_sent_today(user, alert_type):
    alert_sent = user.get('alert_sent', {})
    last_sent = alert_sent.get(alert_type)
    
    if not last_sent:
        return True
    
    last_sent_date = datetime.fromisoformat(last_sent).date()
    today = datetime.utcnow().date()
    
    return last_sent_date < today

def clear_flag(user_id, flag_name, alert_type):
    try:
        table = dynamodb.Table('mediaflow-users')
        table.update_item(
            Key={'user_id': user_id},
            UpdateExpression=f'SET {flag_name} = :false, alert_sent.{alert_type} = :date',
            ExpressionAttributeValues={
                ':false': False,
                ':date': datetime.utcnow().isoformat()
            }
        )
    except Exception as e:
        print(f'Erro ao limpar flag: {str(e)}')

def send_email(user, template):
    templates = {
        'storage_limit': {
            'subject': 'Limite de armazenamento atingido',
            'body': f'''Olá {user.get('name', 'usuário')},

Você atingiu o limite de armazenamento do seu plano.

Faça upgrade para continuar enviando vídeos:
https://midiaflow.sstechnologies-cloud.com/pricing

Equipe Mídiaflow'''
        },
        'bandwidth_limit': {
            'subject': 'Limite de bandwidth atingido',
            'body': f'''Olá {user.get('name', 'usuário')},

Você atingiu o limite de bandwidth do seu plano.

Faça upgrade para continuar:
https://midiaflow.sstechnologies-cloud.com/pricing

Equipe Mídiaflow'''
        },
        'trial_expired': {
            'subject': 'Seu trial expirou - Continue de onde parou',
            'body': f'''Olá {user.get('name', 'usuário')},

Seu trial de 15 dias expirou. Seus vídeos estão seguros e acessíveis.

Faça upgrade para continuar:
• Basic: $19.99/mês (50 GB)
• Pro: $39.99/mês (200 GB)

Acesse: https://midiaflow.sstechnologies-cloud.com/pricing

Equipe Mídiaflow'''
        },
        'last_chance': {
            'subject': '50% OFF - Última chance antes do arquivamento',
            'body': f'''Olá {user.get('name', 'usuário')},

Última chance! Use o cupom VOLTA50 para 50% OFF no primeiro mês.

Seus vídeos serão arquivados amanhã (mas não deletados).

Ativar agora: https://midiaflow.sstechnologies-cloud.com/pricing?cupom=VOLTA50

Equipe Mídiaflow'''
        },
        'comeback': {
            'subject': 'Sentimos sua falta - 3 meses por $29.99',
            'body': f'''Olá {user.get('name', 'usuário')},

Sentimos sua falta! Oferta especial: 3 meses por apenas $29.99.

Use o cupom: VOLTA3X

Reativar conta: https://midiaflow.sstechnologies-cloud.com/pricing?cupom=VOLTA3X

Equipe Mídiaflow'''
        },
        'deletion_warning': {
            'subject': '⚠️ Seus vídeos serão deletados em 30 dias',
            'body': f'''Olá {user.get('name', 'usuário')},

ATENÇÃO: Seus vídeos serão deletados permanentemente em 30 dias.

Para salvar seus vídeos, faça upgrade agora:
https://midiaflow.sstechnologies-cloud.com/pricing

Equipe Mídiaflow'''
        }
    }
    
    email_data = templates.get(template)
    if not email_data:
        return
    
    try:
        ses.send_email(
            Source='noreply@midiaflow.sstechnologies-cloud.com',
            Destination={'ToAddresses': [user.get('email')]},
            Message={
                'Subject': {'Data': email_data['subject']},
                'Body': {'Text': {'Data': email_data['body']}}
            }
        )
    except Exception as e:
        print(f"Erro ao enviar email para {user.get('email')}: {str(e)}")

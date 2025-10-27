import boto3
from datetime import datetime, timedelta

logs = boto3.client('logs', region_name='us-east-1')

# Lambdas de upload
lambda_groups = [
    '/aws/lambda/mediaflow-upload-handler',
    '/aws/lambda/mediaflow-multipart-handler'
]

# Buscar últimos 30 dias
start_time = int((datetime.now() - timedelta(days=30)).timestamp() * 1000)
end_time = int(datetime.now().timestamp() * 1000)

print('Buscando logs de upload com "Jiggly" nos ultimos 30 dias...\n')

for group in lambda_groups:
    print(f'\n=== {group} ===\n')
    
    try:
        response = logs.filter_log_events(
            logGroupName=group,
            startTime=start_time,
            endTime=end_time,
            filterPattern='Jiggly'
        )
        
        events = response.get('events', [])
        print(f'Encontrados: {len(events)} eventos\n')
        
        for event in events[:10]:  # Primeiros 10
            timestamp = datetime.fromtimestamp(event['timestamp'] / 1000)
            message = event['message']
            print(f'{timestamp}: {message[:200]}')
            
        if len(events) > 10:
            print(f'\n... e mais {len(events) - 10} eventos')
            
    except Exception as e:
        print(f'Erro: {e}')

print('\n\nConcluido!')

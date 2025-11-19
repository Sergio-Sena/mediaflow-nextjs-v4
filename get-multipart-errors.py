#!/usr/bin/env python3
import boto3
from datetime import datetime, timedelta

logs = boto3.client('logs', region_name='us-east-1')

# Buscar logs dos últimos 24 horas
start_time = int((datetime.now() - timedelta(hours=24)).timestamp() * 1000)
end_time = int(datetime.now().timestamp() * 1000)

log_group = '/aws/lambda/mediaflow-multipart-handler'

try:
    response = logs.filter_log_events(
        logGroupName=log_group,
        startTime=start_time,
        endTime=end_time,
        interleaved=True
    )
    
    print(f"\n{'='*70}")
    print(f"Ultimos eventos - {log_group}")
    print(f"Total: {len(response['events'])} eventos")
    print(f"{'='*70}\n")
    
    # Mostrar últimos 50 eventos
    for event in response['events'][-50:]:
        timestamp = datetime.fromtimestamp(event['timestamp'] / 1000)
        message = event['message'].strip()
        
        print(f"{timestamp.strftime('%Y-%m-%d %H:%M:%S')} | {message}")
    
except Exception as e:
    print(f"Erro: {str(e)}\n")

print(f"\n{'='*70}\n")

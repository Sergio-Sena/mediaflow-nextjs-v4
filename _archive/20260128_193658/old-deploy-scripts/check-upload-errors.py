#!/usr/bin/env python3
import boto3
from datetime import datetime, timedelta

logs = boto3.client('logs', region_name='us-east-1')

# Buscar logs dos últimos 60 minutos
start_time = int((datetime.now() - timedelta(minutes=60)).timestamp() * 1000)
end_time = int(datetime.now().timestamp() * 1000)

log_group = '/aws/lambda/mediaflow-upload-handler'

try:
    print(f"\n{'='*70}")
    print(f"Ultimos erros - {log_group}")
    print(f"{'='*70}\n")
    
    response = logs.filter_log_events(
        logGroupName=log_group,
        startTime=start_time,
        endTime=end_time,
        interleaved=True
    )
    
    if not response['events']:
        print("Nenhum evento encontrado nos ultimos 60 minutos\n")
    else:
        # Mostrar últimos 30 eventos
        for event in response['events'][-30:]:
            timestamp = datetime.fromtimestamp(event['timestamp'] / 1000)
            message = event['message'].strip()
            
            # Destacar erros
            if 'ERROR' in message or 'error' in message or 'Exception' in message or 'Traceback' in message:
                print(f"[ERRO] {timestamp.strftime('%Y-%m-%d %H:%M:%S')}")
                print(f"  {message}\n")
            elif 'WARN' in message or 'warn' in message:
                print(f"[AVISO] {timestamp.strftime('%Y-%m-%d %H:%M:%S')}")
                print(f"  {message}\n")
        
except Exception as e:
    print(f"Erro ao buscar logs: {str(e)}\n")

print(f"{'='*70}\n")

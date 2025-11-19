#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import boto3
import json
from datetime import datetime, timedelta
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

logs = boto3.client('logs', region_name='us-east-1')

# Buscar logs dos últimos 30 minutos
start_time = int((datetime.now() - timedelta(minutes=30)).timestamp() * 1000)
end_time = int(datetime.now().timestamp() * 1000)

log_groups = [
    '/aws/lambda/upload-handler',
    '/aws/lambda/multipart-handler',
    '/aws/apigateway/upload-api'
]

for log_group in log_groups:
    try:
        print(f"\n{'='*60}")
        print(f"Log Group: {log_group}")
        print(f"{'='*60}\n")
        
        response = logs.filter_log_events(
            logGroupName=log_group,
            startTime=start_time,
            endTime=end_time,
            interleaved=True
        )
        
        if not response['events']:
            print("Sem erros nos ultimos 30 minutos\n")
            continue
        
        # Mostrar últimos 20 eventos
        for event in response['events'][-20:]:
            timestamp = datetime.fromtimestamp(event['timestamp'] / 1000)
            message = event['message']
            
            # Destacar erros
            if 'ERROR' in message or 'error' in message or 'Exception' in message:
                print(f"[ERRO] [{timestamp.strftime('%H:%M:%S')}] {message}")
            elif 'WARN' in message or 'warn' in message:
                print(f"[AVISO] [{timestamp.strftime('%H:%M:%S')}] {message}")
            else:
                print(f"[INFO] [{timestamp.strftime('%H:%M:%S')}] {message}")
        
    except Exception as e:
        print(f"[AVISO] Erro ao buscar {log_group}: {str(e)}\n")

print(f"\n{'='*60}")
print("Verificacao concluida")
print(f"{'='*60}\n")

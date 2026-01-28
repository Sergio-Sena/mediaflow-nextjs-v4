#!/usr/bin/env python3
import boto3
from datetime import datetime, timedelta

logs = boto3.client('logs', region_name='us-east-1')

# Buscar logs dos últimos 24 horas
start_time = int((datetime.now() - timedelta(hours=24)).timestamp() * 1000)
end_time = int(datetime.now().timestamp() * 1000)

lambdas = [
    '/aws/lambda/mediaflow-upload-handler',
    '/aws/lambda/mediaflow-multipart-handler',
    '/aws/lambda/video-streaming-upload',
    '/aws/lambda/video-streaming-v2-upload'
]

for log_group in lambdas:
    try:
        response = logs.filter_log_events(
            logGroupName=log_group,
            startTime=start_time,
            endTime=end_time,
            interleaved=True
        )
        
        if not response['events']:
            continue
        
        print(f"\n{'='*70}")
        print(f"Log Group: {log_group}")
        print(f"Total de eventos: {len(response['events'])}")
        print(f"{'='*70}\n")
        
        # Mostrar últimos 15 eventos
        for event in response['events'][-15:]:
            timestamp = datetime.fromtimestamp(event['timestamp'] / 1000)
            message = event['message'].strip()
            
            if 'ERROR' in message or 'error' in message or 'Exception' in message or 'Traceback' in message:
                print(f"[ERRO] {timestamp.strftime('%H:%M:%S')}")
                print(f"  {message}\n")
        
    except Exception as e:
        pass

print(f"{'='*70}\n")

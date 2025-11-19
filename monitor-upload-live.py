#!/usr/bin/env python3
import boto3
from datetime import datetime, timedelta
import time

logs = boto3.client('logs', region_name='us-east-1')

print("\n" + "="*70)
print("MONITORANDO UPLOAD EM TEMPO REAL")
print("="*70 + "\n")

while True:
    start_time = int((datetime.now() - timedelta(seconds=30)).timestamp() * 1000)
    end_time = int(datetime.now().timestamp() * 1000)
    
    response = logs.filter_log_events(
        logGroupName='/aws/lambda/mediaflow-multipart-handler',
        startTime=start_time,
        endTime=end_time,
        interleaved=True
    )
    
    if response['events']:
        print(f"\n[{datetime.now().strftime('%H:%M:%S')}] Eventos encontrados: {len(response['events'])}")
        
        for event in response['events'][-5:]:
            msg = event['message'].strip()
            if 'START' in msg or 'END' in msg or 'REPORT' in msg or 'User ID' in msg:
                print(f"  {msg[:100]}")
    else:
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Aguardando eventos...")
    
    time.sleep(2)

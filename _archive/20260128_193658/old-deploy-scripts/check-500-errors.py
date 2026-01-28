#!/usr/bin/env python3
import boto3
from datetime import datetime, timedelta

logs = boto3.client('logs', region_name='us-east-1')

start_time = int((datetime.now() - timedelta(minutes=5)).timestamp() * 1000)
end_time = int(datetime.now().timestamp() * 1000)

response = logs.filter_log_events(
    logGroupName='/aws/lambda/mediaflow-multipart-handler',
    startTime=start_time,
    endTime=end_time,
    interleaved=True
)

print("\nUltimos eventos com ERRO:\n")
for event in response['events']:
    message = event['message'].strip()
    if 'ERROR' in message or 'error' in message or 'Traceback' in message or 'Exception' in message:
        print(f"{message}\n")

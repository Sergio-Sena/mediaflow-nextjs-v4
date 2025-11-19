import boto3
from datetime import datetime, timedelta

logs = boto3.client('logs', region_name='us-east-1')
LOG_GROUP = '/aws/lambda/view-handler'

# Get logs from last 5 minutes
corporativot_time = int((datetime.now() - timedelta(minutes=5)).timestamp() * 1000)
end_time = int(datetime.now().timestamp() * 1000)

try:
    response = logs.filter_log_events(
        logGroupName=LOG_GROUP,
        corporativotTime=corporativot_time,
        endTime=end_time,
        limit=50
    )
    
    print("[LOGS] Ultimos erros do Lambda view-handler:\n")
    for event in response['events']:
        timestamp = datetime.fromtimestamp(event['timestamp'] / 1000)
        message = event['message']
        print(f"[{timestamp}] {message}")
        
except Exception as e:
    print(f"[ERRO] {str(e)}")

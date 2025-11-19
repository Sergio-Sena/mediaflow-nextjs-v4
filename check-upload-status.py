#!/usr/bin/env python3
import boto3
from datetime import datetime, timedelta

logs = boto3.client('logs', region_name='us-east-1')
s3 = boto3.client('s3', region_name='us-east-1')

print("\n" + "="*70)
print("STATUS DO UPLOAD")
print("="*70 + "\n")

# Verificar logs dos ultimos 2 minutos
start_time = int((datetime.now() - timedelta(minutes=2)).timestamp() * 1000)
end_time = int(datetime.now().timestamp() * 1000)

response = logs.filter_log_events(
    logGroupName='/aws/lambda/mediaflow-multipart-handler',
    startTime=start_time,
    endTime=end_time,
    interleaved=True
)

if response['events']:
    print(f"Total de eventos: {len(response['events'])}\n")
    
    # Contar STARTs e ENDs
    starts = sum(1 for e in response['events'] if 'START' in e['message'])
    ends = sum(1 for e in e['events'] if 'END' in e['message'])
    
    print(f"Requisicoes iniciadas: {starts}")
    print(f"Requisicoes finalizadas: {ends}")
    
    if starts > ends:
        print(f"\n⏳ UPLOAD EM CURSO - {starts - ends} requisicoes pendentes")
    else:
        print(f"\n✅ UPLOAD CONCLUIDO")
    
    print("\nUltimos eventos:")
    for event in response['events'][-10:]:
        msg = event['message'].strip()
        if any(x in msg for x in ['START', 'END', 'REPORT', 'User ID']):
            print(f"  {msg[:80]}")
else:
    print("Nenhum evento encontrado nos ultimos 2 minutos")
    print("Upload pode estar congelado ou nao iniciou")

print("\n" + "="*70 + "\n")

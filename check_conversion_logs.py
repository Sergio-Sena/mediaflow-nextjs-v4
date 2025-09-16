#!/usr/bin/env python3
import boto3
from datetime import datetime, timedelta

def check_conversion_logs():
    logs = boto3.client('logs')
    
    # Log groups das funções de conversão
    log_groups = [
        '/aws/lambda/mediaflow-convert-handler',
        '/aws/lambda/mediaflow-cleanup-handler'
    ]
    
    # Últimas 24 horas
    end_time = datetime.now()
    start_time = end_time - timedelta(hours=24)
    
    print("LOGS DE CONVERSAO - ULTIMAS 24H")
    print("=" * 50)
    
    for log_group in log_groups:
        print(f"\n{log_group}:")
        try:
            response = logs.filter_log_events(
                logGroupName=log_group,
                startTime=int(start_time.timestamp() * 1000),
                endTime=int(end_time.timestamp() * 1000)
            )
            
            events = response.get('events', [])
            if not events:
                print("  Nenhum log encontrado")
                continue
                
            # Mostrar últimos 10 eventos
            for event in events[-10:]:
                timestamp = datetime.fromtimestamp(event['timestamp'] / 1000)
                message = event['message'].strip()
                print(f"  {timestamp.strftime('%H:%M:%S')}: {message}")
                
        except Exception as e:
            print(f"  Erro: {e}")

if __name__ == "__main__":
    check_conversion_logs()
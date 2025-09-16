#!/usr/bin/env python3
import boto3
import json
from datetime import datetime, timedelta

def check_post_conversion():
    logs = boto3.client('logs')
    s3 = boto3.client('s3')
    
    print("VERIFICACAO POS-CONVERSAO")
    print("=" * 40)
    
    # 1. Verificar logs do cleanup handler
    print("\n1. LOGS CLEANUP HANDLER:")
    try:
        end_time = datetime.now()
        start_time = end_time - timedelta(hours=2)
        
        response = logs.filter_log_events(
            logGroupName='/aws/lambda/mediaflow-cleanup-handler',
            startTime=int(start_time.timestamp() * 1000),
            endTime=int(end_time.timestamp() * 1000)
        )
        
        events = response.get('events', [])
        if events:
            for event in events[-5:]:
                timestamp = datetime.fromtimestamp(event['timestamp'] / 1000)
                print(f"  {timestamp.strftime('%H:%M:%S')}: {event['message'].strip()}")
        else:
            print("  Nenhum log de cleanup encontrado")
    except Exception as e:
        print(f"  Erro: {e}")
    
    # 2. Verificar EventBridge rules
    print("\n2. EVENTBRIDGE RULES:")
    try:
        events = boto3.client('events')
        response = events.list_rules(NamePrefix='mediaflow')
        
        for rule in response.get('Rules', []):
            print(f"  {rule['Name']}: {rule['State']}")
            
            # Verificar targets
            targets = events.list_targets_by_rule(Rule=rule['Name'])
            for target in targets.get('Targets', []):
                print(f"    -> {target.get('Arn', 'Unknown target')}")
                
    except Exception as e:
        print(f"  Erro: {e}")
    
    # 3. Verificar arquivos recentes
    print("\n3. ARQUIVOS RECENTES (ShyBlanche):")
    try:
        response = s3.list_objects_v2(
            Bucket='mediaflow-uploads-969430605054',
            Prefix='ShyBlanche/'
        )
        
        files = []
        if 'Contents' in response:
            for obj in response['Contents']:
                if not obj['Key'].endswith('/'):
                    files.append({
                        'key': obj['Key'],
                        'modified': obj['LastModified'],
                        'size': obj['Size'] / (1024*1024)
                    })
        
        # Ordenar por data
        files.sort(key=lambda x: x['modified'], reverse=True)
        
        for file in files[:5]:
            print(f"  {file['key']} ({file['size']:.1f}MB) - {file['modified'].strftime('%H:%M:%S')}")
            
    except Exception as e:
        print(f"  Erro: {e}")

if __name__ == "__main__":
    check_post_conversion()
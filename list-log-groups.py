#!/usr/bin/env python3
import boto3

logs = boto3.client('logs', region_name='us-east-1')

try:
    response = logs.describe_log_groups()
    
    print("\nLog Groups disponiveis:\n")
    for lg in response['logGroups']:
        print(f"  - {lg['logGroupName']}")
    
    if not response['logGroups']:
        print("  Nenhum log group encontrado")
        
except Exception as e:
    print(f"Erro: {str(e)}")

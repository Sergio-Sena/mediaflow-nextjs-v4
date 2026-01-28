#!/usr/bin/env python3
import boto3

apigw = boto3.client('apigateway', region_name='us-east-1')

api_id = 'gdb962d234'

print("Fazendo deploy da API Gateway...\n")

try:
    response = apigw.create_deployment(
        restApiId=api_id,
        stageName='prod',
        description='CORS fix deployment'
    )
    
    print(f"Deploy ID: {response['id']}")
    print(f"Status: {response['status']}")
    print("API Gateway atualizada com sucesso!")
    
except Exception as e:
    print(f"Erro: {str(e)}")

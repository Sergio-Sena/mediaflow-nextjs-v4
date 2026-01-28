#!/usr/bin/env python3
import boto3

apigw = boto3.client('apigateway', region_name='us-east-1')

# Obter API
api_id = 'gdb962d234'
resources = apigw.get_resources(restApiId=api_id)['items']

# Encontrar /multipart/{action}
for res in resources:
    if res.get('path') == '/multipart/{action}':
        print(f"Recurso: {res['path']}")
        print(f"Resource ID: {res['id']}\n")
        
        # Obter integração POST
        integration = apigw.get_integration(
            restApiId=api_id,
            resourceId=res['id'],
            httpMethod='POST'
        )
        
        print(f"Tipo: {integration['type']}")
        print(f"URI: {integration.get('uri', 'N/A')}")
        print(f"Timeout: {integration.get('timeoutInMillis', 29000)}ms")
        print(f"HTTP Method: {integration.get('httpMethod', 'N/A')}")

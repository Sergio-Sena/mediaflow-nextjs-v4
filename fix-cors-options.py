#!/usr/bin/env python3
import boto3

apigw = boto3.client('apigateway', region_name='us-east-1')

api_id = 'gdb962d234'
resources = apigw.get_resources(restApiId=api_id)['items']

# Encontrar /multipart/{action}
for res in resources:
    if res.get('path') == '/multipart/{action}':
        resource_id = res['id']
        print(f"Recurso: {res['path']} (ID: {resource_id})\n")
        
        # Verificar se OPTIONS existe
        try:
            options = apigw.get_integration(
                restApiId=api_id,
                resourceId=resource_id,
                httpMethod='OPTIONS'
            )
            print(f"OPTIONS existe: {options['type']}")
            print(f"URI: {options.get('uri', 'N/A')}")
        except:
            print("OPTIONS nao existe - criando...")
            
            # Criar integração MOCK para OPTIONS
            apigw.put_integration(
                restApiId=api_id,
                resourceId=resource_id,
                httpMethod='OPTIONS',
                type='MOCK',
                requestTemplates={'application/json': '{"statusCode": 200}'}
            )
            
            # Criar response
            apigw.put_integration_response(
                restApiId=api_id,
                resourceId=resource_id,
                httpMethod='OPTIONS',
                statusCode='200',
                responseParameters={
                    'method.response.header.Access-Control-Allow-Headers': "'Content-Type,Authorization'",
                    'method.response.header.Access-Control-Allow-Methods': "'POST,OPTIONS'",
                    'method.response.header.Access-Control-Allow-Origin': "'*'"
                }
            )
            
            print("OPTIONS criado com sucesso!")

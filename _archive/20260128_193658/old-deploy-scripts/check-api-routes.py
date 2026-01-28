#!/usr/bin/env python3
import boto3

apigw = boto3.client('apigateway', region_name='us-east-1')

# Listar APIs
apis = apigw.get_rest_apis()['items']
print(f"\nAPIs encontradas: {len(apis)}\n")

for api in apis:
    if 'gdb962d234' in api['id'] or 'upload' in api['name'].lower():
        print(f"API: {api['name']} ({api['id']})")
        
        # Listar recursos
        resources = apigw.get_resources(restApiId=api['id'])['items']
        print(f"  Recursos: {len(resources)}")
        
        for res in resources:
            path = res.get('path', '/')
            if 'multipart' in path or 'upload' in path:
                print(f"    - {path}")
                
                # Listar métodos
                if 'resourceMethods' in res:
                    for method in res['resourceMethods']:
                        print(f"      {method}")

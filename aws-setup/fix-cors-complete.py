#!/usr/bin/env python3
"""Fix CORS for API Gateway"""
import boto3
import json

client = boto3.client('apigateway', region_name='us-east-1')

# Get API ID
apis = client.get_rest_apis()
api_id = None
for api in apis['items']:
    if 'mediaflow' in api['name'].lower() or 'midiaflow' in api['name'].lower():
        api_id = api['id']
        print(f"Found API: {api['name']} ({api_id})")
        break

if not api_id:
    print("API not found")
    exit(1)

# Get resources
resources = client.get_resources(restApiId=api_id)

# Find /auth/login resource
for resource in resources['items']:
    path = resource.get('path', '')
    if '/auth/login' in path or path == '/auth':
        resource_id = resource['id']
        print(f"Found resource: {path} ({resource_id})")
        
        # Check if OPTIONS method exists
        methods = resource.get('resourceMethods', {})
        
        if 'OPTIONS' not in methods:
            print("Creating OPTIONS method...")
            client.put_method(
                restApiId=api_id,
                resourceId=resource_id,
                httpMethod='OPTIONS',
                authorizationType='NONE'
            )
            
            # Add mock integration
            client.put_integration(
                restApiId=api_id,
                resourceId=resource_id,
                httpMethod='OPTIONS',
                type='MOCK',
                requestTemplates={'application/json': '{"statusCode": 200}'}
            )
            
            # Add method response
            client.put_method_response(
                restApiId=api_id,
                resourceId=resource_id,
                httpMethod='OPTIONS',
                statusCode='200',
                responseParameters={
                    'method.response.header.Access-Control-Allow-Headers': True,
                    'method.response.header.Access-Control-Allow-Methods': True,
                    'method.response.header.Access-Control-Allow-Origin': True
                }
            )
            
            # Add integration response
            client.put_integration_response(
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
            print("OPTIONS method created")
        else:
            print("OPTIONS method already exists")

# Deploy API
print("Deploying API...")
client.create_deployment(
    restApiId=api_id,
    stageName='prod',
    description='CORS fix deployment'
)
print("API deployed successfully!")

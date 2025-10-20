#!/usr/bin/env python3
import boto3

client = boto3.client('apigateway', region_name='us-east-1')
API_ID = 'gdb962d234'

# Enable CORS for /auth/login
response = client.update_integration_response(
    restApiId=API_ID,
    resourceId='auth-resource-id',
    httpMethod='POST',
    statusCode='200',
    patchOperations=[
        {
            'op': 'add',
            'path': '/responseParameters/method.response.header.Access-Control-Allow-Origin',
            'value': "'*'"
        }
    ]
)

print("CORS enabled for /auth/login")

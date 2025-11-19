#!/usr/bin/env python3
import boto3
import json

lambda_client = boto3.client('lambda', region_name='us-east-1')

# Simular evento de /multipart/init
event = {
    "httpMethod": "POST",
    "path": "/multipart/init",
    "headers": {
        "Authorization": "Bearer eyJhbGciOiAiSFMyNTYiLCAidHlwIjogIkpXVCJ9.eyJlbWFpbCI6ICJzZXJnaW9AbWlkaWFmbG93LmNvbSIsICJ1c2VyX2lkIjogInNlcmdpb19zZW5hIiwgInMzX3ByZWZpeCI6ICJ1c2Vycy9zZXJnaW9fc2VuYS8iLCAicm9sZSI6ICJ1c2VyIiwgImV4cCI6IDE3NjM2NDQ5Mjh9.gWT_U_mgrS-74hZc7bxgOfbdxIchDvtmjKv2k7VqA5Q"
    },
    "body": json.dumps({
        "filename": "Star/kate kuray/test.mp4",
        "fileSize": 1000000000
    })
}

print("Testando /multipart/init...\n")

try:
    response = lambda_client.invoke(
        FunctionName='mediaflow-multipart-handler',
        InvocationType='RequestResponse',
        Payload=json.dumps(event)
    )
    
    result = json.loads(response['Payload'].read())
    print(f"Status: {response['StatusCode']}")
    print(f"Response: {json.dumps(result, indent=2)}")
    
except Exception as e:
    print(f"Erro: {str(e)}")

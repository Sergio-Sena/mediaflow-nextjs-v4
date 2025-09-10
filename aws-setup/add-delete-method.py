#!/usr/bin/env python3
import boto3

# Add DELETE method to /files resource
apigateway = boto3.client('apigateway')
lambda_client = boto3.client('lambda')

api_id = 'gdb962d234'
resource_id = '7s6xdy'  # /files resource ID
account_id = '969430605054'
region = 'us-east-1'

try:
    # Add DELETE method
    apigateway.put_method(
        restApiId=api_id,
        resourceId=resource_id,
        httpMethod='DELETE',
        authorizationType='NONE'
    )
    print("Added DELETE method")
    
    # Add integration
    function_arn = f"arn:aws:lambda:{region}:{account_id}:function:mediaflow-files-handler"
    integration_uri = f"arn:aws:apigateway:{region}:lambda:path/2015-03-31/functions/{function_arn}/invocations"
    
    apigateway.put_integration(
        restApiId=api_id,
        resourceId=resource_id,
        httpMethod='DELETE',
        type='AWS_PROXY',
        integrationHttpMethod='POST',
        uri=integration_uri
    )
    print("Added DELETE integration")
    
    # Deploy
    apigateway.create_deployment(
        restApiId=api_id,
        stageName='prod'
    )
    print("Deployed API")
    
except Exception as e:
    print(f"Error: {e}")
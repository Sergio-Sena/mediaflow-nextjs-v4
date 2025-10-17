import boto3
import zipfile
import json
import os

lambda_client = boto3.client('lambda', region_name='us-east-1')
iam_client = boto3.client('iam', region_name='us-east-1')
apigateway = boto3.client('apigateway', region_name='us-east-1')

with open('mediaflow-config.json', 'r') as f:
    config = json.load(f)

# Zip Lambda
zip_path = 'lambda-functions/update-user/function.zip'
with zipfile.ZipFile(zip_path, 'w') as zipf:
    zipf.write('lambda-functions/update-user/index.py', 'index.py')

with open(zip_path, 'rb') as f:
    zip_content = f.read()

# Deploy Lambda
function_name = 'mediaflow-update-user'
try:
    lambda_client.update_function_code(
        FunctionName=function_name,
        ZipFile=zip_content
    )
    print(f"Updated Lambda: {function_name}")
except lambda_client.exceptions.ResourceNotFoundException:
    lambda_client.create_function(
        FunctionName=function_name,
        Runtime='python3.11',
        Role=config['lambda_role_arn'],
        Handler='index.lambda_handler',
        Code={'ZipFile': zip_content},
        Timeout=30,
        Environment={'Variables': {}}
    )
    print(f"Created Lambda: {function_name}")

# Add API Gateway route
api_id = config['api_gateway']['api_id']

# Create resource
try:
    resources = apigateway.get_resources(restApiId=api_id)
    root_id = [r for r in resources['items'] if r['path'] == '/'][0]['id']
    
    resource = apigateway.create_resource(
        restApiId=api_id,
        parentId=root_id,
        pathPart='update-user'
    )
    resource_id = resource['id']
    print(f"Created resource: /update-user")
except:
    resources = apigateway.get_resources(restApiId=api_id)
    resource_id = [r for r in resources['items'] if r.get('pathPart') == 'update-user'][0]['id']
    print(f"Resource exists: /update-user")

# Create POST method
try:
    apigateway.put_method(
        restApiId=api_id,
        resourceId=resource_id,
        httpMethod='POST',
        authorizationType='NONE'
    )
    
    lambda_arn = lambda_client.get_function(FunctionName=function_name)['Configuration']['FunctionArn']
    
    apigateway.put_integration(
        restApiId=api_id,
        resourceId=resource_id,
        httpMethod='POST',
        type='AWS_PROXY',
        integrationHttpMethod='POST',
        uri=f'arn:aws:apigateway:us-east-1:lambda:path/2015-03-31/functions/{lambda_arn}/invocations'
    )
    
    # Lambda permission
    lambda_client.add_permission(
        FunctionName=function_name,
        StatementId='apigateway-invoke-update-user',
        Action='lambda:InvokeFunction',
        Principal='apigateway.amazonaws.com',
        SourceArn=f'arn:aws:execute-api:us-east-1:{config["account_id"]}:{api_id}/*/*'
    )
    
    print("Created POST method")
except Exception as e:
    print(f"Method exists or error: {e}")

# Deploy API
apigateway.create_deployment(
    restApiId=api_id,
    stageName='prod'
)

print(f"\nLambda deployed!")
print(f"URL: https://{api_id}.execute-api.us-east-1.amazonaws.com/prod/update-user")

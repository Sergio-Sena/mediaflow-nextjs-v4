import boto3
import zipfile
import json

lambda_client = boto3.client('lambda', region_name='us-east-1')
apigateway = boto3.client('apigateway', region_name='us-east-1')

with open('mediaflow-config.json', 'r') as f:
    config = json.load(f)

# Zip Lambda
zip_path = 'lambda-functions/avatar-presigned/function.zip'
with zipfile.ZipFile(zip_path, 'w') as zipf:
    zipf.write('lambda-functions/avatar-presigned/index.py', 'index.py')

with open(zip_path, 'rb') as f:
    zip_content = f.read()

# Deploy Lambda
function_name = 'mediaflow-avatar-presigned'
try:
    lambda_client.update_function_code(
        FunctionName=function_name,
        ZipFile=zip_content
    )
    print(f"Updated: {function_name}")
except:
    lambda_client.create_function(
        FunctionName=function_name,
        Runtime='python3.11',
        Role=config['lambda_role_arn'],
        Handler='index.lambda_handler',
        Code={'ZipFile': zip_content},
        Timeout=30
    )
    print(f"Created: {function_name}")

# Add API Gateway route
api_id = config['api_gateway']['api_id']
resources = apigateway.get_resources(restApiId=api_id)
root_id = [r for r in resources['items'] if r['path'] == '/'][0]['id']

try:
    resource = apigateway.create_resource(
        restApiId=api_id,
        parentId=root_id,
        pathPart='avatar-presigned'
    )
    resource_id = resource['id']
except:
    resource_id = [r for r in resources['items'] if r.get('pathPart') == 'avatar-presigned'][0]['id']

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
    
    lambda_client.add_permission(
        FunctionName=function_name,
        StatementId='apigateway-avatar-presigned',
        Action='lambda:InvokeFunction',
        Principal='apigateway.amazonaws.com',
        SourceArn=f'arn:aws:execute-api:us-east-1:{config["account_id"]}:{api_id}/*/*'
    )
except Exception as e:
    print(f"Method exists: {e}")

apigateway.create_deployment(restApiId=api_id, stageName='prod')
print(f"\nDeployed: https://{api_id}.execute-api.us-east-1.amazonaws.com/prod/avatar-presigned")

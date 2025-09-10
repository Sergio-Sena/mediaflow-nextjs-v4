#!/usr/bin/env python3
import boto3

# Add convert route to API Gateway
apigateway = boto3.client('apigateway')

api_id = 'gdb962d234'
account_id = '969430605054'
region = 'us-east-1'

try:
    # Get root resource
    resources = apigateway.get_resources(restApiId=api_id)
    root_id = None
    
    for item in resources['items']:
        if item['path'] == '/':
            root_id = item['id']
            break
    
    print(f"Root resource ID: {root_id}")
    
    # Create /convert resource
    try:
        convert_resource = apigateway.create_resource(
            restApiId=api_id,
            parentId=root_id,
            pathPart='convert'
        )
        convert_resource_id = convert_resource['id']
        print(f"Created /convert resource: {convert_resource_id}")
    except Exception as e:
        if 'ConflictException' in str(e):
            # Resource exists, find it
            for item in resources['items']:
                if item.get('pathPart') == 'convert':
                    convert_resource_id = item['id']
                    print(f"Found existing /convert resource: {convert_resource_id}")
                    break
        else:
            raise e
    
    # Add methods and integration
    function_arn = f"arn:aws:lambda:{region}:{account_id}:function:mediaflow-convert-handler"
    integration_uri = f"arn:aws:apigateway:{region}:lambda:path/2015-03-31/functions/{function_arn}/invocations"
    
    for method in ['GET', 'POST', 'OPTIONS']:
        try:
            # Add method
            apigateway.put_method(
                restApiId=api_id,
                resourceId=convert_resource_id,
                httpMethod=method,
                authorizationType='NONE'
            )
            print(f"Added {method} method")
            
            # Add integration
            apigateway.put_integration(
                restApiId=api_id,
                resourceId=convert_resource_id,
                httpMethod=method,
                type='AWS_PROXY',
                integrationHttpMethod='POST',
                uri=integration_uri
            )
            print(f"Added {method} integration")
            
        except Exception as e:
            if 'ConflictException' not in str(e):
                print(f"Error with {method}: {e}")
    
    # Add Lambda permission
    lambda_client = boto3.client('lambda')
    try:
        lambda_client.add_permission(
            FunctionName='mediaflow-convert-handler',
            StatementId='apigateway-convert-invoke',
            Action='lambda:InvokeFunction',
            Principal='apigateway.amazonaws.com',
            SourceArn=f"arn:aws:execute-api:{region}:{account_id}:{api_id}/*/*"
        )
        print("Added Lambda permission")
    except Exception as e:
        if 'ResourceConflictException' not in str(e):
            print(f"Permission error: {e}")
    
    # Deploy
    apigateway.create_deployment(
        restApiId=api_id,
        stageName='prod'
    )
    print("Deployed API")
    
    print("✅ MediaConvert route ready!")
    print("URL: https://gdb962d234.execute-api.us-east-1.amazonaws.com/prod/convert")
    
except Exception as e:
    print(f"Error: {e}")
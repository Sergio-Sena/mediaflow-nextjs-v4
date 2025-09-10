#!/usr/bin/env python3
import boto3
import json

def add_view_route():
    """Add /view/{key} route to API Gateway"""
    
    with open('mediaflow-config.json', 'r') as f:
        config = json.load(f)
    
    apigateway = boto3.client('apigateway')
    lambda_client = boto3.client('lambda')
    
    api_id = config['api_gateway']['api_id']
    
    # Get root resource
    resources = apigateway.get_resources(restApiId=api_id)
    root_id = resources['items'][0]['id']
    
    # Create /view resource
    view_resource = apigateway.create_resource(
        restApiId=api_id,
        parentId=root_id,
        pathPart='view'
    )
    view_resource_id = view_resource['id']
    
    # Create /{key} resource under /view
    key_resource = apigateway.create_resource(
        restApiId=api_id,
        parentId=view_resource_id,
        pathPart='{key}'
    )
    key_resource_id = key_resource['id']
    
    # Add GET method
    apigateway.put_method(
        restApiId=api_id,
        resourceId=key_resource_id,
        httpMethod='GET',
        authorizationType='NONE'
    )
    
    # Add OPTIONS method
    apigateway.put_method(
        restApiId=api_id,
        resourceId=key_resource_id,
        httpMethod='OPTIONS',
        authorizationType='NONE'
    )
    
    # Get Lambda function ARN
    lambda_response = lambda_client.get_function(FunctionName='mediaflow-view-handler')
    function_arn = lambda_response['Configuration']['FunctionArn']
    
    # Create integration for GET
    integration_uri = f"arn:aws:apigateway:{config['region']}:lambda:path/2015-03-31/functions/{function_arn}/invocations"
    
    for method in ['GET', 'OPTIONS']:
        apigateway.put_integration(
            restApiId=api_id,
            resourceId=key_resource_id,
            httpMethod=method,
            type='AWS_PROXY',
            integrationHttpMethod='POST',
            uri=integration_uri
        )
        
        # Add Lambda permission
        try:
            lambda_client.add_permission(
                FunctionName='mediaflow-view-handler',
                StatementId=f"apigateway-view-{method}-{key_resource_id}",
                Action='lambda:InvokeFunction',
                Principal='apigateway.amazonaws.com',
                SourceArn=f"arn:aws:execute-api:{config['region']}:{config['account_id']}:{api_id}/*/*"
            )
        except:
            pass
    
    # Deploy API
    apigateway.create_deployment(
        restApiId=api_id,
        stageName='prod'
    )
    
    print("View route added to API Gateway")

if __name__ == "__main__":
    add_view_route()
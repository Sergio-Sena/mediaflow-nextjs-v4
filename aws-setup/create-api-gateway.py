#!/usr/bin/env python3
import boto3
import json
import time

def create_api_gateway():
    """Create API Gateway and connect Lambda functions"""
    
    # Load config
    with open('mediaflow-config.json', 'r') as f:
        config = json.load(f)
    
    apigateway = boto3.client('apigateway')
    lambda_client = boto3.client('lambda')
    
    print("Creating API Gateway...")
    
    # Create REST API
    api_response = apigateway.create_rest_api(
        name='mediaflow-api',
        description='Mediaflow Next.js API',
        endpointConfiguration={'types': ['REGIONAL']}
    )
    api_id = api_response['id']
    print(f"Created API: {api_id}")
    
    # Get root resource
    resources = apigateway.get_resources(restApiId=api_id)
    root_id = resources['items'][0]['id']
    
    # Create resources and methods
    routes = [
        {
            'path': 'auth',
            'methods': [
                {'method': 'POST', 'path': 'login', 'function': 'mediaflow-auth-handler'},
                {'method': 'OPTIONS', 'path': 'login', 'function': 'mediaflow-auth-handler'}
            ]
        },
        {
            'path': 'files',
            'methods': [
                {'method': 'GET', 'path': '', 'function': 'mediaflow-files-handler'},
                {'method': 'DELETE', 'path': '{key}', 'function': 'mediaflow-files-handler'},
                {'method': 'POST', 'path': 'bulk-delete', 'function': 'mediaflow-files-handler'},
                {'method': 'OPTIONS', 'path': '', 'function': 'mediaflow-files-handler'}
            ]
        },
        {
            'path': 'upload',
            'methods': [
                {'method': 'POST', 'path': 'presigned', 'function': 'mediaflow-upload-handler'},
                {'method': 'OPTIONS', 'path': 'presigned', 'function': 'mediaflow-upload-handler'}
            ]
        },
        {
            'path': 'cleanup',
            'methods': [
                {'method': 'POST', 'path': '', 'function': 'mediaflow-cleanup-handler'},
                {'method': 'OPTIONS', 'path': '', 'function': 'mediaflow-cleanup-handler'}
            ]
        }
    ]
    
    created_resources = {}
    
    for route in routes:
        # Create main resource
        resource_response = apigateway.create_resource(
            restApiId=api_id,
            parentId=root_id,
            pathPart=route['path']
        )
        main_resource_id = resource_response['id']
        created_resources[route['path']] = main_resource_id
        print(f"Created resource: /{route['path']}")
        
        for method_config in route['methods']:
            resource_id = main_resource_id
            
            # Create sub-resource if needed
            if method_config['path'] and method_config['path'] != '':
                if method_config['path'] not in created_resources:
                    sub_resource_response = apigateway.create_resource(
                        restApiId=api_id,
                        parentId=main_resource_id,
                        pathPart=method_config['path']
                    )
                    resource_id = sub_resource_response['id']
                    created_resources[method_config['path']] = resource_id
                    print(f"Created sub-resource: /{route['path']}/{method_config['path']}")
                else:
                    resource_id = created_resources[method_config['path']]
            
            # Create method
            apigateway.put_method(
                restApiId=api_id,
                resourceId=resource_id,
                httpMethod=method_config['method'],
                authorizationType='NONE'
            )
            
            # Get Lambda function ARN
            lambda_response = lambda_client.get_function(FunctionName=method_config['function'])
            function_arn = lambda_response['Configuration']['FunctionArn']
            
            # Create integration
            integration_uri = f"arn:aws:apigateway:{config['region']}:lambda:path/2015-03-31/functions/{function_arn}/invocations"
            
            apigateway.put_integration(
                restApiId=api_id,
                resourceId=resource_id,
                httpMethod=method_config['method'],
                type='AWS_PROXY',
                integrationHttpMethod='POST',
                uri=integration_uri
            )
            
            # Add Lambda permission
            try:
                lambda_client.add_permission(
                    FunctionName=method_config['function'],
                    StatementId=f"apigateway-{api_id}-{method_config['method']}-{resource_id}",
                    Action='lambda:InvokeFunction',
                    Principal='apigateway.amazonaws.com',
                    SourceArn=f"arn:aws:execute-api:{config['region']}:{config['account_id']}:{api_id}/*/*"
                )
            except:
                pass  # Permission might already exist
            
            print(f"Created method: {method_config['method']} /{route['path']}/{method_config['path']}")
    
    # Deploy API
    print("Deploying API...")
    apigateway.create_deployment(
        restApiId=api_id,
        stageName='prod'
    )
    
    # Update config
    api_url = f"https://{api_id}.execute-api.{config['region']}.amazonaws.com/prod"
    config['api_gateway'] = {
        'api_id': api_id,
        'api_url': api_url,
        'stage': 'prod'
    }
    
    with open('mediaflow-config.json', 'w') as f:
        json.dump(config, f, indent=2)
    
    print(f"API Gateway deployed: {api_url}")
    return api_url

def test_api(api_url):
    """Test API endpoints"""
    import requests
    
    print("\nTesting API endpoints...")
    
    # Test auth endpoint
    try:
        response = requests.post(f"{api_url}/auth/login", 
            json={"email": "sergiosenaadmin@sstech", "password": "sergiosena"},
            timeout=10
        )
        if response.status_code == 200:
            print("✅ Auth endpoint working")
            token = response.json().get('token')
        else:
            print(f"❌ Auth endpoint failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Auth endpoint error: {str(e)}")
        return False
    
    # Test files endpoint
    try:
        response = requests.get(f"{api_url}/files", timeout=10)
        if response.status_code == 200:
            print("✅ Files endpoint working")
        else:
            print(f"❌ Files endpoint failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Files endpoint error: {str(e)}")
    
    # Test upload endpoint
    try:
        response = requests.post(f"{api_url}/upload/presigned",
            json={"filename": "test.mp4", "contentType": "video/mp4"},
            timeout=10
        )
        if response.status_code == 200:
            print("✅ Upload endpoint working")
        else:
            print(f"❌ Upload endpoint failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Upload endpoint error: {str(e)}")
    
    return True

if __name__ == "__main__":
    api_url = create_api_gateway()
    time.sleep(5)  # Wait for deployment
    test_api(api_url)
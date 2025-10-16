import boto3
import zipfile
import os
import json

lambda_client = boto3.client('lambda', region_name='us-east-1')
iam_client = boto3.client('iam', region_name='us-east-1')
apigateway = boto3.client('apigateway', region_name='us-east-1')

FUNCTION_NAME = 'mediaflow-create-user'
ROLE_ARN = 'arn:aws:iam::969430605054:role/mediaflow-lambda-role'
API_ID = 'gdb962d234'

def create_zip():
    zip_path = 'lambda-functions/create-user/create-user.zip'
    with zipfile.ZipFile(zip_path, 'w') as zipf:
        zipf.write('lambda-functions/create-user/lambda_function.py', 'lambda_function.py')
    return zip_path

def deploy_lambda():
    zip_path = create_zip()
    
    with open(zip_path, 'rb') as f:
        zip_content = f.read()
    
    try:
        # Tentar atualizar
        lambda_client.update_function_code(
            FunctionName=FUNCTION_NAME,
            ZipFile=zip_content
        )
        print(f'Lambda {FUNCTION_NAME} atualizada')
    except lambda_client.exceptions.ResourceNotFoundException:
        # Criar nova
        lambda_client.create_function(
            FunctionName=FUNCTION_NAME,
            Runtime='python3.12',
            Role=ROLE_ARN,
            Handler='lambda_function.lambda_handler',
            Code={'ZipFile': zip_content},
            Timeout=30,
            MemorySize=256
        )
        print(f'Lambda {FUNCTION_NAME} criada')

def setup_api_routes():
    # GET /prod/users/{user_id} - já existe
    # POST /prod/users/create - criar
    # DELETE /prod/users/{user_id} - criar
    
    resources = apigateway.get_resources(restApiId=API_ID)
    
    # Encontrar resource /users
    users_resource = None
    for resource in resources['items']:
        if resource['path'] == '/users':
            users_resource = resource
            break
    
    if not users_resource:
        print('Resource /users nao encontrado')
        return
    
    # Criar /users/create
    try:
        create_resource = apigateway.create_resource(
            restApiId=API_ID,
            parentId=users_resource['id'],
            pathPart='create'
        )
        print('Resource /users/create criado')
    except:
        # Já existe
        for resource in resources['items']:
            if resource['path'] == '/users/create':
                create_resource = resource
                break
    
    # POST /users/create
    try:
        apigateway.put_method(
            restApiId=API_ID,
            resourceId=create_resource['id'],
            httpMethod='POST',
            authorizationType='NONE'
        )
        
        apigateway.put_integration(
            restApiId=API_ID,
            resourceId=create_resource['id'],
            httpMethod='POST',
            type='AWS_PROXY',
            integrationHttpMethod='POST',
            uri=f'arn:aws:apigateway:us-east-1:lambda:path/2015-03-31/functions/arn:aws:lambda:us-east-1:969430605054:function:{FUNCTION_NAME}/invocations'
        )
        print('POST /users/create configurado')
    except:
        print('POST /users/create ja existe')
    
    # DELETE /users/{user_id}
    # Encontrar resource /users/{user_id}
    user_id_resource = None
    for resource in resources['items']:
        if resource['path'] == '/users/{user_id}':
            user_id_resource = resource
            break
    
    if not user_id_resource:
        # Criar {user_id}
        user_id_resource = apigateway.create_resource(
            restApiId=API_ID,
            parentId=users_resource['id'],
            pathPart='{user_id}'
        )
        print('Resource /users/{user_id} criado')
    
    try:
        apigateway.put_method(
            restApiId=API_ID,
            resourceId=user_id_resource['id'],
            httpMethod='DELETE',
            authorizationType='NONE'
        )
        
        apigateway.put_integration(
            restApiId=API_ID,
            resourceId=user_id_resource['id'],
            httpMethod='DELETE',
            type='AWS_PROXY',
            integrationHttpMethod='POST',
            uri=f'arn:aws:apigateway:us-east-1:lambda:path/2015-03-31/functions/arn:aws:lambda:us-east-1:969430605054:function:{FUNCTION_NAME}/invocations'
        )
        print('DELETE /users/{user_id} configurado')
    except:
        print('DELETE /users/{user_id} ja existe')
    
    # Deploy API
    apigateway.create_deployment(
        restApiId=API_ID,
        stageName='prod'
    )
    print('API Gateway deployed')

def add_lambda_permissions():
    try:
        lambda_client.add_permission(
            FunctionName=FUNCTION_NAME,
            StatementId='apigateway-create-user',
            Action='lambda:InvokeFunction',
            Principal='apigateway.amazonaws.com',
            SourceArn=f'arn:aws:execute-api:us-east-1:969430605054:{API_ID}/*/*'
        )
        print('Permissoes adicionadas')
    except:
        print('Permissoes ja existem')

if __name__ == '__main__':
    print('Deploying create-user Lambda...')
    deploy_lambda()
    setup_api_routes()
    add_lambda_permissions()
    print('Deploy completo!')
    print('Endpoints:')
    print('   POST https://gdb962d234.execute-api.us-east-1.amazonaws.com/prod/users/create')
    print('   DELETE https://gdb962d234.execute-api.us-east-1.amazonaws.com/prod/users/{user_id}')

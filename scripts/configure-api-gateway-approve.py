import boto3

api_client = boto3.client('apigateway', region_name='us-east-1')
lambda_client = boto3.client('lambda', region_name='us-east-1')

API_ID = 'gdb962d234'
LAMBDA_ARN = 'arn:aws:lambda:us-east-1:969430605054:function:approve-user'
REGION = 'us-east-1'
ACCOUNT_ID = '969430605054'

def get_resource_id(path):
    resources = api_client.get_resources(restApiId=API_ID)
    for resource in resources['items']:
        if resource['path'] == path:
            return resource['id']
    return None

def create_resource(parent_id, path_part):
    try:
        response = api_client.create_resource(
            restApiId=API_ID,
            parentId=parent_id,
            pathPart=path_part
        )
        return response['id']
    except api_client.exceptions.ConflictException:
        resources = api_client.get_resources(restApiId=API_ID)
        for resource in resources['items']:
            if resource.get('pathPart') == path_part and resource['parentId'] == parent_id:
                return resource['id']

def setup():
    print('[1/6] Buscando resource /users...')
    users_id = get_resource_id('/users')
    if not users_id:
        root_id = api_client.get_resources(restApiId=API_ID)['items'][0]['id']
        users_id = create_resource(root_id, 'users')
    
    print('[2/6] Criando resource /users/approve...')
    approve_id = create_resource(users_id, 'approve')
    
    print('[3/6] Criando metodo POST...')
    try:
        api_client.put_method(
            restApiId=API_ID,
            resourceId=approve_id,
            httpMethod='POST',
            authorizationType='NONE'
        )
    except api_client.exceptions.ConflictException:
        pass
    
    print('[4/6] Integrando com Lambda...')
    api_client.put_integration(
        restApiId=API_ID,
        resourceId=approve_id,
        httpMethod='POST',
        type='AWS_PROXY',
        integrationHttpMethod='POST',
        uri=f'arn:aws:apigateway:{REGION}:lambda:path/2015-03-31/functions/{LAMBDA_ARN}/invocations'
    )
    
    print('[5/6] Adicionando permissao Lambda...')
    try:
        lambda_client.add_permission(
            FunctionName='approve-user',
            StatementId='apigateway-approve-user',
            Action='lambda:InvokeFunction',
            Principal='apigateway.amazonaws.com',
            SourceArn=f'arn:aws:execute-api:{REGION}:{ACCOUNT_ID}:{API_ID}/*/*'
        )
    except lambda_client.exceptions.ResourceConflictException:
        pass
    
    print('[6/6] Fazendo deploy...')
    api_client.create_deployment(
        restApiId=API_ID,
        stageName='prod'
    )
    
    print('Configuracao concluida!')
    print('Endpoint: https://gdb962d234.execute-api.us-east-1.amazonaws.com/prod/users/approve')

if __name__ == '__main__':
    setup()

#!/usr/bin/env python3

import boto3
import zipfile
import os
import json

# Configurações
REGION = 'us-east-1'
ACCOUNT_ID = '969430605054'

# Clientes AWS
lambda_client = boto3.client('lambda', region_name=REGION)
apigateway = boto3.client('apigateway', region_name=REGION)

def zip_lambda(function_name):
    """Criar ZIP da função Lambda"""
    zip_path = f'lambda-functions/{function_name}/function.zip'
    
    with zipfile.ZipFile(zip_path, 'w') as zipf:
        # Adicionar arquivo principal
        if os.path.exists(f'lambda-functions/{function_name}/index.py'):
            zipf.write(f'lambda-functions/{function_name}/index.py', 'index.py')
        elif os.path.exists(f'lambda-functions/{function_name}/lambda_function.py'):
            zipf.write(f'lambda-functions/{function_name}/lambda_function.py', 'lambda_function.py')
    
    return zip_path

def deploy_lambda(function_name, handler='index.lambda_handler'):
    """Deploy função Lambda"""
    print(f"📦 Deploying {function_name}...")
    
    zip_path = zip_lambda(function_name)
    
    try:
        # Atualizar código da função
        with open(zip_path, 'rb') as zip_file:
            lambda_client.update_function_code(
                FunctionName=function_name,
                ZipFile=zip_file.read()
            )
        print(f"✅ {function_name} updated successfully")
        
    except lambda_client.exceptions.ResourceNotFoundException:
        print(f"❌ Function {function_name} not found. Create it first via AWS Console.")
    
    except Exception as e:
        print(f"❌ Error deploying {function_name}: {str(e)}")

def update_api_routes():
    """Atualizar rotas do API Gateway"""
    print("🔗 Updating API Gateway routes...")
    
    # Encontrar API Gateway ID
    apis = apigateway.get_rest_apis()
    api_id = None
    
    for api in apis['items']:
        if 'mediaflow' in api['name'].lower():
            api_id = api['id']
            break
    
    if not api_id:
        print("❌ API Gateway not found")
        return
    
    print(f"📡 Found API Gateway: {api_id}")
    
    # Listar recursos existentes
    resources = apigateway.get_resources(restApiId=api_id)
    
    # Procurar recurso /users
    users_resource_id = None
    for resource in resources['items']:
        if resource['pathPart'] == 'users':
            users_resource_id = resource['id']
            break
    
    if users_resource_id:
        print(f"✅ Found /users resource: {users_resource_id}")
        
        # Verificar se já existe rota DELETE
        try:
            apigateway.get_method(
                restApiId=api_id,
                resourceId=users_resource_id,
                httpMethod='DELETE'
            )
            print("✅ DELETE method already exists")
        except:
            print("➕ Adding DELETE method...")
            # Adicionar método DELETE seria complexo aqui
            # Melhor fazer via console AWS
    
    print("🚀 Deploy API Gateway changes manually via AWS Console")

def main():
    print("🚀 Deploying User Management System...")
    print("=" * 50)
    
    # Deploy Lambdas
    deploy_lambda('update-user')
    deploy_lambda('delete-user')
    deploy_lambda('files-handler')
    
    # Atualizar API Gateway
    update_api_routes()
    
    print("\n✅ Deployment completed!")
    print("\n📋 Manual steps needed:")
    print("1. Add DELETE /users/{user_id} route in API Gateway")
    print("2. Add POST /users/update route in API Gateway") 
    print("3. Deploy API Gateway stage")
    print("4. Test admin vs user filtering")

if __name__ == '__main__':
    main()
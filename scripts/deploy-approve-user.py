import boto3
import zipfile
import os
import time

lambda_client = boto3.client('lambda', region_name='us-east-1')
iam_client = boto3.client('iam', region_name='us-east-1')

FUNCTION_NAME = 'approve-user'
ROLE_ARN = 'arn:aws:iam::969430605054:role/mediaflow-lambda-role'
LAMBDA_DIR = '../aws-setup/lambda-functions/approve-user'

def create_zip():
    zip_path = f'{LAMBDA_DIR}/function.zip'
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        zipf.write(f'{LAMBDA_DIR}/lambda_function.py', 'lambda_function.py')
    return zip_path

def deploy():
    print(f'[1/3] Criando ZIP...')
    zip_path = create_zip()
    
    print(f'[2/3] Fazendo upload para Lambda...')
    with open(zip_path, 'rb') as f:
        zip_content = f.read()
    
    try:
        lambda_client.get_function(FunctionName=FUNCTION_NAME)
        print(f'[3/3] Atualizando funcao existente...')
        lambda_client.update_function_code(
            FunctionName=FUNCTION_NAME,
            ZipFile=zip_content
        )
    except lambda_client.exceptions.ResourceNotFoundException:
        print(f'[3/3] Criando nova funcao...')
        lambda_client.create_function(
            FunctionName=FUNCTION_NAME,
            Runtime='python3.11',
            Role=ROLE_ARN,
            Handler='lambda_function.lambda_handler',
            Code={'ZipFile': zip_content},
            Timeout=30,
            MemorySize=256
        )
        time.sleep(2)
    
    print(f'Deploy concluido!')
    print(f'Endpoint: https://gdb962d234.execute-api.us-east-1.amazonaws.com/prod/users/approve')

if __name__ == '__main__':
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    deploy()

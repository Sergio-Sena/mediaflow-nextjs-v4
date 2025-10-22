import boto3
import zipfile
import os

lambda_client = boto3.client('lambda', region_name='us-east-1')

# Zip Lambda
os.chdir('lambda-functions/folder-operations')
with zipfile.ZipFile('lambda.zip', 'w') as zipf:
    zipf.write('lambda_function.py')

# Deploy
with open('lambda.zip', 'rb') as f:
    try:
        lambda_client.create_function(
            FunctionName='folder-operations',
            Runtime='python3.12',
            Role='arn:aws:iam::969430605054:role/mediaflow-lambda-role',
            Handler='lambda_function.lambda_handler',
            Code={'ZipFile': f.read()},
            Timeout=30,
            MemorySize=256
        )
        print('Lambda folder-operations criada')
    except lambda_client.exceptions.ResourceConflictException:
        f.seek(0)
        lambda_client.update_function_code(
            FunctionName='folder-operations',
            ZipFile=f.read()
        )
        print('Lambda folder-operations atualizada')

os.remove('lambda.zip')
print('Deploy concluido')

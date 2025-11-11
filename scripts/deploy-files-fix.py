import boto3
import zipfile
import os

lambda_client = boto3.client('lambda', region_name='us-east-1')

# Criar ZIP
zip_path = 'aws-setup/lambda-functions/files-handler/files-handler-fixed.zip'
with zipfile.ZipFile(zip_path, 'w') as zipf:
    zipf.write('aws-setup/lambda-functions/files-handler/lambda_function.py', 'lambda_function.py')
    zipf.write('aws-setup/lambda-functions/lib/logger.py', 'logger.py')

# Deploy
with open(zip_path, 'rb') as f:
    lambda_client.update_function_code(
        FunctionName='mediaflow-files-handler',
        ZipFile=f.read()
    )

print("=" * 80)
print("FILES-HANDLER DEPLOYADO")
print("=" * 80)
print("Mudancas:")
print("  - Removida role 'media_owner'")
print("  - Admin agora ve TUDO")
print("  - Users veem apenas suas pastas")
print("=" * 80)

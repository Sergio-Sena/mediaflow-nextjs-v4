import boto3
import zipfile
import os

lambda_client = boto3.client('lambda', region_name='us-east-1')

zip_path = 'mediaflow-view-handler.zip'
with zipfile.ZipFile(zip_path, 'w') as zipf:
    zipf.write('aws-setup/lambda-functions/view-handler/lambda_function.py', 'lambda_function.py')

with open(zip_path, 'rb') as f:
    lambda_client.update_function_code(
        FunctionName='mediaflow-view-handler',
        ZipFile=f.read()
    )

os.remove(zip_path)
print("[OK] Lambda mediaflow-view-handler atualizado")

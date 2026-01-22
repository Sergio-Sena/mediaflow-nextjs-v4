import boto3
import zipfile
import os
import subprocess

# Instalar dependências
print("Instalando dependencias...")
subprocess.run(['pip', 'install', 'PyJWT', '-t', 'temp_lambda'], check=True)

# Criar ZIP
print("Criando ZIP...")
with zipfile.ZipFile('view-handler.zip', 'w') as zipf:
    # Adicionar código
    zipf.write('aws-setup/lambda-functions/view-handler/lambda_function.py', 'lambda_function.py')
    
    # Adicionar dependências
    for root, dirs, files in os.walk('temp_lambda'):
        for file in files:
            file_path = os.path.join(root, file)
            arcname = os.path.relpath(file_path, 'temp_lambda')
            zipf.write(file_path, arcname)

# Deploy
print("Fazendo deploy...")
lambda_client = boto3.client('lambda', region_name='us-east-1')
with open('view-handler.zip', 'rb') as f:
    lambda_client.update_function_code(
        FunctionName='mediaflow-view-handler',
        ZipFile=f.read()
    )

# Cleanup
import shutil
shutil.rmtree('temp_lambda')
os.remove('view-handler.zip')

print("Deploy completo!")

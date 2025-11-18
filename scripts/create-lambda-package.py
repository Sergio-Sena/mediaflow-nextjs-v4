import os
import subprocess
import zipfile
import shutil

print("[1/4] Instalando dependencias...")
subprocess.run([
    "pip", "install", 
    "PyJWT==2.8.0",
    "-t", "lambda_package"
], check=True)

print("[2/4] Copiando codigo Lambda...")
shutil.copy(
    "aws-setup/lambda-functions/view-handler/lambda_function.py",
    "lambda_package/lambda_function.py"
)

print("[3/4] Criando ZIP...")
with zipfile.ZipFile('mediaflow-view-handler.zip', 'w', zipfile.ZIP_DEFLATED) as zipf:
    for root, dirs, files in os.walk('lambda_package'):
        for file in files:
            file_path = os.path.join(root, file)
            arcname = os.path.relpath(file_path, 'lambda_package')
            zipf.write(file_path, arcname)

print("[4/4] Fazendo deploy...")
import boto3
lambda_client = boto3.client('lambda', region_name='us-east-1')

with open('mediaflow-view-handler.zip', 'rb') as f:
    lambda_client.update_function_code(
        FunctionName='mediaflow-view-handler',
        ZipFile=f.read()
    )

print("[OK] Limpando...")
shutil.rmtree('lambda_package')
os.remove('mediaflow-view-handler.zip')

print("\n[SUCESSO] Lambda atualizado com dependencias!")

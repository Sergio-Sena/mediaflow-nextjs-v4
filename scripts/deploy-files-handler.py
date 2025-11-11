import boto3
import zipfile
import os
import tempfile

lambda_client = boto3.client('lambda', region_name='us-east-1')

print("Deploying files-handler with media_owner role...")

# Create zip
zip_path = os.path.join(tempfile.gettempdir(), 'files-handler.zip')

with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
    zipf.write('aws-setup/lambda-functions/files-handler/lambda_function.py', 'lambda_function.py')
    zipf.write('aws-setup/lambda-functions/lib/logger.py', 'logger.py')

# Deploy
with open(zip_path, 'rb') as f:
    zip_content = f.read()

response = lambda_client.update_function_code(
    FunctionName='mediaflow-files-handler',
    ZipFile=zip_content
)

print("OK - files-handler deployed")
print("\n=== Sistema Atualizado ===")
print("Sergio Sena (media_owner): Ve TODAS as midias")
print("Admin: Apenas tarefas administrativas (nao ve midias)")
print("\nCusto total: $0.00")

import boto3
import zipfile
import os
import json

def deploy_secure_view():
    print("=" * 60)
    print("DEPLOY DA FUNCAO VIEW COM AUTENTICACAO")
    print("=" * 60)
    
    lambda_client = boto3.client('lambda', region_name='us-east-1')
    
    # Create zip file
    zip_path = 'view-handler-secure.zip'
    
    with zipfile.ZipFile(zip_path, 'w') as zip_file:
        zip_file.write(
            'aws-setup/lambda-functions/view-handler/lambda_function.py',
            'lambda_function.py'
        )
    
    # Read zip file
    with open(zip_path, 'rb') as zip_file:
        zip_content = zip_file.read()
    
    try:
        # Update function code
        response = lambda_client.update_function_code(
            FunctionName='mediaflow-view-handler',
            ZipFile=zip_content
        )
        
        print("[OK] Funcao Lambda atualizada com sucesso")
        print(f"[INFO] Versao: {response['Version']}")
        print(f"[INFO] Ultima modificacao: {response['LastModified']}")
        
        # Update environment variables to include JWT_SECRET
        lambda_client.update_function_configuration(
            FunctionName='mediaflow-view-handler',
            Environment={
                'Variables': {
                    'UPLOADS_BUCKET': 'mediaflow-uploads-969430605054',
                    'PROCESSED_BUCKET': 'mediaflow-processed-969430605054',
                    'JWT_SECRET': 'your-secret-key'
                }
            }
        )
        
        print("[OK] Variaveis de ambiente atualizadas")
        
    except Exception as e:
        print(f"[ERRO] Falha no deploy: {str(e)}")
    
    # Cleanup
    if os.path.exists(zip_path):
        os.remove(zip_path)
    
    print("\n[CONCLUIDO] Deploy da seguranca implementado")

if __name__ == "__main__":
    deploy_secure_view()
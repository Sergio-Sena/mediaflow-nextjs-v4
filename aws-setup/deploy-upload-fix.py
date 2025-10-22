#!/usr/bin/env python3
"""Deploy da Lambda upload-handler corrigida"""

import boto3
import zipfile
from pathlib import Path

def create_zip():
    lambda_dir = Path(__file__).parent / 'lambda-functions' / 'upload-handler'
    zip_path = lambda_dir / 'upload-handler-fixed.zip'
    
    print(f"Criando ZIP: {zip_path}")
    
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        zipf.write(lambda_dir / 'lambda_function.py', 'lambda_function.py')
    
    print(f"ZIP criado: {zip_path.stat().st_size} bytes")
    return zip_path

def deploy(zip_path):
    lambda_client = boto3.client('lambda', region_name='us-east-1')
    function_name = 'mediaflow-upload-handler'
    
    print(f"\nDeploy Lambda: {function_name}")
    
    with open(zip_path, 'rb') as f:
        response = lambda_client.update_function_code(
            FunctionName=function_name,
            ZipFile=f.read(),
            Publish=True
        )
    
    print(f"Lambda atualizada!")
    print(f"Version: {response['Version']}")
    print(f"Code Size: {response['CodeSize']} bytes")

def main():
    print("=" * 60)
    print("DEPLOY UPLOAD-HANDLER FIX")
    print("=" * 60)
    print("\nCorrecao: user_id ao inves de username")
    print("Antes: users/anonymous/")
    print("Depois: users/{user_id}/\n")
    
    zip_path = create_zip()
    deploy(zip_path)
    
    print("\n" + "=" * 60)
    print("DEPLOY CONCLUIDO!")
    print("=" * 60)
    print("\nTeste: Faca logout/login e upload novamente")

if __name__ == '__main__':
    main()

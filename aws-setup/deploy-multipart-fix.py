#!/usr/bin/env python3
"""
Deploy da Lambda multipart-handler corrigida
Corrige o problema de path duplicado (users/anonymous/users/user_admin/)
"""

import boto3
import zipfile
import os
from pathlib import Path

def create_lambda_zip():
    """Criar ZIP da Lambda"""
    lambda_dir = Path(__file__).parent / 'lambda-functions' / 'multipart-handler'
    zip_path = lambda_dir / 'multipart-handler-fixed.zip'
    
    print(f"Criando ZIP: {zip_path}")
    
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        zipf.write(lambda_dir / 'lambda_function.py', 'lambda_function.py')
    
    print(f"ZIP criado: {zip_path.stat().st_size} bytes")
    return zip_path

def deploy_lambda(zip_path):
    """Deploy da Lambda na AWS"""
    lambda_client = boto3.client('lambda', region_name='us-east-1')
    function_name = 'mediaflow-multipart-handler'
    
    print(f"\nFazendo deploy da Lambda: {function_name}")
    
    with open(zip_path, 'rb') as f:
        zip_content = f.read()
    
    try:
        response = lambda_client.update_function_code(
            FunctionName=function_name,
            ZipFile=zip_content,
            Publish=True
        )
        
        print(f"Lambda atualizada com sucesso!")
        print(f"   Version: {response['Version']}")
        print(f"   Last Modified: {response['LastModified']}")
        print(f"   Code Size: {response['CodeSize']} bytes")
        
        return True
        
    except Exception as e:
        print(f"Erro no deploy: {e}")
        return False

def main():
    print("=" * 60)
    print("DEPLOY MULTIPART-HANDLER FIX")
    print("=" * 60)
    print("\nCorrecao: user_id ao inves de username no JWT")
    print("   Antes: users/anonymous/users/user_admin/")
    print("   Depois: users/user_admin/")
    print()
    
    # Criar ZIP
    zip_path = create_lambda_zip()
    
    # Deploy
    if deploy_lambda(zip_path):
        print("\n" + "=" * 60)
        print("DEPLOY CONCLUIDO COM SUCESSO!")
        print("=" * 60)
        print("\nTeste agora:")
        print("   1. Faca logout e login novamente")
        print("   2. Faca upload de um arquivo >100MB")
        print("   3. Verifique o path no S3: users/user_admin/")
        print()
    else:
        print("\nDeploy falhou!")

if __name__ == '__main__':
    main()

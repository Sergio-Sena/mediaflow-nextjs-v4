#!/usr/bin/env python3
"""
Deploy fix para Lambda multipart-handler
Corrige duplicação do prefixo users/ no path dos arquivos
"""

import boto3
import zipfile
import os
import sys
from pathlib import Path

def create_deployment_package():
    """Criar pacote ZIP da Lambda"""
    lambda_dir = Path("aws-setup/lambda-functions/multipart-handler")
    zip_path = lambda_dir / "multipart-handler-fixed.zip"
    
    print(f"Criando pacote: {zip_path}")
    
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        # Adicionar lambda_function.py
        lambda_file = lambda_dir / "lambda_function.py"
        if lambda_file.exists():
            zipf.write(lambda_file, "lambda_function.py")
            print(f"Adicionado: lambda_function.py")
        else:
            print(f"Erro: Arquivo nao encontrado: {lambda_file}")
            return None
    
    return zip_path

def deploy_lambda(zip_path):
    """Deploy da Lambda para AWS"""
    try:
        lambda_client = boto3.client('lambda', region_name='us-east-1')
        
        print(f"Fazendo deploy da Lambda...")
        
        with open(zip_path, 'rb') as zip_file:
            response = lambda_client.update_function_code(
                FunctionName='mediaflow-multipart-handler',
                ZipFile=zip_file.read()
            )
        
        print(f"Deploy concluido!")
        print(f"Versao: {response['Version']}")
        print(f"Ultima modificacao: {response['LastModified']}")
        print(f"SHA256: {response['CodeSha256'][:16]}...")
        
        return True
        
    except Exception as e:
        print(f"Erro no deploy: {e}")
        return False

def main():
    print("Deploy Fix - Lambda Multipart Handler")
    print("=" * 50)
    
    # Verificar se estamos no diretório correto
    if not Path("aws-setup/lambda-functions/multipart-handler").exists():
        print("Erro: Execute este script na raiz do projeto!")
        sys.exit(1)
    
    # Criar pacote
    zip_path = create_deployment_package()
    if not zip_path:
        print("Erro: Falha ao criar pacote!")
        sys.exit(1)
    
    # Deploy
    if deploy_lambda(zip_path):
        print("\nFix deployado com sucesso!")
        print("\nMudancas:")
        print("- Corrigida duplicacao do prefixo users/ no path")
        print("- Lambda agora verifica se filename ja tem prefixo users/")
        print("- Path correto: users/user_admin/Star/arquivo.mp4")
        print("- Sem duplicacao: users/user_admin/users/user_admin/Star/arquivo.mp4")
    else:
        print("\nErro: Falha no deploy!")
        sys.exit(1)

if __name__ == "__main__":
    main()
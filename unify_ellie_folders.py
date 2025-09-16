#!/usr/bin/env python3
"""
Script para unificar pastas Ellie_morre e Elllie_morre em Ellie_moore
"""

import boto3
import json
from botocore.exceptions import ClientError

def load_config():
    """Carrega configuração do Mediaflow"""
    with open('aws-setup/mediaflow-config.json', 'r') as f:
        return json.load(f)

def copy_s3_object(source_bucket, source_key, dest_bucket, dest_key):
    """Copia objeto no S3"""
    s3 = boto3.client('s3')
    
    try:
        copy_source = {'Bucket': source_bucket, 'Key': source_key}
        s3.copy_object(CopySource=copy_source, Bucket=dest_bucket, Key=dest_key)
        return True
    except ClientError as e:
        print(f"Erro ao copiar {source_key}: {e}")
        return False

def delete_s3_object(bucket, key):
    """Deleta objeto no S3"""
    s3 = boto3.client('s3')
    
    try:
        s3.delete_object(Bucket=bucket, Key=key)
        return True
    except ClientError as e:
        print(f"Erro ao deletar {key}: {e}")
        return False

def list_folder_files(bucket_name, folder_name):
    """Lista todos os arquivos de uma pasta"""
    s3 = boto3.client('s3')
    
    try:
        response = s3.list_objects_v2(
            Bucket=bucket_name,
            Prefix=f"{folder_name}/"
        )
        
        files = []
        if 'Contents' in response:
            for obj in response['Contents']:
                if not obj['Key'].endswith('/'):  # Não incluir a própria pasta
                    files.append(obj['Key'])
        
        return files
    except ClientError as e:
        print(f"Erro ao listar arquivos: {e}")
        return []

def unify_folders():
    """Unifica as pastas Ellie_morre e Elllie_morre em Ellie_moore"""
    config = load_config()
    bucket = config['buckets']['uploads']
    
    print("MEDIAFLOW - Unificacao de Pastas Ellie")
    print("=" * 50)
    
    # Pastas origem
    source_folders = ['Ellie_morre', 'Elllie_morre']
    target_folder = 'Ellie_moore'
    
    print(f"Bucket: {bucket}")
    print(f"Pasta destino: {target_folder}")
    print("=" * 50)
    
    total_files = 0
    moved_files = 0
    
    for source_folder in source_folders:
        print(f"\nProcessando pasta: {source_folder}")
        
        # Listar arquivos da pasta origem
        files = list_folder_files(bucket, source_folder)
        
        if not files:
            print(f"  Nenhum arquivo encontrado em {source_folder}")
            continue
        
        print(f"  Encontrados {len(files)} arquivo(s)")
        total_files += len(files)
        
        # Mover cada arquivo
        for file_key in files:
            # Extrair nome do arquivo (sem a pasta)
            file_name = file_key.split('/')[-1]
            
            # Novo caminho na pasta destino
            new_key = f"{target_folder}/{file_name}"
            
            print(f"    Movendo: {file_name}")
            
            # Copiar arquivo para nova localização
            if copy_s3_object(bucket, file_key, bucket, new_key):
                # Deletar arquivo original
                if delete_s3_object(bucket, file_key):
                    moved_files += 1
                    print(f"      OK: {file_name}")
                else:
                    print(f"      ERRO ao deletar: {file_name}")
            else:
                print(f"      ERRO ao copiar: {file_name}")
    
    print("\n" + "=" * 50)
    print("RESUMO DA UNIFICACAO")
    print("=" * 50)
    print(f"Total de arquivos processados: {total_files}")
    print(f"Arquivos movidos com sucesso: {moved_files}")
    print(f"Pasta destino criada: {target_folder}")
    
    if moved_files == total_files:
        print("\nSUCESSO: Todos os arquivos foram unificados!")
        
        # Verificar se as pastas antigas estão vazias para deletá-las
        print("\nVerificando pastas antigas...")
        for source_folder in source_folders:
            remaining_files = list_folder_files(bucket, source_folder)
            if not remaining_files:
                print(f"  {source_folder}: vazia (pode ser removida)")
            else:
                print(f"  {source_folder}: ainda contém {len(remaining_files)} arquivo(s)")
    else:
        print(f"\nAVISO: {total_files - moved_files} arquivo(s) não foram movidos")
    
    print(f"\nNova estrutura:")
    print(f"  {target_folder}/ - Todos os arquivos unificados")

def main():
    try:
        # Confirmar ação
        print("ATENCAO: Esta operacao ira:")
        print("1. Mover todos os arquivos de 'Ellie_morre' para 'Ellie_moore'")
        print("2. Mover todos os arquivos de 'Elllie_morre' para 'Ellie_moore'")
        print("3. As pastas originais ficarao vazias")
        print()
        
        confirm = input("Deseja continuar? (s/N): ").lower().strip()
        
        if confirm in ['s', 'sim', 'y', 'yes']:
            unify_folders()
        else:
            print("Operacao cancelada.")
    
    except KeyboardInterrupt:
        print("\nOperacao interrompida pelo usuario.")
    except Exception as e:
        print(f"Erro inesperado: {e}")

if __name__ == "__main__":
    main()
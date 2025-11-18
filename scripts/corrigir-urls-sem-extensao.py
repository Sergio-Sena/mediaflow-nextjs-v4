#!/usr/bin/env python3
"""
Corrigir URLs sem extensao copiando arquivos .html
"""

import boto3
import subprocess

def main():
    print("Corrigindo URLs sem extensao (.html)")
    print("=" * 50)
    
    bucket_name = 'mediaflow-frontend-969430605054'
    
    # Paginas que precisam de URL sem extensao
    pages = [
        'pricing', 'login', 'register', 'dashboard', 'admin', 
        'docs', 'termos', 'privacidade', 'sla', 'users', '2fa'
    ]
    
    copied = 0
    errors = 0
    
    for page in pages:
        try:
            print(f"Copiando {page}.html -> {page}")
            
            result = subprocess.run([
                'aws', 's3', 'cp', 
                f's3://{bucket_name}/{page}.html',
                f's3://{bucket_name}/{page}',
                '--content-type', 'text/html',
                '--cache-control', 'public, max-age=0, must-revalidate'
            ], capture_output=True, text=True)
            
            if result.returncode == 0:
                print(f"  OK")
                copied += 1
            else:
                print(f"  Erro: {result.stderr}")
                errors += 1
                
        except Exception as e:
            print(f"  Erro: {e}")
            errors += 1
    
    print(f"\nResultado: {copied} copiados, {errors} erros")
    
    # Invalidar cache
    if copied > 0:
        print("Invalidando cache CloudFront...")
        paths = [f"/{page}" for page in pages]
        
        try:
            result = subprocess.run([
                'aws', 'cloudfront', 'create-invalidation',
                '--distribution-id', 'E2HZKZ9ZJK18IU',
                '--paths'] + paths,
                capture_output=True, text=True
            )
            
            if result.returncode == 0:
                print("Cache invalidado com sucesso")
            else:
                print(f"Erro ao invalidar cache: {result.stderr}")
                
        except Exception as e:
            print(f"Erro ao invalidar cache: {e}")

if __name__ == "__main__":
    main()
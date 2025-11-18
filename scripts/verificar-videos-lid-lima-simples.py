#!/usr/bin/env python3
"""
Verificar se os videos de Moana, Carros e Lilo & Stitch estao na pasta do usuario lid_lima
"""

import boto3
import json
from collections import defaultdict

def main():
    print("Verificando videos de Moana, Carros e Lilo & Stitch para lid_lima")
    print("=" * 70)
    
    # Configurar S3
    s3_client = boto3.client('s3')
    bucket_name = 'mediaflow-uploads-969430605054'
    
    # Termos de busca para os filmes
    search_terms = {
        'moana': ['moana'],
        'carros': ['carros', 'cars'],
        'lilo_stitch': ['lilo', 'stitch']
    }
    
    # Buscar arquivos do lid_lima
    print("Buscando arquivos na pasta users/lid_lima/...")
    
    try:
        # Listar objetos na pasta do lid_lima
        paginator = s3_client.get_paginator('list_objects_v2')
        pages = paginator.paginate(
            Bucket=bucket_name,
            Prefix='users/lid_lima/'
        )
        
        lid_lima_files = []
        for page in pages:
            if 'Contents' in page:
                for obj in page['Contents']:
                    lid_lima_files.append(obj['Key'])
        
        print(f"Encontrados {len(lid_lima_files)} arquivos na pasta lid_lima")
        
        # Organizar por filme
        movies_found = defaultdict(list)
        
        for file_key in lid_lima_files:
            filename = file_key.lower()
            
            # Verificar cada filme
            for movie, terms in search_terms.items():
                for term in terms:
                    if term in filename:
                        movies_found[movie].append(file_key)
                        break
        
        # Relatorio por filme
        print("\nRELATORIO POR FILME:")
        print("-" * 50)
        
        for movie, files in movies_found.items():
            movie_name = {
                'moana': 'Moana',
                'carros': 'Carros',
                'lilo_stitch': 'Lilo & Stitch'
            }[movie]
            
            print(f"\n{movie_name}: {len(files)} arquivo(s)")
            for file_key in sorted(files):
                # Obter informacoes do arquivo
                try:
                    response = s3_client.head_object(Bucket=bucket_name, Key=file_key)
                    size_mb = response['ContentLength'] / (1024 * 1024)
                    modified = response['LastModified'].strftime('%Y-%m-%d %H:%M')
                    
                    filename = file_key.split('/')[-1]
                    print(f"  {filename}")
                    print(f"    Tamanho: {size_mb:.1f} MB | Data: {modified}")
                    print(f"    Caminho: {file_key}")
                except Exception as e:
                    print(f"  Erro ao obter info: {file_key}")
        
        # Verificar se ha arquivos nao categorizados (possiveis filmes perdidos)
        all_categorized = set()
        for files in movies_found.values():
            all_categorized.update(files)
        
        uncategorized = [f for f in lid_lima_files if f not in all_categorized and f.endswith(('.mp4', '.avi', '.mkv', '.mov', '.ts'))]
        
        if uncategorized:
            print(f"\nARQUIVOS NAO CATEGORIZADOS: {len(uncategorized)}")
            print("-" * 50)
            for file_key in sorted(uncategorized):
                filename = file_key.split('/')[-1]
                print(f"  {filename}")
                print(f"    Caminho: {file_key}")
        
        # Resumo final
        total_movie_files = sum(len(files) for files in movies_found.values())
        print(f"\nRESUMO FINAL:")
        print("-" * 30)
        print(f"Total de filmes encontrados: {total_movie_files}")
        print(f"Total de arquivos lid_lima: {len(lid_lima_files)}")
        print(f"Arquivos nao categorizados: {len(uncategorized)}")
        
        # Verificar se existem nas outras pastas (para comparacao)
        print(f"\nVERIFICANDO OUTRAS PASTAS...")
        print("-" * 40)
        
        other_locations = defaultdict(list)
        
        # Buscar em toda a estrutura S3
        paginator = s3_client.get_paginator('list_objects_v2')
        pages = paginator.paginate(Bucket=bucket_name)
        
        for page in pages:
            if 'Contents' in page:
                for obj in page['Contents']:
                    key = obj['Key']
                    if not key.startswith('users/lid_lima/'):  # Excluir lid_lima
                        filename = key.lower()
                        
                        for movie, terms in search_terms.items():
                            for term in terms:
                                if term in filename:
                                    other_locations[movie].append(key)
                                    break
        
        for movie, files in other_locations.items():
            if files:
                movie_name = {
                    'moana': 'Moana',
                    'carros': 'Carros', 
                    'lilo_stitch': 'Lilo & Stitch'
                }[movie]
                
                print(f"\n{movie_name} encontrado em outras pastas: {len(files)}")
                for file_key in sorted(files)[:5]:  # Mostrar apenas os primeiros 5
                    folder = '/'.join(file_key.split('/')[:-1])
                    filename = file_key.split('/')[-1]
                    print(f"  Pasta: {folder}/")
                    print(f"  Arquivo: {filename}")
                
                if len(files) > 5:
                    print(f"  ... e mais {len(files) - 5} arquivo(s)")
        
    except Exception as e:
        print(f"Erro ao acessar S3: {str(e)}")
        return
    
    print(f"\nVerificacao concluida!")

if __name__ == "__main__":
    main()
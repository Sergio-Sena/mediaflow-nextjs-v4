#!/usr/bin/env python3
"""
Deleta CloudFronts inativos do Mídiaflow
"""

import boto3
import time

client = boto3.client('cloudfront')

DISTRIBUTIONS_TO_DELETE = [
    'E3ODIUY4LXU8TH',  # Antigo Mídiaflow
    'E12GJ6BBJXZML5'   # Antigo Mídiaflow
]

def disable_distribution(dist_id):
    print(f"\n1. Desabilitando {dist_id}...")
    
    # Get config
    response = client.get_distribution_config(Id=dist_id)
    config = response['DistributionConfig']
    etag = response['ETag']
    
    if not config['Enabled']:
        print(f"   Já está desabilitado")
        return etag
    
    # Disable
    config['Enabled'] = False
    
    response = client.update_distribution(
        Id=dist_id,
        DistributionConfig=config,
        IfMatch=etag
    )
    
    print(f"   Desabilitado! Aguardando deploy...")
    return response['ETag']

def wait_for_deployed(dist_id):
    print(f"2. Aguardando status 'Deployed' para {dist_id}...")
    
    while True:
        response = client.get_distribution(Id=dist_id)
        status = response['Distribution']['Status']
        
        print(f"   Status: {status}")
        
        if status == 'Deployed':
            print(f"   Pronto para deletar!")
            return response['ETag']
        
        time.sleep(30)

def delete_distribution(dist_id, etag):
    print(f"3. Deletando {dist_id}...")
    
    try:
        client.delete_distribution(
            Id=dist_id,
            IfMatch=etag
        )
        print(f"   Deletado com sucesso!")
        return True
    except Exception as e:
        print(f"   Erro: {e}")
        return False

def main():
    print("=" * 60)
    print("Deletando CloudFronts inativos do Mídiaflow")
    print("=" * 60)
    
    for dist_id in DISTRIBUTIONS_TO_DELETE:
        print(f"\n{'='*60}")
        print(f"Processando: {dist_id}")
        print(f"{'='*60}")
        
        try:
            # Step 1: Disable
            etag = disable_distribution(dist_id)
            
            # Step 2: Wait for deployed
            etag = wait_for_deployed(dist_id)
            
            # Step 3: Delete
            success = delete_distribution(dist_id, etag)
            
            if success:
                print(f"\n✅ {dist_id} deletado com sucesso!")
            else:
                print(f"\n❌ Falha ao deletar {dist_id}")
                
        except Exception as e:
            print(f"\n❌ Erro ao processar {dist_id}: {e}")
    
    print("\n" + "="*60)
    print("Processo concluído!")
    print("="*60)

if __name__ == '__main__':
    main()

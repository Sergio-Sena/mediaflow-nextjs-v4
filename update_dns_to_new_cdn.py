#!/usr/bin/env python3
import boto3

def update_dns():
    route53 = boto3.client('route53')
    
    # Configurações
    hosted_zone_id = 'Z07937031ROGP6XAEMPWJ'  # sstechnologies-cloud.com
    domain_name = 'mediaflow.sstechnologies-cloud.com'
    new_cdn_domain = 'd14rytve54170x.cloudfront.net'
    
    print("ATUALIZANDO DNS PARA NOVO CDN")
    print("=" * 40)
    print(f"Dominio: {domain_name}")
    print(f"Novo CDN: {new_cdn_domain}")
    
    try:
        # Atualizar registro CNAME
        response = route53.change_resource_record_sets(
            HostedZoneId=hosted_zone_id,
            ChangeBatch={
                'Changes': [{
                    'Action': 'UPSERT',
                    'ResourceRecordSet': {
                        'Name': domain_name,
                        'Type': 'CNAME',
                        'TTL': 300,
                        'ResourceRecords': [{'Value': new_cdn_domain}]
                    }
                }]
            }
        )
        
        change_id = response['ChangeInfo']['Id']
        status = response['ChangeInfo']['Status']
        
        print(f"DNS atualizado!")
        print(f"Change ID: {change_id}")
        print(f"Status: {status}")
        print(f"\nPropagacao DNS: 2-5 minutos")
        print(f"URL: https://{domain_name}")
        
    except Exception as e:
        print(f"Erro: {e}")

if __name__ == "__main__":
    update_dns()
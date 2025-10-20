#!/usr/bin/env python3
"""
Remove old mediaflow domain (keep midiaflow only)
"""
import boto3
import json

# AWS clients
cloudfront = boto3.client('cloudfront', region_name='us-east-1')
route53 = boto3.client('route53', region_name='us-east-1')

def list_cloudfront_distributions():
    """List all CloudFront distributions"""
    print("🔍 Listando CloudFront distributions...")
    response = cloudfront.list_distributions()
    
    if 'DistributionList' not in response or 'Items' not in response['DistributionList']:
        print("❌ Nenhuma distribution encontrada")
        return
    
    for dist in response['DistributionList']['Items']:
        dist_id = dist['Id']
        domain = dist['DomainName']
        aliases = dist.get('Aliases', {}).get('Items', [])
        status = dist['Status']
        
        print(f"\n📦 Distribution ID: {dist_id}")
        print(f"   Domain: {domain}")
        print(f"   Aliases: {', '.join(aliases) if aliases else 'None'}")
        print(f"   Status: {status}")
        
        # Check if it's the old mediaflow domain
        if any('mediaflow.sstechnologies-cloud.com' in alias for alias in aliases):
            print(f"   ⚠️  OLD DOMAIN FOUND!")
            print(f"   Para remover: aws cloudfront delete-distribution --id {dist_id}")

def list_route53_records():
    """List Route53 records"""
    print("\n🔍 Listando Route53 hosted zones...")
    response = route53.list_hosted_zones()
    
    for zone in response['HostedZones']:
        zone_id = zone['Id'].split('/')[-1]
        zone_name = zone['Name']
        
        if 'sstechnologies-cloud.com' in zone_name:
            print(f"\n📍 Zone: {zone_name} ({zone_id})")
            
            # List records
            records = route53.list_resource_record_sets(HostedZoneId=zone_id)
            
            for record in records['ResourceRecordSets']:
                name = record['Name']
                rtype = record['Type']
                
                if 'mediaflow' in name.lower():
                    print(f"   ⚠️  OLD RECORD: {name} ({rtype})")
                    print(f"      Para remover manualmente via console AWS")

if __name__ == '__main__':
    print("🗑️  Removendo domínio antigo mediaflow.sstechnologies-cloud.com\n")
    
    try:
        list_cloudfront_distributions()
        list_route53_records()
        
        print("\n" + "="*60)
        print("⚠️  ATENÇÃO: Remoção manual necessária")
        print("="*60)
        print("\n1. CloudFront: Desabilitar distribution primeiro, depois deletar")
        print("2. Route53: Remover registros DNS via console AWS")
        print("\n✅ Domínio midiaflow.sstechnologies-cloud.com permanece ativo")
        
    except Exception as e:
        print(f"❌ Erro: {e}")

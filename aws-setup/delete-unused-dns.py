import boto3
import json

route53 = boto3.client('route53')
zone_id = 'Z07937031ROGP6XAEMPWJ'

records_to_delete = [
    {'name': 'aws-cert.sstechnologies-cloud.com.', 'value': 'd3sti4gw25532i.cloudfront.net'},
    {'name': 'simulados.sstechnologies-cloud.com.', 'value': 'd3sti4gw25532i.cloudfront.net'},
    {'name': 'v2-aws-services.sstechnologies-cloud.com.', 'value': 'd10mjoe1zes9j1.cloudfront.net'},
    {'name': 'v2-hub.sstechnologies-cloud.com.', 'value': 'd10mjoe1zes9j1.cloudfront.net'},
    {'name': 'v2-portfolio.sstechnologies-cloud.com.', 'value': 'd10mjoe1zes9j1.cloudfront.net'}
]

changes = []
for record in records_to_delete:
    # Buscar tipo do record (A ou CNAME)
    response = route53.list_resource_record_sets(
        HostedZoneId=zone_id,
        StartRecordName=record['name'],
        MaxItems='1'
    )
    
    if response['ResourceRecordSets']:
        existing = response['ResourceRecordSets'][0]
        if existing['Name'] == record['name']:
            record_type = existing['Type']
            
            if record_type == 'A':
                # A record com alias
                changes.append({
                    'Action': 'DELETE',
                    'ResourceRecordSet': {
                        'Name': record['name'],
                        'Type': 'A',
                        'AliasTarget': {
                            'HostedZoneId': 'Z2FDTNDATAQYW2',  # CloudFront hosted zone
                            'DNSName': record['value'],
                            'EvaluateTargetHealth': False
                        }
                    }
                })
            else:
                # CNAME record
                changes.append({
                    'Action': 'DELETE',
                    'ResourceRecordSet': {
                        'Name': record['name'],
                        'Type': 'CNAME',
                        'TTL': 300,
                        'ResourceRecords': [{'Value': record['value']}]
                    }
                })
            
            print(f"[OK] Preparado para deletar: {record['name']}")

if changes:
    route53.change_resource_record_sets(
        HostedZoneId=zone_id,
        ChangeBatch={'Changes': changes}
    )
    print(f"\n[SUCESSO] {len(changes)} records deletados")
else:
    print("[AVISO] Nenhum record encontrado para deletar")

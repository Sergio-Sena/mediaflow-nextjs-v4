import boto3
import json

route53 = boto3.client('route53')
hosted_zone_id = 'Z07937031ROGP6XAEMPWJ'

# Atualizar registro CNAME
change_batch = {
    'Changes': [{
        'Action': 'UPSERT',
        'ResourceRecordSet': {
            'Name': 'midiaflow.sstechnologies-cloud.com',
            'Type': 'CNAME',
            'TTL': 300,
            'ResourceRecords': [{'Value': 'dau2z7fot0cqr.cloudfront.net'}]
        }
    }]
}

response = route53.change_resource_record_sets(
    HostedZoneId=hosted_zone_id,
    ChangeBatch=change_batch
)

print(json.dumps({
    'Status': response['ChangeInfo']['Status'],
    'Id': response['ChangeInfo']['Id'],
    'SubmittedAt': str(response['ChangeInfo']['SubmittedAt'])
}, indent=2))

print("\nDNS atualizado! Aguarde 5-10 minutos para propagacao.")

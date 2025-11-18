import boto3

cloudfront = boto3.client('cloudfront', region_name='us-east-1')

response = cloudfront.list_distributions()

if 'DistributionList' in response and 'Items' in response['DistributionList']:
    for dist in response['DistributionList']['Items']:
        print(f"ID: {dist['Id']}")
        print(f"Domain: {dist['DomainName']}")
        print(f"Aliases: {dist.get('Aliases', {}).get('Items', [])}")
        print("---")
else:
    print("Nenhuma distribuicao encontrada")

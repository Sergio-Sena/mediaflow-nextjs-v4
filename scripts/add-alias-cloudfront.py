import boto3
import json

client = boto3.client('cloudfront')

# Obter config atual
response = client.get_distribution_config(Id='E1A2CZM0WKF6LX')
config = response['DistributionConfig']
etag = response['ETag']

# Adicionar alias
config['Aliases'] = {
    'Quantity': 1,
    'Items': ['midiaflow.sstechnologies-cloud.com']
}

# Adicionar certificado SSL
config['ViewerCertificate'] = {
    'ACMCertificateArn': 'arn:aws:acm:us-east-1:969430605054:certificate/5da53d3b-4f07-4aeb-9654-0b1bfea7bc0a',
    'SSLSupportMethod': 'sni-only',
    'MinimumProtocolVersion': 'TLSv1.2_2021',
    'Certificate': 'arn:aws:acm:us-east-1:969430605054:certificate/5da53d3b-4f07-4aeb-9654-0b1bfea7bc0a',
    'CertificateSource': 'acm'
}

# Atualizar distribuição
update_response = client.update_distribution(
    Id='E1A2CZM0WKF6LX',
    DistributionConfig=config,
    IfMatch=etag
)

print(json.dumps({
    'Status': update_response['Distribution']['Status'],
    'DomainName': update_response['Distribution']['DomainName'],
    'Aliases': update_response['Distribution']['DistributionConfig']['Aliases']
}, indent=2))

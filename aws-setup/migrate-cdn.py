import boto3

cf = boto3.client('cloudfront')
old_dist_id = 'E2HZKZ9ZJK18IU'
new_dist_id = 'E1O4R8P5BGZTMW'
domain = 'midiaflow.sstechnologies-cloud.com'
cert_arn = 'arn:aws:acm:us-east-1:969430605054:certificate/5da53d3b-4f07-4aeb-9654-0b1bfea7bc0a'

print("[1/4] Removendo alias do CDN antigo...")
old_config = cf.get_distribution_config(Id=old_dist_id)
old_config['DistributionConfig']['Aliases'] = {'Quantity': 0, 'Items': []}
cf.update_distribution(
    Id=old_dist_id,
    DistributionConfig=old_config['DistributionConfig'],
    IfMatch=old_config['ETag']
)
print("[OK] Alias removido do antigo")

print("[2/4] Aguardando propagacao (90s)...")
import time
time.sleep(90)

print("[3/4] Adicionando alias no CDN novo...")
new_config = cf.get_distribution_config(Id=new_dist_id)
new_config['DistributionConfig']['Aliases'] = {'Quantity': 1, 'Items': [domain]}
new_config['DistributionConfig']['ViewerCertificate'] = {
    'ACMCertificateArn': cert_arn,
    'SSLSupportMethod': 'sni-only',
    'MinimumProtocolVersion': 'TLSv1.2_2021'
}
cf.update_distribution(
    Id=new_dist_id,
    DistributionConfig=new_config['DistributionConfig'],
    IfMatch=new_config['ETag']
)
print("[OK] Alias adicionado ao novo")

print("[4/4] Desabilitando CDN antigo...")
old_config2 = cf.get_distribution_config(Id=old_dist_id)
old_config2['DistributionConfig']['Enabled'] = False
cf.update_distribution(
    Id=old_dist_id,
    DistributionConfig=old_config2['DistributionConfig'],
    IfMatch=old_config2['ETag']
)
print("[OK] CDN antigo desabilitado")

print(f"\n[SUCESSO] Migracao completa!")
print(f"Novo CDN: {new_dist_id}")
print(f"Aguarde 5-10 minutos para propagacao DNS")
print(f"Depois delete o antigo: aws cloudfront delete-distribution --id {old_dist_id}")

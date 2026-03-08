import boto3
import json

client = boto3.client('cloudfront')

# Desabilitar E1O4R8P5BGZTMW
print("Desabilitando E1O4R8P5BGZTMW...")
try:
    response1 = client.get_distribution_config(Id='E1O4R8P5BGZTMW')
    config1 = response1['DistributionConfig']
    etag1 = response1['ETag']
    
    config1['Enabled'] = False
    config1['Aliases'] = {'Quantity': 0}
    
    client.update_distribution(
        Id='E1O4R8P5BGZTMW',
        DistributionConfig=config1,
        IfMatch=etag1
    )
    print("OK E1O4R8P5BGZTMW desabilitada")
except Exception as e:
    print(f"ERRO E1O4R8P5BGZTMW: {e}")

# Desabilitar EFJXJ07BDK7UF
print("\nDesabilitando EFJXJ07BDK7UF...")
try:
    response2 = client.get_distribution_config(Id='EFJXJ07BDK7UF')
    config2 = response2['DistributionConfig']
    etag2 = response2['ETag']
    
    config2['Enabled'] = False
    config2['Aliases'] = {'Quantity': 0}
    
    client.update_distribution(
        Id='EFJXJ07BDK7UF',
        DistributionConfig=config2,
        IfMatch=etag2
    )
    print("OK EFJXJ07BDK7UF desabilitada")
except Exception as e:
    print(f"ERRO EFJXJ07BDK7UF: {e}")

print("\nAguarde 5-10 minutos para as distribuicoes serem desabilitadas.")

import boto3
import json

cf = boto3.client('cloudfront', region_name='us-east-1')

config = {
    "CallerReference": "midiaflow-green-2026",
    "Comment": "MidiaFlow Green Environment",
    "Enabled": True,
    "Origins": {
        "Quantity": 1,
        "Items": [{
            "Id": "S3-midiaflow-green",
            "DomainName": "midiaflow-green-969430605054.s3-website-us-east-1.amazonaws.com",
            "CustomOriginConfig": {
                "HTTPPort": 80,
                "HTTPSPort": 443,
                "OriginProtocolPolicy": "http-only"
            }
        }]
    },
    "DefaultCacheBehavior": {
        "TargetOriginId": "S3-midiaflow-green",
        "ViewerProtocolPolicy": "redirect-to-https",
        "AllowedMethods": {"Quantity": 2, "Items": ["GET", "HEAD"]},
        "CachedMethods": {"Quantity": 2, "Items": ["GET", "HEAD"]},
        "ForwardedValues": {
            "QueryString": False,
            "Cookies": {"Forward": "none"}
        },
        "MinTTL": 0,
        "TrustedSigners": {"Enabled": False, "Quantity": 0}
    }
}

try:
    response = cf.create_distribution(DistributionConfig=config)
    dist_id = response['Distribution']['Id']
    domain = response['Distribution']['DomainName']
    
    print(f"✅ CloudFront Green criado!")
    print(f"Distribution ID: {dist_id}")
    print(f"URL: https://{domain}")
    print(f"\n⏳ Aguarde ~15min para propagar...")
    
except Exception as e:
    print(f"❌ Erro: {e}")

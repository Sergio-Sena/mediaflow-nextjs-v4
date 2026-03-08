import boto3
import json

cloudfront = boto3.client('cloudfront')

config = {
    "CallerReference": "mediaflow-website-endpoint-2026",
    "Comment": "MidiaFlow - S3 Website Endpoint (CORRETO)",
    "Enabled": True,
    "Origins": {
        "Quantity": 1,
        "Items": [{
            "Id": "S3-Website-mediaflow",
            "DomainName": "mediaflow-frontend-969430605054.s3-website-us-east-1.amazonaws.com",
            "CustomOriginConfig": {
                "HTTPPort": 80,
                "HTTPSPort": 443,
                "OriginProtocolPolicy": "http-only"
            }
        }]
    },
    "DefaultRootObject": "index.html",
    "DefaultCacheBehavior": {
        "TargetOriginId": "S3-Website-mediaflow",
        "ViewerProtocolPolicy": "redirect-to-https",
        "AllowedMethods": {
            "Quantity": 2,
            "Items": ["GET", "HEAD"],
            "CachedMethods": {
                "Quantity": 2,
                "Items": ["GET", "HEAD"]
            }
        },
        "Compress": True,
        "ForwardedValues": {
            "QueryString": False,
            "Cookies": {"Forward": "none"}
        },
        "MinTTL": 0,
        "DefaultTTL": 86400,
        "MaxTTL": 31536000,
        "TrustedSigners": {
            "Enabled": False,
            "Quantity": 0
        }
    }
}

response = cloudfront.create_distribution(DistributionConfig=config)
print(json.dumps(response, indent=2, default=str))

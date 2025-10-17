import boto3
import json

s3 = boto3.client('s3', region_name='us-east-1')
bucket = 'mediaflow-uploads-969430605054'

# Configurar CORS
cors_config = {
    'CORSRules': [
        {
            'AllowedHeaders': ['*'],
            'AllowedMethods': ['GET', 'PUT', 'POST', 'DELETE', 'HEAD'],
            'AllowedOrigins': ['*'],
            'ExposeHeaders': ['ETag'],
            'MaxAgeSeconds': 3000
        }
    ]
}

print(f"Setting CORS for {bucket}...")
s3.put_bucket_cors(Bucket=bucket, CORSConfiguration=cors_config)
print("CORS configured!")

# Tornar avatars públicos
print("\nMaking avatars public...")
s3.put_bucket_policy(
    Bucket=bucket,
    Policy=json.dumps({
        'Version': '2012-10-17',
        'Statement': [{
            'Sid': 'PublicReadAvatars',
            'Effect': 'Allow',
            'Principal': '*',
            'Action': 's3:GetObject',
            'Resource': f'arn:aws:s3:::{bucket}/avatars/*'
        }]
    })
)
print("Avatars are now public!")

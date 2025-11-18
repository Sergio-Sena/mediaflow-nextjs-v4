import boto3
import time

cloudfront = boto3.client('cloudfront', region_name='us-east-1')
DISTRIBUTION_ID = 'E2HZKZ9ZJK18IU'

response = cloudfront.create_invalidation(
    DistributionId=DISTRIBUTION_ID,
    InvalidationBatch={
        'Paths': {
            'Quantity': 1,
            'Items': ['/*']
        },
        'CallerReference': str(time.time())
    }
)

print(f"[OK] Invalidacao criada: {response['Invalidation']['Id']}")
print("[INFO] Aguarde 2-5 minutos para o cache ser limpo")

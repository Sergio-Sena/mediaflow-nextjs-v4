import boto3
import time

cf = boto3.client('cloudfront')
print('Invalidating CloudFront...')
cf.create_invalidation(
    DistributionId='E2HZKZ9ZJK18IU',
    InvalidationBatch={
        'Paths': {
            'Quantity': 1,
            'Items': ['/*']
        },
        'CallerReference': str(time.time())
    }
)
print('Cache invalidated!')
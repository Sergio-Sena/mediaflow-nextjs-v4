import boto3
import json

lambda_client = boto3.client('lambda')

# Atualizar CORS para aceitar qualquer CloudFront
response = lambda_client.update_function_configuration(
    FunctionName='mediaflow-upload-handler',
    Environment={
        'Variables': {
            'ALLOWED_ORIGINS': 'https://dau2z7fot0cqr.cloudfront.net,https://d2komwe8ylb0dt.cloudfront.net,https://dej0zoy1rccqg.cloudfront.net,https://midiaflow.sstechnologies-cloud.com,http://localhost:3000'
        }
    }
)

print(json.dumps(response, indent=2, default=str))

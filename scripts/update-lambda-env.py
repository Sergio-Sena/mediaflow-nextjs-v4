import boto3

lambda_client = boto3.client('lambda', region_name='us-east-1')

lambda_client.update_function_configuration(
    FunctionName='mediaflow-view-handler',
    Environment={
        'Variables': {
            'UPLOADS_BUCKET': 'mediaflow-uploads-969430605054',
            'PROCESSED_BUCKET': 'mediaflow-processed-969430605054',
            'JWT_SECRET': 'mediaflow-secret-key-2024-production'
        }
    }
)

print("[OK] Variaveis de ambiente atualizadas")
print("[INFO] Aguarde 10 segundos para Lambda atualizar...")

import boto3
import json

s3 = boto3.client('s3', region_name='us-east-1')
bucket = 'mediaflow-uploads-969430605054'

lifecycle_policy = {
    'Rules': [
        {
            'ID': 'Move-to-Intelligent-Tiering-after-60-days',
            'Status': 'Enabled',
            'Filter': {
                'Prefix': ''  # Aplica a TODOS os arquivos
            },
            'Transitions': [
                {
                    'Days': 60,
                    'StorageClass': 'INTELLIGENT_TIERING'
                }
            ]
        }
    ]
}

print('Criando Lifecycle Policy...\n')
print(json.dumps(lifecycle_policy, indent=2))
print('\n' + '='*50)

try:
    s3.put_bucket_lifecycle_configuration(
        Bucket=bucket,
        LifecycleConfiguration=lifecycle_policy
    )
    
    print('\nLifecycle Policy criada com sucesso!')
    print('\nRegra ativa:')
    print('   - Apos 60 dias -> INTELLIGENT_TIERING')
    print('   - Aplica a: TODOS os arquivos (existentes + novos)')
    print('   - Performance: Zero impacto')
    print('   - Economia: ~30-40% em arquivos antigos')
    
except Exception as e:
    print(f'\nErro: {e}')

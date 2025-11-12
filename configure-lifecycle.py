import boto3

s3 = boto3.client('s3', region_name='us-east-1')
bucket = 'mediaflow-uploads-969430605054'

lifecycle_config = {
    'Rules': [
        {
            'ID': 'trial-to-glacier-7d',
            'Status': 'Enabled',
            'Filter': {'Prefix': 'users/'},
            'Transitions': [
                {
                    'Days': 7,
                    'StorageClass': 'GLACIER_IR'
                }
            ],
            'Expiration': {'Days': 120}
        },
        {
            'ID': 'inactive-to-intelligent-30d',
            'Status': 'Enabled',
            'Filter': {'Prefix': 'users/'},
            'Transitions': [
                {
                    'Days': 30,
                    'StorageClass': 'INTELLIGENT_TIERING'
                }
            ]
        },
        {
            'ID': 'inactive-to-glacier-90d',
            'Status': 'Enabled',
            'Filter': {'Prefix': 'users/'},
            'Transitions': [
                {
                    'Days': 90,
                    'StorageClass': 'GLACIER_IR'
                }
            ]
        }
    ]
}

print(f"Configurando lifecycle para bucket: {bucket}")
s3.put_bucket_lifecycle_configuration(
    Bucket=bucket,
    LifecycleConfiguration=lifecycle_config
)

print("[OK] Lifecycle configurado com sucesso!")
print("\nRegras aplicadas:")
print("  - Trial -> Glacier após 7 dias")
print("  - Inativo -> Intelligent-Tiering após 30 dias")
print("  - Inativo -> Glacier após 90 dias")
print("  - Exclusão automática após 120 dias")

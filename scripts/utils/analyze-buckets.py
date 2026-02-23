import boto3
import json

s3 = boto3.client('s3')

buckets = [
    'mediaflow-frontend-969430605054',
    'mediaflow-processed-969430605054',
    'mediaflow-uploads-969430605054',
    'midiaflow-backups-969430605054'
]

print("=" * 80)
print("ANÁLISE DE BUCKETS MEDIAFLOW")
print("=" * 80)

for bucket_name in buckets:
    print(f"\n{'=' * 80}")
    print(f"BUCKET: {bucket_name}")
    print(f"{'=' * 80}")
    
    try:
        # Região
        location = s3.get_bucket_location(Bucket=bucket_name)
        region = location['LocationConstraint'] or 'us-east-1'
        print(f"Região: {region}")
        
        # Tags
        try:
            tags = s3.get_bucket_tagging(Bucket=bucket_name)
            print(f"Tags: {tags.get('TagSet', [])}")
        except:
            print("Tags: Nenhuma")
        
        # Contagem de objetos
        response = s3.list_objects_v2(Bucket=bucket_name, MaxKeys=1000)
        total_objects = response.get('KeyCount', 0)
        print(f"Total de objetos (primeiros 1000): {total_objects}")
        
        # Tamanho total
        total_size = sum(obj['Size'] for obj in response.get('Contents', []))
        total_size_mb = total_size / (1024 * 1024)
        print(f"Tamanho total: {total_size_mb:.2f} MB")
        
        # Exemplos de arquivos
        if response.get('Contents'):
            print("\nExemplos de arquivos (primeiros 5):")
            for obj in response['Contents'][:5]:
                size_mb = obj['Size'] / (1024 * 1024)
                key = obj['Key'][:70] + '...' if len(obj['Key']) > 70 else obj['Key']
                print(f"  - {key} ({size_mb:.2f} MB)")
        
        # Estrutura de pastas
        prefixes = set()
        for obj in response.get('Contents', []):
            parts = obj['Key'].split('/')
            if len(parts) > 1:
                prefixes.add(parts[0])
        
        if prefixes:
            print(f"\nPastas principais: {', '.join(sorted(prefixes))}")
        
    except Exception as e:
        print(f"ERRO: {e}")

print("\n" + "=" * 80)
print("ANÁLISE CONCLUÍDA")
print("=" * 80)

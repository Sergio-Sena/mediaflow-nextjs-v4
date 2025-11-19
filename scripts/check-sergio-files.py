import boto3
import json

def check_sergio_files():
    print("=" * 80)
    print("ARQUIVOS DO SERGIO SENA")
    print("=" * 80)
    
    s3 = boto3.client('s3', region_name='us-east-1')
    
    buckets = [
        'mediaflow-uploads-969430605054',
        'mediaflow-processed-969430605054'
    ]
    
    for bucket in buckets:
        print(f"\n[BUCKET] {bucket}")
        print("-" * 50)
        
        try:
            # List files in sergio_sena folder
            response = s3.list_objects_v2(
                Bucket=bucket,
                Prefix='users/sergio_sena/',
                MaxKeys=10
            )
            
            if 'Contents' in response:
                print(f"Encontrados {len(response['Contents'])} arquivos:")
                for obj in response['Contents']:
                    print(f"  - {obj['Key']} ({obj['Size']} bytes)")
            else:
                print("Nenhum arquivo encontrado")
                
        except Exception as e:
            print(f"Erro ao licorporativo arquivos: {str(e)}")

if __name__ == "__main__":
    check_sergio_files()
import boto3

def check_lid_lima():
    print("=" * 60)
    print("ARQUIVOS DO LID LIMA")
    print("=" * 60)
    
    s3 = boto3.client('s3', region_name='us-east-1')
    
    buckets = [
        'mediaflow-uploads-969430605054',
        'mediaflow-processed-969430605054'
    ]
    
    for bucket in buckets:
        print(f"\n[BUCKET] {bucket}")
        print("-" * 40)
        
        try:
            # List files in lid_lima folder
            response = s3.list_objects_v2(
                Bucket=bucket,
                Prefix='users/lid_lima/',
                MaxKeys=20
            )
            
            if 'Contents' in response:
                print(f"Encontrados {len(response['Contents'])} arquivos:")
                for obj in response['Contents']:
                    size_mb = obj['Size'] / (1024 * 1024)
                    print(f"  - {obj['Key']} ({size_mb:.1f} MB)")
            else:
                print("Nenhum arquivo encontrado")
                
        except Exception as e:
            print(f"Erro: {str(e)}")

if __name__ == "__main__":
    check_lid_lima()
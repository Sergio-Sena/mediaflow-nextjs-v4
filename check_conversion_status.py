#!/usr/bin/env python3
import boto3
import requests

def check_conversion_status():
    print("STATUS DA CONVERSAO")
    print("=" * 30)
    
    # 1. Verificar jobs MediaConvert
    try:
        mediaconvert = boto3.client('mediaconvert')
        endpoints = mediaconvert.describe_endpoints()
        endpoint_url = endpoints['Endpoints'][0]['Url']
        mc_client = boto3.client('mediaconvert', endpoint_url=endpoint_url)
        
        response = mc_client.list_jobs(MaxResults=5, Order='DESCENDING')
        
        print("JOBS RECENTES:")
        for job in response.get('Jobs', []):
            print(f"  {job['Id']}: {job['Status']} ({job.get('JobPercentComplete', 0)}%)")
            if 'UserMetadata' in job:
                original = job['UserMetadata'].get('OriginalFile', 'Unknown')
                print(f"    Arquivo: {original}")
    except Exception as e:
        print(f"Erro MediaConvert: {e}")
    
    # 2. Verificar arquivos no bucket
    print("\nARQUIVOS SHYBLANCHE:")
    try:
        s3 = boto3.client('s3')
        response = s3.list_objects_v2(
            Bucket='mediaflow-uploads-969430605054',
            Prefix='ShyBlanche/'
        )
        
        if 'Contents' in response:
            for obj in response['Contents']:
                if not obj['Key'].endswith('/'):
                    size_mb = obj['Size'] / (1024*1024)
                    print(f"  {obj['Key']} ({size_mb:.1f}MB)")
    except Exception as e:
        print(f"Erro S3: {e}")

if __name__ == "__main__":
    check_conversion_status()
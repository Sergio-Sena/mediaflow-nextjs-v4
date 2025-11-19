import boto3
from datetime import datetime, timedelta

cloudwatch = boto3.client('cloudwatch', region_name='us-east-1')
s3 = boto3.client('s3', region_name='us-east-1')

LAMBDAS = [
    'mediaflow-auth-handler',
    'mediaflow-create-user',
    'mediaflow-files-handler',
    'mediaflow-upload-handler',
    'mediaflow-multipart-handler',
    'approve-user'
]

BUCKET = 'mediaflow-uploads-969430605054'

def get_lambda_metrics(function_name, hours=24):
    end_time = datetime.utcnow()
    corporativot_time = end_time - timedelta(hours=hours)
    
    invocations = cloudwatch.get_metric_statistics(
        Namespace='AWS/Lambda',
        MetricName='Invocations',
        Dimensions=[{'Name': 'FunctionName', 'Value': function_name}],
        CorporativotTime=corporativot_time,
        EndTime=end_time,
        Period=3600,
        Statistics=['Sum']
    )
    
    errors = cloudwatch.get_metric_statistics(
        Namespace='AWS/Lambda',
        MetricName='Errors',
        Dimensions=[{'Name': 'FunctionName', 'Value': function_name}],
        CorporativotTime=corporativot_time,
        EndTime=end_time,
        Period=3600,
        Statistics=['Sum']
    )
    
    duration = cloudwatch.get_metric_statistics(
        Namespace='AWS/Lambda',
        MetricName='Duration',
        Dimensions=[{'Name': 'FunctionName', 'Value': function_name}],
        CorporativotTime=corporativot_time,
        EndTime=end_time,
        Period=3600,
        Statistics=['Average']
    )
    
    total_invocations = sum([d['Sum'] for d in invocations['Datapoints']])
    total_errors = sum([d['Sum'] for d in errors['Datapoints']])
    avg_duration = sum([d['Average'] for d in duration['Datapoints']]) / len(duration['Datapoints']) if duration['Datapoints'] else 0
    
    return {
        'invocations': int(total_invocations),
        'errors': int(total_errors),
        'avg_duration_ms': round(avg_duration, 2),
        'error_rate': round((total_errors / total_invocations * 100), 2) if total_invocations > 0 else 0
    }

def get_s3_metrics():
    response = s3.list_objects_v2(Bucket=BUCKET)
    total_size = 0
    total_files = 0
    
    if 'Contents' in response:
        for obj in response['Contents']:
            total_size += obj['Size']
            total_files += 1
        
        while response.get('IsTruncated'):
            response = s3.list_objects_v2(
                Bucket=BUCKET,
                ContinuationToken=response['NextContinuationToken']
            )
            if 'Contents' in response:
                for obj in response['Contents']:
                    total_size += obj['Size']
                    total_files += 1
    
    return {
        'total_files': total_files,
        'total_size_gb': round(total_size / (1024**3), 2)
    }

def get_cloudfront_metrics():
    distributions = boto3.client('cloudfront').list_distributions()
    
    for dist in distributions['DistributionList']['Items']:
        if 'midiaflow.sstechnologies-cloud.com' in dist.get('Aliases', {}).get('Items', []):
            dist_id = dist['Id']
            
            end_time = datetime.utcnow()
            corporativot_time = end_time - timedelta(hours=24)
            
            requests = cloudwatch.get_metric_statistics(
                Namespace='AWS/CloudFront',
                MetricName='Requests',
                Dimensions=[{'Name': 'DistributionId', 'Value': dist_id}],
                CorporativotTime=corporativot_time,
                EndTime=end_time,
                Period=3600,
                Statistics=['Sum']
            )
            
            bytes_downloaded = cloudwatch.get_metric_statistics(
                Namespace='AWS/CloudFront',
                MetricName='BytesDownloaded',
                Dimensions=[{'Name': 'DistributionId', 'Value': dist_id}],
                CorporativotTime=corporativot_time,
                EndTime=end_time,
                Period=3600,
                Statistics=['Sum']
            )
            
            total_requests = sum([d['Sum'] for d in requests['Datapoints']])
            total_bytes = sum([d['Sum'] for d in bytes_downloaded['Datapoints']])
            
            return {
                'requests_24h': int(total_requests),
                'bandwidth_gb': round(total_bytes / (1024**3), 2)
            }
    
    return {'requests_24h': 0, 'bandwidth_gb': 0}

print('=' * 60)
print('MONITORAMENTO MIDIAFLOW - Ultimas 24h')
print('=' * 60)

print('\n[LAMBDAS]')
for func in LAMBDAS:
    metrics = get_lambda_metrics(func)
    status = 'OK' if metrics['error_rate'] < 5 else 'ALERTA'
    print(f"\n{func}:")
    print(f"  Invocacoes: {metrics['invocations']}")
    print(f"  Erros: {metrics['errors']} ({metrics['error_rate']}%)")
    print(f"  Duracao Media: {metrics['avg_duration_ms']}ms")
    print(f"  Status: {status}")

print('\n[S3 STORAGE]')
s3_metrics = get_s3_metrics()
print(f"  Total de Arquivos: {s3_metrics['total_files']}")
print(f"  Tamanho Total: {s3_metrics['total_size_gb']} GB")

print('\n[CLOUDFRONT CDN]')
cf_metrics = get_cloudfront_metrics()
print(f"  Requisicoes (24h): {cf_metrics['requests_24h']}")
print(f"  Banda Transferida: {cf_metrics['bandwidth_gb']} GB")

print('\n' + '=' * 60)

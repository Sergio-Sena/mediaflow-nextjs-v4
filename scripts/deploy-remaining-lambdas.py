import boto3
import zipfile
import os
from pathlib import Path
import tempfile

lambda_client = boto3.client('lambda', region_name='us-east-1')
cloudwatch = boto3.client('cloudwatch', region_name='us-east-1')
logs_client = boto3.client('logs', region_name='us-east-1')

LAMBDAS = [
    {'name': 'folder-operations', 'function_name': 'folder-operations'},
    {'name': 'approve-user', 'function_name': 'approve-user'}
]

def create_zip(lambda_name):
    """Create deployment package with logger"""
    base_path = Path(f'aws-setup/lambda-functions/{lambda_name}')
    lib_path = Path('aws-setup/lambda-functions/lib')
    zip_path = os.path.join(tempfile.gettempdir(), f'{lambda_name}.zip')
    
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        # Add lambda function
        lambda_file = base_path / 'lambda_function.py'
        if lambda_file.exists():
            zipf.write(lambda_file, 'lambda_function.py')
        
        # Add logger lib
        logger_file = lib_path / 'logger.py'
        if logger_file.exists():
            zipf.write(logger_file, 'logger.py')
    
    return zip_path

def deploy_lambda(lambda_config):
    """Deploy Lambda with logging"""
    lambda_name = lambda_config['name']
    function_name = lambda_config['function_name']
    
    print(f"Deploying {lambda_name}...")
    
    zip_path = create_zip(lambda_name)
    
    with open(zip_path, 'rb') as f:
        zip_content = f.read()
    
    try:
        response = lambda_client.update_function_code(
            FunctionName=function_name,
            ZipFile=zip_content
        )
        print(f"OK - {lambda_name} deployed")
        return True
    except Exception as e:
        print(f"ERROR - {lambda_name} failed: {e}")
        return False

def create_alarm(lambda_config):
    """Create CloudWatch alarm for errors"""
    function_name = lambda_config['function_name']
    alarm_name = f'{function_name}-errors'
    
    try:
        cloudwatch.put_metric_alarm(
            AlarmName=alarm_name,
            ComparisonOperator='GreaterThanThreshold',
            EvaluationPeriods=1,
            MetricName='Errors',
            Namespace='AWS/Lambda',
            Period=300,
            Statistic='Sum',
            Threshold=5.0,
            ActionsEnabled=False,
            AlarmDescription=f'Alert when {function_name} has >5 errors in 5min',
            Dimensions=[
                {'Name': 'FunctionName', 'Value': function_name}
            ]
        )
        print(f"OK - Alarm created: {alarm_name}")
    except Exception as e:
        print(f"WARN - Alarm creation failed: {e}")

def set_log_retention(lambda_config):
    """Set CloudWatch Logs retention to 7 days"""
    function_name = lambda_config['function_name']
    log_group = f'/aws/lambda/{function_name}'
    
    try:
        logs_client.put_retention_policy(
            logGroupName=log_group,
            retentionInDays=7
        )
        print(f"OK - Log retention set: {log_group}")
    except Exception as e:
        print(f"WARN - Log retention failed: {e}")

if __name__ == '__main__':
    print("Deploying Remaining Lambdas\\n")
    
    success_count = 0
    for lambda_config in LAMBDAS:
        if deploy_lambda(lambda_config):
            success_count += 1
            create_alarm(lambda_config)
            set_log_retention(lambda_config)
        print()
    
    print(f"\\nDeployment complete: {success_count}/{len(LAMBDAS)} Lambdas")

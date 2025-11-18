import boto3
import zipfile
import io

lambda_client = boto3.client('lambda', region_name='us-east-1')

response = lambda_client.get_function(FunctionName='mediaflow-view-handler')
code_url = response['Code']['Location']

print(f"[INFO] Lambda code URL: {code_url[:80]}...")

# Get function configuration
config = response['Configuration']
print(f"\n[CONFIG]")
print(f"  Runtime: {config['Runtime']}")
print(f"  Handler: {config['Handler']}")
print(f"  Timeout: {config['Timeout']}s")
print(f"  Memory: {config['MemorySize']}MB")

# Check environment variables
env_vars = config.get('Environment', {}).get('Variables', {})
print(f"\n[ENV VARS]")
for key, value in env_vars.items():
    if 'SECRET' in key:
        print(f"  {key}: ***")
    else:
        print(f"  {key}: {value}")

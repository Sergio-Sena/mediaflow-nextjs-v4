import boto3

s3 = boto3.client('s3', region_name='us-east-1')
bucket = 'mediaflow-uploads-969430605054'
temp_key = 'temp/moana1-original.mp4'

print(f"Deletando: {temp_key}")
s3.delete_object(Bucket=bucket, Key=temp_key)
print("Deletado!")

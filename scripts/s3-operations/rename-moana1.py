import boto3

s3 = boto3.client('s3', region_name='us-east-1')
bucket = 'mediaflow-uploads-969430605054'

old_key = 'users/lid_lima/Moana/Moana.Um.Mar.de.Aventuras.2017.1080p.BluRay.DD5.1.x264.DUAL-TDF.mp4'
new_key = 'users/lid_lima/Moana/Moana.1.Um.Mar.de.Aventuras.2017.mp4'

print(f"Renomeando: {old_key}")
print(f"Para: {new_key}")

s3.copy_object(
    Bucket=bucket,
    CopySource={'Bucket': bucket, 'Key': old_key},
    Key=new_key
)

s3.delete_object(Bucket=bucket, Key=old_key)

print("Concluido!")

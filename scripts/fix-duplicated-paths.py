#!/usr/bin/env python3
import boto3

s3 = boto3.client('s3', region_name='us-east-1')
bucket = 'mediaflow-uploads-969430605054'
prefix = 'users/user_admin/users/user_admin/'

print("Corrigindo paths duplicados...")
print("=" * 60)

paginator = s3.get_paginator('list_objects_v2')
pages = paginator.paginate(Bucket=bucket, Prefix=prefix)

moved = 0
for page in pages:
    if 'Contents' in page:
        for obj in page['Contents']:
            source_key = obj['Key']
            if source_key.endswith('/'):
                continue
            
            # Remover duplicacao: users/user_admin/users/user_admin/ -> users/user_admin/
            dest_key = source_key.replace('users/user_admin/users/user_admin/', 'users/user_admin/')
            
            print(f"\nMovendo:")
            print(f"  De: {source_key}")
            print(f"  Para: {dest_key}")
            
            # Copiar (multipart para arquivos grandes)
            size = obj['Size']
            if size > 5 * 1024 * 1024 * 1024:  # >5GB
                # Multipart copy
                mpu = s3.create_multipart_upload(
                    Bucket=bucket,
                    Key=dest_key,
                    StorageClass='INTELLIGENT_TIERING'
                )
                
                part_size = 500 * 1024 * 1024  # 500MB
                parts = []
                part_num = 1
                
                for start in range(0, size, part_size):
                    end = min(start + part_size - 1, size - 1)
                    part = s3.upload_part_copy(
                        Bucket=bucket,
                        Key=dest_key,
                        CopySource={'Bucket': bucket, 'Key': source_key},
                        PartNumber=part_num,
                        UploadId=mpu['UploadId'],
                        CopySourceRange=f'bytes={start}-{end}'
                    )
                    parts.append({'PartNumber': part_num, 'ETag': part['CopyPartResult']['ETag']})
                    part_num += 1
                
                s3.complete_multipart_upload(
                    Bucket=bucket,
                    Key=dest_key,
                    UploadId=mpu['UploadId'],
                    MultipartUpload={'Parts': parts}
                )
            else:
                s3.copy_object(
                    Bucket=bucket,
                    CopySource={'Bucket': bucket, 'Key': source_key},
                    Key=dest_key,
                    StorageClass='INTELLIGENT_TIERING'
                )
            
            # Deletar original
            s3.delete_object(Bucket=bucket, Key=source_key)
            
            moved += 1
            print("  OK")

print(f"\n\nArquivos movidos: {moved}")
print("Duplicacao corrigida!")

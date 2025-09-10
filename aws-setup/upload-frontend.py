#!/usr/bin/env python3
import boto3
import json
import os
from pathlib import Path
import mimetypes

def upload_to_s3():
    """Upload Next.js build to S3"""
    
    with open('mediaflow-config.json', 'r') as f:
        config = json.load(f)
    
    s3_client = boto3.client('s3')
    bucket_name = config['buckets']['frontend']
    build_dir = Path('../out')
    
    print(f"Uploading to S3: {bucket_name}")
    
    uploaded_count = 0
    
    for file_path in build_dir.rglob('*'):
        if file_path.is_file():
            relative_path = file_path.relative_to(build_dir)
            s3_key = str(relative_path).replace('\\', '/')
            
            content_type, _ = mimetypes.guess_type(str(file_path))
            if not content_type:
                if file_path.suffix == '.html':
                    content_type = 'text/html'
                elif file_path.suffix == '.css':
                    content_type = 'text/css'
                elif file_path.suffix == '.js':
                    content_type = 'application/javascript'
                else:
                    content_type = 'application/octet-stream'
            
            try:
                s3_client.upload_file(
                    str(file_path),
                    bucket_name,
                    s3_key,
                    ExtraArgs={'ContentType': content_type}
                )
                uploaded_count += 1
                if uploaded_count % 10 == 0:
                    print(f"Uploaded {uploaded_count} files...")
            except Exception as e:
                print(f"Error uploading {s3_key}: {str(e)}")
    
    print(f"Upload complete! {uploaded_count} files")
    
    # Configure website
    try:
        s3_client.put_bucket_website(
            Bucket=bucket_name,
            WebsiteConfiguration={
                'IndexDocument': {'Suffix': 'index.html'},
                'ErrorDocument': {'Key': '404.html'}
            }
        )
        
        bucket_policy = {
            "Version": "2012-10-17",
            "Statement": [{
                "Effect": "Allow",
                "Principal": "*",
                "Action": "s3:GetObject",
                "Resource": f"arn:aws:s3:::{bucket_name}/*"
            }]
        }
        
        s3_client.put_bucket_policy(
            Bucket=bucket_name,
            Policy=json.dumps(bucket_policy)
        )
        
        website_url = f"http://{bucket_name}.s3-website-us-east-1.amazonaws.com"
        print(f"Website URL: {website_url}")
        
        config['frontend_url'] = website_url
        with open('mediaflow-config.json', 'w') as f:
            json.dump(config, f, indent=2)
        
        return website_url
    except Exception as e:
        print(f"Website config error: {str(e)}")
        return None

if __name__ == "__main__":
    upload_to_s3()
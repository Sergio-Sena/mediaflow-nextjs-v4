import boto3
import json
import os
import sys
import io
from pathlib import Path
import mimetypes

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

def upload_to_s3():
    """Upload build to S3"""
    
    s3_client = boto3.client('s3', region_name='us-east-1')
    bucket_name = 'mediaflow-frontend-969430605054'
    build_dir = Path('.next/standalone')
    
    print(f"Deploying to S3: {bucket_name}")
    print("=" * 60)
    
    if not build_dir.exists():
        build_dir = Path('out')
    
    if not build_dir.exists():
        print("Build directory not found! Run 'npm run build' first")
        return False
    
    uploaded = 0
    
    for file_path in build_dir.rglob('*'):
        if file_path.is_file():
            relative_path = file_path.relative_to(build_dir)
            s3_key = str(relative_path).replace('\\\\', '/')
            
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
                    ExtraArgs={
                        'ContentType': content_type,
                        'CacheControl': 'public, max-age=31536000' if file_path.suffix in ['.js', '.css', '.png', '.jpg', '.ico', '.woff', '.woff2'] else 'public, max-age=0'
                    }
                )
                uploaded += 1
                if uploaded % 50 == 0:
                    print(f"  Uploaded {uploaded} files...")
            except Exception as e:
                print(f"  Error: {s3_key} - {e}")
    
    print(f"\n✅ Deploy complete! {uploaded} files uploaded")
    print(f"🌐 URL: https://midiaflow.sstechnologies-cloud.com")
    return True

if __name__ == "__main__":
    print("Midiaflow - Deploy to Production")
    print("=" * 60)
    upload_to_s3()

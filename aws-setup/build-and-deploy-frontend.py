#!/usr/bin/env python3
import subprocess
import boto3
import os
import json
from pathlib import Path
import mimetypes

def build_nextjs():
    """Build Next.js for static export"""
    print("Building Next.js for AWS...")
    
    # Copy AWS config
    subprocess.run(['copy', 'next.config.aws.js', 'next.config.js'], shell=True, check=True)
    
    # Build
    result = subprocess.run(['npm', 'run', 'build'], cwd='..', capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Build failed: {result.stderr}")
        return False
    
    print("Build successful!")
    return True

def upload_to_s3():
    """Upload build to S3 frontend bucket"""
    
    # Load config
    with open('mediaflow-config.json', 'r') as f:
        config = json.load(f)
    
    s3_client = boto3.client('s3')
    bucket_name = config['buckets']['frontend']
    build_dir = Path('../out')
    
    print(f"Uploading to S3 bucket: {bucket_name}")
    
    if not build_dir.exists():
        print("Build directory not found!")
        return False
    
    uploaded_count = 0
    
    for file_path in build_dir.rglob('*'):
        if file_path.is_file():
            # Get relative path
            relative_path = file_path.relative_to(build_dir)
            s3_key = str(relative_path).replace('\\', '/')
            
            # Determine content type
            content_type, _ = mimetypes.guess_type(str(file_path))
            if not content_type:
                content_type = 'application/octet-stream'
            
            # Special handling for HTML files
            if file_path.suffix == '.html':
                content_type = 'text/html'
            elif file_path.suffix == '.css':
                content_type = 'text/css'
            elif file_path.suffix == '.js':
                content_type = 'application/javascript'
            
            try:
                s3_client.upload_file(
                    str(file_path),
                    bucket_name,
                    s3_key,
                    ExtraArgs={
                        'ContentType': content_type,
                        'CacheControl': 'public, max-age=31536000' if file_path.suffix in ['.js', '.css', '.png', '.jpg', '.ico'] else 'public, max-age=0'
                    }
                )
                uploaded_count += 1
                if uploaded_count % 10 == 0:
                    print(f"Uploaded {uploaded_count} files...")
            except Exception as e:
                print(f"Error uploading {s3_key}: {str(e)}")
    
    print(f"Upload complete! {uploaded_count} files uploaded")
    return True

def configure_s3_website():
    """Configure S3 bucket for static website hosting"""
    
    with open('mediaflow-config.json', 'r') as f:
        config = json.load(f)
    
    s3_client = boto3.client('s3')
    bucket_name = config['buckets']['frontend']
    
    print("Configuring S3 website hosting...")
    
    # Website configuration
    website_config = {
        'IndexDocument': {'Suffix': 'index.html'},
        'ErrorDocument': {'Key': '404.html'}
    }
    
    try:
        s3_client.put_bucket_website(
            Bucket=bucket_name,
            WebsiteConfiguration=website_config
        )
        
        # Public read policy
        bucket_policy = {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Sid": "PublicReadGetObject",
                    "Effect": "Allow",
                    "Principal": "*",
                    "Action": "s3:GetObject",
                    "Resource": f"arn:aws:s3:::{bucket_name}/*"
                }
            ]
        }
        
        s3_client.put_bucket_policy(
            Bucket=bucket_name,
            Policy=json.dumps(bucket_policy)
        )
        
        website_url = f"http://{bucket_name}.s3-website-us-east-1.amazonaws.com"
        print(f"Website configured: {website_url}")
        
        # Update config
        config['frontend_url'] = website_url
        with open('mediaflow-config.json', 'w') as f:
            json.dump(config, f, indent=2)
        
        return website_url
    except Exception as e:
        print(f"Error configuring website: {str(e)}")
        return None

def main():
    print("Mediaflow Frontend Deployment - Phase 4")
    print("=" * 50)
    
    # Step 1: Build Next.js
    if not build_nextjs():
        return
    
    # Step 2: Upload to S3
    if not upload_to_s3():
        return
    
    # Step 3: Configure website
    website_url = configure_s3_website()
    
    if website_url:
        print("\n" + "=" * 50)
        print("Phase 4 Complete!")
        print(f"Frontend URL: {website_url}")
        print("Frontend now uses AWS APIs (no 10MB limit!)")
    else:
        print("Deployment failed!")

if __name__ == "__main__":
    main()
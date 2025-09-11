#!/usr/bin/env python3
import boto3

def cleanup_ts_files():
    """Remove all .ts files from S3 bucket"""
    
    s3_client = boto3.client('s3')
    bucket_name = 'mediaflow-uploads-969430605054'
    
    print(f"Scanning for .ts files in: {bucket_name}")
    
    # List all .ts files
    response = s3_client.list_objects_v2(Bucket=bucket_name)
    all_files = response.get('Contents', [])
    
    ts_files = []
    for obj in all_files:
        key = obj['Key']
        if key.lower().endswith('.ts'):
            ts_files.append(key)
    
    print(f"Found {len(ts_files)} .ts files to delete")
    
    if not ts_files:
        print("No .ts files found!")
        return
    
    # Delete all .ts files
    deleted_count = 0
    
    for ts_file in ts_files:
        try:
            s3_client.delete_object(Bucket=bucket_name, Key=ts_file)
            deleted_count += 1
            print(f"[OK] Deleted: {ts_file[:50]}...")
        except Exception as e:
            print(f"[ERROR] Failed to delete {ts_file[:50]}...: {str(e)}")
    
    print(f"\n[SUMMARY]")
    print(f"Deleted: {deleted_count}/{len(ts_files)} files")
    print(f"Bucket cleaned - ready for new uploads!")

if __name__ == "__main__":
    cleanup_ts_files()
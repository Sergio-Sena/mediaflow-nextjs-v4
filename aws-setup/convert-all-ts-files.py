#!/usr/bin/env python3
import boto3
import json

def convert_all_ts_files():
    """Trigger conversion for all .ts files in S3"""
    
    s3_client = boto3.client('s3')
    lambda_client = boto3.client('lambda')
    
    bucket_name = 'mediaflow-uploads-969430605054'
    convert_function = 'mediaflow-convert-handler'
    
    print(f"Scanning bucket: {bucket_name}")
    
    # List all .ts files
    response = s3_client.list_objects_v2(Bucket=bucket_name)
    all_files = response.get('Contents', [])
    
    ts_files = []
    for obj in all_files:
        key = obj['Key']
        if key.lower().endswith('.ts'):
            ts_files.append(key)
    
    print(f"Found {len(ts_files)} .ts files to convert")
    # Skip printing filenames with special characters
    
    if not ts_files:
        print("No .ts files found!")
        return
    
    # Trigger conversion for each file
    converted_count = 0
    failed_count = 0
    
    for ts_file in ts_files:
        try:
            # Invoke convert lambda manually
            payload = {
                'httpMethod': 'POST',
                'body': json.dumps({'key': ts_file})
            }
            
            response = lambda_client.invoke(
                FunctionName=convert_function,
                Payload=json.dumps(payload)
            )
            
            result = json.loads(response['Payload'].read())
            
            if result.get('statusCode') == 200:
                body = json.loads(result.get('body', '{}'))
                if body.get('success'):
                    print(f"[OK] Queued: {ts_file}")
                    converted_count += 1
                else:
                    print(f"[ERROR] Failed: {ts_file} - {body.get('message')}")
                    failed_count += 1
            else:
                print(f"[ERROR] HTTP {result.get('statusCode')}: {ts_file}")
                failed_count += 1
                
        except Exception as e:
            print(f"[ERROR] Exception for {ts_file}: {str(e)}")
            failed_count += 1
    
    print(f"\n[SUMMARY]")
    print(f"Queued for conversion: {converted_count}")
    print(f"Failed: {failed_count}")
    print(f"Total: {len(ts_files)}")
    
    if converted_count > 0:
        print(f"\n[INFO] All conversions will complete automatically")
        print(f"[INFO] Original .ts files will be replaced by .mp4")
        print(f"[INFO] Check MediaConvert console for progress")

if __name__ == "__main__":
    convert_all_ts_files()
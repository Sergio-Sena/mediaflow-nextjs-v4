import json
import boto3
import os
from urllib.parse import unquote

s3 = boto3.client('s3')
UPLOADS_BUCKET = os.environ.get('UPLOADS_BUCKET', 'mediaflow-uploads-969430605054')
PROCESSED_BUCKET = os.environ.get('PROCESSED_BUCKET', 'mediaflow-processed-969430605054')

def lambda_handler(event, context):
    try:
        if event['httpMethod'] == 'OPTIONS':
            return cors_response(200, {})
        
        key = unquote(event['pathParameters']['key'])
        
        # Try processed bucket first (optimized videos), then uploads
        bucket_to_use = UPLOADS_BUCKET
        
        # Check if optimized version exists in processed bucket
        try:
            # Look for converted version (with _1080p suffix)
            base_name = key.rsplit('.', 1)[0]
            converted_key = f"{base_name}_1080p.mp4"
            s3.head_object(Bucket=PROCESSED_BUCKET, Key=converted_key)
            bucket_to_use = PROCESSED_BUCKET
            key = converted_key
        except:
            # If no converted version, check original in processed bucket
            try:
                s3.head_object(Bucket=PROCESSED_BUCKET, Key=key)
                bucket_to_use = PROCESSED_BUCKET
            except:
                # Fall back to uploads bucket
                pass
        
        # Generate presigned URL
        view_url = s3.generate_presigned_url(
            'get_object',
            Params={'Bucket': bucket_to_use, 'Key': key},
            ExpiresIn=3600
        )
        
        return cors_response(200, {
            'success': True,
            'viewUrl': view_url
        })
        
    except Exception as e:
        return cors_response(500, {'success': False, 'message': str(e)})

def cors_response(status_code, body):
    return {
        'statusCode': status_code,
        'headers': {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Headers': 'Content-Type,Authorization',
            'Access-Control-Allow-Methods': 'GET,OPTIONS'
        },
        'body': json.dumps(body)
    }
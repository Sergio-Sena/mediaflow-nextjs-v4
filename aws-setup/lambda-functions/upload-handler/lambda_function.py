import json
import boto3
import os
from datetime import datetime

s3 = boto3.client('s3')
UPLOADS_BUCKET = os.environ.get('UPLOADS_BUCKET', 'mediaflow-uploads-969430605054')

def lambda_handler(event, context):
    try:
        if event['httpMethod'] == 'OPTIONS':
            return cors_response(200, {})
        
        body = json.loads(event.get('body', '{}'))
        filename = body.get('filename')
        content_type = body.get('contentType', 'application/octet-stream')
        
        if not filename:
            return cors_response(400, {'success': False, 'message': 'Filename required'})
        
        # Generate presigned URL for upload (NO SIZE LIMIT)
        presigned_url = s3.generate_presigned_url(
            'put_object',
            Params={
                'Bucket': UPLOADS_BUCKET,
                'Key': filename,
                'ContentType': content_type
            },
            ExpiresIn=3600  # 1 hour
        )
        
        return cors_response(200, {
            'success': True,
            'uploadUrl': presigned_url,
            'key': filename,
            'bucket': UPLOADS_BUCKET
        })
        
    except Exception as e:
        return cors_response(500, {'success': False, 'message': str(e)})

def cors_response(status_code, body):
    return {
        'statusCode': status_code,
        'headers': {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Headers': 'Content-Type,Authorization',
            'Access-Control-Allow-Methods': 'POST,OPTIONS'
        },
        'body': json.dumps(body)
    }
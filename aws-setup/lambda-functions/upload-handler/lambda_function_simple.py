import json
import boto3
import os

s3 = boto3.client('s3')
UPLOADS_BUCKET = os.environ.get('UPLOADS_BUCKET', 'midiaflow-uploads-969430605054')

def lambda_handler(event, context):
    try:
        print(f"Event: {json.dumps(event)}")
        
        if event.get('httpMethod') == 'OPTIONS':
            return cors_response(200, {})
        
        body = json.loads(event.get('body', '{}'))
        filename = body.get('filename', 'test.mp4')
        content_type = body.get('contentType', 'video/mp4')
        
        print(f"Generating presigned URL for: {filename}")
        
        presigned_url = s3.generate_presigned_url(
            'put_object',
            Params={
                'Bucket': UPLOADS_BUCKET,
                'Key': filename,
                'ContentType': content_type
            },
            ExpiresIn=7200
        )
        
        print(f"Success: {presigned_url[:50]}...")
        
        return cors_response(200, {
            'success': True,
            'uploadUrl': presigned_url,
            'key': filename,
            'bucket': UPLOADS_BUCKET
        })
        
    except Exception as e:
        print(f"Error: {str(e)}")
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

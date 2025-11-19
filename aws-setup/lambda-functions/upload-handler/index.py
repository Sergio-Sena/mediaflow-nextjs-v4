import json
import boto3
import os

s3 = boto3.client('s3')
BUCKET = os.environ.get('UPLOADS_BUCKET', 'midiaflow-uploads-969430605054')

def lambda_handler(event, context):
    print(f"Event: {event}")
    
    try:
        if event.get('httpMethod') == 'OPTIONS':
            return {
                'statusCode': 200,
                'headers': {
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Methods': 'POST,OPTIONS',
                    'Access-Control-Allow-Headers': 'Content-Type'
                },
                'body': ''
            }
        
        body = json.loads(event.get('body', '{}'))
        filename = body.get('filename')
        content_type = body.get('contentType', 'application/octet-stream')
        
        if not filename:
            return error_response(400, 'Filename required')
        
        url = s3.generate_presigned_url(
            'put_object',
            Params={'Bucket': BUCKET, 'Key': filename, 'ContentType': content_type},
            ExpiresIn=7200
        )
        
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Content-Type': 'application/json'
            },
            'body': json.dumps({
                'success': True,
                'uploadUrl': url,
                'key': filename,
                'bucket': BUCKET
            })
        }
    except Exception as e:
        print(f"Error: {e}")
        return error_response(500, str(e))

def error_response(code, msg):
    return {
        'statusCode': code,
        'headers': {'Access-Control-Allow-Origin': '*', 'Content-Type': 'application/json'},
        'body': json.dumps({'success': False, 'message': msg})
    }

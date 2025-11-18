import json
import boto3
import os
from urllib.parse import unquote

s3 = boto3.client('s3')

UPLOADS_BUCKET = os.environ.get('UPLOADS_BUCKET', 'mediaflow-uploads-969430605054')

def lambda_handler(event, context):
    print(f"Event: {json.dumps(event)}")
    
    # CORS headers
    headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Headers': 'Content-Type,Authorization',
        'Access-Control-Allow-Methods': 'GET,OPTIONS'
    }
    
    try:
        if event['httpMethod'] == 'OPTIONS':
            return {'statusCode': 200, 'headers': headers, 'body': '{}'}
        
        # Get key from path
        key = unquote(event['pathParameters']['key'])
        print(f"Key: {key}")
        
        # Generate presigned URL
        view_url = s3.generate_presigned_url(
            'get_object',
            Params={'Bucket': UPLOADS_BUCKET, 'Key': key},
            ExpiresIn=3600
        )
        
        return {
            'statusCode': 200,
            'headers': headers,
            'body': json.dumps({
                'success': True,
                'viewUrl': view_url
            })
        }
        
    except Exception as e:
        print(f"Error: {str(e)}")
        return {
            'statusCode': 500,
            'headers': headers,
            'body': json.dumps({
                'success': False,
                'message': str(e)
            })
        }

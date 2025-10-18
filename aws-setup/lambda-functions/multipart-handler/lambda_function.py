import json
import boto3
import os

s3 = boto3.client('s3')
BUCKET = os.environ.get('UPLOADS_BUCKET', 'mediaflow-uploads-969430605054')

def lambda_handler(event, context):
    try:
        method = event['httpMethod']
        
        if method == 'OPTIONS':
            return cors_response(200, {})
        
        body = json.loads(event.get('body', '{}'))
        action = body.get('action')
        
        if action == 'initiate':
            return initiate_upload(body)
        elif action == 'get-url':
            return get_presigned_url(body)
        elif action == 'complete':
            return complete_upload(body)
        elif action == 'abort':
            return abort_upload(body)
        else:
            return cors_response(400, {'success': False, 'message': 'Invalid action'})
            
    except Exception as e:
        print(f"Error: {str(e)}")
        return cors_response(500, {'success': False, 'message': str(e)})

def initiate_upload(body):
    filename = sanitize_filename(body['filename'])
    content_type = body.get('contentType', 'application/octet-stream')
    
    response = s3.create_multipart_upload(
        Bucket=BUCKET,
        Key=filename,
        ContentType=content_type
    )
    
    print(f"Initiated multipart upload: {response['UploadId']}")
    
    return cors_response(200, {
        'success': True,
        'uploadId': response['UploadId']
    })

def get_presigned_url(body):
    upload_id = body['uploadId']
    part_number = body['partNumber']
    key = body['key']
    
    url = s3.generate_presigned_url(
        'upload_part',
        Params={
            'Bucket': BUCKET,
            'Key': key,
            'UploadId': upload_id,
            'PartNumber': part_number
        },
        ExpiresIn=900
    )
    
    return cors_response(200, {
        'success': True,
        'presignedUrl': url
    })

def complete_upload(body):
    upload_id = body['uploadId']
    key = body['key']
    parts = body['parts']
    
    s3.complete_multipart_upload(
        Bucket=BUCKET,
        Key=key,
        UploadId=upload_id,
        MultipartUpload={'Parts': parts}
    )
    
    print(f"Completed multipart upload: {upload_id}")
    
    return cors_response(200, {'success': True})

def abort_upload(body):
    upload_id = body['uploadId']
    key = body['key']
    
    s3.abort_multipart_upload(
        Bucket=BUCKET,
        Key=key,
        UploadId=upload_id
    )
    
    print(f"Aborted multipart upload: {upload_id}")
    
    return cors_response(200, {'success': True})

def sanitize_filename(filename):
    # Remover path traversal
    filename = filename.replace('../', '').replace('..\\', '')
    # Remover caracteres perigosos
    dangerous_chars = ['<', '>', ':', '"', '|', '?', '*', '\x00']
    for char in dangerous_chars:
        filename = filename.replace(char, '')
    return filename

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

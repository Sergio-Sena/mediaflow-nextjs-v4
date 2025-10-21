import json
import boto3
import base64
from datetime import datetime

s3 = boto3.client('s3')
BUCKET = 'mediaflow-uploads-969430605054'

def lambda_handler(event, context):
    try:
        print(f"Event: {json.dumps(event)}")
        
        if event['httpMethod'] == 'OPTIONS':
            print("Handling OPTIONS preflight")
            return cors_response(200, {'message': 'CORS OK'})
        
        path = event.get('path', '')
        body = json.loads(event.get('body', '{}'))
        
        # Extrair username do JWT
        username = extract_username(event)
        
        # INIT - Iniciar multipart upload
        if '/init' in path:
            filename = body.get('filename', '')
            file_size = body.get('fileSize', 0)
            
            # SEMPRE usar users/{username}/ independente do filename
            key = f"users/{username}/{filename}"
            
            response = s3.create_multipart_upload(
                Bucket=BUCKET,
                Key=key,
                Metadata={
                    'original_name': filename,
                    'upload_timestamp': datetime.now().isoformat(),
                    'file_size': str(file_size)
                }
            )
            
            return cors_response(200, {
                'success': True,
                'uploadId': response['UploadId'],
                'key': key
            })
        
        # PART - Gerar presigned URL para upload de parte
        if '/part' in path:
            key = body.get('key')
            upload_id = body.get('uploadId')
            part_number = body.get('partNumber')
            
            url = s3.generate_presigned_url(
                'upload_part',
                Params={
                    'Bucket': BUCKET,
                    'Key': key,
                    'UploadId': upload_id,
                    'PartNumber': part_number
                },
                ExpiresIn=3600
            )
            
            return cors_response(200, {
                'success': True,
                'uploadUrl': url
            })
        
        # COMPLETE - Finalizar multipart upload
        if '/complete' in path:
            key = body.get('key')
            upload_id = body.get('uploadId')
            parts = body.get('parts', [])
            
            s3.complete_multipart_upload(
                Bucket=BUCKET,
                Key=key,
                UploadId=upload_id,
                MultipartUpload={'Parts': parts}
            )
            
            return cors_response(200, {
                'success': True,
                'message': 'Upload completed',
                'key': key
            })
        
        # ABORT - Cancelar multipart upload
        if '/abort' in path:
            key = body.get('key')
            upload_id = body.get('uploadId')
            
            s3.abort_multipart_upload(
                Bucket=BUCKET,
                Key=key,
                UploadId=upload_id
            )
            
            return cors_response(200, {
                'success': True,
                'message': 'Upload aborted'
            })
        
        return cors_response(400, {
            'success': False,
            'message': 'Invalid endpoint'
        })
        
    except Exception as e:
        return cors_response(500, {
            'success': False,
            'message': str(e)
        })

def extract_username(event):
    """Extrair username do JWT sem biblioteca externa"""
    auth_header = event.get('headers', {}).get('Authorization', '') or \
                  event.get('headers', {}).get('authorization', '')
    
    if not auth_header:
        return 'anonymous'
    
    try:
        # Remover 'Bearer '
        token = auth_header.replace('Bearer ', '').strip()
        
        # JWT format: header.payload.signature
        parts = token.split('.')
        if len(parts) != 3:
            return 'anonymous'
        
        # Decodificar payload (segunda parte)
        payload = parts[1]
        
        # Adicionar padding se necessário
        padding = 4 - (len(payload) % 4)
        if padding != 4:
            payload += '=' * padding
        
        # Decodificar base64
        decoded = base64.urlsafe_b64decode(payload)
        payload_data = json.loads(decoded)
        
        # Extrair username
        username = payload_data.get('username', 'anonymous')
        print(f"Username extraído do JWT: {username}")
        return username
        
    except Exception as e:
        print(f"Erro ao parsear JWT: {e}")
        return 'anonymous'

def cors_response(status_code, body):
    return {
        'statusCode': status_code,
        'headers': {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Headers': 'Content-Type,Authorization',
            'Access-Control-Allow-Methods': 'POST,DELETE,OPTIONS'
        },
        'body': json.dumps(body)
    }

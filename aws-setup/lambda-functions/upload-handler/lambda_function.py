import json
import boto3
import os
import re
import jwt
from datetime import datetime

s3 = boto3.client('s3')
UPLOADS_BUCKET = os.environ.get('UPLOADS_BUCKET', 'mediaflow-uploads-969430605054')
SECRET_KEY = os.environ.get('JWT_SECRET', '17b8312c72fdcffbff89f2f4a564fb26e936002d344717ab7753a237fcd57aea')

def lambda_handler(event, context):
    try:
        if event['httpMethod'] == 'OPTIONS':
            return cors_response(200, {})
        
        # Check route
        if event.get('path', '').endswith('/check'):
            body = json.loads(event.get('body', '{}'))
            filenames = body.get('filenames', [])
            
            results = []
            for filename in filenames:
                sanitized = sanitize_filename(filename)
                exists = check_file_exists(sanitized)
                results.append({
                    'original': filename,
                    'sanitized': sanitized,
                    'exists': exists
                })
            
            return cors_response(200, {'success': True, 'files': results})
        
        # Upload route (existing logic)
        body = json.loads(event.get('body', '{}'))
        filename = body.get('filename')
        file_size = body.get('fileSize', 0)
        content_type = body.get('contentType', 'application/octet-stream')
        
        if not filename:
            return cors_response(400, {'success': False, 'message': 'Filename required'})
        
        # Extrair user_id do JWT
        user_id = extract_user_id(event)
        
        sanitized_name = sanitize_filename(filename)
        
        # SEMPRE salvar em users/{user_id}/ respeitando estrutura original
        # Se já começa com users/, não duplicar
        if not sanitized_name.startswith('users/'):
            sanitized_name = f'users/{user_id}/{sanitized_name}'
        else:
            # Já tem users/ no início, usar como está
            pass

        needs_conversion = should_convert(sanitized_name, file_size)
        
        metadata = {
            'original_name': sanitized_name,
            'needs_conversion': str(needs_conversion).lower(),
            'file_type': get_file_type(sanitized_name),
            'upload_timestamp': datetime.now().isoformat()
        }
        
        presigned_url = s3.generate_presigned_url(
            'put_object',
            Params={
                'Bucket': UPLOADS_BUCKET,
                'Key': sanitized_name,
                'ContentType': content_type,
                'Metadata': metadata
            },
            ExpiresIn=7200
        )
        
        return cors_response(200, {
            'success': True,
            'uploadUrl': presigned_url,
            'key': sanitized_name,
            'originalName': filename,
            'sanitizedName': sanitized_name,
            'needsConversion': needs_conversion,
            'bucket': UPLOADS_BUCKET
        })
        
    except Exception as e:
        return cors_response(500, {'success': False, 'message': str(e)})

def check_file_exists(key):
    """Check if file exists in S3"""
    try:
        s3.head_object(Bucket=UPLOADS_BUCKET, Key=key)
        return True
    except:
        return False

def sanitize_filename(filename):
    """Sanitize filename: remove emojis, special chars, limit to 45 chars"""
    emoji_pattern = re.compile("["
        u"\U0001F600-\U0001F64F"
        u"\U0001F300-\U0001F5FF"
        u"\U0001F680-\U0001F6FF"
        u"\U0001F1E0-\U0001F1FF"
        u"\U00002702-\U000027B0"
        u"\U000024C2-\U0001F251"
        "]+", flags=re.UNICODE)
    
    clean = emoji_pattern.sub('', filename)
    clean = re.sub(r'[^a-zA-Z0-9._/-]', '_', clean)
    clean = re.sub(r'_+', '_', clean)
    clean = clean.strip('_')
    
    if len(clean) > 45:
        name_part, ext = os.path.splitext(clean)
        max_name_len = 45 - len(ext) - 3
        if max_name_len > 0:
            clean = name_part[:max_name_len] + '...' + ext
        else:
            clean = name_part[:42] + '...' + ext
    
    if not clean or clean == '.':
        clean = 'file_' + datetime.now().strftime('%Y%m%d_%H%M%S')
    
    return clean

def should_convert(filename, file_size_bytes):
    """Determine if file needs conversion"""
    ext = filename.lower().split('.')[-1] if '.' in filename else ''
    size_mb = file_size_bytes / (1024 * 1024) if file_size_bytes else 0
    
    always_convert = ['ts', 'avi', 'mov', 'mkv', 'webm', 'flv', 'wmv', 'm4v', '3gp']
    if ext in always_convert:
        return True
    
    if ext == 'mp4' and size_mb > 500:
        return True
    
    return False

def get_file_type(filename):
    """Get file type category"""
    ext = filename.lower().split('.')[-1] if '.' in filename else ''
    
    video_exts = ['mp4', 'avi', 'mov', 'mkv', 'webm', 'ts', 'flv', 'wmv', 'm4v', '3gp']
    image_exts = ['jpg', 'jpeg', 'png', 'gif', 'webp', 'bmp', 'svg', 'ico', 'tiff', 'tif']
    doc_exts = ['pdf', 'doc', 'docx', 'txt', 'rtf', 'xls', 'xlsx', 'ppt', 'pptx', 'odt', 'ods', 'odp', 'csv']
    
    if ext in video_exts:
        return 'video'
    elif ext in image_exts:
        return 'image'
    elif ext in doc_exts:
        return 'document'
    else:
        return 'other'

def extract_user_id(event):
    """Extrair user_id do JWT"""
    auth_header = event.get('headers', {}).get('Authorization', '') or \
                  event.get('headers', {}).get('authorization', '')
    
    if not auth_header:
        return 'anonymous'
    
    try:
        token = auth_header.replace('Bearer ', '').strip()
        decoded = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        user_id = decoded.get('user_id', 'anonymous')
        print(f"User ID extraído: {user_id}")
        return user_id
    except Exception as e:
        print(f"Erro JWT: {e}")
        return 'anonymous'

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

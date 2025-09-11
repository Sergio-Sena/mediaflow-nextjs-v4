import json
import boto3
import os
import re
from datetime import datetime

s3 = boto3.client('s3')
UPLOADS_BUCKET = os.environ.get('UPLOADS_BUCKET', 'mediaflow-uploads-969430605054')

def lambda_handler(event, context):
    try:
        if event['httpMethod'] == 'OPTIONS':
            return cors_response(200, {})
        
        body = json.loads(event.get('body', '{}'))
        filename = body.get('filename')
        file_size = body.get('fileSize', 0)
        content_type = body.get('contentType', 'application/octet-stream')
        
        if not filename:
            return cors_response(400, {'success': False, 'message': 'Filename required'})
        
        # Sanitize filename and detect conversion need
        sanitized_name = sanitize_filename(filename)
        needs_conversion = should_convert(sanitized_name, file_size)
        
        # Metadata for conversion logic (ASCII only)
        metadata = {
            'original_name': sanitized_name,  # Use sanitized name (ASCII safe)
            'needs_conversion': str(needs_conversion).lower(),
            'file_type': get_file_type(sanitized_name),
            'upload_timestamp': datetime.now().isoformat()
        }
        
        # Generate presigned URL for upload with metadata
        presigned_url = s3.generate_presigned_url(
            'put_object',
            Params={
                'Bucket': UPLOADS_BUCKET,
                'Key': sanitized_name,
                'ContentType': content_type,
                'Metadata': metadata
            },
            ExpiresIn=7200  # 2 hours para uploads grandes
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

def sanitize_filename(filename):
    """Sanitize filename: remove emojis, special chars, limit to 45 chars"""
    # Remove emojis (Unicode ranges)
    emoji_pattern = re.compile("["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map
        u"\U0001F1E0-\U0001F1FF"  # flags
        u"\U00002702-\U000027B0"
        u"\U000024C2-\U0001F251"
        "]+", flags=re.UNICODE)
    
    clean = emoji_pattern.sub('', filename)
    
    # Remove special characters, keep only alphanumeric, dots, hyphens, underscores, slashes
    clean = re.sub(r'[^a-zA-Z0-9._/-]', '_', clean)
    
    # Remove multiple underscores
    clean = re.sub(r'_+', '_', clean)
    
    # Remove leading/trailing underscores
    clean = clean.strip('_')
    
    # Limit to 45 characters (preserve extension)
    if len(clean) > 45:
        name_part, ext = os.path.splitext(clean)
        max_name_len = 45 - len(ext) - 3  # Reserve 3 chars for "..."
        if max_name_len > 0:
            clean = name_part[:max_name_len] + '...' + ext
        else:
            clean = name_part[:42] + '...' + ext
    
    # Ensure filename is not empty
    if not clean or clean == '.':
        clean = 'file_' + datetime.now().strftime('%Y%m%d_%H%M%S')
    
    return clean

def should_convert(filename, file_size_bytes):
    """Determine if file needs conversion"""
    ext = filename.lower().split('.')[-1] if '.' in filename else ''
    size_mb = file_size_bytes / (1024 * 1024) if file_size_bytes else 0
    
    # Always convert these formats to MP4
    always_convert = ['ts', 'avi', 'mov', 'mkv', 'webm', 'flv', 'wmv', 'm4v', '3gp']
    if ext in always_convert:
        return True
    
    # Convert large MP4 files for optimization (>500MB)
    if ext == 'mp4' and size_mb > 500:
        return True
    
    return False

def get_file_type(filename):
    """Get file type category"""
    ext = filename.lower().split('.')[-1] if '.' in filename else ''
    
    video_exts = ['mp4', 'avi', 'mov', 'mkv', 'webm', 'ts', 'flv', 'wmv', 'm4v', '3gp']
    image_exts = ['jpg', 'jpeg', 'png', 'gif', 'webp', 'bmp']
    doc_exts = ['pdf', 'doc', 'docx', 'txt', 'rtf']
    
    if ext in video_exts:
        return 'video'
    elif ext in image_exts:
        return 'image'
    elif ext in doc_exts:
        return 'document'
    else:
        return 'other'

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
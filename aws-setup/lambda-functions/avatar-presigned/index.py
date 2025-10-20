import json
import boto3

s3 = boto3.client('s3', region_name='us-east-1')

def lambda_handler(event, context):
    try:
        if isinstance(event.get('body'), str):
            body = json.loads(event['body'])
        else:
            body = event.get('body', {})
        
        user_id = body.get('userId')
        file_ext = body.get('fileExt', 'png')
        
        if not user_id:
            return {
                'statusCode': 400,
                'headers': {
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Headers': '*',
                    'Access-Control-Allow-Methods': '*'
                },
                'body': json.dumps({'success': False, 'error': 'userId required'})
            }
        
        key = f'avatars/avatar_{user_id}.{file_ext}'
        
        # Normalizar content type
        content_type_map = {
            'jpg': 'image/jpeg',
            'jpeg': 'image/jpeg',
            'png': 'image/png',
            'gif': 'image/gif',
            'webp': 'image/webp'
        }
        content_type = content_type_map.get(file_ext.lower(), 'image/jpeg')
        
        presigned_url = s3.generate_presigned_url(
            'put_object',
            Params={
                'Bucket': 'mediaflow-uploads-969430605054',
                'Key': key,
                'ContentType': content_type
            },
            ExpiresIn=300
        )
        
        # Garantir que não há HTML entities na URL
        presigned_url = presigned_url.replace('&amp;', '&')
        
        avatar_url = f'https://mediaflow-uploads-969430605054.s3.amazonaws.com/{key}'
        
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': '*',
                'Access-Control-Allow-Methods': '*'
            },
            'body': json.dumps({
                'success': True,
                'presignedUrl': presigned_url,
                'avatarUrl': avatar_url
            })
        }
        
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': '*',
                'Access-Control-Allow-Methods': '*'
            },
            'body': json.dumps({'success': False, 'error': str(e)})
        }

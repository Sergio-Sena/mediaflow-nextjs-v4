import json
import boto3
import os
import uuid
from datetime import datetime, timezone

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('mediaflow-public-content')
JWT_SECRET = os.environ['JWT_SECRET']


def verify_token(event):
    import hmac, hashlib, base64
    headers = event.get('headers', {})
    auth = headers.get('Authorization') or headers.get('authorization', '')
    if not auth.startswith('Bearer '):
        return None
    token = auth.replace('Bearer ', '')
    try:
        parts = token.split('.')
        if len(parts) != 3:
            return None
        payload = json.loads(base64.urlsafe_b64decode(parts[1] + '=='))
        message = f"{parts[0]}.{parts[1]}"
        expected_sig = base64.urlsafe_b64encode(
            hmac.new(JWT_SECRET.encode(), message.encode(), hashlib.sha256).digest()
        ).decode().rstrip('=')
        if expected_sig != parts[2]:
            return None
        return payload
    except:
        return None


def lambda_handler(event, context):
    try:
        method = event['httpMethod']
        if method == 'OPTIONS':
            return cors_response(200, {})

        user = verify_token(event)
        if not user:
            return cors_response(401, {'success': False, 'message': 'Unauthorized'})

        if method == 'GET':
            return get_public_content(event, user)
        elif method == 'POST':
            body = json.loads(event.get('body', '{}'))
            action = body.get('action', 'share')
            if action == 'share':
                return share_content(body, user)
            elif action == 'like':
                return like_content(body, user)
            elif action == 'comment':
                return add_comment(body, user)
            elif action == 'deactivate':
                return deactivate_content(body, user)
            else:
                return cors_response(400, {'success': False, 'message': f'Unknown action: {action}'})
        elif method == 'DELETE':
            return unshare_content(event, user)

    except Exception as e:
        return cors_response(500, {'success': False, 'message': str(e)})


def share_content(body, user):
    file_key = body.get('file_key')
    title = body.get('title', '')
    file_type = body.get('type', 'video')
    category = body.get('category', 'Geral')

    if not file_key:
        return cors_response(400, {'success': False, 'message': 'file_key required'})

    user_prefix = user.get('s3_prefix', f"users/{user['user_id']}/")
    if not file_key.startswith(user_prefix) and user.get('role') != 'admin':
        return cors_response(403, {'success': False, 'message': 'You can only share your own files'})

    content_id = str(uuid.uuid4())
    item = {
        'content_id': content_id,
        'owner_id': user['user_id'],
        'owner_name': user.get('email', '').split('@')[0],
        'file_key': file_key,
        'title': title or file_key.split('/')[-1],
        'type': file_type,
        'category': category,
        'shared_at': datetime.now(timezone.utc).isoformat(),
        'likes': 0,
        'liked_by': [],
        'comments': [],
        'is_active': True
    }
    table.put_item(Item=item)
    return cors_response(200, {'success': True, 'content_id': content_id, 'message': 'Content shared'})


def get_public_content(event, user):
    resp = table.scan(
        FilterExpression='is_active = :active',
        ExpressionAttributeValues={':active': True}
    )
    items = resp.get('Items', [])
    items.sort(key=lambda x: x.get('shared_at', ''), reverse=True)
    return cors_response(200, {'success': True, 'content': items})


def unshare_content(event, user):
    body = json.loads(event.get('body', '{}'))
    content_id = body.get('content_id')
    if not content_id:
        return cors_response(400, {'success': False, 'message': 'content_id required'})

    resp = table.get_item(Key={'content_id': content_id})
    item = resp.get('Item')
    if not item:
        return cors_response(404, {'success': False, 'message': 'Content not found'})

    if item['owner_id'] != user['user_id'] and user.get('role') != 'admin':
        return cors_response(403, {'success': False, 'message': 'Permission denied'})

    table.delete_item(Key={'content_id': content_id})
    return cors_response(200, {'success': True, 'message': 'Content removed'})


def like_content(body, user):
    content_id = body.get('content_id')
    if not content_id:
        return cors_response(400, {'success': False, 'message': 'content_id required'})

    # Check if already liked
    resp = table.get_item(Key={'content_id': content_id})
    item = resp.get('Item')
    if not item:
        return cors_response(404, {'success': False, 'message': 'Content not found'})

    liked_by = item.get('liked_by', [])
    user_id = user['user_id']

    if user_id in liked_by:
        # Unlike
        liked_by.remove(user_id)
        table.update_item(
            Key={'content_id': content_id},
            UpdateExpression='SET likes = :likes, liked_by = :liked_by',
            ExpressionAttributeValues={':likes': len(liked_by), ':liked_by': liked_by}
        )
        return cors_response(200, {'success': True, 'likes': len(liked_by), 'liked': False})
    else:
        # Like
        liked_by.append(user_id)
        table.update_item(
            Key={'content_id': content_id},
            UpdateExpression='SET likes = :likes, liked_by = :liked_by',
            ExpressionAttributeValues={':likes': len(liked_by), ':liked_by': liked_by}
        )
        return cors_response(200, {'success': True, 'likes': len(liked_by), 'liked': True})


def add_comment(body, user):
    content_id = body.get('content_id')
    text = body.get('text', '').strip()

    if not content_id or not text:
        return cors_response(400, {'success': False, 'message': 'content_id and text required'})

    comment = {
        'comment_id': str(uuid.uuid4()),
        'user_id': user['user_id'],
        'user_name': user.get('email', '').split('@')[0],
        'text': text[:500],  # Limit 500 chars
        'created_at': datetime.now(timezone.utc).isoformat()
    }

    table.update_item(
        Key={'content_id': content_id},
        UpdateExpression='SET comments = list_append(if_not_exists(comments, :empty), :comment)',
        ExpressionAttributeValues={':comment': [comment], ':empty': []}
    )

    return cors_response(200, {'success': True, 'comment': comment})


def deactivate_content(body, user):
    """Admin only - deactivate content."""
    if user.get('role') != 'admin':
        return cors_response(403, {'success': False, 'message': 'Admin only'})

    content_id = body.get('content_id')
    if not content_id:
        return cors_response(400, {'success': False, 'message': 'content_id required'})

    table.update_item(
        Key={'content_id': content_id},
        UpdateExpression='SET is_active = :inactive',
        ExpressionAttributeValues={':inactive': False}
    )

    return cors_response(200, {'success': True, 'message': 'Content deactivated'})


def cors_response(status_code, body):
    return {
        'statusCode': status_code,
        'headers': {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Headers': 'Content-Type,Authorization',
            'Access-Control-Allow-Methods': 'GET,POST,DELETE,OPTIONS'
        },
        'body': json.dumps(body, default=str)
    }

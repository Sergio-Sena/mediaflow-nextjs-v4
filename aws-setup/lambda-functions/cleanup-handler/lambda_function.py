import json
import boto3
import os
from datetime import datetime, timedelta

s3 = boto3.client('s3')
UPLOADS_BUCKET = os.environ.get('UPLOADS_BUCKET', 'mediaflow-uploads-969430605054')
PROCESSED_BUCKET = os.environ.get('PROCESSED_BUCKET', 'mediaflow-processed-969430605054')

def lambda_handler(event, context):
    try:
        # Check if triggered by MediaConvert completion
        if 'source' in event and event['source'] == 'aws.mediaconvert':
            return handle_mediaconvert_completion(event)
        
        # Manual cleanup trigger
        if event.get('httpMethod') == 'POST':
            return manual_cleanup()
        
        # Scheduled cleanup (EventBridge)
        return scheduled_cleanup()
        
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'success': False, 'message': str(e)})
        }

def handle_mediaconvert_completion(event):
    """Clean original file after successful conversion"""
    try:
        detail = event.get('detail', {})
        status = detail.get('status')
        
        if status == 'COMPLETE':
            # Get original file from UserMetadata
            user_metadata = detail.get('userMetadata', {})
            original_file = user_metadata.get('OriginalFile')
            
            if original_file:
                # Delete original file from uploads bucket
                s3.delete_object(Bucket=UPLOADS_BUCKET, Key=original_file)
                print(f"Auto-deleted original file: {original_file}")
                
                return {
                    'statusCode': 200, 
                    'body': json.dumps({
                        'success': True,
                        'message': f'Auto-cleaned: {original_file}',
                        'optimization': user_metadata.get('OptimizationType', 'Standard')
                    })
                }
        elif status == 'ERROR':
            print(f"MediaConvert job failed: {detail.get('errorMessage', 'Unknown error')}")
            return {'statusCode': 200, 'body': 'Job failed - no cleanup needed'}
        
        return {'statusCode': 200, 'body': 'No cleanup needed'}
    except Exception as e:
        print(f"Cleanup error: {str(e)}")
        return {'statusCode': 500, 'body': str(e)}

def manual_cleanup():
    """Manual cleanup of old files and orphaned chunks"""
    try:
        cutoff_date = datetime.now() - timedelta(hours=1)  # 1 hour for chunks
        cleaned = []
        
        # Clean uploads bucket
        response = s3.list_objects_v2(Bucket=UPLOADS_BUCKET)
        all_files = response.get('Contents', [])
        
        # Find orphaned chunks
        chunk_files = []
        main_files = set()
        
        for obj in all_files:
            key = obj['Key']
            if '.part' in key and key.split('.part')[-1].isdigit():
                chunk_files.append(obj)
            else:
                main_files.add(key)
        
        # Remove orphaned chunks
        for chunk_obj in chunk_files:
            chunk_key = chunk_obj['Key']
            base_name = chunk_key.split('.part')[0]
            
            # Check if main file exists
            main_exists = any(base_name in main_file for main_file in main_files)
            
            if not main_exists and chunk_obj['LastModified'].replace(tzinfo=None) < cutoff_date:
                s3.delete_object(Bucket=UPLOADS_BUCKET, Key=chunk_key)
                cleaned.append(chunk_key)
        
        # Note: We don't auto-delete old files as this is a backup system
        
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': 'Content-Type,Authorization',
                'Access-Control-Allow-Methods': 'POST,OPTIONS'
            },
            'body': json.dumps({
                'success': True,
                'cleaned': cleaned,
                'count': len(cleaned)
            })
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': 'Content-Type,Authorization',
                'Access-Control-Allow-Methods': 'POST,OPTIONS'
            },
            'body': json.dumps({'success': False, 'message': str(e)})
        }

def scheduled_cleanup():
    """Scheduled cleanup via EventBridge - only orphaned chunks"""
    try:
        cutoff_date = datetime.now() - timedelta(hours=2)  # 2 hours for chunks
        cleaned_count = 0
        
        # Only clean orphaned chunks, not user files
        response = s3.list_objects_v2(Bucket=UPLOADS_BUCKET)
        all_files = response.get('Contents', [])
        
        # Find orphaned chunks only
        chunk_files = []
        main_files = set()
        
        for obj in all_files:
            key = obj['Key']
            if '.part' in key and key.split('.part')[-1].isdigit():
                chunk_files.append(obj)
            else:
                main_files.add(key)
        
        # Remove only orphaned chunks
        for chunk_obj in chunk_files:
            chunk_key = chunk_obj['Key']
            base_name = chunk_key.split('.part')[0]
            
            main_exists = any(base_name in main_file for main_file in main_files)
            
            if not main_exists and chunk_obj['LastModified'].replace(tzinfo=None) < cutoff_date:
                s3.delete_object(Bucket=UPLOADS_BUCKET, Key=chunk_key)
                cleaned_count += 1
        
        return {
            'statusCode': 200,
            'body': json.dumps({
                'success': True,
                'cleaned_count': cleaned_count,
                'timestamp': datetime.now().isoformat()
            })
        }
    except Exception as e:
        return {'statusCode': 500, 'body': str(e)}
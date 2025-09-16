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
    """Log MediaConvert completion - NO AUTO CLEANUP"""
    try:
        detail = event.get('detail', {})
        status = detail.get('status')
        
        print(f"MediaConvert event: {status}")
        print(f"Event detail: {json.dumps(detail)}")
        
        if status == 'COMPLETE':
            user_metadata = detail.get('userMetadata', {})
            original_file = user_metadata.get('OriginalFile')
            output_file = user_metadata.get('OutputFile')
            
            print(f"✅ CONVERSION COMPLETE")
            print(f"📁 Original file: {original_file}")
            print(f"🎥 Output file: {output_file}")
            print(f"💡 Manual cleanup required - both files will remain")
            
            return {
                'statusCode': 200, 
                'body': json.dumps({
                    'success': True,
                    'message': f'Conversion complete: {original_file} -> {output_file}',
                    'action': 'conversion_logged'
                })
            }
        elif status == 'ERROR':
            print(f"❌ MediaConvert job failed: {detail.get('errorMessage', 'Unknown error')}")
            return {'statusCode': 200, 'body': 'Job failed - logged'}
        
        return {'statusCode': 200, 'body': 'Event logged'}
    except Exception as e:
        print(f"Logging error: {str(e)}")
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
        
        # Clean empty folders
        empty_folders = find_empty_folders()
        for folder in empty_folders:
            # S3 doesn't have real folders, just delete the marker if exists
            try:
                s3.delete_object(Bucket=UPLOADS_BUCKET, Key=folder)
                cleaned.append(f"📁 {folder}")
            except:
                pass
        
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

def find_empty_folders():
    """Find empty folders in S3 bucket"""
    try:
        response = s3.list_objects_v2(Bucket=UPLOADS_BUCKET)
        all_objects = response.get('Contents', [])
        
        # Get all folder prefixes
        folders = set()
        for obj in all_objects:
            key = obj['Key']
            if '/' in key:
                folder = '/'.join(key.split('/')[:-1]) + '/'
                folders.add(folder)
        
        # Check which folders are empty
        empty_folders = []
        for folder in folders:
            # List objects with this prefix
            folder_response = s3.list_objects_v2(
                Bucket=UPLOADS_BUCKET,
                Prefix=folder,
                MaxKeys=1
            )
            
            # If no objects found, folder is empty
            if not folder_response.get('Contents'):
                empty_folders.append(folder)
        
        return empty_folders
    except Exception as e:
        print(f"Error finding empty folders: {e}")
        return []

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
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
        
        print(f"MediaConvert event: {status}")
        print(f"Event detail: {json.dumps(detail)}")
        
        if status == 'COMPLETE':
            # Get original file from UserMetadata
            user_metadata = detail.get('userMetadata', {})
            original_file = user_metadata.get('OriginalFile')
            output_file = user_metadata.get('OutputFile')
            
            print(f"Original file: {original_file}")
            print(f"Output file: {output_file}")
            
            if original_file and output_file:
                try:
                    # Get actual converted file name from MediaConvert output
                    output_details = detail.get('outputGroupDetails', [{}])[0]
                    actual_output_paths = output_details.get('outputDetails', [{}])[0].get('outputFilePaths', [])
                    
                    if actual_output_paths:
                        # Extract actual S3 key from full S3 path
                        actual_s3_path = actual_output_paths[0]
                        actual_output_key = actual_s3_path.replace(f's3://{UPLOADS_BUCKET}/', '')
                        
                        print(f"Actual converted file: {actual_output_key}")
                        
                        # Check if converted file exists
                        s3.head_object(Bucket=UPLOADS_BUCKET, Key=actual_output_key)
                        
                        # Generate target key (original file with .mp4 extension)
                        original_base = original_file.rsplit('.', 1)[0]  # Remove extension
                        target_key = f"{original_base}.mp4"
                        
                        print(f"Moving {actual_output_key} to {target_key}")
                        
                        # Copy converted file to original location with .mp4 extension
                        s3.copy_object(
                            Bucket=UPLOADS_BUCKET,
                            CopySource={'Bucket': UPLOADS_BUCKET, 'Key': actual_output_key},
                            Key=target_key
                        )
                        
                        # Delete original file and temp converted file
                        s3.delete_object(Bucket=UPLOADS_BUCKET, Key=original_file)
                        if actual_output_key != target_key:
                            s3.delete_object(Bucket=UPLOADS_BUCKET, Key=actual_output_key)
                        
                        print(f"SUCCESS: Replaced {original_file} with {target_key}")
                        
                        return {
                            'statusCode': 200, 
                            'body': json.dumps({
                                'success': True,
                                'message': f'Replaced {original_file} with {target_key}',
                                'action': 'file_replaced'
                            })
                        }
                    else:
                        print("ERROR: No output file paths found in MediaConvert response")
                        return {'statusCode': 500, 'body': 'No output paths found'}
                except Exception as e:
                    print(f"ERROR: Could not replace file: {str(e)}")
                    return {'statusCode': 500, 'body': f'Replacement failed: {str(e)}'}
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
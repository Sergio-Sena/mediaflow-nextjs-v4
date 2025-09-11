import json
import boto3
import os
import uuid
import time

mediaconvert = boto3.client('mediaconvert', region_name='us-east-1')
s3 = boto3.client('s3')

UPLOADS_BUCKET = os.environ.get('UPLOADS_BUCKET', 'mediaflow-uploads-969430605054')
PROCESSED_BUCKET = os.environ.get('PROCESSED_BUCKET', 'mediaflow-processed-969430605054')

def lambda_handler(event, context):
    try:
        method = event['httpMethod']
        
        if method == 'OPTIONS':
            return cors_response(200, {})
        elif method == 'POST':
            body = json.loads(event['body'])
            return start_conversion(body.get('key'))
        elif method == 'GET':
            return list_jobs()
            
    except Exception as e:
        return cors_response(500, {'success': False, 'message': str(e)})

def sanitize_filename(filename):
    """Sanitize filename for MediaConvert"""
    import re
    # Remove emojis
    emoji_pattern = re.compile("["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map
        u"\U0001F1E0-\U0001F1FF"  # flags
        u"\U00002702-\U000027B0"
        u"\U000024C2-\U0001F251"
        "]+", flags=re.UNICODE)
    sanitized = emoji_pattern.sub('', filename)
    
    # Remove special characters
    sanitized = re.sub(r'[^a-zA-Z0-9._-]', '_', sanitized)
    sanitized = re.sub(r'_+', '_', sanitized)
    sanitized = sanitized.strip('_')
    
    if not sanitized or sanitized == '.':
        sanitized = 'converted_video'
    
    return sanitized

def get_optimal_settings(file_size_mb):
    """Get optimal conversion settings"""
    if file_size_mb > 3000:
        return {
            'width': 1920, 'height': 1080, 'bitrate': 5000000,
            'name': '1080p', 'description': '4K→1080p optimization'
        }
    elif file_size_mb > 1500:
        return {
            'width': 1920, 'height': 1080, 'bitrate': 4000000,
            'name': '1080p', 'description': 'High quality→1080p optimization'
        }
    else:
        return {
            'width': 1920, 'height': 1080, 'bitrate': 3000000,
            'name': '1080p', 'description': 'Quality preservation (1080p max)'
        }

def check_and_cleanup_original(original_key, converted_key):
    """Check if conversion succeeded and cleanup original"""
    try:
        # Wait a bit for file to be fully written
        time.sleep(5)
        
        # Check if converted file exists and has reasonable size
        try:
            converted_obj = s3.head_object(Bucket=PROCESSED_BUCKET, Key=converted_key)
            converted_size = converted_obj['ContentLength']
            
            # If converted file is too small (< 1MB), don't delete original
            if converted_size < 1024 * 1024:
                print(f"Converted file too small ({converted_size} bytes), keeping original")
                return False
                
            # Get original file size for comparison
            original_obj = s3.head_object(Bucket=UPLOADS_BUCKET, Key=original_key)
            original_size = original_obj['ContentLength']
            
            # If converted is less than 10% of original, something went wrong
            if converted_size < (original_size * 0.1):
                print(f"Converted file suspiciously small, keeping original")
                return False
            
            # Conversion looks good, delete original
            s3.delete_object(Bucket=UPLOADS_BUCKET, Key=original_key)
            print(f"✅ Deleted original file: {original_key}")
            print(f"📊 Original: {original_size/1024/1024:.1f}MB → Converted: {converted_size/1024/1024:.1f}MB")
            return True
            
        except Exception as e:
            print(f"❌ Error checking converted file: {str(e)}")
            return False
            
    except Exception as e:
        print(f"❌ Error in cleanup process: {str(e)}")
        return False

def start_conversion(file_key):
    """Start MediaConvert job with auto-cleanup"""
    try:
        if not file_key:
            return cors_response(400, {'success': False, 'message': 'File key required'})
        
        # Check if file exists and get size
        try:
            obj_info = s3.head_object(Bucket=UPLOADS_BUCKET, Key=file_key)
            file_size_mb = obj_info['ContentLength'] / (1024 * 1024)
        except:
            return cors_response(404, {'success': False, 'message': 'File not found'})
        
        # Video file validation
        video_extensions = [
            '.mp4', '.avi', '.mov', '.mkv', '.webm', '.ts', '.flv', '.wmv',
            '.m4v', '.3gp', '.f4v', '.mts', '.m2ts', '.asf', '.vob', '.mpg', '.mpeg'
        ]
        if not any(file_key.lower().endswith(ext) for ext in video_extensions):
            return cors_response(400, {'success': False, 'message': 'Not a supported video file'})
        
        # Sanitize filename
        original_name = file_key.split('/')[-1]
        sanitized_name = sanitize_filename(original_name)
        optimal = get_optimal_settings(file_size_mb)
        
        # Get MediaConvert endpoint
        endpoints = mediaconvert.describe_endpoints()
        endpoint_url = endpoints['Endpoints'][0]['Url']
        mc_client = boto3.client('mediaconvert', endpoint_url=endpoint_url)
        
        # Generate job settings
        job_id = str(uuid.uuid4())
        input_uri = f"s3://{UPLOADS_BUCKET}/{file_key}"
        output_key = sanitized_name.rsplit('.', 1)[0]
        converted_key = f"{output_key}_{optimal['name']}.mp4"
        
        job_settings = {
            "Role": "arn:aws:iam::969430605054:role/MediaConvertRole",
            "Settings": {
                "Inputs": [{
                    "FileInput": input_uri,
                    "AudioSelectors": {
                        "Audio Selector 1": {
                            "DefaultSelection": "DEFAULT"
                        }
                    },
                    "VideoSelector": {}
                }],
                "OutputGroups": [{
                    "Name": "File Group",
                    "OutputGroupSettings": {
                        "Type": "FILE_GROUP_SETTINGS",
                        "FileGroupSettings": {
                            "Destination": f"s3://{PROCESSED_BUCKET}/{output_key}_"
                        }
                    },
                    "Outputs": [{
                        "NameModifier": optimal['name'],
                        "VideoDescription": {
                            "Width": optimal['width'],
                            "Height": optimal['height'],
                            "CodecSettings": {
                                "Codec": "H_264",
                                "H264Settings": {
                                    "Bitrate": optimal['bitrate'],
                                    "RateControlMode": "CBR",
                                    "CodecProfile": "HIGH",
                                    "CodecLevel": "AUTO",
                                    "SceneChangeDetect": "ENABLED"
                                }
                            }
                        },
                        "AudioDescriptions": [{
                            "CodecSettings": {
                                "Codec": "AAC",
                                "AacSettings": {
                                    "Bitrate": 128000,
                                    "SampleRate": 48000,
                                    "CodingMode": "CODING_MODE_2_0"
                                }
                            }
                        }],
                        "ContainerSettings": {
                            "Container": "MP4"
                        }
                    }]
                }]
            },
            "UserMetadata": {
                "OriginalFile": file_key,
                "ConvertedFile": converted_key,
                "JobId": job_id,
                "OptimizationType": optimal['description'],
                "OriginalSizeMB": str(int(file_size_mb)),
                "AutoCleanup": "true"
            }
        }
        
        # Submit job
        response = mc_client.create_job(**job_settings)
        
        # Schedule cleanup check (in a real scenario, you'd use EventBridge or SNS)
        # For now, we'll check after a delay
        try:
            # Wait for job to potentially complete (async)
            import threading
            cleanup_thread = threading.Thread(
                target=delayed_cleanup_check,
                args=(file_key, converted_key, response['Job']['Id'])
            )
            cleanup_thread.start()
        except:
            pass  # Cleanup will be manual if threading fails
        
        return cors_response(200, {
            'success': True,
            'jobId': response['Job']['Id'],
            'status': response['Job']['Status'],
            'message': f'Conversion started for {file_key} (auto-cleanup enabled)',
            'autoCleanup': True
        })
        
    except Exception as e:
        return cors_response(500, {'success': False, 'message': str(e)})

def delayed_cleanup_check(original_key, converted_key, job_id):
    """Check job status and cleanup after delay"""
    try:
        # Wait for job to complete (typical video conversion takes 5-15 minutes)
        max_wait = 30 * 60  # 30 minutes max
        check_interval = 60  # Check every minute
        waited = 0
        
        endpoints = mediaconvert.describe_endpoints()
        endpoint_url = endpoints['Endpoints'][0]['Url']
        mc_client = boto3.client('mediaconvert', endpoint_url=endpoint_url)
        
        while waited < max_wait:
            time.sleep(check_interval)
            waited += check_interval
            
            try:
                job_response = mc_client.get_job(Id=job_id)
                status = job_response['Job']['Status']
                
                if status == 'COMPLETE':
                    print(f"✅ Job {job_id} completed, checking cleanup...")
                    check_and_cleanup_original(original_key, converted_key)
                    break
                elif status in ['ERROR', 'CANCELED']:
                    print(f"❌ Job {job_id} failed ({status}), keeping original")
                    break
                else:
                    print(f"⏳ Job {job_id} status: {status}, waiting...")
                    
            except Exception as e:
                print(f"Error checking job status: {str(e)}")
                break
                
    except Exception as e:
        print(f"Error in delayed cleanup: {str(e)}")

def list_jobs():
    """List recent MediaConvert jobs"""
    try:
        endpoints = mediaconvert.describe_endpoints()
        endpoint_url = endpoints['Endpoints'][0]['Url']
        mc_client = boto3.client('mediaconvert', endpoint_url=endpoint_url)
        
        response = mc_client.list_jobs(MaxResults=10, Order='DESCENDING')
        
        jobs = []
        for job in response.get('Jobs', []):
            jobs.append({
                'id': job['Id'],
                'status': job['Status'],
                'createdAt': job['CreatedAt'].isoformat(),
                'progress': job.get('JobPercentComplete', 0),
                'originalFile': job.get('UserMetadata', {}).get('OriginalFile', 'Unknown'),
                'autoCleanup': job.get('UserMetadata', {}).get('AutoCleanup') == 'true'
            })
        
        return cors_response(200, {'success': True, 'jobs': jobs})
        
    except Exception as e:
        return cors_response(500, {'success': False, 'message': str(e)})

def cors_response(status_code, body):
    return {
        'statusCode': status_code,
        'headers': {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Headers': 'Content-Type,Authorization',
            'Access-Control-Allow-Methods': 'GET,POST,OPTIONS'
        },
        'body': json.dumps(body)
    }
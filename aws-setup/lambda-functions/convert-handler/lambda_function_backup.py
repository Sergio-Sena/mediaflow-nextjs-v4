import json
import boto3
import os
import uuid

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
    # Remove emojis (Unicode ranges for emojis)
    emoji_pattern = re.compile("["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map
        u"\U0001F1E0-\U0001F1FF"  # flags
        u"\U00002702-\U000027B0"
        u"\U000024C2-\U0001F251"
        "]+", flags=re.UNICODE)
    sanitized = emoji_pattern.sub('', filename)
    
    # Remove special characters, keep only alphanumeric, dots, hyphens, underscores
    sanitized = re.sub(r'[^a-zA-Z0-9._-]', '_', sanitized)
    # Remove multiple underscores
    sanitized = re.sub(r'_+', '_', sanitized)
    # Ensure it doesn't start/end with underscore
    sanitized = sanitized.strip('_')
    
    # Ensure filename is not empty
    if not sanitized or sanitized == '.':
        sanitized = 'converted_video'
    
    return sanitized

def get_optimal_settings(file_size_mb):
    """Get optimal conversion settings - only downscale if >1080p"""
    if file_size_mb > 3000:  # >3GB - likely 4K or higher
        return {
            'width': 1920, 'height': 1080, 'bitrate': 5000000,
            'name': '1080p', 'description': '4K→1080p optimization'
        }
    elif file_size_mb > 1500:  # 1.5-3GB - likely 1440p or high bitrate 1080p
        return {
            'width': 1920, 'height': 1080, 'bitrate': 4000000,
            'name': '1080p', 'description': 'High quality→1080p optimization'
        }
    else:  # ≤1.5GB - likely 1080p or lower, maintain quality
        return {
            'width': 1920, 'height': 1080, 'bitrate': 3000000,
            'name': '1080p', 'description': 'Quality preservation (1080p max)'
        }

def start_conversion(file_key):
    """Start MediaConvert job for video file"""
    try:
        if not file_key:
            return cors_response(400, {'success': False, 'message': 'File key required'})
        
        # Check if file exists and get size
        try:
            obj_info = s3.head_object(Bucket=UPLOADS_BUCKET, Key=file_key)
            file_size_mb = obj_info['ContentLength'] / (1024 * 1024)
        except:
            return cors_response(404, {'success': False, 'message': 'File not found'})
        
        # Extended video file support
        video_extensions = [
            '.mp4', '.avi', '.mov', '.mkv', '.webm', '.ts', '.flv', '.wmv',
            '.m4v', '.3gp', '.f4v', '.mts', '.m2ts', '.asf', '.vob', '.mpg', '.mpeg'
        ]
        if not any(file_key.lower().endswith(ext) for ext in video_extensions):
            return cors_response(400, {'success': False, 'message': 'Not a supported video file'})
        
        # Sanitize filename for MediaConvert
        original_name = file_key.split('/')[-1]
        sanitized_name = sanitize_filename(original_name)
        
        # Get optimal settings based on file size
        optimal = get_optimal_settings(file_size_mb)
        
        # Get MediaConvert endpoint
        endpoints = mediaconvert.describe_endpoints()
        endpoint_url = endpoints['Endpoints'][0]['Url']
        mc_client = boto3.client('mediaconvert', endpoint_url=endpoint_url)
        
        # Generate job settings with sanitized name
        job_id = str(uuid.uuid4())
        input_uri = f"s3://{UPLOADS_BUCKET}/{file_key}"
        output_key = sanitized_name.rsplit('.', 1)[0]
        
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
                    "Outputs": [
                        {
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
                        }
                    ]
                }]
            },
            "UserMetadata": {
                "OriginalFile": file_key,
                "JobId": job_id,
                "OptimizationType": optimal['description'],
                "OriginalSizeMB": str(int(file_size_mb))
            }
        }
        
        # Submit job
        response = mc_client.create_job(**job_settings)
        
        return cors_response(200, {
            'success': True,
            'jobId': response['Job']['Id'],
            'status': response['Job']['Status'],
            'message': f'Conversion started for {file_key}'
        })
        
    except Exception as e:
        return cors_response(500, {'success': False, 'message': str(e)})

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
                'originalFile': job.get('UserMetadata', {}).get('OriginalFile', 'Unknown')
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
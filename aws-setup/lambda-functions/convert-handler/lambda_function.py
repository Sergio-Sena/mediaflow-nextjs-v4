import json
import boto3
import os
import uuid
import urllib.parse

mediaconvert = boto3.client('mediaconvert', region_name='us-east-1')
s3 = boto3.client('s3')

UPLOADS_BUCKET = os.environ.get('UPLOADS_BUCKET', 'mediaflow-uploads-969430605054')
PROCESSED_BUCKET = os.environ.get('PROCESSED_BUCKET', 'mediaflow-processed-969430605054')

def lambda_handler(event, context):
    """Handle S3 events for automatic video conversion"""
    
    try:
        # Check if this is an S3 event
        if 'Records' in event:
            return handle_s3_event(event)
        else:
            # Fallback to HTTP handler for manual triggers
            return handle_http_request(event, context)
            
    except Exception as e:
        print(f"Error: {str(e)}")
        return {'statusCode': 500, 'body': json.dumps({'error': str(e)})}

def handle_s3_event(event):
    """Process S3 ObjectCreated events - DISABLED for manual conversion"""
    
    results = []
    
    for record in event['Records']:
        # Extract S3 info
        bucket = record['s3']['bucket']['name']
        key = urllib.parse.unquote_plus(record['s3']['object']['key'])
        
        print(f"S3 event received but auto-conversion disabled: {bucket}/{key}")
        results.append({'success': True, 'message': f'Auto-conversion disabled for {key}'})
    
    return {
        'statusCode': 200,
        'body': json.dumps({
            'success': True,
            'processed': len(results),
            'results': results,
            'message': 'Auto-conversion disabled - use manual conversion'
        })
    }

def handle_http_request(event, context):
    """Handle HTTP requests (manual conversion)"""
    
    try:
        method = event.get('httpMethod', 'POST')
        
        if method == 'OPTIONS':
            return cors_response(200, {})
        elif method == 'POST':
            body = json.loads(event['body'])
            return cors_response(200, start_conversion(body.get('key')))
        elif method == 'GET':
            return cors_response(200, list_jobs())
            
    except Exception as e:
        return cors_response(500, {'success': False, 'message': str(e)})

def start_conversion(file_key):
    """Start MediaConvert job for video file"""
    
    try:
        print(f"Starting conversion for: {file_key}")
        
        # Check if file exists and get size
        try:
            obj_info = s3.head_object(Bucket=UPLOADS_BUCKET, Key=file_key)
            file_size_mb = obj_info['ContentLength'] / (1024 * 1024)
            print(f"File size: {file_size_mb:.2f} MB")
        except Exception as e:
            print(f"File not found: {str(e)}")
            return {'success': False, 'message': 'File not found'}
        
        # Get MediaConvert endpoint
        endpoints = mediaconvert.describe_endpoints()
        endpoint_url = endpoints['Endpoints'][0]['Url']
        mc_client = boto3.client('mediaconvert', endpoint_url=endpoint_url)
        
        # Generate sanitized output name
        original_name = file_key.split('/')[-1]
        sanitized_name = sanitize_filename(original_name)
        output_key = sanitized_name.rsplit('.', 1)[0] + '.mp4'
        
        # Preserve folder structure
        if '/' in file_key:
            folder_path = '/'.join(file_key.split('/')[:-1])
            output_key = f"{folder_path}/{output_key}"
        
        job_id = str(uuid.uuid4())
        input_uri = f"s3://{UPLOADS_BUCKET}/{file_key}"
        output_uri = f"s3://{UPLOADS_BUCKET}/{output_key}"
        
        # Use clean destination and name
        if '/' in output_key:
            folder_path = '/'.join(output_key.split('/')[:-1])
            destination_path = f"s3://{UPLOADS_BUCKET}/{folder_path}/"
            clean_filename = output_key.split('/')[-1].replace('.mp4', '')
        else:
            destination_path = f"s3://{UPLOADS_BUCKET}/"
            clean_filename = output_key.replace('.mp4', '')
        
        # Fix: NameModifier cannot be empty, use a valid modifier
        clean_filename = "_converted"  # Valid non-empty modifier
        
        print(f"Input: {input_uri}")
        print(f"Output: {output_uri}")
        
        # Job settings for H.264 conversion
        job_settings = {
            "Role": "arn:aws:iam::969430605054:role/MediaConvertRole",
            "Settings": {
                "Inputs": [{
                    "FileInput": input_uri,
                    "AudioSelectors": {
                        "Audio Selector 1": {"DefaultSelection": "DEFAULT"}
                    },
                    "VideoSelector": {}
                }],
                "OutputGroups": [{
                    "Name": "File Group",
                    "OutputGroupSettings": {
                        "Type": "FILE_GROUP_SETTINGS",
                        "FileGroupSettings": {
                            "Destination": destination_path
                        }
                    },
                    "Outputs": [
                        # Vídeo MP4
                        {
                            "NameModifier": clean_filename,
                            "VideoDescription": {
                                "Width": 1280,
                                "Height": 720,
                                "CodecSettings": {
                                    "Codec": "H_264",
                                    "H264Settings": {
                                        "Bitrate": 2000000,
                                        "RateControlMode": "CBR",
                                        "CodecProfile": "HIGH",
                                        "CodecLevel": "AUTO"
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
                            "ContainerSettings": {"Container": "MP4"}
                        },
                        # Thumbnail JPG
                        {
                            "NameModifier": "_thumb",
                            "VideoDescription": {
                                "Width": 320,
                                "Height": 180,
                                "CodecSettings": {
                                    "Codec": "FRAME_CAPTURE",
                                    "FrameCaptureSettings": {
                                        "FramerateNumerator": 1,
                                        "FramerateDenominator": 10,
                                        "MaxCaptures": 1,
                                        "Quality": 80
                                    }
                                }
                            },
                            "ContainerSettings": {"Container": "RAW"}
                        }
                    ]
                }]
            },
            "UserMetadata": {
                "OriginalFile": file_key,
                "OutputFile": output_key,
                "JobId": job_id
            }
        }
        
        # Add metadata for auto-replacement
        job_settings['UserMetadata']['AutoReplace'] = 'true'
        job_settings['UserMetadata']['OriginalKey'] = file_key
        
        # Submit job
        response = mc_client.create_job(**job_settings)
        
        print(f"MediaConvert job created: {response['Job']['Id']}")
        
        return {
            'success': True,
            'jobId': response['Job']['Id'],
            'status': response['Job']['Status'],
            'originalFile': file_key,
            'outputFile': output_key,
            'message': f'Conversion started for {file_key} - will auto-replace when complete'
        }
        
    except Exception as e:
        print(f"Conversion error: {str(e)}")
        return {'success': False, 'message': str(e)}

def sanitize_filename(filename):
    """Sanitize filename for MediaConvert"""
    import re
    
    # Remove emojis and special characters
    sanitized = re.sub(r'[^\w\s.-]', '_', filename)
    sanitized = re.sub(r'\s+', '_', sanitized)
    sanitized = re.sub(r'_+', '_', sanitized)
    sanitized = sanitized.strip('_')
    
    if not sanitized:
        sanitized = 'converted_video'
    
    return sanitized

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
        
        return {'success': True, 'jobs': jobs}
        
    except Exception as e:
        return {'success': False, 'message': str(e)}

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
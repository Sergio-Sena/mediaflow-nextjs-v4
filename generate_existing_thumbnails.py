#!/usr/bin/env python3
import boto3
import json
import uuid

def generate_thumbnails_for_existing():
    """Gerar thumbnails para todos os vídeos existentes no S3"""
    
    s3 = boto3.client('s3')
    mediaconvert = boto3.client('mediaconvert', region_name='us-east-1')
    
    bucket = 'mediaflow-uploads-969430605054'
    
    print("GERANDO THUMBNAILS PARA VIDEOS EXISTENTES")
    print("=" * 50)
    
    try:
        # Listar todos os arquivos do bucket
        response = s3.list_objects_v2(Bucket=bucket)
        
        if 'Contents' not in response:
            print("Nenhum arquivo encontrado")
            return
        
        # Filtrar apenas vídeos
        video_extensions = ['.mp4', '.avi', '.mov', '.mkv', '.ts', '.webm']
        video_files = []
        
        for obj in response['Contents']:
            key = obj['Key']
            if any(key.lower().endswith(ext) for ext in video_extensions):
                # Verificar se já tem thumbnail
                thumb_key = key.rsplit('.', 1)[0] + '_thumb.jpg'
                
                try:
                    s3.head_object(Bucket=bucket, Key=thumb_key)
                    print(f"SKIP: {key} (thumbnail já existe)")
                except:
                    video_files.append(key)
                    print(f"QUEUE: {key}")
        
        print(f"\nEncontrados {len(video_files)} vídeos sem thumbnail")
        
        if not video_files:
            print("Todos os vídeos já têm thumbnails!")
            return
        
        # Confirmar processamento
        response = input(f"\nGerar thumbnails para {len(video_files)} vídeos? (y/N): ")
        if response.lower() != 'y':
            print("Cancelado")
            return
        
        # Get MediaConvert endpoint
        endpoints = mediaconvert.describe_endpoints()
        endpoint_url = endpoints['Endpoints'][0]['Url']
        mc_client = boto3.client('mediaconvert', endpoint_url=endpoint_url)
        
        # Processar cada vídeo
        success_count = 0
        
        for video_key in video_files:
            try:
                job_id = create_thumbnail_job(mc_client, bucket, video_key)
                if job_id:
                    print(f"✅ Job criado para {video_key}: {job_id}")
                    success_count += 1
                else:
                    print(f"❌ Falha para {video_key}")
                    
            except Exception as e:
                print(f"❌ Erro em {video_key}: {e}")
        
        print(f"\n🎯 RESULTADO:")
        print(f"✅ {success_count}/{len(video_files)} jobs criados")
        print(f"⏱️ Thumbnails estarão prontos em 5-15 minutos")
        
    except Exception as e:
        print(f"❌ Erro: {e}")

def create_thumbnail_job(mc_client, bucket, video_key):
    """Criar job MediaConvert só para thumbnail"""
    
    try:
        # Preparar paths
        input_uri = f"s3://{bucket}/{video_key}"
        
        # Output path (mesmo local do vídeo)
        if '/' in video_key:
            folder_path = '/'.join(video_key.split('/')[:-1])
            destination_path = f"s3://{bucket}/{folder_path}/"
        else:
            destination_path = f"s3://{bucket}/"
        
        # Job settings - APENAS thumbnail
        job_settings = {
            "Role": "arn:aws:iam::969430605054:role/MediaConvertRole",
            "Settings": {
                "Inputs": [{
                    "FileInput": input_uri,
                    "VideoSelector": {},
                    "TimecodeSource": "ZEROBASED"
                }],
                "OutputGroups": [{
                    "Name": "Thumbnail Group",
                    "OutputGroupSettings": {
                        "Type": "FILE_GROUP_SETTINGS",
                        "FileGroupSettings": {
                            "Destination": destination_path
                        }
                    },
                    "Outputs": [{
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
                    }]
                }]
            },
            "UserMetadata": {
                "OriginalFile": video_key,
                "JobType": "ThumbnailOnly",
                "JobId": str(uuid.uuid4())
            }
        }
        
        # Criar job
        response = mc_client.create_job(**job_settings)
        return response['Job']['Id']
        
    except Exception as e:
        print(f"Erro ao criar job: {e}")
        return None

if __name__ == "__main__":
    generate_thumbnails_for_existing()
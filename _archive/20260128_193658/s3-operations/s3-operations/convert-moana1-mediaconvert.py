import boto3
import os
import time
from tqdm import tqdm

s3 = boto3.client('s3', region_name='us-east-1')
mediaconvert = boto3.client('mediaconvert', region_name='us-east-1')

bucket = 'mediaflow-uploads-969430605054'
local_file = r'C:\Users\dell 5557\Videos\Moana.Um.Mar.de.Aventuras\Moana.Um.Mar.de.Aventuras.2017.1080p.BluRay.DD5.1.x264.DUAL-TDF.mp4'
temp_key = 'temp/moana1-original.mp4'
output_key = 'users/lid_lima/Moana/Moana.1.Um.Mar.de.Aventuras.2017.mp4'

# Upload arquivo original
print("Fazendo upload do arquivo para S3...")
file_size = os.path.getsize(local_file)
print(f"Tamanho: {file_size / (1024**3):.2f} GB")
with tqdm(total=file_size, unit='B', unit_scale=True) as pbar:
    s3.upload_file(local_file, bucket, temp_key, Callback=lambda b: pbar.update(b))

print("Upload concluido!")

# Obter endpoint MediaConvert
print("\nConfigurando MediaConvert...")
endpoints = mediaconvert.describe_endpoints()
mediaconvert_endpoint = endpoints['Endpoints'][0]['Url']
mediaconvert = boto3.client('mediaconvert', region_name='us-east-1', endpoint_url=mediaconvert_endpoint)

# Job de conversao (video copy + audio AAC)
job_settings = {
    "Role": "arn:aws:iam::969430605054:role/MediaConvertRole",
    "Settings": {
        "Inputs": [{
            "FileInput": f"s3://{bucket}/{temp_key}",
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
                    "Destination": f"s3://{bucket}/users/lid_lima/Moana/"
                }
            },
            "Outputs": [{
                "ContainerSettings": {
                    "Container": "MP4",
                    "Mp4Settings": {}
                },
                "VideoDescription": {
                    "Width": 1920,
                    "Height": 1080,
                    "CodecSettings": {
                        "Codec": "H_264",
                        "H264Settings": {
                            "MaxBitrate": 8000000,
                            "RateControlMode": "QVBR",
                            "QualityTuningLevel": "SINGLE_PASS_HQ"
                        }
                    }
                },
                "AudioDescriptions": [{
                    "CodecSettings": {
                        "Codec": "AAC",
                        "AacSettings": {
                            "Bitrate": 192000,
                            "CodingMode": "CODING_MODE_2_0",
                            "SampleRate": 48000
                        }
                    }
                }],
                "NameModifier": "-Moana.1.Um.Mar.de.Aventuras.2017"
            }]
        }]
    }
}

print("\nIniciando conversao no MediaConvert...")
response = mediaconvert.create_job(**job_settings)
job_id = response['Job']['Id']
print(f"Job ID: {job_id}")
print("Isso pode levar alguns minutos...")

# Aguardar conclusao
print("\nAguardando conversao (verificando a cada 10s)...")
while True:
    job = mediaconvert.get_job(Id=job_id)
    status = job['Job']['Status']
    progress = job['Job'].get('JobPercentComplete', 0)
    print(f"Status: {status} - Progresso: {progress}%")
    
    if status == 'COMPLETE':
        print("\n=== CONVERSAO CONCLUIDA ===")
        break
    elif status == 'ERROR':
        print(f"\n=== ERRO NA CONVERSAO ===")
        print(f"Mensagem: {job['Job'].get('ErrorMessage', 'Desconhecido')}")
        break
    
    time.sleep(10)

# Deletar arquivo temporario
print("\nLimpando arquivo temporario...")
s3.delete_object(Bucket=bucket, Key=temp_key)
print("Arquivo temporario deletado!")

# Renomear arquivo convertido
print("\nRenomeando arquivo convertido...")
converted_key = 'users/lid_lima/Moana/moana1-original-Moana.1.Um.Mar.de.Aventuras.2017.mp4'
try:
    s3.copy_object(
        Bucket=bucket,
        CopySource={'Bucket': bucket, 'Key': converted_key},
        Key=output_key
    )
    s3.delete_object(Bucket=bucket, Key=converted_key)
    print(f"Renomeado para: {output_key}")
except Exception as e:
    print(f"Aviso: {e}")

print("\n=== PROCESSO CONCLUIDO ===")
print(f"Arquivo final: s3://{bucket}/{output_key}")
print("Audio convertido para AAC (compativel com mobile)")

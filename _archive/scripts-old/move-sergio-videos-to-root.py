import boto3
from botocore.exceptions import ClientError

s3 = boto3.client('s3')
BUCKET = 'mediaflow-uploads-969430605054'
USER_PREFIX = 'users/sergio_sena/'

def list_videos_in_subfolders():
    """Lista todos os vídeos nas subpastas do sergio_sena"""
    videos = []
    
    try:
        paginator = s3.get_paginator('list_objects_v2')
        pages = paginator.paginate(Bucket=BUCKET, Prefix=USER_PREFIX)
        
        for page in pages:
            if 'Contents' in page:
                for obj in page['Contents']:
                    key = obj['Key']
                    
                    # Pular se já está na raiz
                    if key.count('/') == 2:  # users/sergio_sena/arquivo.mp4
                        continue
                    
                    # Verificar se é vídeo e está em subpasta
                    if key.count('/') > 2 and any(key.lower().endswith(ext) for ext in ['.mp4', '.avi', '.mkv', '.mov', '.wmv']):
                        filename = key.split('/')[-1]
                        subfolder = key.replace(USER_PREFIX, '').split('/')[0]
                        videos.append({
                            'current_key': key,
                            'filename': filename,
                            'subfolder': subfolder,
                            'new_key': f"{USER_PREFIX}{filename}",
                            'size_mb': round(obj['Size'] / (1024*1024), 2)
                        })
    
    except Exception as e:
        print(f"Erro ao listar: {e}")
    
    return videos

def move_video(current_key, new_key):
    """Move um vídeo para nova localização"""
    try:
        # Copiar para nova localização
        s3.copy_object(
            Bucket=BUCKET,
            CopySource={'Bucket': BUCKET, 'Key': current_key},
            Key=new_key
        )
        
        # Deletar localização antiga
        s3.delete_object(Bucket=BUCKET, Key=current_key)
        
        return True
    except Exception as e:
        print(f"Erro ao mover {current_key}: {e}")
        return False

def main():
    print("🔍 Listando vídeos nas subpastas do sergio_sena...\n")
    
    videos = list_videos_in_subfolders()
    
    if not videos:
        print("✅ Nenhum vídeo encontrado em subpastas")
        return
    
    print(f"📹 Encontrados {len(videos)} vídeos:\n")
    
    for i, video in enumerate(videos, 1):
        print(f"{i}. {video['filename']} ({video['size_mb']} MB)")
        print(f"   De: {video['subfolder']}/")
        print(f"   Para: raiz/")
        print()
    
    # Confirmar operação
    confirm = input("Mover todos os vídeos para a raiz? (s/N): ").lower()
    if confirm != 's':
        print("❌ Operação cancelada")
        return
    
    print("\n🚀 Movendo vídeos...\n")
    
    moved = 0
    failed = 0
    
    for video in videos:
        print(f"Movendo: {video['filename']}... ", end="")
        
        if move_video(video['current_key'], video['new_key']):
            print("✅ OK")
            moved += 1
        else:
            print("❌ ERRO")
            failed += 1
    
    print(f"\n📊 Resultado:")
    print(f"   Movidos: {moved}")
    print(f"   Erros: {failed}")
    print(f"   Total: {len(videos)}")

if __name__ == '__main__':
    main()
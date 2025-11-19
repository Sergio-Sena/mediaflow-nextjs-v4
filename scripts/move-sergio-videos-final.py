import boto3

s3 = boto3.client('s3')
BUCKET = 'mediaflow-uploads-969430605054'
USER_PREFIX = 'users/sergio_sena/'

def move_videos_to_root():
    print("Movendo videos das subpastas para a raiz do sergio_sena...\n")
    
    try:
        paginator = s3.get_paginator('list_objects_v2')
        pages = paginator.paginate(Bucket=BUCKET, Prefix=USER_PREFIX)
        
        videos_to_move = []
        
        for page in pages:
            if 'Contents' in page:
                for obj in page['Contents']:
                    key = obj['Key']
                    relative_path = key.replace(USER_PREFIX, '')
                    
                    # Pular se ja esta na raiz ou nao e video
                    if '/' not in relative_path:
                        continue
                    
                    filename = key.split('/')[-1]
                    if any(filename.lower().endswith(ext) for ext in ['.mp4', '.avi', '.mkv', '.mov', '.wmv']):
                        new_key = f"{USER_PREFIX}{filename}"
                        size_mb = round(obj['Size'] / (1024*1024), 2)
                        
                        videos_to_move.append({
                            'old_key': key,
                            'new_key': new_key,
                            'filename': filename,
                            'size_mb': size_mb
                        })
        
        if not videos_to_move:
            print("[OK] Nenhum video encontrado em subpastas")
            return
        
        print(f"Encontrados {len(videos_to_move)} videos para mover:\n")
        
        for i, video in enumerate(videos_to_move[:10], 1):  # Mostrar apenas os primeiros 10
            print(f"{i}. {video['filename']} ({video['size_mb']} MB)")
        
        if len(videos_to_move) > 10:
            print(f"... e mais {len(videos_to_move) - 10} videos")
        
        confirm = input(f"\nMover todos os {len(videos_to_move)} videos para a raiz? (s/N): ").lower()
        if confirm != 's':
            print("[CANCEL] Operacao cancelada")
            return
        
        print("\nMovendo videos...\n")
        
        moved = 0
        failed = 0
        
        for video in videos_to_move:
            try:
                # Copiar para nova localizacao
                s3.copy_object(
                    Bucket=BUCKET,
                    CopySource={'Bucket': BUCKET, 'Key': video['old_key']},
                    Key=video['new_key']
                )
                
                # Deletar localizacao antiga
                s3.delete_object(Bucket=BUCKET, Key=video['old_key'])
                
                print(f"[OK] {video['filename']}")
                moved += 1
                
            except Exception as e:
                print(f"[ERROR] {video['filename']}: {e}")
                failed += 1
        
        print(f"\nResultado:")
        print(f"   Movidos: {moved}")
        print(f"   Erros: {failed}")
        print(f"   Total: {len(videos_to_move)}")
        
    except Exception as e:
        print(f"Erro geral: {e}")

if __name__ == '__main__':
    move_videos_to_root()
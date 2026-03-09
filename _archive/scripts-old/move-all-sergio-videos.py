import boto3

s3 = boto3.client('s3')
BUCKET = 'mediaflow-uploads-969430605054'

def move_all_videos():
    print("Movendo todos os videos para users/sergio_sena/ (raiz)...\n")
    
    folders_to_check = [
        'users/sergio_sena/Video/Carros/',
        'users/sergio_sena/Video/Moana/',
        'users/sergio_sena/video/Lilo & Stitch/'
    ]
    
    videos_to_move = []
    
    try:
        for folder in folders_to_check:
            print(f"Verificando: {folder}")
            
            paginator = s3.get_paginator('list_objects_v2')
            pages = paginator.paginate(Bucket=BUCKET, Prefix=folder)
            
            for page in pages:
                if 'Contents' in page:
                    for obj in page['Contents']:
                        key = obj['Key']
                        filename = key.split('/')[-1]
                        
                        if filename.lower().endswith(('.mp4', '.avi', '.mkv', '.mov')):
                            new_key = f"users/sergio_sena/{filename}"
                            size_mb = round(obj['Size'] / (1024*1024), 2)
                            
                            videos_to_move.append({
                                'old_key': key,
                                'new_key': new_key,
                                'filename': filename,
                                'size_mb': size_mb,
                                'folder': folder.split('/')[-2]
                            })
        
        if not videos_to_move:
            print("[OK] Nenhum video encontrado para mover")
            return
        
        print(f"\nEncontrados {len(videos_to_move)} videos:\n")
        
        for i, video in enumerate(videos_to_move, 1):
            print(f"{i}. {video['filename']} ({video['size_mb']} MB) - de {video['folder']}/")
        
        confirm = input(f"\nMover todos os {len(videos_to_move)} videos para a raiz? (s/N): ").lower()
        if confirm != 's':
            print("[CANCEL] Operacao cancelada")
            return
        
        print("\nMovendo videos...\n")
        
        moved = 0
        failed = 0
        
        for video in videos_to_move:
            try:
                s3.copy_object(
                    Bucket=BUCKET,
                    CopySource={'Bucket': BUCKET, 'Key': video['old_key']},
                    Key=video['new_key']
                )
                
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
    move_all_videos()
import boto3

s3 = boto3.client('s3')
bucket = 'mediaflow-uploads-969430605054'

print("=" * 80)
print("MOVER PASTAS PARA RAIZ")
print("=" * 80)

folders_to_move = [
    'Folder1/',
    'Folder2/'
]

total_moved = 0
total_errors = 0

for folder in folders_to_move:
    print(f"\n[PROCESSANDO] {folder}")
    
    # Listar arquivos na pasta
    try:
        response = s3.list_objects_v2(
            Bucket=bucket, 
            Prefix=f'users/lid_lima/{folder}',
            MaxKeys=1000
        )
        
        files = response.get('Contents', [])
        print(f"  Encontrados: {len(files)} arquivos")
        
        if not files:
            print(f"  [SKIP] Pasta vazia ou nao existe")
            continue
        
        moved = 0
        errors = 0
        
        for obj in files:
            old_key = obj['Key']
            # users/lid_lima/Folder1/video.mp4 -> users/lid_lima/video.mp4
            filename = old_key.replace(f'users/lid_lima/{folder}', '').lstrip('/')
            new_key = f'users/lid_lima/{filename}'
            
            try:
                # Copiar
                s3.copy_object(
                    Bucket=bucket,
                    CopySource={'Bucket': bucket, 'Key': old_key},
                    Key=new_key
                )
                
                # Deletar original
                s3.delete_object(Bucket=bucket, Key=old_key)
                
                moved += 1
                print(f"  [OK] {filename}")
                
            except Exception as e:
                print(f"  [ERRO] {filename}: {e}")
                errors += 1
        
        print(f"  Movidos: {moved}")
        if errors > 0:
            print(f"  Erros: {errors}")
        
        total_moved += moved
        total_errors += errors
        
    except Exception as e:
        print(f"  [ERRO] {e}")

print("\n" + "=" * 80)
print("CONCLUSAO")
print("=" * 80)
print(f"Total movidos: {total_moved}")
print(f"Total erros: {total_errors}")

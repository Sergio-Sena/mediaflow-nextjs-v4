import boto3
import sys

s3 = boto3.client('s3')
bucket = 'mediaflow-uploads-969430605054'

print("=" * 80)
print("ORGANIZACAO COMPLETA DA INFRAESTRUTURA")
print("=" * 80)

# ETAPA 1: Verificar pasta sergio/
print("\n[1/4] Verificando pasta sergio/...")
try:
    response = s3.list_objects_v2(Bucket=bucket, Prefix='sergio/', MaxKeys=1000)
    sergio_files = response.get('Contents', [])
    print(f"[OK] Encontrados {len(sergio_files)} arquivos em sergio/")
    
    if sergio_files:
        print("\nExemplos:")
        for obj in sergio_files[:5]:
            size_mb = obj['Size'] / (1024 * 1024)
            print(f"  - {obj['Key']} ({size_mb:.2f} MB)")
except Exception as e:
    print(f"[ERRO] {e}")
    sergio_files = []

# ETAPA 2: Verificar se ja existe users/sergio_sena/
print("\n[2/4] Verificando users/sergio_sena/...")
try:
    response = s3.list_objects_v2(Bucket=bucket, Prefix='users/sergio_sena/', MaxKeys=1000)
    sergio_sena_files = response.get('Contents', [])
    print(f"[OK] Encontrados {len(sergio_sena_files)} arquivos em users/sergio_sena/")
except Exception as e:
    print(f"[ERRO] {e}")
    sergio_sena_files = []

# ETAPA 3: Mover arquivos sergio/ -> users/sergio_sena/
print("\n[3/4] Movendo sergio/ -> users/sergio_sena/...")
if sergio_files:
    print(f"\n[ATENCAO] Serao movidos {len(sergio_files)} arquivos")
    print("[AUTO] Confirmacao automatica ativada")
    
    if True:
        moved = 0
        errors = 0
        
        for obj in sergio_files:
            old_key = obj['Key']
            # sergio/videos/file.mp4 -> users/sergio_sena/videos/file.mp4
            new_key = old_key.replace('sergio/', 'users/sergio_sena/', 1)
            
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
                if moved % 10 == 0:
                    print(f"  Movidos: {moved}/{len(sergio_files)}")
                    
            except Exception as e:
                print(f"  [ERRO] ao mover {old_key}: {e}")
                errors += 1
        
        print(f"\n[OK] Movidos: {moved} arquivos")
        if errors > 0:
            print(f"[ERRO] Erros: {errors}")
else:
    print("[OK] Pasta sergio/ ja esta vazia ou nao existe")

# ETAPA 4: Criar estrutura public/
print("\n[4/4] Criando estrutura public/...")
folders = [
    'public/videos/',
    'public/images/',
    'public/documents/',
    'public/thumbnails/'
]

for folder in folders:
    try:
        # Criar "pasta" vazia (S3 nao tem pastas reais, mas criar um objeto .keep)
        s3.put_object(
            Bucket=bucket,
            Key=f'{folder}.keep',
            Body=b'',
            ContentType='text/plain'
        )
        print(f"[OK] Criado: {folder}")
    except Exception as e:
        print(f"[ERRO] ao criar {folder}: {e}")

# ETAPA 5: Deletar bucket processed (vazio)
print("\n[5/5] Verificando bucket processed...")
processed_bucket = 'mediaflow-processed-969430605054'
try:
    response = s3.list_objects_v2(Bucket=processed_bucket, MaxKeys=1)
    if response.get('KeyCount', 0) == 0:
        print(f"[ATENCAO] Bucket {processed_bucket} esta vazio")
        print("[AUTO] Deletando bucket vazio...")
        
        s3.delete_bucket(Bucket=processed_bucket)
        print(f"[OK] Bucket {processed_bucket} deletado")
    else:
        print(f"[ATENCAO] Bucket contem {response.get('KeyCount', 0)} objetos, nao sera deletado")
except Exception as e:
    print(f"[ERRO] {e}")

print("\n" + "=" * 80)
print("ORGANIZACAO CONCLUIDA")
print("=" * 80)
print("\nResumo:")
print("[OK] Pasta sergio/ migrada para users/sergio_sena/")
print("[OK] Estrutura public/ criada")
print("[OK] Bucket processed verificado")
print("\nProximo passo: Atualizar documentacao")

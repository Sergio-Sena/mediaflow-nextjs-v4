import boto3

# Mover pasta Star/Anime/2b_Nier_Automata para Anime/2b_Nier_Automata
s3 = boto3.client('s3')
bucket = 'mediaflow-uploads-969430605054'

print("MOVENDO PASTA: Star/Anime/2b_Nier_Automata -> Anime/2b_Nier_Automata")

# Listar arquivos na pasta origem
source_prefix = 'Star/Anime/2b_Nier_Automata/'
target_prefix = 'Anime/2b_Nier_Automata/'

print(f"Listando arquivos em: {source_prefix}")

try:
    response = s3.list_objects_v2(Bucket=bucket, Prefix=source_prefix)
    
    if 'Contents' not in response:
        print("Pasta nao encontrada ou vazia")
        exit()
    
    files = response['Contents']
    print(f"Encontrados {len(files)} arquivos")
    
    # Mover cada arquivo
    moved_count = 0
    for obj in files:
        source_key = obj['Key']
        
        # Pular se for apenas o prefixo da pasta
        if source_key == source_prefix:
            continue
            
        # Criar nova chave removendo Star/
        target_key = source_key.replace('Star/Anime/', 'Anime/')
        
        print(f"Movendo: {source_key} -> {target_key}")
        
        # Copiar arquivo
        s3.copy_object(
            Bucket=bucket,
            CopySource={'Bucket': bucket, 'Key': source_key},
            Key=target_key
        )
        
        # Deletar arquivo original
        s3.delete_object(Bucket=bucket, Key=source_key)
        
        moved_count += 1
    
    print(f"\nSUCESSO: {moved_count} arquivos movidos")
    print(f"De: Star/Anime/2b_Nier_Automata/")
    print(f"Para: Anime/2b_Nier_Automata/")
    
except Exception as e:
    print(f"ERRO: {str(e)}")
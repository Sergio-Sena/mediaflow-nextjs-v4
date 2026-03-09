import boto3

s3 = boto3.client('s3')
BUCKET = 'mediaflow-uploads-969430605054'

def rename_tilde_files():
    print("Renomeando arquivos removendo '~1'...\n")
    
    try:
        paginator = s3.get_paginator('list_objects_v2')
        pages = paginator.paginate(Bucket=BUCKET)
        
        files_to_rename = []
        
        for page in pages:
            if 'Contents' in page:
                for obj in page['Contents']:
                    key = obj['Key']
                    filename = key.split('/')[-1]
                    
                    if '~1' in filename:
                        new_filename = filename.replace('~1', '')
                        folder_path = '/'.join(key.split('/')[:-1]) + '/'
                        new_key = folder_path + new_filename
                        
                        files_to_rename.append({
                            'old_key': key,
                            'new_key': new_key,
                            'old_filename': filename,
                            'new_filename': new_filename
                        })
        
        if not files_to_rename:
            print("[OK] Nenhum arquivo com '~1' encontrado")
            return
        
        print(f"Encontrados {len(files_to_rename)} arquivos para renomear:\n")
        
        for i, file_info in enumerate(files_to_rename, 1):
            try:
                print(f"{i}. {file_info['old_filename']}")
                print(f"   -> {file_info['new_filename']}\n")
            except:
                print(f"{i}. [arquivo com caracteres especiais]\n")
        
        print(f"[AUTO] Iniciando renomeacao de {len(files_to_rename)} arquivos automaticamente...\n")
        
        print("\nRenomeando arquivos...\n")
        
        renamed = 0
        failed = 0
        
        for file_info in files_to_rename:
            try:
                print(f"Renomeando: {file_info['old_filename']}... ", end="", flush=True)
                
                # Copiar com novo nome
                s3.copy_object(
                    Bucket=BUCKET,
                    CopySource={'Bucket': BUCKET, 'Key': file_info['old_key']},
                    Key=file_info['new_key']
                )
                
                # Deletar arquivo antigo
                s3.delete_object(Bucket=BUCKET, Key=file_info['old_key'])
                
                print("OK")
                renamed += 1
                
            except Exception as e:
                print(f"ERRO: {e}")
                failed += 1
        
        print(f"\nResultado:")
        print(f"   Renomeados: {renamed}")
        print(f"   Erros: {failed}")
        print(f"   Total: {len(files_to_rename)}")
        
    except Exception as e:
        print(f"Erro: {e}")

if __name__ == '__main__':
    rename_tilde_files()
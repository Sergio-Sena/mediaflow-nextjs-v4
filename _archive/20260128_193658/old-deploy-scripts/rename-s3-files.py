import boto3
import re

S3_BUCKET = "mediaflow-uploads-969430605054"
S3_PREFIX = "users/sergio_sena/"

s3 = boto3.client('s3')

print("=" * 80)
print("RENOMEACAO AUTOMATICA - S3")
print("=" * 80)
print(f"\nBucket: {S3_BUCKET}")
print(f"Prefix: {S3_PREFIX}")
print("\nBuscando arquivos...\n")

# Listar todos os arquivos
files_to_rename = []
total_files = 0

try:
    paginator = s3.get_paginator('list_objects_v2')
    for page in paginator.paginate(Bucket=S3_BUCKET, Prefix=S3_PREFIX):
        if 'Contents' in page:
            for obj in page['Contents']:
                key = obj['Key']
                filename = key.split('/')[-1]
                total_files += 1
                
                # Verificar se precisa renomear
                needs_rename = False
                new_filename = filename
                changes = []
                
                # Remove "EPORNER.COM - "
                if "EPORNER.COM - " in new_filename:
                    new_filename = new_filename.replace("EPORNER.COM - ", "")
                    changes.append("Removido 'EPORNER.COM - '")
                    needs_rename = True
                
                # Remove códigos entre colchetes [...]
                if re.search(r'\[.*?\]', new_filename):
                    old = new_filename
                    new_filename = re.sub(r'\[.*?\]', '', new_filename)
                    changes.append("Removido [...]")
                    needs_rename = True
                
                # Remove códigos alfanuméricos no início
                match = re.match(r'^[a-zA-Z0-9]+\s+', new_filename)
                if match:
                    removed = match.group(0).strip()
                    new_filename = re.sub(r'^[a-zA-Z0-9]+\s+', '', new_filename)
                    changes.append(f"Removido codigo '{removed}'")
                    needs_rename = True
                
                # Remove espaços extras
                new_filename = re.sub(r'\s+', ' ', new_filename).strip()
                
                if needs_rename and filename != new_filename:
                    # Reconstruir key completo
                    path_parts = key.split('/')[:-1]
                    new_key = '/'.join(path_parts) + '/' + new_filename
                    
                    files_to_rename.append({
                        'old_key': key,
                        'new_key': new_key,
                        'old_name': filename,
                        'new_name': new_filename,
                        'size': obj['Size'],
                        'changes': changes
                    })

except Exception as e:
    print(f"ERRO ao listar S3: {e}")
    exit(1)

print("=" * 80)
print("PLANO DE RENOMEACAO")
print("=" * 80)

print(f"\nTotal de arquivos: {total_files}")
print(f"Arquivos para renomear: {len(files_to_rename)}")

if not files_to_rename:
    print("\nNenhum arquivo precisa ser renomeado!")
    exit(0)

# Mostrar todos os arquivos que serão renomeados
print("\n" + "-" * 80)
print("LISTA COMPLETA DE RENOMEACOES:")
print("-" * 80)

for i, item in enumerate(files_to_rename, 1):
    print(f"\n[{i}/{len(files_to_rename)}]")
    print(f"  DE:   {item['old_name'].encode('ascii', 'ignore').decode()}")
    print(f"  PARA: {item['new_name'].encode('ascii', 'ignore').decode()}")
    print(f"  Mudancas: {', '.join(item['changes'])}")
    print(f"  Tamanho: {item['size'] / (1024**2):.2f} MB")
    print(f"  Path: {item['old_key']}")

# Resumo de custo
COPY_COST = len(files_to_rename) * 0.0004 / 1000
print("\n" + "=" * 80)
print("RESUMO")
print("=" * 80)
print(f"\nArquivos: {len(files_to_rename)}")
print(f"Operacoes: {len(files_to_rename) * 2} (COPY + DELETE)")
print(f"Custo: ${COPY_COST:.6f} USD (~R$ {COPY_COST * 6:.4f} BRL)")
print(f"Tempo estimado: {len(files_to_rename) * 1.5 / 60:.1f} minutos")

# Confirmação
print("\n" + "=" * 80)
print("ATENCAO: Revise a lista acima antes de continuar!")
print("=" * 80)

resposta = input("\nDeseja executar a renomeacao? (sim/nao): ").strip().lower()

if resposta != 'sim':
    print("\nOperacao cancelada pelo usuario")
    exit(0)

# Executar renomeação
print("\n" + "=" * 80)
print("EXECUTANDO RENOMEACAO")
print("=" * 80)

success = 0
errors = 0

for i, item in enumerate(files_to_rename, 1):
    print(f"\n[{i}/{len(files_to_rename)}] {item['old_name'].encode('ascii', 'ignore').decode()}")
    
    try:
        # COPY para novo nome
        s3.copy_object(
            Bucket=S3_BUCKET,
            CopySource={'Bucket': S3_BUCKET, 'Key': item['old_key']},
            Key=item['new_key']
        )
        
        # DELETE arquivo antigo
        s3.delete_object(
            Bucket=S3_BUCKET,
            Key=item['old_key']
        )
        
        print(f"  OK -> {item['new_name'].encode('ascii', 'ignore').decode()}")
        success += 1
        
    except Exception as e:
        print(f"  ERRO: {e}")
        errors += 1

print("\n" + "=" * 80)
print("RENOMEACAO CONCLUIDA")
print("=" * 80)
print(f"\nSucesso: {success}")
print(f"Erros: {errors}")
print(f"Total: {len(files_to_rename)}")
print("\n" + "=" * 80)

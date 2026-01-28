import boto3
import re

S3_BUCKET = "mediaflow-uploads-969430605054"
S3_PREFIX = "users/sergio_sena/"

s3 = boto3.client('s3')

print("=" * 80)
print("ANÁLISE DE RENOMEAÇÃO - S3")
print("=" * 80)
print(f"\nBucket: {S3_BUCKET}")
print(f"Prefix: {S3_PREFIX}")
print("\nBuscando arquivos...\n")

# Listar todos os arquivos
files_to_rename = []
total_files = 0
total_size = 0

try:
    paginator = s3.get_paginator('list_objects_v2')
    for page in paginator.paginate(Bucket=S3_BUCKET, Prefix=S3_PREFIX):
        if 'Contents' in page:
            for obj in page['Contents']:
                key = obj['Key']
                filename = key.split('/')[-1]
                total_files += 1
                total_size += obj['Size']
                
                # Verificar se precisa renomear
                needs_rename = False
                new_filename = filename
                
                # Remove "EPORNER.COM - "
                if "EPORNER.COM - " in new_filename:
                    new_filename = new_filename.replace("EPORNER.COM - ", "")
                    needs_rename = True
                
                # Remove códigos entre colchetes [...]
                if re.search(r'\[.*?\]', new_filename):
                    new_filename = re.sub(r'\[.*?\]', '', new_filename)
                    needs_rename = True
                
                # Remove códigos alfanuméricos no início
                match = re.match(r'^[a-zA-Z0-9]+\s+', new_filename)
                if match:
                    new_filename = re.sub(r'^[a-zA-Z0-9]+\s+', '', new_filename)
                    needs_rename = True
                
                # Remove espaços extras
                new_filename = re.sub(r'\s+', ' ', new_filename).strip()
                
                if needs_rename and filename != new_filename:
                    files_to_rename.append({
                        'old_key': key,
                        'old_name': filename,
                        'new_name': new_filename,
                        'size': obj['Size']
                    })

except Exception as e:
    print(f"ERRO ao listar S3: {e}")
    exit(1)

print("=" * 80)
print("RESULTADO DA ANÁLISE")
print("=" * 80)

print(f"\nTotal de arquivos analisados: {total_files}")
print(f"Tamanho total: {total_size / (1024**3):.2f} GB")
print(f"\nArquivos que precisam renomear: {len(files_to_rename)}")

if files_to_rename:
    print("\n" + "-" * 80)
    print("EXEMPLOS DE RENOMEAÇÃO (primeiros 10):")
    print("-" * 80)
    
    for i, item in enumerate(files_to_rename[:10], 1):
        print(f"\n[{i}]")
        print(f"  DE:   {item['old_name'].encode('ascii', 'ignore').decode()}")
        print(f"  PARA: {item['new_name'].encode('ascii', 'ignore').decode()}")
        print(f"  Tamanho: {item['size'] / (1024**2):.2f} MB")

# Cálculo de custo
print("\n" + "=" * 80)
print("ESTIMATIVA DE CUSTO AWS S3")
print("=" * 80)

# Preços AWS S3 us-east-1 (Janeiro 2025)
COPY_REQUEST_COST = 0.0004 / 1000  # $0.0004 por 1000 requests (PUT/COPY)
DELETE_REQUEST_COST = 0.0  # DELETE é gratuito
GET_REQUEST_COST = 0.0004 / 1000  # $0.0004 por 1000 requests (GET)

# Para renomear no S3: COPY (novo) + DELETE (antigo)
total_operations = len(files_to_rename) * 2  # COPY + DELETE
copy_operations = len(files_to_rename)
delete_operations = len(files_to_rename)

copy_cost = copy_operations * COPY_REQUEST_COST
delete_cost = delete_operations * DELETE_REQUEST_COST
total_cost = copy_cost + delete_cost

print(f"\nOperações necessárias:")
print(f"  - COPY (criar novo): {copy_operations} operações")
print(f"  - DELETE (remover antigo): {delete_operations} operações")
print(f"  - Total: {total_operations} operações")

print(f"\nCusto estimado:")
print(f"  - COPY requests: ${copy_cost:.6f}")
print(f"  - DELETE requests: ${delete_cost:.6f} (gratuito)")
print(f"  - TOTAL: ${total_cost:.6f}")

print(f"\nCusto em Reais (cotação R$ 6,00):")
print(f"  - TOTAL: R$ {total_cost * 6:.4f}")

print("\n" + "=" * 80)
print("OBSERVAÇÕES")
print("=" * 80)
print("""
1. Custo muito baixo (centavos) devido ao pequeno número de operações
2. DELETE é gratuito no S3
3. Não há custo de transferência (dados permanecem no S3)
4. Tempo estimado: ~1-2 segundos por arquivo
5. Operação reversível (pode fazer backup antes)
""")

print("\n" + "=" * 80)
if files_to_rename:
    print(f"RESUMO: {len(files_to_rename)} arquivos | ${total_cost:.6f} USD | R$ {total_cost * 6:.4f} BRL")
else:
    print("RESUMO: Nenhum arquivo precisa ser renomeado!")
print("=" * 80)

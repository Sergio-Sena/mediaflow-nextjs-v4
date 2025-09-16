#!/usr/bin/env python3
import boto3
import json

def check_ts_files():
    s3 = boto3.client('s3')
    bucket = 'mediaflow-uploads-969430605054'
    
    print("ANALISE DE ARQUIVOS .TS")
    print("=" * 40)
    
    try:
        response = s3.list_objects_v2(Bucket=bucket)
        
        ts_files = []
        total_size = 0
        
        if 'Contents' in response:
            for obj in response['Contents']:
                key = obj['Key']
                if key.endswith('.ts') and not key.endswith('/'):
                    size_mb = obj['Size'] / (1024 * 1024)
                    ts_files.append({
                        'key': key,
                        'size_mb': size_mb,
                        'modified': obj['LastModified']
                    })
                    total_size += size_mb
        
        print(f"ARQUIVOS .TS ENCONTRADOS: {len(ts_files)}")
        print(f"TAMANHO TOTAL: {total_size:.1f} MB")
        print("-" * 40)
        
        # Mostrar alguns exemplos
        for i, file in enumerate(ts_files[:5]):
            print(f"{i+1}. {file['key']} ({file['size_mb']:.1f}MB)")
        
        if len(ts_files) > 5:
            print(f"... e mais {len(ts_files) - 5} arquivo(s)")
        
        # Verificar se há MP4 correspondentes
        print("\nVERIFICACAO DE CONVERSOES:")
        converted_count = 0
        
        for ts_file in ts_files[:3]:  # Verificar apenas os primeiros 3
            ts_key = ts_file['key']
            mp4_key = ts_key.replace('.ts', '.mp4')
            
            try:
                s3.head_object(Bucket=bucket, Key=mp4_key)
                print(f"  {ts_key} -> JA CONVERTIDO")
                converted_count += 1
            except:
                print(f"  {ts_key} -> NAO CONVERTIDO")
        
        print(f"\nRESUMO:")
        print(f"  Total .TS: {len(ts_files)}")
        print(f"  Convertidos: {converted_count} (amostra)")
        print(f"  Tamanho total: {total_size:.1f} MB")
        
        return ts_files
        
    except Exception as e:
        print(f"Erro: {e}")
        return []

if __name__ == "__main__":
    check_ts_files()
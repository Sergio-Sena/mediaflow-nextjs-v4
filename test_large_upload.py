#!/usr/bin/env python3
import os

def check_large_files():
    print("ARQUIVOS > 100MB PARA TESTE")
    print("=" * 40)
    
    # Verificar pasta teste
    teste_path = "teste"
    mb_100 = 100 * 1024 * 1024
    
    for file in os.listdir(teste_path):
        file_path = os.path.join(teste_path, file)
        if os.path.isfile(file_path):
            size = os.path.getsize(file_path)
            size_mb = size / (1024 * 1024)
            
            if size > mb_100:
                print(f"GRANDE: {file}")
                print(f"   Tamanho: {size_mb:.1f} MB")
                print(f"   Deve usar: LargeFileUpload")
            else:
                print(f"PEQUENO: {file}")
                print(f"   Tamanho: {size_mb:.1f} MB") 
                print(f"   Deve usar: SmallFileUpload")
            print()

if __name__ == "__main__":
    check_large_files()
import os
import re

FOLDER = r"C:\Users\dell 5557\Videos\IDM\Star\Kate Kuray"

print("=" * 50)
print("RENOMEANDO ARQUIVOS")
print("=" * 50)
print(f"\nPasta: {FOLDER}\n")
print("Removendo:")
print('- "EPORNER.COM - "')
print('- "[...]" (colchetes e conteúdo)\n')

count = 0

for filename in os.listdir(FOLDER):
    original = filename
    novo = filename
    
    # Remove "EPORNER.COM - "
    novo = novo.replace("EPORNER.COM - ", "")
    
    # Remove tudo entre colchetes incluindo os colchetes
    novo = re.sub(r'\[.*?\]', '', novo)
    
    # Remove espaços duplos
    novo = re.sub(r'\s+', ' ', novo)
    
    # Remove espaços no início e fim
    novo = novo.strip()
    
    if original != novo:
        print(f"[{count}] Renomeando:")
        print(f"    DE: {original}")
        print(f"    PARA: {novo}")
        
        original_path = os.path.join(FOLDER, original)
        novo_path = os.path.join(FOLDER, novo)
        
        try:
            os.rename(original_path, novo_path)
            count += 1
            print("    ✅ OK\n")
        except Exception as e:
            print(f"    ❌ ERRO: {e}\n")

print("=" * 50)
print(f"CONCLUÍDO: {count} arquivos renomeados")
print("=" * 50)

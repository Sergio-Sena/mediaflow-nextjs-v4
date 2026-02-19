import os
import re

FOLDER = r"C:\Users\dell 5557\Videos\IDM\Star\Kate Kuray"

print("=" * 50)
print("REMOVENDO CÓDIGOS DOS ARQUIVOS")
print("=" * 50)

count = 0

for filename in os.listdir(FOLDER):
    original = filename
    
    # Remove códigos alfanuméricos no início (ex: 8zoDtJiJljb, DJ2GVkQEs1t)
    novo = re.sub(r'^[a-zA-Z0-9]+\s+', '', filename)
    
    # Remove "EPORNER.COM - " se ainda existir
    novo = novo.replace("EPORNER.COM - ", "")
    
    # Remove espaços extras
    novo = re.sub(r'\s+', ' ', novo).strip()
    
    if original != novo:
        print(f"\n[{count}]")
        print(f"DE:   {original}")
        print(f"PARA: {novo}")
        
        try:
            os.rename(
                os.path.join(FOLDER, original),
                os.path.join(FOLDER, novo)
            )
            count += 1
            print("[OK]")
        except Exception as e:
            print(f"[ERRO]: {e}")

print("\n" + "=" * 50)
print(f"CONCLUÍDO: {count} arquivos renomeados")
print("=" * 50)

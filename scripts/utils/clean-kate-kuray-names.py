import os
import re

FOLDER = r"C:\Users\dell 5557\Videos\IDM\Star\Kate Kuray"

print("=" * 80)
print("LIMPANDO NOMES DE ARQUIVOS")
print("=" * 80)

count = 0

for filename in os.listdir(FOLDER):
    if not filename.endswith('.mp4'):
        continue
    
    original = filename
    
    # Remove "EPORNER.COM - "
    novo = original.replace("EPORNER.COM - ", "")
    
    # Remove códigos alfanuméricos entre colchetes [abc123]
    novo = re.sub(r'\[[\w]+\]\s*', '', novo)
    
    # Remove espaços extras
    novo = re.sub(r'\s+', ' ', novo).strip()
    
    if original != novo:
        print(f"\n[{count + 1}]")
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

print("\n" + "=" * 80)
print(f"CONCLUIDO: {count} arquivos renomeados")
print("=" * 80)

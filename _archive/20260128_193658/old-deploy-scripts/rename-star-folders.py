import os
import re

BASE_FOLDER = r"C:\Users\dell 5557\Videos\IDM\Star"
FOLDERS = ["Kate Kuray", "Little Angel"]

print("=" * 80)
print("RENOMEACAO - PASTAS STAR")
print("=" * 80)

total_renamed = 0

for folder_name in FOLDERS:
    folder_path = os.path.join(BASE_FOLDER, folder_name)
    
    if not os.path.exists(folder_path):
        print(f"\n[AVISO] Pasta nao encontrada: {folder_name}")
        continue
    
    print(f"\n{'=' * 80}")
    print(f"PASTA: {folder_name}")
    print("=" * 80)
    
    files = os.listdir(folder_path)
    renamed_count = 0
    
    for filename in files:
        original = filename
        novo = filename
        
        # Remove "EPORNER.COM - "
        novo = novo.replace("EPORNER.COM - ", "")
        
        # Remove codigos entre colchetes [...]
        novo = re.sub(r'\[.*?\]', '', novo)
        
        # Remove espacos extras
        novo = re.sub(r'\s+', ' ', novo).strip()
        
        if original != novo:
            print(f"\n[{renamed_count}]")
            print(f"  DE:   {original}")
            print(f"  PARA: {novo}")
            
            try:
                os.rename(
                    os.path.join(folder_path, original),
                    os.path.join(folder_path, novo)
                )
                print("  [OK]")
                renamed_count += 1
                total_renamed += 1
            except Exception as e:
                print(f"  [ERRO]: {e}")
    
    print(f"\nPasta '{folder_name}': {renamed_count} arquivos renomeados")

print("\n" + "=" * 80)
print(f"TOTAL: {total_renamed} arquivos renomeados em {len(FOLDERS)} pastas")
print("=" * 80)

#!/usr/bin/env python3
import os
import hashlib
from collections import defaultdict

local_dir = r'C:\Users\dell 5557\Videos\IDM\Corporativo\Comatozze'

print("=" * 60)
print("VERIFICANDO PASTA COMATOZZE LOCAL")
print("=" * 60)

# 1. Verificar duplicados por hash
print("\n1. Verificando duplicados...")
file_hashes = defaultdict(list)

for filename in os.listdir(local_dir):
    filepath = os.path.join(local_dir, filename)
    if os.path.isfile(filepath):
        # Hash do arquivo
        with open(filepath, 'rb') as f:
            file_hash = hashlib.md5(f.read()).hexdigest()
        file_hashes[file_hash].append(filename)

duplicates = {h: files for h, files in file_hashes.items() if len(files) > 1}

if duplicates:
    print(f"   Encontrados {len(duplicates)} grupos de duplicados:")
    for hash_val, files in duplicates.items():
        print(f"\n   Duplicados ({len(files)} arquivos):")
        for f in files:
            size_mb = os.path.getsize(os.path.join(local_dir, f)) / (1024**2)
            print(f"     - {f} ({size_mb:.1f} MB)")
else:
    print("   Nenhum duplicado encontrado")

# 2. Verificar sanitização
print("\n2. Verificando nomes...")
needs_sanitize = []

for filename in os.listdir(local_dir):
    has_special = any(c in filename for c in ['á', 'é', 'í', 'ó', 'ú', 'ã', 'õ', 'ç'])
    too_long = len(filename) > 100
    double_space = '  ' in filename
    
    if has_special or too_long or double_space:
        issues = []
        if has_special: issues.append('ACENTOS')
        if too_long: issues.append(f'LONGO({len(filename)})')
        if double_space: issues.append('ESPACOS')
        
        needs_sanitize.append((filename, issues))

print(f"   Total: {len(os.listdir(local_dir))} arquivos")
print(f"   Precisam sanitizar: {len(needs_sanitize)}")

if needs_sanitize:
    print("\n   Arquivos com problemas:")
    for filename, issues in needs_sanitize:
        issues_str = ', '.join(issues)
        print(f"     [{issues_str}] {filename[:70]}")

print("\n" + "=" * 60)

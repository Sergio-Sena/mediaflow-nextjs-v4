#!/usr/bin/env python3
import os
import hashlib
import unicodedata
import re
from collections import defaultdict

local_dir = r'C:\Users\dell 5557\Videos\IDM\Star\Comatozze'

def sanitize_filename(filename):
    nfkd = unicodedata.normalize('NFKD', filename)
    filename = ''.join([c for c in nfkd if not unicodedata.combining(c)])
    filename = re.sub(r'\s+', ' ', filename)
    
    name, ext = filename.rsplit('.', 1) if '.' in filename else (filename, '')
    if len(name) > 95:
        name = name[:95]
    
    return f"{name}.{ext}" if ext else name

print("=" * 60)
print("CORRIGINDO PASTA COMATOZZE")
print("=" * 60)

# 1. Deletar duplicados
print("\n1. Deletando duplicados...")
file_hashes = defaultdict(list)

for filename in os.listdir(local_dir):
    filepath = os.path.join(local_dir, filename)
    if os.path.isfile(filepath):
        with open(filepath, 'rb') as f:
            file_hash = hashlib.md5(f.read()).hexdigest()
        file_hashes[file_hash].append(filename)

deleted = 0
for hash_val, files in file_hashes.items():
    if len(files) > 1:
        # Manter o primeiro, deletar os outros
        for filename in files[1:]:
            filepath = os.path.join(local_dir, filename)
            print(f"   Deletando: {filename}")
            os.remove(filepath)
            deleted += 1

print(f"   {deleted} duplicados deletados")

# 2. Sanitizar nomes
print("\n2. Sanitizando nomes...")
renamed = 0

for filename in os.listdir(local_dir):
    new_filename = sanitize_filename(filename)
    
    if new_filename != filename:
        old_path = os.path.join(local_dir, filename)
        new_path = os.path.join(local_dir, new_filename)
        
        print(f"   {filename[:60]}")
        print(f"   -> {new_filename[:60]}")
        
        os.rename(old_path, new_path)
        renamed += 1

print(f"   {renamed} arquivos renomeados")

print("\n" + "=" * 60)
print(f"Concluido! {deleted} deletados, {renamed} renomeados")

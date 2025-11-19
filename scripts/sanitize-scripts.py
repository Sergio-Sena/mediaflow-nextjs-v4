#!/usr/bin/env python3
"""
Script para sanitizar referências inadequadas nos scripts
"""

import os
import re
from pathlib import Path

# Mapeamento de substituições
REPLACEMENTS = {
    'Star': 'Corporativo',
    'star': 'corporativo', 
    'NSFW': 'Conteudo',
    'nsfw': 'conteudo',
    'anastangel': 'usuario1',
    'jiggly': 'usuario2',
    'pornhub': 'exemplo',
    'Pornhub': 'Exemplo'
}

def sanitize_file(file_path):
    """Sanitiza um arquivo específico"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Aplicar substituições
        for old, new in REPLACEMENTS.items():
            content = content.replace(old, new)
        
        # Se houve mudanças, salvar
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"[OK] Sanitizado: {file_path}")
            return True
        else:
            print(f"[SKIP] Sem mudancas: {file_path}")
            return False
            
    except Exception as e:
        print(f"[ERROR] Erro em {file_path}: {e}")
        return False

def main():
    scripts_dir = Path(__file__).parent
    
    print("Sanitizando scripts...\n")
    
    sanitized = 0
    total = 0
    
    # Sanitizar todos os arquivos .py e .js
    for ext in ['*.py', '*.js', '*.md']:
        for file_path in scripts_dir.rglob(ext):
            if file_path.name != 'sanitize-scripts.py':  # Não sanitizar a si mesmo
                total += 1
                if sanitize_file(file_path):
                    sanitized += 1
    
    print(f"\nResultado:")
    print(f"   Total: {total} arquivos")
    print(f"   Sanitizados: {sanitized} arquivos")
    print(f"   Sem mudanças: {total - sanitized} arquivos")

if __name__ == '__main__':
    main()
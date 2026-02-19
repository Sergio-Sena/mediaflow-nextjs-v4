#!/usr/bin/env python3
"""
Script para organizar automaticamente o projeto Mídiaflow
"""

import os
import shutil
from pathlib import Path

# Mapeamento de arquivos para destinos
MAPPINGS = {
    'scripts/aws/monitoring/': [
        'get-lambda-errors.py',
        'get-multipart-errors.py',
        'monitor-upload-live.py',
    ],
    'scripts/utils/': [
        'move_files.py',
        'organize-for-performance.py',
        'organize-now.py',
        'organize-project-v2.py',
        'sanitize-and-clean.py',
        'remove-codes.py',
    ],
    'scripts/media/upload/': [
        'upload_and_rename.py',
    ],
    'docs/deploy/': [
        'DEPLOY_FINAL.md',
        'DEPLOY_SUMMARY.md',
        'MANUAL_DEPLOY_SUCCESS.md',
        'PRE_DEPLOY_CHECKLIST.md',
        'ROLLBACK_GUIDE.md',
    ],
    'docs/maintenance/': [
        'SANITIZACAO_COMPLETA.md',
        'COMMIT_SUMMARY.md',
    ],
    '_archive/old-configs/': [
        'dashboard-s3.html',
        'test-payload.json',
        'test-token.js',
        'backup-view-handler-config.json',
        'dist-config.json',
        'dist-config-updated.json',
        'dist-old-config.json',
        'dist-old-disable.json',
        'cloudfront-list.json',
    ],
}

def organize():
    root = Path.cwd()
    moved = 0
    not_found = 0
    
    print("Organizando projeto Midiaflow...\n")
    
    for dest_dir, files in MAPPINGS.items():
        dest_path = root / dest_dir
        dest_path.mkdir(parents=True, exist_ok=True)
        
        for file in files:
            src = root / file
            if src.exists():
                dst = dest_path / file
                print(f"OK {file} -> {dest_dir}")
                shutil.move(str(src), str(dst))
                moved += 1
            else:
                print(f"AVISO: {file} (nao encontrado)")
                not_found += 1
    
    print(f"\nResumo:")
    print(f"   Movidos: {moved}")
    print(f"   Nao encontrados: {not_found}")
    print("\nOrganizacao concluida!")

if __name__ == '__main__':
    organize()

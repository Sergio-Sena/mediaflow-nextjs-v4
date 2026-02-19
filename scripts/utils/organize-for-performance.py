#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de Organização para Melhorar Performance do Amazon Q
Move arquivos obsoletos para _archive/ mantendo apenas essenciais
"""

import os
import sys
import shutil
from pathlib import Path
from datetime import datetime

# Fix encoding for Windows
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

# Diretório raiz do projeto
ROOT = Path(__file__).parent

# Criar pasta de arquivo
ARCHIVE = ROOT / "_archive"
ARCHIVE_DATE = ARCHIVE / datetime.now().strftime("%Y%m%d_%H%M%S")

def create_archive_structure():
    """Cria estrutura de arquivo"""
    folders = [
        ARCHIVE_DATE / "backups",
        ARCHIVE_DATE / "migration-scripts",
        ARCHIVE_DATE / "s3-operations",
        ARCHIVE_DATE / "old-deploy-scripts",
        ARCHIVE_DATE / "old-sessions",
        ARCHIVE_DATE / "old-tests"
    ]
    for folder in folders:
        folder.mkdir(parents=True, exist_ok=True)
    print(f"OK - Estrutura criada em: {ARCHIVE_DATE}")

def move_folder(source, destination):
    """Move pasta com segurança"""
    if source.exists():
        try:
            shutil.move(str(source), str(destination))
            print(f"  OK - Movido: {source.name}")
            return True
        except Exception as e:
            print(f"  ERRO ao mover {source.name}: {e}")
            return False
    return False

def organize_project():
    """Organiza projeto movendo arquivos obsoletos"""
    
    print("\nINICIANDO ORGANIZACAO...\n")
    
    create_archive_structure()
    
    # 1. Mover backups
    print("\n[1/6] Movendo backups...")
    backup_folders = [
        ROOT / "backup",
        ROOT / "backup-lambdas-v4.8.2",
        ROOT / "backup-v4.9.1-20262201-111214"
    ]
    for folder in backup_folders:
        move_folder(folder, ARCHIVE_DATE / "backups")
    
    # 2. Mover scripts de migração
    print("\n[2/6] Movendo scripts de migracao...")
    migration = ROOT / "scripts" / "migration"
    if migration.exists():
        move_folder(migration, ARCHIVE_DATE / "migration-scripts")
    
    # 3. Mover operações S3
    print("\n[3/6] Movendo scripts S3...")
    s3_ops = ROOT / "scripts" / "s3-operations"
    if s3_ops.exists():
        move_folder(s3_ops, ARCHIVE_DATE / "s3-operations")
    
    # 4. Mover scripts de teste antigos
    print("\n[4/6] Movendo testes antigos...")
    testing = ROOT / "scripts" / "testing"
    if testing.exists():
        move_folder(testing, ARCHIVE_DATE / "old-tests")
    
    # 5. Mover scripts de deploy antigos da raiz
    print("\n[5/6] Movendo deploy scripts antigos...")
    deploy_patterns = [
        "deploy-*.py",
        "fix-*.py",
        "test-*.py",
        "check-*.py",
        "upload-*.py",
        "*.bat"
    ]
    
    moved_count = 0
    for pattern in deploy_patterns:
        for file in ROOT.glob(pattern):
            if file.is_file():
                try:
                    shutil.move(str(file), str(ARCHIVE_DATE / "old-deploy-scripts" / file.name))
                    moved_count += 1
                except Exception as e:
                    print(f"  ERRO: {file.name}: {e}")
    
    print(f"  OK - Movidos {moved_count} arquivos")
    
    # 6. Organizar memoria/
    print("\n[6/6] Organizando documentacao...")
    memoria = ROOT / "memoria"
    if memoria.exists():
        # Criar estrutura
        (memoria / "ATUAL").mkdir(exist_ok=True)
        (memoria / "HISTORICO").mkdir(exist_ok=True)
        
        # Arquivos a manter na raiz
        keep_in_root = [
            "README.md",
            "HISTORICO_COMPLETO.md",
            "V4.9_SUMMARY.md",
            "DIAGNOSTICO_PERFORMANCE_AMAZON_Q.md"
        ]
        
        # Mover sessões antigas para HISTORICO
        for file in memoria.glob("SESSAO_*.md"):
            try:
                shutil.move(str(file), str(memoria / "HISTORICO" / file.name))
            except:
                pass
        
        print("  OK - Documentacao organizada")
    
    print("\nORGANIZACAO CONCLUIDA!\n")
    print(f"Arquivos arquivados em: {ARCHIVE_DATE}")
    print("\nPROXIMOS PASSOS:")
    print("  1. Testar se o projeto ainda funciona")
    print("  2. Verificar performance do Amazon Q")
    print("  3. Se tudo OK, pode deletar _archive/ depois de 1 semana")

def show_summary():
    """Mostra resumo do que será feito"""
    print("\n" + "="*60)
    print("ORGANIZACAO PARA PERFORMANCE DO AMAZON Q")
    print("="*60)
    print("\nO que sera feito:")
    print("  - Mover backups para _archive/")
    print("  - Mover scripts de migracao")
    print("  - Mover scripts S3")
    print("  - Mover scripts de teste")
    print("  - Mover deploy scripts antigos")
    print("  - Organizar documentacao")
    print("\nO que sera mantido:")
    print("  - app/ (frontend)")
    print("  - components/")
    print("  - lib/")
    print("  - aws-setup/lambda-functions/")
    print("  - Documentacao essencial")
    print("\nAVISO: NADA sera deletado, apenas movido para _archive/")
    print("="*60 + "\n")

if __name__ == "__main__":
    show_summary()
    
    response = input("Deseja continuar? (s/n): ").lower()
    if response == 's':
        organize_project()
    else:
        print("\nOperacao cancelada")

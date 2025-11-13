import os

import os
import shutil

# Estrutura de organização
MOVES = {
    # Backups -> backup/
    'backup_20251111_210237.json': 'backup/',
    'backup_migration_20251111_171603.json': 'backup/',
    'backup_migration_20251111_171716.json': 'backup/',
    'backup_migration_20251111_172913.json': 'backup/',
    'backup_migration_20251111_183827.json': 'backup/',
    
    # Scripts de migração -> scripts/migration/
    'check_admin.py': 'scripts/migration/',
    'check_credentials.py': 'scripts/migration/',
    'check_migration_status.py': 'scripts/migration/',
    'check_users_prefix.py': 'scripts/migration/',
    'confirm_and_delete.py': 'scripts/migration/',
    'continue_migration.py': 'scripts/migration/',
    'count_all_files.py': 'scripts/migration/',
    'fix_2fa_fields.py': 'scripts/migration/',
    'fix_admin_prefix.py': 'scripts/migration/',
    'fix_api_gateway_cors.py': 'scripts/migration/',
    'fix_migration.py': 'scripts/migration/',
    'fix_s3_prefix.py': 'scripts/migration/',
    'migrate_admin_to_sergio.py': 'scripts/migration/',
    'migrate_auto.py': 'scripts/migration/',
    'migrate_final.py': 'scripts/migration/',
    'migrate_step_by_step.py': 'scripts/migration/',
    'rollback.py': 'scripts/migration/',
    'set_admin_avatar.py': 'scripts/migration/',
    'set_sergio_avatar.py': 'scripts/migration/',
    'setup_final_users.py': 'scripts/migration/',
    'validate_migration.py': 'scripts/migration/',
    'verify_before_migration.py': 'scripts/migration/',
    
    # Scripts de teste -> scripts/testing/
    'test_cors.py': 'scripts/testing/',
    'test_dynamodb.py': 'scripts/testing/',
    'test_s3.py': 'scripts/testing/',
    'test_user_files.py': 'scripts/testing/',
    'test-check-limits.json': 'scripts/testing/',
    'test-payload.json': 'scripts/testing/',
    
    # Scripts AWS -> scripts/aws/
    'configure-lifecycle.py': 'scripts/aws/',
    'deploy.py': 'scripts/aws/',
    
    # Docs de deploy -> docs/
    'CICD_QUICKSTART.md': 'docs/',
    'DEPLOY_COMMANDS.md': 'docs/',
    'DEPLOY_FOLDER_MANAGER_V2.md': 'docs/',
    'DEPLOY.md': 'docs/',
    'DEPLOYMENT.md': 'docs/',
    'SETUP_CICD.md': 'docs/',
    'MIGRACAO_CHECKLIST.md': 'docs/',
    
    # Arquivos temporários -> deletar
    'response.json': None,
    'organize-project.py': None,
}

# Criar diretórios necessários
dirs = ['backup', 'scripts/migration', 'scripts/testing', 'scripts/aws', 'docs']
for d in dirs:
    os.makedirs(d, exist_ok=True)

print("Organizando projeto...\n")

moved = 0
deleted = 0
skipped = 0

for file, dest in MOVES.items():
    if not os.path.exists(file):
        skipped += 1
        continue
    
    if dest is None:
        os.remove(file)
        print(f"[DELETADO] {file}")
        deleted += 1
    else:
        dest_path = os.path.join(dest, file)
        if os.path.exists(dest_path):
            skipped += 1
        else:
            shutil.move(file, dest_path)
            print(f"[OK] {file} -> {dest}")
            moved += 1

print(f"\n[CONCLUIDO] Movidos: {moved} | Deletados: {deleted} | Pulados: {skipped}")

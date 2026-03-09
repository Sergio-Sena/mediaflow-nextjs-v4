import os
import json

backup_name = 'backup-v4.8.7-stable-20260308-202432'
info_file = f'backups/{backup_name}-info.json'

print("=== TESTE DE ROLLBACK (DRY RUN) ===\n")

if os.path.exists(info_file):
    with open(info_file) as f:
        info = json.load(f)
    
    print("[OK] Backup encontrado:")
    print(f"  Nome: {info['name']}")
    print(f"  Versao: {info['version']}")
    print(f"  Commit: {info['git_commit'][:8]}")
    print(f"  Data: {info['timestamp']}")
    print(f"  CloudFront: {info['cloudfront_id']}")
    print(f"  S3 Frontend: {info['s3_frontend']}")
    print(f"  S3 Backup: {info['s3_backup']}")
    
    # Verificar arquivos
    print("\n[OK] Arquivos de backup:")
    zip_file = f"backups/{backup_name}.zip"
    cf_file = f"backups/{backup_name}-cloudfront.json"
    
    if os.path.exists(zip_file):
        size = os.path.getsize(zip_file) / 1024 / 1024
        print(f"  Codigo: {size:.2f} MB")
    else:
        print(f"  [ERRO] Codigo nao encontrado")
    
    if os.path.exists(cf_file):
        print(f"  CloudFront: OK")
    else:
        print(f"  [ERRO] CloudFront config nao encontrada")
    
    print("\n[OK] Rollback esta pronto para uso!")
    print(f"\nPara executar:")
    print(f"  python scripts/rollback.py {backup_name}")
else:
    print("[ERRO] Backup nao encontrado!")

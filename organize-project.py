import os
import shutil

# Arquivos para mover
MOVES = {
    # Duplicados -> scripts/
    'duplicados_admin.txt': 'scripts/',
    'duplicados_avancado.json': 'scripts/',
    'duplicados_avancado.txt': 'scripts/',
    'duplicados_completo.json': 'scripts/',
    'duplicados_completo.txt': 'scripts/',
    'DUPLICADOS_ENCONTRADOS.md': 'scripts/',
    
    # Configs CloudFront -> aws-setup/
    'cf-config-temp.json': 'aws-setup/',
    'cf-config-updated.json': 'aws-setup/',
    'cloudfront-config.json': 'aws-setup/',
    'cloudfront-e2h-config.json': 'aws-setup/',
    'create-midiaflow-dns.json': 'aws-setup/',
    
    # Scripts -> scripts/
    'create-test-user.py': 'scripts/',
    'move-anime-folders.py': 'scripts/',
    'test-login.js': 'scripts/testing/',
    'test-payload.json': 'scripts/testing/',
    
    # Docs -> memoria/
    'MUDANCAS_DESDE_PORTO_SEGURO.md': 'memoria/',
    'PROPOSTA_DASHBOARD_STREAMING.md': 'memoria/',
    'RELATORIO_TESTES.md': 'memoria/',
    'TESTE_PRODUCAO_MIDIAFLOW.md': 'memoria/',
    
    # Deploy docs -> raiz (manter)
    # CHANGELOG.md, DEPLOY.md, README.md ficam na raiz
    
    # Temp files -> deletar
    'temp-users.json': None,
    'cicd-test.txt': None,
    'lambda-layer.zip': None,
}

print("Organizando projeto local...\n")

moved = 0
deleted = 0
skipped = 0

for file, dest in MOVES.items():
    if not os.path.exists(file):
        print(f"[SKIP] {file} (nao existe)")
        skipped += 1
        continue
    
    if dest is None:
        # Deletar
        os.remove(file)
        print(f"[DEL] {file}")
        deleted += 1
    else:
        # Mover
        dest_path = os.path.join(dest, file)
        if os.path.exists(dest_path):
            print(f"[SKIP] {file} (ja existe em {dest})")
            skipped += 1
        else:
            shutil.move(file, dest_path)
            print(f"[OK] {file} -> {dest}")
            moved += 1

print(f"\nMovidos: {moved} | Deletados: {deleted} | Pulados: {skipped}")
print("\nOrganizacao concluida!")

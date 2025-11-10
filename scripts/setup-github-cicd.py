"""
Script para configurar CI/CD no GitHub
Requer: GitHub CLI (gh) instalado
"""

import subprocess
import json

print("=" * 80)
print("CONFIGURACAO CI/CD GITHUB")
print("=" * 80)
print()

# Verificar se gh CLI esta instalado
try:
    result = subprocess.run(['gh', '--version'], capture_output=True, text=True)
    print(f"✅ GitHub CLI instalado: {result.stdout.split()[2]}")
except:
    print("❌ GitHub CLI nao encontrado!")
    print("Instale: https://cli.github.com/")
    exit(1)

print()
print("=" * 80)
print("SECRETS NECESSARIOS")
print("=" * 80)
print()

secrets = {
    'AWS_ACCESS_KEY_ID': 'Sua AWS Access Key ID',
    'AWS_SECRET_ACCESS_KEY': 'Sua AWS Secret Access Key',
    'JWT_SECRET': '17b8312c72fdcffbff89f2f4a564fb26e936002d344717ab7753a237fcd57aea',
    'NEXT_PUBLIC_API_URL': 'https://api.midiaflow.sstechnologies-cloud.com',
    'S3_BUCKET_FRONTEND': 'midiaflow-frontend-969430605054',
    'CLOUDFRONT_DISTRIBUTION_ID': 'Seu CloudFront Distribution ID'
}

print("Vou configurar os seguintes secrets:")
print()
for key, value in secrets.items():
    if 'SECRET' in key or 'KEY' in key:
        display = value[:20] + '...' if len(value) > 20 else value
    else:
        display = value
    print(f"  {key}: {display}")

print()
resp = input("Continuar? (s/n): ")
if resp.lower() != 's':
    print("Cancelado")
    exit(0)

print()
print("=" * 80)
print("CONFIGURANDO SECRETS")
print("=" * 80)

# Pedir valores reais
print()
print("Digite os valores (ou ENTER para usar padrao):")
print()

final_secrets = {}
for key, default in secrets.items():
    if 'AWS_ACCESS_KEY_ID' in key or 'AWS_SECRET_ACCESS_KEY' in key or 'CLOUDFRONT' in key:
        value = input(f"{key}: ").strip()
        if not value:
            print(f"  ⚠️  Usando valor padrao (pode nao funcionar)")
            value = default
    else:
        value = default
    final_secrets[key] = value

print()
print("Configurando secrets no GitHub...")
print()

for key, value in final_secrets.items():
    try:
        result = subprocess.run(
            ['gh', 'secret', 'set', key, '-b', value],
            capture_output=True,
            text=True,
            cwd=r'c:\Projetos Git\drive-online-clean-NextJs'
        )
        if result.returncode == 0:
            print(f"✅ {key}")
        else:
            print(f"❌ {key}: {result.stderr}")
    except Exception as e:
        print(f"❌ {key}: {e}")

print()
print("=" * 80)
print("CRIANDO BRANCH DEVELOP")
print("=" * 80)

try:
    subprocess.run(['git', 'checkout', '-b', 'develop'], cwd=r'c:\Projetos Git\drive-online-clean-NextJs')
    subprocess.run(['git', 'push', '-u', 'origin', 'develop'], cwd=r'c:\Projetos Git\drive-online-clean-NextJs')
    print("✅ Branch develop criada")
except Exception as e:
    print(f"⚠️  Branch develop: {e}")

print()
print("=" * 80)
print("CONCLUIDO!")
print("=" * 80)
print()
print("Proximos passos:")
print("1. Verifique secrets: https://github.com/SEU_USER/SEU_REPO/settings/secrets/actions")
print("2. Teste deploy: git push origin develop")
print("3. Veja Actions: https://github.com/SEU_USER/SEU_REPO/actions")
print()

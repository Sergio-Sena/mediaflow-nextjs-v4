"""
Script para ajucorporativo permissoes:
- Users comuns veem apenas users/user_admin/
- Sergio Sena (media_owner) ve tudo
"""

# Atualizar files-handler Lambda
lambda_code = """
# Na funcao list_files, trocar logica:

# ANTES:
if user_role == 'media_owner':
    user_prefix = ''  # Media owner ve tudo
elif user_role == 'admin':
    user_prefix = 'admin-no-media'  # Admin nao ve midias
elif user_prefix:
    pass  # User ve sua pasta

# DEPOIS:
if user_role == 'media_owner':
    user_prefix = ''  # Media owner ve tudo
elif user_role == 'admin':
    user_prefix = 'admin-no-media'  # Admin nao ve midias
elif user_role == 'user':
    user_prefix = 'users/user_admin/'  # Users veem apenas pasta do admin
"""

print("=" * 80)
print("MUDANCA DE PERMISSOES")
print("=" * 80)
print()
print("Para aplicar a mudanca:")
print()
print("1. Edite: aws-setup/lambda-functions/files-handler/lambda_function.py")
print()
print("2. Localize a funcao list_files() linha ~40")
print()
print("3. Substitua:")
print("   elif user_prefix:")
print("       pass")
print()
print("   Por:")
print("   elif user_role == 'user':")
print("       user_prefix = 'users/user_admin/'")
print()
print("4. Deploy:")
print("   python aws-setup/deploy-files-handler.py")
print()
print("=" * 80)
print("RESULTADO:")
print("=" * 80)
print("- Users comuns: Veem apenas users/user_admin/")
print("- Sergio Sena: Ve TUDO")
print("- Admin: Nao ve midias")
print()

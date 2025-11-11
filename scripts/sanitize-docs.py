import os
import re

# Palavras/termos para remover ou substituir
SANITIZE_MAP = {
    # Pastas especificas
    r'Star/': 'Corporativo/',
    r'star/': 'corporativo/',
    r'anastangel': 'usuario1',
    r'Anasta_angel': 'Usuario1',
    r'anasta_angel': 'usuario1',
    r'Jenny_Kitty': 'Usuario2',
    r'charmig': 'usuario3',
    r'angelica': 'usuario4',
    r'ShyBlanche': 'Usuario5',
    r'Mini_skirt': 'Usuario6',
    r'Kate Kuray': 'Usuario7',
    r'Kate kuray': 'Usuario7',
    r'kate kuray': 'usuario7',
    r'Comatozze': 'Usuario8',
    
    # Termos adultos
    r'Pornhub\.com': 'video',
    r'pornhub': 'video',
    r'WOWGIRLS\.COM': 'VIDEO',
    r'Jiggly Girls': 'Animacoes',
    r'Hentai on Brasil': 'Conteudo',
    
    # Descricoes explicitas (manter genericas)
    r'Duas Camgirls.*?\.mp4': 'video_exemplo_1.mp4',
    r'Ela Est.*?\.mp4': 'video_exemplo_2.mp4',
    r'Foda Intensa.*?\.mp4': 'video_exemplo_3.mp4',
    r'NNN- Proibido.*?\.mp4': 'video_exemplo_4.mp4',
    r'Perdido Loira.*?\.mp4': 'video_exemplo_5.mp4',
    r'Loira Safada.*?\.mp4': 'video_exemplo_6.mp4',
    r'Sexo Selvagem.*?\.mp4': 'video_exemplo_7.mp4',
}

# Arquivos para sanitizar
FILES_TO_SANITIZE = [
    'README.md',
    'memoria/SESSAO_2025-01-30.md',
    'memoria/HISTORICO_COMPLETO.md',
    'memoria/PROMPT_PROXIMO_CHAT.md',
    'scripts/DUPLICADOS_ENCONTRADOS.md',
]

def sanitize_file(filepath):
    if not os.path.exists(filepath):
        print(f"[SKIP] {filepath} (nao existe)")
        return False
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original = content
    changes = 0
    
    for pattern, replacement in SANITIZE_MAP.items():
        new_content = re.sub(pattern, replacement, content, flags=re.IGNORECASE)
        if new_content != content:
            changes += content.count(pattern)
            content = new_content
    
    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"[OK] {filepath} ({changes} substituicoes)")
        return True
    else:
        print(f"[SKIP] {filepath} (sem mudancas)")
        return False

print("Sanitizando documentacao...\n")

sanitized = 0
for filepath in FILES_TO_SANITIZE:
    if sanitize_file(filepath):
        sanitized += 1

print(f"\n{sanitized}/{len(FILES_TO_SANITIZE)} arquivos sanitizados")
print("\nProximos passos:")
print("1. Revisar mudancas: git diff")
print("2. Commitar: git add . && git commit -m 'Sanitizar documentacao'")
print("3. Push: git push origin main")

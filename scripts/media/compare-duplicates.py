# -*- coding: utf-8 -*-
"""
Detecta duplicatas no S3 por:
  1. Tamanho exato igual (independente do nome)
  2. Nome similar + tamanho próximo (±2%)
  3. Mesmo nome em pastas diferentes
  4. Mesmo nome, extensão diferente (.mkv vs .mp4)

Categorias:
  CERTO   - duplicata confirmada, pode deletar em lote
  REVISAR - precisa verificar antes de deletar

Uso:
  python compare-duplicates.py           # lista tudo
  python compare-duplicates.py --delete  # deleta com confirmação por categoria
"""
import sys
import re
import json
import subprocess
from collections import defaultdict
from difflib import SequenceMatcher

sys.stdout.reconfigure(encoding='utf-8')

BUCKET   = 'mediaflow-uploads-969430605054'
PREFIX   = 'users/sergio_sena/'
PROFILE  = 'default'
AWS      = 'aws'
SIZE_TOL = 0.02

IGNORE_PREFIXES = re.compile(r'^(pov[-_]?|hmv[-_]?|pmv[-_]?)', re.IGNORECASE)
NUMERIC_SUFFIX  = re.compile(r'_(\d+)$')
SERIES_PATTERNS = re.compile(
    r'(_parte_\d+|_part_\d+|_s\d+e\d+|_ep\d+|androvid_join|_join_\d+_\d+)',
    re.IGNORECASE
)


def is_series(name_a, name_b):
    if SERIES_PATTERNS.search(name_a) and SERIES_PATTERNS.search(name_b):
        return True
    m_a = NUMERIC_SUFFIX.search(name_a)
    m_b = NUMERIC_SUFFIX.search(name_b)
    if m_a and m_b:
        if name_a[:m_a.start()] == name_b[:m_b.start()] and m_a.group(1) != m_b.group(1):
            return True
    return False


def list_s3_objects():
    print('Listando objetos no S3...')
    result = subprocess.run(
        [AWS, 's3api', 'list-objects-v2', '--bucket', BUCKET,
         '--prefix', PREFIX, '--profile', PROFILE,
         '--query', 'Contents[?ends_with(Key, `.mp4`) || ends_with(Key, `.mkv`) || ends_with(Key, `.ts`)].{Key:Key,Size:Size}'],
        capture_output=True
    )
    if result.returncode != 0:
        print(f'ERRO: {result.stderr}')
        sys.exit(1)
    objects = json.loads(result.stdout.decode('utf-8', errors='replace') or '[]')
    print(f'Total de vídeos: {len(objects)}\n')
    return objects


def normalize_name(key):
    name = key.split('/')[-1].rsplit('.', 1)[0].lower()
    name = IGNORE_PREFIXES.sub('', name)
    name = re.sub(r'[_\-\s]+', ' ', name).strip()
    return name


def similarity(a, b):
    return SequenceMatcher(None, a, b).ratio()


def fmt_size(size):
    if size >= 1024**3:
        return f'{size/1024**3:.2f} GB'
    elif size >= 1024**2:
        return f'{size/1024**2:.1f} MB'
    return f'{size/1024:.1f} KB'


def classify(reason, items):
    """
    Retorna 'CERTO' ou 'REVISAR' baseado no motivo e nos itens.
    CERTO:
      - exact_size + nomes muito similares (>85%)
      - same_name_diff_ext (.mkv vs .mp4)
      - similar_name + size ±0% (sanitização diferente do mesmo arquivo)
    REVISAR:
      - exact_size + nomes completamente diferentes
      - very_similar_name com tamanhos diferentes (>10%)
      - same_name_diff_folder
    """
    name_a = normalize_name(items[0]['Key'])
    name_b = normalize_name(items[-1]['Key'])
    sim    = similarity(name_a, name_b)
    sizes  = [i['Size'] for i in items]
    size_diff = abs(sizes[0] - sizes[-1]) / max(sizes) if max(sizes) > 0 else 0

    if reason == 'same_name_diff_ext':
        return 'CERTO'
    if reason == 'exact_size' and sim >= 0.75:
        return 'CERTO'
    if 'size(±0.0%)' in reason or 'size(±0.1%)' in reason:
        return 'CERTO'
    if reason == 'exact_size' and sim < 0.75:
        return 'REVISAR'
    if reason == 'same_name_diff_folder':
        return 'REVISAR'
    if size_diff > 0.10:
        return 'REVISAR'
    return 'REVISAR'


def find_duplicates(objects):
    groups = []
    seen_pairs = set()
    by_size = defaultdict(list)
    for obj in objects:
        by_size[obj['Size']].append(obj)

    def add_group(items, reason):
        keys = tuple(sorted(i['Key'] for i in items))
        if keys not in seen_pairs:
            seen_pairs.add(keys)
            items_sorted = sorted(items, key=lambda x: x['Size'], reverse=True)
            confidence   = classify(reason, items_sorted)
            groups.append({'reason': reason, 'confidence': confidence, 'items': items_sorted})

    # 1. Tamanho exato igual
    for size, items in by_size.items():
        if len(items) > 1:
            for i in range(len(items)):
                for j in range(i+1, len(items)):
                    na = normalize_name(items[i]['Key'])
                    nb = normalize_name(items[j]['Key'])
                    if not is_series(na, nb):
                        add_group([items[i], items[j]], 'exact_size')

    # 2-4. Comparações por nome
    for i, a in enumerate(objects):
        name_a   = normalize_name(a['Key'])
        folder_a = '/'.join(a['Key'].split('/')[:-1])
        ext_a    = a['Key'].rsplit('.', 1)[-1].lower()

        for b in objects[i+1:]:
            pair = tuple(sorted([a['Key'], b['Key']]))
            if pair in seen_pairs:
                continue

            name_b   = normalize_name(b['Key'])
            folder_b = '/'.join(b['Key'].split('/')[:-1])
            ext_b    = b['Key'].rsplit('.', 1)[-1].lower()

            if is_series(name_a, name_b):
                continue

            size_diff = abs(a['Size'] - b['Size']) / max(a['Size'], b['Size'])
            sim       = similarity(name_a, name_b)

            if name_a == name_b and ext_a != ext_b:
                add_group([a, b], 'same_name_diff_ext')
                continue
            if name_a == name_b and folder_a != folder_b:
                add_group([a, b], 'same_name_diff_folder')
                continue
            if sim >= 0.80 and size_diff <= SIZE_TOL:
                add_group([a, b], f'similar_name({sim:.0%})_size(±{size_diff:.1%})')
                continue
            if sim >= 0.90:
                add_group([a, b], f'very_similar_name({sim:.0%})')

    return groups


def print_group(idx, total, group):
    conf  = group['confidence']
    tag   = '✅ CERTO  ' if conf == 'CERTO' else '⚠️  REVISAR'
    items = group['items']
    print(f'┌─ [{idx}/{total}] {tag} | {group["reason"]}')
    for j, item in enumerate(items):
        parts  = item['Key'].split('/')
        folder = '/'.join(parts[2:-1])
        name   = parts[-1]
        marker = '★' if j == 0 else '↳'
        print(f'│  {marker} {fmt_size(item["Size"]):>10}  [{folder}]')
        print(f'│             {name}')
    print('│')
    print('└' + '─'*60)


def delete_object(key):
    result = subprocess.run(
        [AWS, 's3', 'rm', f's3://{BUCKET}/{key}', '--profile', PROFILE],
        capture_output=True, text=True
    )
    return result.returncode == 0


def main():
    delete_mode = '--delete' in sys.argv
    objects     = list_s3_objects()
    groups      = find_duplicates(objects)

    if not groups:
        print('Nenhuma duplicata encontrada!')
        return

    certos   = [g for g in groups if g['confidence'] == 'CERTO']
    revisars = [g for g in groups if g['confidence'] == 'REVISAR']
    total    = len(groups)

    print(f'{"="*62}')
    print(f'DUPLICATAS: {total} grupos  |  ✅ CERTO: {len(certos)}  |  ⚠️  REVISAR: {len(revisars)}')
    print(f'{"="*62}\n')

    deleted_count = 0

    # ── BLOCO 1: CERTO ──────────────────────────────────────────
    if certos:
        print(f'{"─"*62}')
        print(f'✅  CERTO — duplicatas confirmadas ({len(certos)} grupos)')
        print(f'{"─"*62}\n')

        for idx, group in enumerate(certos, 1):
            print_group(idx, len(certos), group)

        if delete_mode:
            print(f'\nDeletar todos os {len(certos)} menores acima de uma vez?')
            resp = input('[s = deletar todos / n = pular / u = um a um]: ').strip().lower()

            if resp == 's':
                for group in certos:
                    to_delete = group['items'][-1]
                    if delete_object(to_delete['Key']):
                        print(f'  ✓ {to_delete["Key"].split("/")[-1]}')
                        deleted_count += 1
                    else:
                        print(f'  ✗ ERRO: {to_delete["Key"].split("/")[-1]}')

            elif resp == 'u':
                for idx, group in enumerate(certos, 1):
                    to_delete = group['items'][-1]
                    parts     = to_delete['Key'].split('/')
                    print(f'\n[{idx}/{len(certos)}] Deletar: {parts[-1]} ({fmt_size(to_delete["Size"])})?')
                    r = input('  [s/n/q]: ').strip().lower()
                    if r == 'q':
                        break
                    elif r == 's':
                        if delete_object(to_delete['Key']):
                            print(f'  ✓ Deletado')
                            deleted_count += 1
                        else:
                            print(f'  ✗ ERRO')

    # ── BLOCO 2: REVISAR ────────────────────────────────────────
    if revisars:
        print(f'\n{"─"*62}')
        print(f'⚠️   REVISAR — verifique antes de deletar ({len(revisars)} grupos)')
        print(f'{"─"*62}\n')

        for idx, group in enumerate(revisars, 1):
            print_group(idx, len(revisars), group)

            if delete_mode:
                to_delete = group['items'][-1]
                parts     = to_delete['Key'].split('/')
                print(f'  Deletar menor: {parts[-1]} ({fmt_size(to_delete["Size"])})?')
                resp = input('  [s/n/q para sair]: ').strip().lower()
                if resp == 'q':
                    print('Abortado.')
                    break
                elif resp == 's':
                    if delete_object(to_delete['Key']):
                        print(f'  ✓ Deletado')
                        deleted_count += 1
                    else:
                        print(f'  ✗ ERRO')
                print()

    print(f'\n{"="*62}')
    print(f'RESUMO')
    print(f'  Total grupos : {total}')
    print(f'  ✅ CERTO     : {len(certos)}')
    print(f'  ⚠️  REVISAR  : {len(revisars)}')
    if delete_mode:
        print(f'  Deletados    : {deleted_count}')
    else:
        print(f'  Execute com --delete para remover')
    print(f'{"="*62}')


if __name__ == '__main__':
    main()

# 🤝 Handoff — MidiaFlow

> Arquivo de continuidade entre sessões. Atualizar ao final de cada sessão de trabalho.

---

## 📍 Estado atual do projeto

- **Versão:** 4.9.1
- **Último commit:** `d57b8d4` — duration server-side paralelo + otimizações de performance
- **Branch principal:** `main` (produção automática via push)
- **Branch dev:** `dev`
- **URL produção:** https://midiaflow.sstechnologies-cloud.com
- **Pipeline:** `test → ai-audit → build → deploy-frontend → deploy-lambdas → health-check → notify`

---

## ✅ O que foi feito (sessões anteriores)

### Mobile UX — Portrait, Landscape e Desktop (sessão atual)

#### Dashboard — Portrait mobile
- **Header**: hambúrguer removido → avatar + nome (clica vai para `/profile`)
- **Bottom tab bar**: só ícones `text-2xl` + dot ativo (`bg-[#667eea]`), sem labels — mais limpo e espaçoso
- **Filtros FileList**: busca full-width com ícone Search interno; pasta e ordenação viram botões quadrados `38x38px` que abrem dropdowns customizados (dark, `IntersectionObserver`-style); botões uniformes

#### Dashboard — Landscape mobile
- **Header**: só logo + ícone ☰ (`landscape:max-lg:flex`) — completamente limpo
- **Drawer lateral**: desliza da esquerda (`w-56`), overlay com `bg-black/50`, fecha ao clicar fora
  - Seção "Navegação": Biblioteca, Pastas, Upload, Público, Analytics (item ativo com borda roxa)
  - Seção "Conta": avatar + nome + email, Perfil, Gerenciamento (admin), Sair
- **Sem sidebar fixa**: drawer é overlay, não empurra conteúdo
- **Cards**: `landscape:w-[calc(33vw-20px)]` — 3 por linha em vez de 2

#### Dashboard — Desktop
- **Nav tabs**: emojis removidos, só texto limpo, `px-5` uniforme
- **Header**: "Dashboard v4.3" → `v4.9.1` discreto em `font-mono text-gray-600`; nome truncate `max-w-[140px]`
- **Filtros**: visual integrado ao tema dark (`bg-white/5 border-white/10`), ícone Search no input, botões `34x34px` uniformes, contador "X arquivos" à esquerda
- **Cards**: tamanho fixo `sm:w-48 md:w-52 lg:w-48` (não vaza mais `calc(50vw)` para desktop)
- **Hambúrguer**: `landscape:max-lg:flex` — nunca aparece no desktop
- **Drawer**: `lg:hidden` — nunca aparece no desktop

#### Fix ERR_INSUFFICIENT_RESOURCES (thumbnails)
- **Problema**: 763 arquivos → centenas de requests de thumbnail simultâneos → browser sem recursos
- **Solução**: `ThumbnailImage` usa `IntersectionObserver` com `rootMargin: 200px` — só carrega quando card entra na viewport
- Também adicionado `loading="lazy"` no `<img>`

#### Fix sintaxe dashboard
- `</div>` faltando no container `flex justify-between` do header — causava `Unexpected token div`

### Cards dashboard — tamanho unificado com área pública
- **Problema**: Tailwind v4 classes arbitrárias (`w-[calc(...)]`) têm precedência sobre utilitárias (`sm:w-52`) — cards ficavam enormes no desktop
- **Fix**: `style={{ width: 'clamp(160px, calc(50vw - 20px), 208px)' }}` inline no `ContentCarousel` — máximo 208px no desktop, responsivo no mobile

### view-handler — reprodução de conteúdo público
- **Problema**: 403 ao tentar assistir vídeo de outro usuário na área pública
- **Fix 1**: adicionado scan em `mediaflow-public-content` antes de negar acesso
- **Fix 2**: `FilterExpression` corrigido de string raw para `Attr('file_key').eq(key) & Attr('is_active').eq(True)` (boto3 resource exige `Attr()` do `boto3.dynamodb.conditions`)
- **Fix 3**: adicionado `from boto3.dynamodb.conditions import Attr`

### Área pública — cards desktop
- Largura corrigida de `md:w-[200px]/[230px]/[260px]` para `md:w-52 lg:w-48`

### Performance — sessão atual

- **`files-handler`**: duration buscado server-side com `ThreadPoolExecutor(20)` — elimina 763 requests do browser
- **`files-cache`**: TTL aumentado de 5 para 30 minutos
- **`fetchUserData`**: só busca avatar se não estiver no cache local
- **`fetchDurationsInBackground`**: desativado — duration já vem da Lambda
- **`view-handler`**: URL via CloudFront CDN (`/media/*`) em vez de presigned URL S3 direto
- **`view-handler`**: removidos 2 `head_object` desnecessários (bucket processed)
- **`generate_thumbnails.py`**: substituiu 763 `head_object` individuais por 1 listagem única + workers 10→20
- **`VideoPlayer`**: autoplay com `muted=true` inicial, `toggleMute` usa `video.muted` diretamente
- **Lambda timeout**: `mediaflow-files-handler` aumentado para 30s

---

- **Problema**: Lambda `files-handler` fazia `head_object` para cada `.mp4` em paralelo — com 500+ arquivos causava timeout de 30s e erro de CORS
- **Solução**: Duration movida para responsabilidade do frontend
- `files-handler` — removido `ThreadPoolExecutor`, retorna `duration: 0`. Novo endpoint `GET /files?key=...` para buscar duration de arquivo específico
- `lib/duration-cache.ts` — cache permanente no `localStorage`, sem expiração, indexado por `file_key`
- `FileList.tsx` — aplica cache instantaneamente, busca em background só os vídeos sem duration (`!durationCache.get(key)`)
- `share-content` Lambda — salva `duration` no DynamoDB ao compartilhar
- `public-feed/page.tsx` — `PublicItem` com `duration?`, badge `MM:SS` no card
- `scripts/media/update-duration-metadata.py` — rodado uma vez para atualizar 591 arquivos existentes (todos já tinham metadata)
- Deploy via `git push origin main` (pipeline CI/CD)

### Movimentação de arquivos S3
- 7 arquivos movidos de `Star/Emillya_Bunny/` para `outros/`
- Estrutura de pastas ajustada manualmente pelo usuário

### Fix dashboard lento
- `max_workers` e connection pool testados — descartados em favor da solução de cache no frontend

### Redesign visual Sphere/Netflix
- Tema aplicado em todas as páginas: Index, Login, Dashboard, Public-feed, Profile, Admin, Termos, Privacidade, SLA
- Paleta: `#667eea` / `#764ba2` / `#a5b4fc`
- Fundo: `315deg #000 → #0d0d1a → #0a0a1f`
- Glass cards: `rgba(255,255,255,0.08)`

### Hero mockup (Index)
- Substituída lista com nomes reais de arquivos por player mockup animado (scan lines, glow, barra pulsando)
- 3 cards de categoria fictícios: Coleção A, Série 01, Favoritos

### Login visual
- Split screen: imagem de anime Unsplash (`photo-1528360983277-13d401cdc186`) à esquerda
- Overlay gradiente escuro + tint Sphere
- `backgroundPosition: 'center center'`

### Fix script upload (`scripts/media/sanitize-remux-upload.py`)
- `get_s3_folder` usa `BASE_PATH` como referência (preserva estrutura `Anime/`, `Star/` no S3)
- Suporte a múltiplos `--path`: `python sanitize-remux-upload.py --path "...\Anime" --path "...\Star"`
- `get_video_meta` retorna `duration` via ffprobe
- `meta_to_s3_tags` inclui `duration`

### Fix FinOps
- Job `finops` removido do pipeline CI/CD — roda manualmente
- `EMAIL_FROM = 'marketing@sstechnologies-cloud.com'`
- Modelo Bedrock: `claude-haiku-4-5-20251001-v1:0`

### Duration badge nos cards (dashboard)
- Script `scripts/media/update-duration-metadata.py` — atualiza metadata de arquivos existentes no S3 via ffprobe + presigned URL + copy-object (5 threads)
- Lambda `files-handler` — `get_duration()` + `ThreadPoolExecutor(max_workers=10)` para buscar duration em paralelo
- `ContentCarousel.tsx` — `formatDuration()` + badge `MM:SS` no canto inferior esquerdo
- `FileList.tsx` e `dashboard/page.tsx` — `duration?` adicionado nos tipos

---

## ⏸️ Decisões tomadas / descartado

| Item | Decisão | Motivo |
|---|---|---|
| Duration no public-feed | Adiado para v4.10 | 3 camadas (Lambda + DynamoDB + frontend) para um badge — custo/benefício baixo |

---

## 🔜 Próximo passo imediato

Nada pendente urgente. Projeto estável em produção.

---

## 🗺️ Roadmap

- **v4.10** — Área pública: conteúdo compartilhável, multi-resolução, legendas, analytics. Refatorar `PublicItem` com `duration`, `views`, `resolution`
- **Sentry** — erros no frontend em produção
- **Live streaming** — MediaStore + MediaLive
- **API pública**
- **Mobile app** — React Native

---

## 📌 Referências rápidas

| Item | Valor |
|---|---|
| Bucket S3 | `mediaflow-uploads-969430605054` / `us-east-1` |
| Prefixo S3 usuário | `users/sergio_sena/` |
| CDN bucket | `sstech-cdn-unified` → path `/midiaflow/` |
| CloudFront distribution | `E9ZQJ3RPSA04N` |
| Invalidação CDN | `--paths "/midiaflow/*"` |
| DynamoDB auth | `mediaflow-users` |
| DynamoDB social | `mediaflow-public-content` |
| SES verificado | `marketing@sstechnologies-cloud.com` / `us-east-1` |
| FFmpeg local | `C:\ffmpeg\bin\ffmpeg.exe` |
| Mídia local | `C:\Users\dell 5557\Videos\IDM` |
| Rollback | `git revert HEAD && git push` (~8 min) |

---

## 🏗️ Arquivos-chave

| Arquivo | Responsabilidade |
|---|---|
| `app/page.tsx` | Hero com player mockup |
| `app/(auth)/login/page.tsx` | Split screen com imagem anime |
| `app/dashboard/page.tsx` | Dashboard principal |
| `app/public-feed/page.tsx` | Feed público com CategoryRow próprio |
| `components/modules/ContentCarousel.tsx` | Carrossel reutilizável com duration badge |
| `components/modules/FileList.tsx` | Lista de arquivos do dashboard |
| `lib/auth-utils.ts` | `getUserFromToken()` — JWT utils |
| `lib/aws-config.ts` | Endpoints da API |
| `aws-setup/lambda-functions/files-handler/lambda_function.py` | CRUD arquivos + duration paralelo |
| `aws-setup/lambda-functions/share-content/lambda_function.py` | Feed público — share/like/comment |
| `scripts/media/sanitize-remux-upload.py` | Sanitizar + remuxar + upload S3 |
| `scripts/media/update-duration-metadata.py` | Atualizar duration nos arquivos existentes |
| `scripts/finops/cost-report.py` | Relatório FinOps manual (Bedrock + SES) |
| `.github/workflows/deploy-production.yml` | Pipeline CI/CD |

---

## 📋 Checklist antes de fechar uma sessão

- [ ] Este arquivo atualizado
- [ ] `docs/RADAR_PROXIMAS_TAREFAS.md` atualizado
- [ ] Código commitado e pushed para `dev` ou `main`
- [ ] Sem secrets no código
- [ ] Testes passando (`npm test`)

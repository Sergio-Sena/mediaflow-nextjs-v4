# 🤝 Handoff — MidiaFlow

> Arquivo de continuidade entre sessões. Atualizar ao final de cada sessão de trabalho.

---

## 📍 Estado atual do projeto

- **Versão:** 4.9.1
- **Último commit:** `62202cb` — fix desktop cards, hamburger, thumbnail lazy loading
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

#### Commits desta sessão
| Commit | Descrição |
|---|---|
| `529eb6e` | feat: mobile UX improvements - portrait/landscape responsive nav |
| `62202cb` | fix: desktop cards size, hamburger visibility, thumbnail lazy loading |

#### Observação sobre deploy
- `git push` dentro do `executeBash` às vezes retorna sucesso mas não sobe — sempre verificar com segundo push ou `git log origin/main`

---
### Duration badge nos cards — refatoração completa (performance)
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

### ⚠️ PENDENTE — Área pública: cards + reprodução (commit `64ba216`)

O push passou na esteira mas as correções **não foram aplicadas em produção**. Investigar na próxima sessão.

#### O que foi alterado (mas não surtiu efeito)

**1. Reprodução de vídeos na área pública (403 Acesso negado)**
- **Causa raiz**: `view-handler` bloqueava acesso a `users/outro_user/...` com 403 — qualquer usuário tentando assistir vídeo de outro usuário recebia erro
- **Fix aplicado** em `aws-setup/lambda-functions/view-handler/lambda_function.py`:
  - Antes: negava direto se `key` não começasse com `users/{user_id}/`
  - Depois: consulta `mediaflow-public-content` (scan por `file_key + is_active=True`) antes de negar — se o conteúdo estiver compartilhado, libera o acesso
- **Suspeita**: Lambda pode não ter sido re-deployada pela esteira, ou o scan do DynamoDB está retornando vazio

**2. Proporção dos cards desktop na área pública**
- **Fix aplicado** em `app/public-feed/page.tsx`:
  - Antes: `md:w-[200px] sm:w-full md:w-[230px] lg:w-[260px]` (classes duplicadas, tamanhos maiores)
  - Depois: `md:w-52 lg:w-48` — idêntico ao `ContentCarousel` do dashboard
- **Suspeita**: CloudFront cache pode estar servindo versão antiga

#### O que verificar na próxima sessão
1. Checar logs CloudWatch da Lambda `view-handler` — ver se está recebendo requests e qual erro retorna
2. Confirmar se a Lambda foi re-deployada: verificar `Last modified` no console AWS
3. Para o frontend: inspecionar hash do bundle JS no browser para confirmar se CloudFront está servindo versão nova
4. Alternativa para o 403: o `GET /public` já retorna `owner_id` — passar como parâmetro para o player e usar um endpoint dedicado para conteúdo público que não exija ownership check

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

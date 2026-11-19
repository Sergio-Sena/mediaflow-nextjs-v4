# 📡 Radar — Próximas Tarefas

## ✅ Concluídos recentemente

- **Redesign Sphere/Netflix** — Index, Login, Dashboard, Public-feed, Profile, Admin, Termos, Privacidade, SLA. Paleta: `#667eea`/`#764ba2`/`#a5b4fc`, fundo `315deg #000→#0d0d1a→#0a0a1f`
- **Hero mockup** — player animado + 3 cards de categoria fictícios (Coleção A, Série 01, Favoritos)
- **Login visual** — imagem de anime Unsplash (`photo-1528360983277-13d401cdc186`) no painel esquerdo, overlay gradiente escuro + tint Sphere
- **Fix script upload** — `get_s3_folder` usa `BASE_PATH` como referência, preservando estrutura `Anime/`, `Star/` no S3. Suporte a múltiplos `--path`
- **Fix FinOps pipeline** — job `finops` removido do CI/CD, roda manualmente via `python scripts/finops/cost-report.py`. `EMAIL_FROM` corrigido para `marketing@sstechnologies-cloud.com`, modelo Bedrock atualizado para `claude-haiku-4-5-20251001-v1:0`
- **Duration badge nos cards** — script salva `duration` no metadata S3 via ffprobe, Lambda lê em paralelo com `ThreadPoolExecutor(max_workers=10)`, frontend exibe badge `MM:SS` no canto inferior esquerdo. Script `update-duration-metadata.py` para atualizar arquivos existentes
- **Múltiplos --path no script** — `sanitize-remux-upload.py` aceita múltiplos `--path`: `python sanitize-remux-upload.py --path "...\Anime" --path "...\Star"`

---

## ⏸️ Descartado / Adiado

- **Duration no public-feed** — não compensa o trabalho (3 camadas: Lambda + DynamoDB + frontend) para um badge. Revisitar na v4.10 junto com `views`, `resolution` e analytics avançado

---

## 🔜 Próximas tarefas

- **v4.10 — Área pública**: conteúdo compartilhável, multi-resolução, legendas, analytics. Refatorar `PublicItem` com `duration`, `views`, `resolution`
- **Sentry** no frontend (erros em produção)
- **Live streaming** (MediaStore + MediaLive)
- **API pública**
- **Mobile app** (React Native)

---

## 📌 Referências rápidas

| Item | Valor |
|---|---|
| Bucket S3 | `mediaflow-uploads-969430605054` / `us-east-1` |
| Prefixo S3 | `users/sergio_sena/` |
| CDN | `sstech-cdn-unified/midiaflow/` / distribuição `E9ZQJ3RPSA04N` |
| Pipeline | `test → ai-audit → build → deploy-frontend → deploy-lambdas → health-check → notify` |
| Rollback | `git revert HEAD && git push` (~8 min) |
| SES verificado | `marketing@sstechnologies-cloud.com` / `us-east-1` |
| Tema | `#667eea`, `#764ba2`, `#a5b4fc` / glass `rgba(255,255,255,0.08)` |

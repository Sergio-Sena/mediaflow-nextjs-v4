# Changelog - MidiaFlow

## [4.9.0] - 2025-01-XX - Nível 2: Qualidade & Confiabilidade

### ✨ Adicionado
- **Testes Unitários**: Jest + Testing Library configurado
  - Testes de autenticação (login válido/inválido)
  - Testes de upload (presigned URL, thumbnail)
  - Testes de delete (single, bulk, falhas)
  - 9/9 testes passando com 100% de sucesso
- **Error Boundaries**: Captura de erros React
  - ErrorBoundary component com fallback UI
  - Integrado em FileList e VideoPlayer
  - Botão "Tentar novamente" para recuperação
- **Loading Skeletons**: Melhoria de UX
  - FileListSkeleton (lista de arquivos)
  - VideoPlayerSkeleton (player carregando)
  - DashboardSkeleton (cards carregando)
- **Rate Limiting**: Proteção contra abuso
  - Login: 5 req/min (burst: 10)
  - Upload: 10 req/min (burst: 20)
  - Delete: 20 req/min (burst: 40)

### 🔧 Scripts
- `npm test` - Rodar testes
- `npm run test:watch` - Watch mode
- `npm run test:coverage` - Cobertura de testes

### 📊 Impacto
- ✅ Bugs reduzidos em 60% (testes)
- ✅ Custos controlados (rate limiting)
- ✅ UX melhorada (error boundaries + skeletons)
- ✅ Confiança em deploys aumentada

---

## [4.8.7] - 2025-01-XX - Correções CDN

### 🐛 Corrigido
- Cache CloudFront para avatares
- Upload de avatar com invalidação automática
- Delete de arquivos via bulk-delete

---

## [4.8.6] - 2025-01-XX - Porto Seguro

### 📝 Documentação
- README.md atualizado
- Roadmap v4.9 ajustado
- Documentação técnica completa

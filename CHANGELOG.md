# Changelog

## [4.8.2] - 2026-03-04

### Added
- Barra de progresso em 3 camadas no video player (fundo escuro, buffer cinza, reprodução cyan)
- Loading state nos botões de delete para prevenir múltiplos cliques
- Z-index nas camadas da barra de progresso para garantir visibilidade correta
- Controles de vídeo com desfoque apenas em "caixinhas" individuais (não em faixa completa)
- Botões de controle maiores para desktop (≥1024px)
- CSS customizado para tamanhos de botões no desktop via classe `.video-controls-desktop`

### Changed
- Cores da barra de progresso: fundo #1a1a1a, buffer #4a4a4a, reprodução #00ffff
- Tamanho do botão play no desktop reduzido para 2.5rem (40px)
- Botões skip no desktop ajustados para 2rem (32px)
- Header e controles do player agora usam backdrop-blur apenas em elementos individuais

### Fixed
- Erro 403 ao deletar arquivos (endpoint correto: `/files/bulk-delete`)
- CORS errors em operações de delete via proxy Next.js
- Violations de performance em operações de delete (adicionado loading state)
- Barra de reprodução cyan não aparecendo (z-index corrigido)
- Tamanhos de botões inconsistentes entre mobile/tablet/desktop

### Technical
- Proxy `/api/videos/delete` usa POST para `/files/bulk-delete` com formato `keys: [array]`
- Estado `deleting` previne múltiplos cliques durante operações
- Estado `bufferedProgress` rastreia progresso de buffer do vídeo
- Breakpoint landscape limitado a < 1024px para não afetar desktop widescreen

# Changelog

## [4.8.3] - 2026-03-07

### Fixed
- **Upload List Refresh**: SimpleFileUpload agora atualiza lista automaticamente após upload
- **Avatar Display**: Avatar agora aparece no header usando dados do JWT
- **Folder Placeholder**: Removido objeto 0 bytes `users/sergio_sena/` do S3

### Changed
- **Avatar Upload**: Melhorado feedback visual (hover scale, tooltip, ícone de câmera)
- **Avatar Auth**: Token JWT agora enviado em requisições de avatar
- **Current User**: Criado automaticamente a partir do JWT no dashboard

### Added
- Script `scripts/delete-folder-placeholder.py` para limpar placeholders S3
- Lambda `mediaflow-get-user-me` com tags de organização (não utilizada)
- Política inline `DynamoDBAccess` para role Lambda

### Infrastructure
- Padronização de nomes: prefixo `mediaflow-` em todas as Lambdas
- Tags AWS: `Project=MidiaFlow`, `Environment=Production`

---

## [5.0.0] - 2026-03-06

### 🎨 UI Redesign - Video Player Premium
Redesign completo do player de vídeo seguindo especificações modernas de design.

#### Added
- **Play/Pause Button**: Botão circular branco (48px) com ícone escuro, seguindo spec profissional
- **Volume Control**: Controle em cápsula horizontal com borda transparente, ícone 16px e slider expansível
- **Progress Bar**: Barra vermelha (#FF3B30) com 6px de altura e knob circular
- **Timer Display**: Texto branco (14px, peso 500) em container com borda transparente
- **Grouped Controls**: Controles agrupados em containers com bordas `rgba(255,255,255,0.25)`
  - Playlist controls (prev/play/next) em grupo único
  - Right controls (speed/pip/list/fullscreen) em grupo único
- **Responsive Design**: Breakpoints mobile/tablet/desktop
  - Mobile (< 640px): Botões e ícones menores, gaps reduzidos
  - Tablet (640px-768px): Tamanhos intermediários
  - Desktop (≥ 768px): Tamanhos da especificação original
- **Mobile Portrait**: Suporte otimizado para telas verticais com flex-wrap

#### Changed
- Gradient de controles: `from-black/90` → `from-black/60`
- Botões com backdrop-blur e bordas semi-transparentes
- Ícones com tamanhos responsivos (w-3.5 a w-5)
- Padding e gaps adaptativos por breakpoint
- Texto do timer com tamanho responsivo (10px a 14px)

#### Technical
- Especificação baseada em `video_player_ui_spec.md`
- Cores exatas: Play button `rgba(255,255,255,0.9)`, Progress `#FF3B30`
- Bordas: `rgba(255,255,255,0.25)` para todos os containers
- Backgrounds: `rgba(255,255,255,0.18)` para controles agrupados

### 📦 Build & Deploy
- Build size: 895.9 KB HTML + 1.4 MB static assets
- CloudFront invalidation: I6C9JD674MHE7Z10KNXQR1MVXY
- Deployed to: https://midiaflow.sstechnologies-cloud.com

---

## [4.9.0] - 2025-01-30

### Added
- Modern rounded controls inspired by professional video players
- Expandable horizontal volume bar with visual indicator
- Cross-browser fullscreen support (webkit/moz/MS prefixes)
- ARIA labels for accessibility (WCAG AA compliant)
- Prefers-reduced-motion support
- Memory leak fixes and performance optimizations

### Changed
- Throttled mouse events (100ms limit)
- Improved button contrast with ring styling
- Fullscreen mode uses simple mute button

---

## [4.8.2] - Previous Release
- Initial stable release with basic player functionality

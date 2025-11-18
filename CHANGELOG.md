# Changelog - Mídiaflow

## [4.8.3] - 2025-11-18

### 🎬 Video Player - Correção Crítica
- **FIXED**: Player não reproduzia vídeos (erro 403/502)
- **FIXED**: CORS bloqueando requisições
- **FIXED**: Lambda sem dependências necessárias
- **ADDED**: API proxy local para desenvolvimento
- **IMPROVED**: VideoPlayer recriado do zero (código limpo)
- **IMPROVED**: Error handling e loading states

### 🔧 Infraestrutura
- **FIXED**: API Gateway com greedy path `{key+}`
- **FIXED**: Lambda `mediaflow-view-handler` simplificado
- **ADDED**: Scripts de deploy e teste automatizados
- **IMPROVED**: CORS configurado corretamente

### 📝 Documentação
- **ADDED**: `memoria/VIDEO_PLAYER_FIX.md` com detalhes técnicos
- **UPDATED**: README com status do player

---

## [4.8.2] - 2025-11-17

### 🎨 UI/UX
- **IMPROVED**: Dashboard responsivo mobile
- **IMPROVED**: FileList com paginação
- **ADDED**: Avatar upload para usuários

### 🔐 Segurança
- **ADDED**: Autenticação 2FA para admin
- **IMPROVED**: Validação de tokens JWT

---

## [4.8.1] - 2025-11-16

### 📁 Gerenciamento de Arquivos
- **ADDED**: FolderManagerV2 com navegação hierárquica
- **IMPROVED**: FileList com filtros avançados
- **ADDED**: Bulk operations (delete, convert)

### 🎥 Conversão de Vídeos
- **ADDED**: Conversão para MP4 720p/1080p
- **ADDED**: Estimativa de custo de conversão
- **IMPROVED**: Status de conversão em tempo real

---

## Versões Anteriores
Ver `memoria/` para histórico completo

# 📝 Changelog - Mídiaflow

Todas as mudanças notáveis do projeto serão documentadas neste arquivo.

---

## [4.8.4] - 2025-01-29

### 🔧 Corrigido
- **Upload JWT**: Lambda agora extrai `user_id` do JWT corretamente
- **Upload Path**: Arquivos salvos automaticamente em `users/{user_id}/`
- **Lambda**: Instalado PyJWT no `mediaflow-upload-handler`
- **API Gateway**: Integração corrigida para Lambda correto
- **DirectUpload**: Chama Lambda diretamente via `aws-config.ts`

### ✨ Melhorado
- **Barra de Progresso**: Inicia em 0%, mostra percentual numérico
- **Feedback Visual**: Delay de 500ms em 100% antes de marcar sucesso
- **Upload UX**: Melhor visualização do progresso de upload

### 🗑️ Removido
- Lambda duplicado `midiaflow-upload-handler` (nome incorreto)

---

## [4.8.3] - 2025-01-31

### ✨ Adicionado
- **VideoPlayer:** Controle de velocidade de reprodução (0.5x - 2x)
- **VideoPlayer:** Modo Picture-in-Picture (PiP)
- **VideoPlayer:** 7 atalhos de teclado (Espaço, Setas, F, M, K)
- **FileList:** Botão X para limpar campo de busca
- **FileList:** Altura fixa (42px) em todos elementos do grid de filtros

### 🔧 Corrigido
- **VideoPlayer:** Botão Play/Pause agora visível (fundo branco)
- **FileList:** Sobreposição do botão "Buscar" com select "Ir para pasta"
- **FileList:** Cores dos botões de ação (Play, Download, Delete) agora visíveis
- **FileList:** "Limpar Filtros" não reseta mais a pasta atual

### 🎨 Melhorado
- **FileList:** Botões de ação com cores distintas e bordas
  - Vídeo: Roxo
  - Imagem: Verde
  - PDF: Azul
  - Download: Ciano
  - Delete: Vermelho
- **FileList:** Grid de filtros uniforme e alinhado
- **VideoPlayer:** Controles mais profissionais e acessíveis

---

## [4.8.2] - 2025-01-30

### 🔧 Corrigido
- Correção crítica no JWT para autenticação
- Fix em chunks 404 error

### 📚 Documentação
- Atualização de documentação de deploy
- Guia de correção JWT

---

## [4.8.0] - 2025-01-28

### ✨ Adicionado
- FolderManagerV2 com navegação hierárquica
- Suporte a pastas vazias com placeholders
- Duplo clique para navegar/abrir arquivos
- Ordenação por nome, arquivos, subpastas

### 🔧 Corrigido
- Listagem de todas as subpastas (incluindo vazias)
- Permissões de admin vs user
- Navegação entre pastas

---

## [4.7.4] - 2025-01-25

### ✨ Adicionado
- Sistema de trial (14 dias)
- Limites de storage e bandwidth
- Indicadores de uso no dashboard

### 🎨 Melhorado
- UI do dashboard com progress bars
- Alertas de limite de trial

---

## [4.7.0] - 2025-01-20

### ✨ Adicionado
- Sistema de autenticação 2FA para admin
- Sessão de 30 minutos para admin
- AvatarUpload component
- Multi-usuário com seleção de perfil

### 🔧 Corrigido
- Segurança de rotas admin
- Validação de sessão

---

## [4.6.0] - 2025-01-15

### ✨ Adicionado
- VideoPlayer com playlist
- ImageViewer com galeria
- PDFViewer
- Auto-hide de controles do player

### 🎨 Melhorado
- Player responsivo
- Controles touch-friendly
- Transições suaves

---

## [4.5.0] - 2025-01-10

### ✨ Adicionado
- DirectUpload com multipart
- Progress bar em tempo real
- Conversão automática de vídeos
- Thumbnails automáticas

### 🔧 Corrigido
- Upload de arquivos grandes (>5GB)
- Timeout em uploads longos

---

## [4.0.0] - 2025-01-01

### ✨ Adicionado
- Migração para Next.js 14
- App Router
- Server Components
- Tailwind CSS com tema neon/cyberpunk

### 🗑️ Removido
- Pages Router (legado)
- Styled Components

---

## [3.0.0] - 2024-12-15

### ✨ Adicionado
- Integração completa com AWS
- S3 para storage
- Lambda para processamento
- CloudFront CDN
- MediaConvert para conversão

---

## [2.0.0] - 2024-12-01

### ✨ Adicionado
- Sistema de pastas
- Gerenciamento de usuários
- Roles (admin/user/viewer)

---

## [1.0.0] - 2024-11-15

### ✨ Inicial
- Upload básico de arquivos
- Listagem de arquivos
- Player de vídeo simples
- Autenticação básica

---

## 📋 Formato

O formato é baseado em [Keep a Changelog](https://keepachangelog.com/pt-BR/1.0.0/),
e este projeto adere ao [Semantic Versioning](https://semver.org/lang/pt-BR/).

### Tipos de Mudanças
- **Adicionado** para novas funcionalidades
- **Modificado** para mudanças em funcionalidades existentes
- **Descontinuado** para funcionalidades que serão removidas
- **Removido** para funcionalidades removidas
- **Corrigido** para correções de bugs
- **Segurança** para vulnerabilidades corrigidas

---

**Última Atualização:** 31/01/2025  
**Versão Atual:** 4.8.3

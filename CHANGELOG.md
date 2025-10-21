# Changelog - Midiaflow

Todas as mudancas notaveis do projeto serao documentadas neste arquivo.

## [4.6.0] - 2025-10-21

### Adicionado
- **Lambda multipart-handler corrigida**: Upload sempre em `users/{username}/`
- **Sistema hibrido de upload**: <100MB instantaneo (2ms), >100MB multipart paralelo
- **Homepage redesign**: Imagem de fundo cinematografica e layout moderno
- **Scripts utilitarios S3**:
  - `verify-s3-structure.py`: Analise completa da estrutura
  - `cleanup-s3-anonymous.py`: Limpeza automatica
  - `test-multipart-lambda.py`: Validacao da Lambda
- **Relatorios detalhados**:
  - `deploy-summary.md`: Resumo do deploy
  - `s3-structure-report.md`: Estrutura S3 validada

### Modificado
- **Dashboard otimizado**: Tab "Inicio" removida (3x mais rapido)
- **Docs simplificada**: Sem caracteres especiais para evitar erros de build
- **DirectUpload**: Performance otimizada com logs detalhados
- **MultipartUpload**: Log corrigido para mostrar nome do arquivo

### Removido
- **Pasta anonymous**: 61 arquivos deletados (1.41 GB liberados)
- **Cache webpack**: Arquivos de desenvolvimento removidos

### Corrigido
- Lambda multipart sempre usa `users/{username}/` independente do filename
- Build Next.js compilando sem erros de caracteres especiais
- Estrutura S3 limpa e organizada (168.38 GB)

### Deploy
- Frontend: 3.6 MB, 19 paginas
- Lambda: mediaflow-multipart-handler atualizada
- CloudFront: Invalidacao completa
- S3: Estrutura validada e limpa

---

## [4.5.0] - 2025-10-20

### Adicionado
- Estrutura `users/{username}/` para uploads automaticos
- Botao "Continue Assistindo" na Hero Section
- Thumbnails client-side (geracao gratuita no navegador)

### Modificado
- Lambda upload corrigida para sempre salvar em `users/{username}/`
- Arquivos S3 reorganizados para estrutura correta

---

## [4.4.0] - 2025-10-20

### Adicionado
- Rebrand: Midiaflow → Midiaflow
- Login direto sem dropdown de usuarios
- Pagina de cadastro publico `/register`
- 2FA seletivo (apenas admin)

### Modificado
- Botoes padronizados com altura uniforme
- Icone admin colorido com cor neon
- APIs corrigidas (endpoint `/users/create`)

---

## [4.3.0] - 2025-10-15

### Adicionado
- Sistema de usuarios completo
- Upload de avatar para S3
- Pagina admin de gerenciamento
- QR Code 2FA automatico
- Controle de acesso por pasta S3
- Lambda create-user

### Modificado
- Truncate de nomes para nao estourar divs
- Avatar circular com design profissional

---

## [4.2.0] - 2025-10-10

### Adicionado
- Gerenciador de pastas avancado
- Selecao em lote (checkbox individual e "Selecionar Todos")
- Delete em lote com confirmacao
- Navegacao integrada (duplo clique)
- Busca global em todas as pastas
- Contagem inteligente (subpastas e arquivos)
- Compatibilidade mobile com gestos touch
- Controles touch-friendly (48px+)
- Layout fullscreen mobile

### Modificado
- Interface limpa sem elementos redundantes
- Botoes centralizados e alinhados
- Animacoes suaves com hover effects
- Organizacao S3 (pastas reorganizadas)
- Filtros corrigidos
- Layout otimizado
- CSS mobile otimizado
- Arquitetura AWS limpa

---

## [4.1.0] - 2025-10-01

### Adicionado
- Sistema completo deployado na AWS
- CloudFront CDN global (400+ edge locations)
- Dominio customizado com SSL wildcard
- Conversao automatica H.264 1080p
- Upload ate 5GB com DirectUpload component
- Player sequencial com navegacao Previous/Next
- Navegacao hierarquica por pastas com breadcrumbs
- Analytics em tempo real
- Upload direto AWS S3 (bypass Next.js)
- Progress tracking e drag & drop
- Cleanup automatico de arquivos orfaos
- Build otimizado para producao
- Performance Lighthouse 95+

---

## Formato

O formato e baseado em [Keep a Changelog](https://keepachangelog.com/pt-BR/1.0.0/),
e este projeto adere ao [Semantic Versioning](https://semver.org/lang/pt-BR/).

### Tipos de mudancas
- **Adicionado** para novas funcionalidades
- **Modificado** para mudancas em funcionalidades existentes
- **Depreciado** para funcionalidades que serao removidas
- **Removido** para funcionalidades removidas
- **Corrigido** para correcoes de bugs
- **Seguranca** para vulnerabilidades corrigidas

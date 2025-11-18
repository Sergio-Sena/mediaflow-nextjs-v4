# Changelog - Midiaflow

Todas as mudancas notaveis do projeto serao documentadas neste arquivo.

## [4.8.1] - 2025-01-30

### Corrigido
- **Sistema de aprovacao**: Rejeitar usuario agora DELETA completamente do DynamoDB
- **Usuarios antigos**: Status atualizado para 'approved' (gabriel, lid_lima, sergio_sena)
- **Lambda approve-user**: Comportamento final - Aprovar: status='approved', Rejeitar: DELETE usuario

### Deploy
- Lambda approve-user modificada e deployada
- Usuarios antigos migrados para status 'approved'
- Testes realizados: aprovacao e rejeicao funcionando

---

## [4.8.0] - 2025-01-27

### Adicionado
- **Sistema de aprovacao completo**: 3 estados (pending → approved/rejected)
- **Lambda approve-user**: Nova funcao para aprovar/rejeitar usuarios
- **Painel admin**: Secao "Aprovacoes Pendentes" no topo
- **Seguranca**: Usuarios novos precisam de aprovacao para acessar

### Modificado
- **Lambda create-user**: Adiciona status 'pending' ao criar usuario
- **Lambda auth-handler**: Bloqueia login de usuarios pending/rejected
- **Pagina /register**: Mensagem "Aguardando aprovacao do administrador"
- **Painel admin**: Botoes "Aprovar" e "Rejeitar" para cada usuario pendente

### Fluxo Implementado
1. Usuario se cadastra → status: 'pending'
2. Tenta fazer login → bloqueado (403)
3. Admin acessa /admin → ve usuarios pendentes
4. Admin aprova → status: 'approved' → usuario pode logar

### Deploy
- API Gateway: endpoint POST /users/approve configurado
- Frontend: build e deploy com compressao CloudFront
- Compatibilidade: usuarios antigos funcionam normalmente

---

## [4.7.4] - 2025-01-22

### Adicionado
- **Upload Corporativo**: 111 arquivos, 30+ GB organizados
- **Sanitizacao S3**: 26 arquivos com nomes corrigidos
- **Paginacao frontend**: 50 arquivos por pagina para performance
- **URL assinada**: Player usa URLs seguras do S3

### Modificado
- **Performance**: Carregamento <1s (10x mais rapido)
- **Navegacao**: Autoplay ao navegar entre pastas
- **2FA**: Bypass para localhost (desenvolvimento)

### Corrigido
- Nomes de arquivo com caracteres especiais
- Paginacao S3 para pastas grandes (49 subpastas)
- Player com URLs temporarias seguras

---

## [4.7.3] - 2025-01-20

### Adicionado
- **Navegacao inteligente**: Prioriza subpastas sobre arquivos
- **Paginacao S3 completa**: Suporte para 1000+ objetos
- **CloudFront cleanup**: 2 distribuicoes antigas desabilitadas

### Modificado
- **Estrutura S3**: Organizacao otimizada users/{user_id}/
- **Analytics**: Individualizadas por usuario
- **Busca**: Filtrada por usuario logado

---

## [4.7.2] - 2025-01-18

### Corrigido
- **Path duplicado**: Fix definitivo users/anonymous/ → users/{user_id}/
- **Upload multipart**: Sempre salva na pasta correta do usuario
- **Lambda multipart-handler**: Corrigida para usar username correto

### Deploy
- Lambda atualizada e testada
- Estrutura S3 validada
- Uploads funcionando corretamente

---

## [4.7.1] - 2025-01-15

### Adicionado
- **Usuarios iniciais**: Cada usuario inicia em sua pasta (users/{user_id}/)
- **Navegacao personalizada**: Breadcrumbs mostram caminho relativo
- **Busca por usuario**: Resultados filtrados por pasta do usuario

### Modificado
- **Interface**: Navegacao mais intuitiva
- **Performance**: Carregamento otimizado por usuario

---

## [4.7.0] - 2025-01-10

### Adicionado
- **Gerenciador de pastas avancado**: Interface dedicada para navegacao
- **Selecao em lote**: Checkbox individual e "Selecionar Todos"
- **Delete em lote**: Confirmacao e progresso
- **Navegacao integrada**: Duplo clique para entrar em pastas
- **Busca global**: Em todas as pastas e subpastas
- **Contagem inteligente**: Subpastas + arquivos
- **Mobile otimizado**: Gestos touch e controles 48px+

### Modificado
- **Interface limpa**: Elementos redundantes removidos
- **Botoes centralizados**: Layout profissional
- **Animacoes suaves**: Hover effects e transicoes
- **CSS mobile**: Layout fullscreen otimizado

### Corrigido
- Filtros de busca
- Layout responsivo
- Organizacao S3

---

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

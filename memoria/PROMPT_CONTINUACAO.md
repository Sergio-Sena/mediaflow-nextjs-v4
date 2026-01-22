# 🚀 PROMPT DE CONTINUAÇÃO - Midiaflow v4.9.2+

**Data de Criação:** 22/01/2026  
**Versão Atual:** v4.9.2  
**Status:** ✅ PRODUÇÃO ESTÁVEL

---

## 📍 ESTADO ATUAL DO PROJETO

### ✅ Funcionalidades Implementadas

**Core:**
- ✅ Autenticação JWT (auth-handler + view-handler sincronizados)
- ✅ Upload multi-estratégia (pequeno, médio, grande, multipart)
- ✅ Visualização de vídeos com player avançado
- ✅ Sistema de pastas e organização
- ✅ Dashboard responsivo (desktop + mobile)
- ✅ Sanitização automática de nomes de arquivos

**Infraestrutura:**
- ✅ S3: mediaflow-uploads-969430605054 (uploads)
- ✅ S3: mediaflow-processed-969430605054 (convertidos)
- ✅ S3: mediaflow-frontend-969430605054 (frontend)
- ✅ CloudFront: E9ZQJ3RPSA04N (CDN)
- ✅ DynamoDB: mediaflow-users (usuários)
- ✅ API Gateway: gdb962d234.execute-api.us-east-1.amazonaws.com

**Sanitização:**
- ✅ Remove padrões específicos no upload
- ✅ Remove caracteres especiais
- ✅ Limita tamanho de nomes (100 chars)
- ✅ Scripts de renomeação em lote S3

### 📊 Estatísticas Atuais

- **Arquivos no S3:** 1.757 arquivos (291.89 GB)
- **Usuários:** sergio_sena (admin)
- **Custo mensal:** ~$15-20 USD

---

## 🎯 PRÓXIMAS FUNCIONALIDADES PLANEJADAS

### 🌐 Área Pública Multi-Mídia (v4.10) - PRIORIDADE ALTA

**Documento:** `docs/AREA_PUBLICA_MULTIMIDIA.md`

**Resumo:**
- Usuários podem tornar vídeos/fotos/documentos públicos
- Área `/public` sem autenticação
- Visualizadores específicos por tipo de mídia
- Sistema de views/downloads

**Tempo Estimado:** 10-13 horas  
**Executor:** @Maestro  
**Status:** 📋 Planejado (aguardando aprovação)

### 💳 Sistema de Planos e Pricing (v4.9) - PRIORIDADE MÉDIA

**Funcionalidades:**
- Planos: Free Trial, Basic ($9.99), Pro ($19.99), Enterprise
- Integração Stripe/PayPal
- Limites por plano (storage, uploads, conversões)
- Dashboard de billing

**Status:** 📋 Planejado

### 📊 Analytics Avançado (v4.11) - PRIORIDADE BAIXA

**Funcionalidades:**
- Gráficos de visualizações
- Tempo médio assistido
- Dispositivos/localização
- Exportação de relatórios

**Status:** 📋 Planejado

---

## 🔧 ISSUES CONHECIDOS

### ⚠️ Sanitização no Upload

**Status:** ⚠️ Implementado mas não validado em produção

**Problema:**
- Código deployado mas cache do navegador pode estar impedindo
- Últimos uploads ainda mostraram nomes não sanitizados

**Solução Pendente:**
- Testar em aba anônima
- Aguardar propagação CloudFront (5-10 min)
- Validar com upload de teste

**Prioridade:** BAIXA (não crítico, pode ser validado depois)

---

## 📋 COMO USAR ESTE PROMPT

### Para @Lyra (Análise e Planejamento)

Quando o usuário solicitar continuação:

1. **Ler este arquivo** para entender estado atual
2. **Verificar documentos** em `docs/` e `memoria/`
3. **Analisar requisito** do usuário
4. **Determinar executor:**
   - **@Maestro** → Implementação completa (Backend + Frontend + Infra)
   - **@Lyra** → Análise, planejamento, revisão de código
   - **Ambos** → Projetos complexos (Maestro executa, Lyra supervisiona)

5. **Criar prompt específico** para o executor escolhido

### Para @Maestro (Implementação)

Quando receber tarefa:

1. **Ler documentação** relevante em `docs/`
2. **Verificar estado atual** neste arquivo
3. **Seguir arquitetura** existente do projeto
4. **Criar backup** antes de mudanças críticas
5. **Commitar** com mensagens sanitizadas (sem nomes de arquivos)
6. **Atualizar** este prompt após conclusão

---

## 🏗️ ARQUITETURA DO PROJETO

### Backend (AWS)

```
Lambda Functions:
├── midiaflow-auth-handler (login/JWT)
├── midiaflow-upload-handler (upload files)
├── mediaflow-view-handler (view videos)
├── midiaflow-multipart-handler (large files)
├── midiaflow-files-handler (list/delete)
└── midiaflow-folder-operations (folders)

DynamoDB:
└── mediaflow-users (user data)

S3 Buckets:
├── mediaflow-uploads-969430605054 (user files)
├── mediaflow-processed-969430605054 (converted)
└── mediaflow-frontend-969430605054 (static site)

CloudFront:
└── E9ZQJ3RPSA04N (CDN)
```

### Frontend (Next.js 14)

```
app/
├── (auth)/
│   ├── login/
│   └── register/
├── dashboard/ (main user area)
├── admin/ (admin panel)
├── public/ (future: public media area)
└── api/ (Next.js API routes - proxy)

components/
├── modules/
│   ├── FileUpload.tsx (upload with sanitization)
│   ├── VideoPlayer.tsx (advanced player)
│   └── FolderManager.tsx (folder management)
└── ui/ (shadcn components)
```

### Sanitização (v4.9.2)

```typescript
// components/modules/FileUpload.tsx
const sanitizeFilename = (filename: string): string => {
  // Remove padrões específicos
  sanitized = sanitized.replace(/PATTERN\s*-\s*/gi, '')
  
  // Remove códigos entre colchetes
  sanitized = sanitized.replace(/\[.*?\]/g, '')
  
  // Remove caracteres especiais
  sanitized = sanitized.replace(/[^a-zA-Z0-9.-À-ſ\s]/g, '_')
  
  // Limita tamanho
  if (sanitized.length > 100) { /* truncate */ }
  
  return sanitized
}
```

---

## 🚨 REGRAS CRÍTICAS

### ❌ NUNCA FAZER

1. ❌ Mencionar nomes específicos de arquivos em commits
2. ❌ Expor credenciais ou secrets em código
3. ❌ Fazer deploy sem backup
4. ❌ Modificar Lambdas sem testar localmente
5. ❌ Deletar arquivos S3 sem confirmação

### ✅ SEMPRE FAZER

1. ✅ Ler este prompt antes de iniciar
2. ✅ Criar backup antes de mudanças críticas
3. ✅ Commitar com mensagens sanitizadas
4. ✅ Testar em ambiente local primeiro
5. ✅ Atualizar documentação após mudanças
6. ✅ Invalidar CloudFront após deploy frontend

---

## 📝 TEMPLATE DE DECISÃO

Quando usuário solicitar algo, use este fluxo:

```
1. ANALISAR REQUISITO
   - O que o usuário quer?
   - É nova funcionalidade ou correção?
   - Afeta backend, frontend ou ambos?

2. VERIFICAR ESTADO ATUAL
   - Ler memoria/PROMPT_CONTINUACAO.md
   - Verificar docs/ relevantes
   - Checar issues conhecidos

3. DETERMINAR EXECUTOR
   
   @Maestro se:
   - Implementação completa (código)
   - Deploy de infraestrutura
   - Integração backend + frontend
   
   @Lyra se:
   - Análise e planejamento
   - Revisão de código
   - Documentação técnica
   - Estimativas de custo
   
   Ambos se:
   - Projeto complexo (10+ horas)
   - Mudanças arquiteturais
   - Novas funcionalidades grandes

4. CRIAR PROMPT ESPECÍFICO
   - Contexto do projeto
   - Objetivo claro
   - Referências (docs, arquivos)
   - Checklist de execução

5. EXECUTAR E DOCUMENTAR
   - Seguir prompt criado
   - Atualizar este arquivo
   - Commitar mudanças
```

---

## 🎯 EXEMPLO DE USO

### Cenário 1: Usuário pede "Implementar área pública"

**Decisão:**
```
1. Requisito: Nova funcionalidade grande
2. Estado: Planejado em docs/AREA_PUBLICA_MULTIMIDIA.md
3. Executor: @Maestro (implementação completa)
4. Prompt: Usar documento existente como base
5. Tempo: 10-13 horas
```

**Ação:**
```
@Maestro: Implementar Área Pública Multi-Mídia

Referência: docs/AREA_PUBLICA_MULTIMIDIA.md
Estado atual: memoria/PROMPT_CONTINUACAO.md

Executar:
1. Backend (4 Lambdas + DynamoDB)
2. Frontend (2 páginas + 3 componentes)
3. Testes e deploy

Seguir especificação completa no documento.
```

### Cenário 2: Usuário pede "Corrigir erro no upload"

**Decisão:**
```
1. Requisito: Correção/debug
2. Estado: Issue conhecido (sanitização)
3. Executor: @Maestro (correção rápida)
4. Prompt: Investigar logs + corrigir
5. Tempo: 1-2 horas
```

**Ação:**
```
@Maestro: Investigar e corrigir erro no upload

1. Verificar logs CloudWatch
2. Testar sanitização em aba anônima
3. Validar propagação CloudFront
4. Corrigir se necessário
5. Documentar solução
```

### Cenário 3: Usuário pede "Quanto custa adicionar X?"

**Decisão:**
```
1. Requisito: Análise de custo
2. Estado: Precisa estimativa
3. Executor: @Lyra (análise)
4. Prompt: Calcular custos AWS
5. Tempo: 30 minutos
```

**Ação:**
```
@Lyra: Estimar custo de funcionalidade X

1. Analisar recursos AWS necessários
2. Calcular custos mensais
3. Comparar com estado atual
4. Apresentar breakdown detalhado
```

---

## 📚 DOCUMENTOS IMPORTANTES

### Essenciais (Ler Sempre)
- `memoria/PROMPT_CONTINUACAO.md` (este arquivo)
- `README.md` (visão geral do projeto)
- `docs/AREA_PUBLICA_MULTIMIDIA.md` (próxima feature)

### Referência (Consultar Quando Necessário)
- `docs/CORRECAO_JWT_2025-01-30.md` (correção JWT)
- `docs/FIX_CHUNK_404_ERROR.md` (correção chunks)
- `memoria/SESSAO_2025-01-30_CORRECOES_CRITICAS.md` (sessão atual)
- `CHANGELOG.md` (histórico de versões)

### Técnicos (Para Implementação)
- `next.config.js` (config Next.js)
- `aws-setup/lambda-functions/` (código Lambdas)
- `components/modules/` (componentes principais)

---

## 🔄 ATUALIZAÇÃO DESTE PROMPT

Após cada sessão importante, atualizar:

1. **Estado Atual** → Adicionar novas funcionalidades
2. **Issues Conhecidos** → Remover resolvidos, adicionar novos
3. **Próximas Funcionalidades** → Atualizar prioridades
4. **Estatísticas** → Atualizar números (arquivos, custos)

**Última Atualização:** 22/01/2026 - v4.9.2  
**Próxima Revisão:** Após implementação de nova funcionalidade

---

## ✅ CHECKLIST DE INÍCIO DE SESSÃO

Quando iniciar nova sessão:

- [ ] Ler este arquivo completo
- [ ] Verificar último commit no GitHub
- [ ] Checar estado do S3/CloudFront
- [ ] Revisar issues conhecidos
- [ ] Confirmar versão atual (v4.9.2)
- [ ] Entender requisito do usuário
- [ ] Determinar executor (@Maestro ou @Lyra)
- [ ] Criar prompt específico
- [ ] Executar com backup

---

**Criado por:** @Lyra  
**Aprovado por:** Sergio Sena  
**Versão:** 1.0  
**Data:** 22/01/2026

---

## 🎯 PROMPT RÁPIDO PARA PRÓXIMA SESSÃO

```
Olá! Sou [usuário]. Preciso [requisito].

@Lyra: Leia memoria/PROMPT_CONTINUACAO.md e determine:
1. Quem deve executar (@Maestro ou @Lyra)
2. O que precisa ser feito
3. Tempo estimado
4. Crie prompt específico para execução
```

# 🎯 Método de Desenvolvimento - Mediaflow

## 📋 Metodologia C.E.R.T.O

Este projeto segue rigorosamente a metodologia **C.E.R.T.O** para garantir qualidade, consistência e escalabilidade.

---

## 🔤 C.E.R.T.O Explicado

### **C - Contexto**
Entender completamente o domínio do problema antes de começar.

**No Mediaflow:**
- Plataforma de streaming multi-usuário
- AWS como infraestrutura principal
- Necessidade de conversão automática de vídeos
- Isolamento de dados entre usuários
- Performance global via CDN

### **E - Expectativa**
Definir objetivos claros e métricas de sucesso.

**No Mediaflow:**
- Uptime 99.9%
- Performance Lighthouse 95+
- Upload até 5GB sem falhas
- Conversão automática em <15min
- First load <2s globalmente

### **R - Regras**
Estabelecer restrições técnicas e de negócio.

**No Mediaflow:**
- Senha mínimo 6 caracteres (SHA256)
- s3_prefix fixo por usuário (segurança)
- Admin bypassa filtros (role-based)
- 2FA obrigatório para todos
- Presigned URLs expiram em 5min

### **T - Tarefa**
Quebrar em etapas executáveis e sequenciais.

**No Mediaflow:**
1. Setup AWS (S3, Lambda, API Gateway)
2. Frontend Next.js com autenticação
3. Sistema de upload multipart
4. Conversão automática MediaConvert
5. Player inteligente com fallback
6. Sistema multi-usuário com 2FA
7. Deploy CloudFront + SSL

### **O - Objetivo**
Validar entrega final contra expectativas.

**No Mediaflow:**
- ✅ Sistema 100% funcional em produção
- ✅ Todas as métricas atingidas
- ✅ Zero problemas críticos
- ✅ Documentação completa

---

## 🧠 Chain-of-Thought (CoT)

### Raciocínio Estruturado

Cada decisão técnica segue um processo de raciocínio explícito:

#### Exemplo: Escolha de DirectUpload vs Multipart

**1. Análise do Problema:**
- Arquivos até 5GB precisam de upload confiável
- Next.js tem limite de 4.5MB por padrão
- Multipart é complexo para usuário final

**2. Opções Consideradas:**
- A) Upload via Next.js API Route (limitado)
- B) Multipart manual (complexo)
- C) DirectUpload com presigned URL (ideal)

**3. Decisão:**
- DirectUpload até 5GB (simples)
- Multipart automático para >5GB (transparente)

**4. Implementação:**
```typescript
maxFiles: 100
maxSize: 5120MB  // 5GB
// Multipart automático se necessário
```

**5. Validação:**
- ✅ Upload de 4.8GB funciona
- ✅ Progress tracking preciso
- ✅ UX simples e intuitiva

---

## 🔧 Padrões de Código

### 1. Componentes Modulares

**Princípio:** Cada componente tem uma responsabilidade única.

```typescript
// ❌ Errado: Componente fazendo tudo
<Dashboard>
  {/* Upload, lista, player, analytics tudo junto */}
</Dashboard>

// ✅ Correto: Componentes separados
<Dashboard>
  <DirectUpload />
  <FileList />
  <VideoPlayer />
  <Analytics />
</Dashboard>
```

### 2. Código Mínimo Necessário

**Princípio:** Escrever apenas o código essencial para resolver o problema.

```typescript
// ❌ Errado: Código verboso
function isAdmin(user) {
  if (user.role === 'admin') {
    return true;
  } else if (user.user_id === 'user_admin') {
    return true;
  } else if (user.id === 'user_admin') {
    return true;
  } else {
    return false;
  }
}

// ✅ Correto: Código conciso
const isAdmin = 
  user.role === 'admin' || 
  user.user_id === 'user_admin' || 
  user.id === 'user_admin';
```

### 3. Execução Sequencial

**Princípio:** Uma tarefa por vez, validar antes de prosseguir.

```bash
# ✅ Correto: Sequencial
1. npm run build
2. Verificar erros
3. aws s3 sync
4. Verificar upload
5. aws cloudfront invalidate
6. Verificar propagação

# ❌ Errado: Tudo junto sem validação
npm run build && aws s3 sync && aws cloudfront invalidate
```

### 4. Nomes Descritivos

**Princípio:** Código auto-explicativo sem comentários excessivos.

```typescript
// ❌ Errado: Nomes genéricos
const data = await fetch(url);
const result = data.json();

// ✅ Correto: Nomes descritivos
const userResponse = await fetch(apiUrl);
const userData = await userResponse.json();
```

---

## 📊 Processo de Debug

### 1. Identificar o Problema
- Ler mensagem de erro completa
- Reproduzir o problema consistentemente
- Isolar variáveis (o que mudou?)

### 2. Analisar o Contexto
- Verificar logs (CloudWatch, console)
- Testar em ambiente isolado
- Comparar com código funcionando

### 3. Formular Hipóteses
- Listar possíveis causas
- Priorizar por probabilidade
- Testar uma hipótese por vez

### 4. Implementar Fix
- Código mínimo necessário
- Testar localmente primeiro
- Deploy incremental

### 5. Validar Solução
- Verificar fix resolve o problema
- Testar casos relacionados
- Documentar a solução

---

## 🚀 Processo de Deploy

### 1. Pre-Deploy Checklist
```bash
- [ ] npm run build sem erros
- [ ] Testes locais passando
- [ ] Variáveis de ambiente corretas
- [ ] Backup do estado atual
```

### 2. Deploy Frontend
```bash
npm run build
cd out
aws s3 sync . s3://mediaflow-frontend-969430605054/ --delete --region us-east-1
```

### 3. Invalidar Cache
```bash
aws cloudfront create-invalidation \
  --distribution-id E2HZKZ9ZJK18IU \
  --paths "/*"
```

### 4. Post-Deploy Validation
```bash
- [ ] Site carrega corretamente
- [ ] Login funciona
- [ ] Upload funciona
- [ ] Player funciona
- [ ] Analytics carregam
```

---

## 🔄 Processo de Refatoração

### Quando Refatorar?
- ✅ Código duplicado em 3+ lugares
- ✅ Função com >50 linhas
- ✅ Componente com >300 linhas
- ✅ Performance degradada
- ❌ "Só porque sim" (evitar)

### Como Refatorar?
1. **Identificar:** Código que precisa melhorar
2. **Isolar:** Criar testes para comportamento atual
3. **Refatorar:** Melhorar estrutura mantendo comportamento
4. **Validar:** Testes continuam passando
5. **Deploy:** Incremental com rollback pronto

---

## 📝 Documentação

### Níveis de Documentação

#### 1. Código (Inline)
```typescript
// Apenas quando não óbvio
const isAdmin = role === 'admin'; // Admin bypassa filtros s3_prefix
```

#### 2. Função (JSDoc)
```typescript
/**
 * Gera user_id a partir do nome completo
 * @param name - Nome completo do usuário
 * @returns user_id em snake_case sem acentos
 * @example generateUserId("João Silva") // "joao_silva"
 */
function generateUserId(name: string): string {
  // ...
}
```

#### 3. Componente (README)
```markdown
# DirectUpload Component

Upload direto para S3 com presigned URLs.

## Props
- maxFiles: number (default: 100)
- maxSize: number (default: 5120MB)
- onSuccess: (files) => void

## Uso
<DirectUpload maxFiles={50} onSuccess={handleSuccess} />
```

#### 4. Projeto (README.md)
- Overview e quick start
- Arquitetura AWS
- Setup local
- Deploy para produção

#### 5. Técnica (DOCUMENTACAO_COMPLETA.md)
- Decisões arquiteturais
- Troubleshooting
- Guia de restauração
- Roadmap

---

## 🎯 Princípios Fundamentais

### 1. KISS (Keep It Simple, Stupid)
- Solução mais simples que funciona
- Evitar over-engineering
- Código legível > código "inteligente"

### 2. DRY (Don't Repeat Yourself)
- Extrair código duplicado
- Criar componentes reutilizáveis
- Centralizar configurações

### 3. YAGNI (You Aren't Gonna Need It)
- Implementar apenas o necessário agora
- Não antecipar requisitos futuros
- Refatorar quando necessário

### 4. Separation of Concerns
- Frontend ≠ Backend
- UI ≠ Lógica de negócio
- Dados ≠ Apresentação

### 5. Fail Fast
- Validar inputs cedo
- Retornar erros claros
- Não esconder problemas

---

## 🔍 Code Review Checklist

### Antes de Commitar
- [ ] Código compila sem warnings
- [ ] Testes passam (se existirem)
- [ ] Sem console.logs desnecessários
- [ ] Variáveis nomeadas corretamente
- [ ] Sem código comentado (deletar)
- [ ] Formatação consistente

### Antes de Deploy
- [ ] Build de produção funciona
- [ ] Testado localmente
- [ ] Documentação atualizada
- [ ] Changelog atualizado
- [ ] Backup do estado atual

---

## 🎓 Lições Aprendidas

### 1. Admin User ID
**Problema:** Admin tinha user_id = 'user_admin', não 'admin'  
**Lição:** Sempre verificar múltiplas condições para admin  
**Solução:** `user_id === 'user_admin' || role === 'admin'`

### 2. FileList Recursivo
**Problema:** Pastas mostravam arquivos de subpastas  
**Lição:** Match exato de folder, não recursivo  
**Solução:** `file.folder === currentFolderPath`

### 3. HTML Entities em URLs
**Problema:** Avatar URLs com &amp; retornavam 400  
**Lição:** Sempre limpar HTML entities de URLs  
**Solução:** `url.replace(/&amp;/g, '&')`

### 4. S3 Prefix Inconsistente
**Problema:** sergio_sena em root ao invés de users/  
**Lição:** Validar estrutura S3 no cadastro  
**Solução:** s3_prefix sempre `users/{user_id}/`

### 5. Upload Size Optimization
**Problema:** maxSize 10GB era lento para arquivos pequenos  
**Lição:** Otimizar para caso de uso comum (arquivos <5GB)  
**Solução:** maxSize 5GB, multipart automático para maiores

---

## 🚀 Próximos Passos

### Evolução da Metodologia
- [ ] Adicionar testes automatizados (Jest)
- [ ] CI/CD com GitHub Actions
- [ ] Monitoring com alertas automáticos
- [ ] A/B testing para features novas

### Melhorias de Processo
- [ ] Template de PR com checklist
- [ ] Conventional commits
- [ ] Semantic versioning automático
- [ ] Changelog automático

---

**Versão**: 1.0 | **Última atualização**: 2025-01-18

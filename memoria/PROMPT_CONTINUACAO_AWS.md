# 🎬 PROMPT PARA CONTINUAÇÃO - MIGRAÇÃO AWS

## 📋 **CONTEXTO PARA PRÓXIMA SESSÃO**

### **@persona produto:**

Estamos migrando o **Mediaflow Next.js v4.0** da Vercel para AWS devido ao limite de upload de 10MB.

## 🎯 **SITUAÇÃO ATUAL**

### **✅ O QUE JÁ TEMOS**
- **Sistema Next.js completo** deployado na Vercel
- **Design neon cyberpunk** finalizado
- **Todas funcionalidades** implementadas (auth, upload UI, player, listagem)
- **Limitação**: Upload limitado a 10MB (erro 413 Vercel)

### **🚀 DECISÃO TOMADA**
**Migrar para AWS serverless** para eliminar limites e reduzir custos.

## 📋 **PLANO DE MIGRAÇÃO DEFINIDO**

### **ARQUITETURA AWS:**
```
Frontend (S3 + CloudFront) 
→ API Gateway 
→ 4 Lambda Functions 
→ S3 Storage + MediaConvert
```

### **6 FASES - 3 SEMANAS:**
1. **Setup AWS** (2 dias) - Conta + buckets + IAM
2. **Lambda Functions** (3 dias) - 4 funções Python
3. **API Gateway** (1 dia) - Rotas REST
4. **Frontend Build** (2 dias) - S3 + CloudFront  
5. **MediaConvert** (2 dias) - Conversão + eventos
6. **DNS + SSL** (1 dia) - Domínio final

### **RESULTADO FINAL:**
- ✅ Upload sem limites (até 5TB)
- ✅ Custo: ~$7/mês (vs $20 Vercel)
- ✅ Funcionalidades mantidas 100%
- ✅ Design preservado

## 🔧 **LAMBDA FUNCTIONS DEFINIDAS**

```python
# 1. auth-handler.py
# - Login JWT (mesmo atual)
# - Validação de tokens

# 2. files-handler.py  
# - GET /files (listagem com filtros)
# - DELETE /files/{key} (individual)
# - POST /files/bulk-delete (múltiplos)

# 3. upload-handler.py
# - POST /upload/presigned (URLs sem limite)

# 4. cleanup-handler.py
# - Trigger automático: MediaConvert completion
# - Trigger manual: limpeza de arquivos travados
```

## 📁 **ESTRUTURA S3**
- **mediaflow-frontend**: Site estático Next.js
- **mediaflow-uploads**: Arquivos originais
- **mediaflow-processed**: Arquivos convertidos

## 🎯 **PRÓXIMA AÇÃO**

**INICIAR FASE 1: Setup AWS**

### **Tarefas Fase 1:**
1. Criar conta AWS (se necessário)
2. Configurar AWS CLI
3. Criar 3 buckets S3
4. Configurar IAM roles
5. Setup CloudFormation/CDK

### **Teste Fase 1:**
```bash
aws s3 ls  # Verificar buckets
aws sts get-caller-identity  # Verificar permissões
```

## 📋 **ARQUIVOS IMPORTANTES**

### **Código Atual (Next.js):**
- `c:\Projetos Git\drive-online-clean-NextJs\` (projeto completo)
- Componentes em `/components/modules/`
- APIs em `/app/api/`

### **Documentação:**
- `memoria/STATUS_FINAL_CONSOLIDADO.md` (este resumo)
- `memoria/MEDIAFLOW-NEXTJS-GUIDE.md` (guia técnico)

## 🎬 **COMANDO PARA INICIAR**

**"Vamos começar a Fase 1 da migração AWS. Preciso configurar a conta AWS e criar os buckets S3."**

---

**Projeto**: Mediaflow Next.js v4.0  
**Status**: Pronto para migração AWS  
**Próximo**: Fase 1 - Setup AWS  
**Objetivo**: Sistema sem limites de upload
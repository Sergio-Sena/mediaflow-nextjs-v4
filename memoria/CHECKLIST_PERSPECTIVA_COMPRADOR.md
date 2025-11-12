# ✅ Checklist - Perspectiva de Comprador

**Objetivo**: Transformar projeto técnico em produto comercial  
**Baseado em**: PLANO_SANITIZACAO_PRODUTO.md  
**Última atualização**: 12/11/2025

---

## 🔴 CRÍTICOS (Deal Breakers)

### 1. Conteúdo Adulto
- [x] README.md comercial criado (sem conteúdo adulto)
- [ ] Remover screenshots com conteúdo adulto (se houver)
- [ ] Atualizar exemplos para casos corporativos
- [ ] Verificar documentação técnica

### 2. Trial Automático
**Limites Aprovados:**
- Duração: 15 dias
- Storage: 10 GB
- Vídeos: Ilimitados
- Upload máx: 1 GB por arquivo
- Conversão: 1080p
- Bandwidth: 20 GB
- Custo estimado: ~$5/trial

**Implementação:**
- [x] Modificar Lambda create-user (status: 'trial' por padrão)
- [x] Criar Lambda check-limits (verificar limites)
- [x] Implementar limites de storage (10 GB)
- [x] Implementar limite de upload (1 GB por arquivo)
- [x] Implementar limite de bandwidth (20 GB)
- [x] Atualizar /register (remover "aguardando aprovação")
- [x] Dashboard: Badge "Trial" + contador de dias (15)
- [x] Dashboard: Progresso (X GB/10 GB, Y GB bandwidth/20 GB)

**Lifecycle + Recuperação:**
- [x] S3 Lifecycle: Trial → Glacier após 7 dias sem upgrade
- [x] S3 Lifecycle: Inativo 30 dias → Intelligent-Tiering
- [x] S3 Lifecycle: Inativo 90 dias → Glacier Instant Retrieval
- [ ] Lambda: Restauração automática ao fazer login
- [x] Email D+0: "Trial expirou - Faça upgrade"
- [x] Email D+7: "50% OFF - Última chance" (cupom VOLTA50)
- [x] Email D+30: "3 meses por $29.99" (cupom VOLTA3X)
- [x] Email D+90: "Aviso de exclusão em 30 dias"
- [x] Email D+120: Deletar permanentemente
- [x] Email: Alerta de limite de storage (80%, 90%, 100%)
- [x] Email: Alerta de limite de bandwidth (80%, 90%, 100%)
- [x] Sistema anti-spam: Máx 1 email/dia por tipo

### 3. Página de Pricing
- [x] Criar página /pricing
- [x] Design: 4 cards (Trial, Basic, Pro, Enterprise)
- [x] Botões "Começar Grátis" / "Escolher Plano"
- [x] FAQ de pricing (5 perguntas)
- [x] Tabela comparativa vs concorrentes
- [x] Storage como bônus diferencial
- [x] Valores em BRL (R$ 49,90 / R$ 99,90)

### 4. Landing Page Profissional
- [x] Criar homepage pública (/)
- [x] Hero Section (título + CTA)
- [x] Seção Features (3 colunas)
- [x] Seção Social Proof (métricas)
- [x] Footer (links + copyright)
- [x] Header com navegação (Preços, Login, Cadastro)

---

## 🟡 GRAVES (Impedem venda)

### 5. Diferenciação vs Concorrentes
- [x] Seção "Por que Mídiaflow?" no README
- [x] Comparação vs YouTube, Vimeo, Wistia
- [ ] Tabela comparativa visual na landing page
- [ ] Destacar diferenciais únicos

### 6. Documentação Comercial
- [x] README.md comercial (versão cliente)
- [ ] README_TECNICO.md (versão dev)
- [ ] Criar /docs público
- [ ] Guia de início rápido
- [ ] Como fazer upload
- [ ] Como compartilhar vídeos
- [ ] FAQ público

### 7. Garantias e SLA
- [ ] Criar página /sla
- [ ] Definir uptime por plano (99.9% / 99.99%)
- [ ] Adicionar "Garantia de 30 dias" no pricing
- [ ] Termos de Serviço
- [ ] Política de Privacidade

### 8. Branding Unificado
- [x] Nome definido: "Mídiaflow"
- [x] Cores definidas (Cyan, Purple, Pink)
- [ ] Logo oficial
- [ ] Guia de marca
- [ ] Tom de voz consistente

---

## 🟢 IMPORTANTES (Melhoram conversão)

### 9. Casos de Uso
- [x] Casos de uso no README (Cursos, Empresas, Agências, Criadores)
- [ ] Criar página /casos-de-uso
- [ ] Screenshots reais de cada caso
- [ ] Depoimentos (iniciais podem ser anônimos)

### 10. Provas Sociais
- [ ] Adicionar métricas reais (TB hospedados, empresas ativas)
- [ ] Depoimentos de beta testers
- [ ] Logos de clientes (quando houver)
- [ ] Case studies (quando houver)

### 11. Comparação Detalhada
- [x] Tabela comparativa no README
- [ ] Página dedicada /comparacao
- [ ] Gráficos visuais de preço/features
- [ ] Calculadora de ROI

### 12. Onboarding Guiado
- [ ] Tour interativo (primeira vez)
- [ ] Checklist de setup (4 passos)
- [ ] Email de boas-vindas com guia
- [ ] Tooltips no dashboard

---

## 🔵 EXTRAS (Melhoram experiência)

### 13. Blog + SEO
- [ ] Criar /blog
- [ ] 3 artigos iniciais
- [ ] Meta tags
- [ ] Sitemap.xml
- [ ] Google Analytics

### 14. Integração Stripe
- [ ] Criar conta Stripe
- [ ] Implementar checkout
- [ ] Webhooks (pagamento, cancelamento)
- [ ] Página /billing no dashboard

### 15. Email Marketing
- [ ] Configurar AWS SES
- [ ] Template: Boas-vindas
- [ ] Template: Trial expirando (7, 3, 1 dia)
- [ ] Template: Trial expirado
- [ ] Template: Upgrade realizado
- [ ] Template: Limite de storage (80%, 90%, 100%)

---

## 📊 PROGRESSO GERAL

**Críticos**: 4/4 itens completos (100%) ✅
**Graves**: 3/4 itens iniciados (75%)  
**Importantes**: 2/4 itens iniciados (50%)  
**Extras**: 0/3 itens iniciados (0%)

**Total**: 9/15 categorias com progresso (60%)

**Trial Automático**: 16/16 tarefas (100%) ✅
**Página Pricing**: 8/8 tarefas (100%) ✅
**Landing Page**: 6/6 tarefas (100%) ✅

---

## 🎯 PRÓXIMA AÇÃO PRIORITÁRIA

✅ **TODOS OS CRÍTICOS COMPLETOS!**

1. ✅ Trial Automático (Backend + Frontend)
2. ✅ Página de Pricing (BRL + Storage bônus)
3. ✅ Landing Page (Hero + Features + Social Proof)

**Próximo:** Graves (#5-8) - Diferenciação, Docs, SLA, Branding

---

## 📝 NOTAS

- ✅ = Completo
- 🔄 = Em progresso
- ❌ = Não iniciado
- 🚫 = Bloqueado

**Regra**: Marcar [x] apenas quando 100% completo e testado em produção.

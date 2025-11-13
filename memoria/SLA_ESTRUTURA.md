# 📊 Estrutura da Página /sla - Mídiaflow

**Data**: 2025-01-30  
**Responsável**: @produto  
**Sprint**: 1.1 - Garantias e SLA

---

## 🎯 Objetivo da Página

Transmitir **confiança** e **transparência** ao comprador através de:
- Garantias claras de uptime
- SLA por plano
- Processo de compensação
- Garantia de reembolso

---

## 📐 Estrutura da Página

### Hero Section
```
🛡️ Garantias e SLA

Transparência total sobre nossos compromissos de disponibilidade e qualidade.
Sua confiança é nossa prioridade.

[Ver Planos] [Falar com Suporte]
```

---

### Seção 1: Uptime por Plano

#### Trial (Grátis)
- **Uptime**: 99.5%
- **Downtime máximo/mês**: 3h 36min
- **Suporte**: Email (48h)
- **Compensação**: Não aplicável

#### Basic ($9.99/mês)
- **Uptime**: 99.9%
- **Downtime máximo/mês**: 43min
- **Suporte**: Email (24h)
- **Compensação**: 10% de crédito por cada 0.1% abaixo do SLA

#### Pro ($19.99/mês)
- **Uptime**: 99.95%
- **Downtime máximo/mês**: 21min
- **Suporte**: Prioritário (4h)
- **Compensação**: 15% de crédito por cada 0.1% abaixo do SLA

#### Enterprise (Sob Consulta)
- **Uptime**: 99.99%
- **Downtime máximo/mês**: 4min
- **Suporte**: 24/7 dedicado
- **Compensação**: 25% de crédito por cada 0.1% abaixo do SLA
- **SLA personalizado**: Disponível

---

### Seção 2: O que está coberto pelo SLA

✅ **Incluído no SLA:**
- Disponibilidade da plataforma (dashboard, upload, player)
- Entrega de vídeos via CDN
- API de integração
- Sistema de autenticação
- Conversão de vídeos

❌ **Não incluído no SLA:**
- Manutenções programadas (notificadas com 48h de antecedência)
- Problemas de internet do usuário
- Ataques DDoS (mitigação em andamento)
- Problemas em serviços de terceiros (AWS, Stripe)

---

### Seção 3: Como calculamos o Uptime

**Fórmula:**
```
Uptime (%) = (Tempo Total - Tempo de Downtime) / Tempo Total × 100
```

**Exemplo (Plano Basic - 99.9%):**
- Tempo total no mês: 43.200 minutos (30 dias)
- Downtime permitido: 43 minutos
- Se downtime = 50 minutos → Uptime = 99.88% → Compensação de 10%

**Monitoramento:**
- Verificações a cada 1 minuto
- Múltiplas localizações globais
- Status público: https://status.midiaflow.com

---

### Seção 4: Processo de Compensação

**Como solicitar:**
1. Abrir ticket em até 7 dias após o incidente
2. Fornecer evidências (prints, logs, horários)
3. Nossa equipe valida em até 48h
4. Crédito aplicado na próxima fatura

**Créditos:**
- Aplicados automaticamente na renovação
- Não podem ser convertidos em dinheiro
- Válidos por 12 meses
- Acumuláveis

**Exemplo:**
- Plano Pro: $19.99/mês
- Downtime: 30 minutos (Uptime = 99.93%)
- SLA prometido: 99.95%
- Diferença: 0.02%
- Compensação: 15% × 0.02% = 0.3% → $0.06 de crédito

---

### Seção 5: Garantia de 30 Dias

**Política de Reembolso:**
- ✅ 30 dias para testar sem riscos
- ✅ Reembolso de 100% do valor pago
- ✅ Sem perguntas ou burocracia
- ✅ Processamento em até 7 dias úteis

**Como solicitar:**
1. Email para suporte@midiaflow.com
2. Assunto: "Solicitação de Reembolso"
3. Incluir email da conta e motivo (opcional)
4. Confirmação em até 24h

**Condições:**
- Válido apenas para primeira assinatura
- Não aplicável a renovações
- Dados da conta serão mantidos por 30 dias (recuperação)

---

### Seção 6: Manutenções Programadas

**Janela de Manutenção:**
- Terças-feiras, 02h-04h (horário de Brasília)
- Notificação por email com 48h de antecedência
- Status em tempo real: https://status.midiaflow.com

**Frequência:**
- Máximo 2 manutenções/mês
- Duração média: 30 minutos
- Downtime não conta para SLA

---

### Seção 7: Monitoramento e Transparência

**Status Público:**
- URL: https://status.midiaflow.com
- Atualização em tempo real
- Histórico de incidentes (90 dias)
- Métricas de uptime por mês

**Notificações:**
- Email automático em caso de incidente
- SMS para planos Pro e Enterprise (opcional)
- Webhook para integrações (API)

---

### Seção 8: Suporte por Plano

#### Trial
- Email: suporte@midiaflow.com
- Tempo de resposta: 48h
- Horário: Segunda a Sexta, 9h-18h

#### Basic
- Email: suporte@midiaflow.com
- Tempo de resposta: 24h
- Horário: Segunda a Sexta, 9h-18h
- Chat ao vivo: Não

#### Pro
- Email: suporte@midiaflow.com
- Tempo de resposta: 4h
- Horário: Segunda a Sábado, 8h-20h
- Chat ao vivo: Sim (horário comercial)

#### Enterprise
- Email dedicado: empresa@midiaflow.com
- Tempo de resposta: 1h
- Horário: 24/7
- Chat ao vivo: Sim (24/7)
- Telefone: Sim
- Gerente de conta: Sim

---

### Seção 9: Segurança e Conformidade

**Certificações:**
- ✅ SSL/HTTPS em todos os vídeos
- ✅ Backup automático diário
- ✅ Conformidade com LGPD
- ✅ Servidores na AWS (Amazon)
- ✅ Certificações ISO 27001 (em andamento)

**Proteção de Dados:**
- Criptografia em repouso (AES-256)
- Criptografia em trânsito (TLS 1.3)
- Backup incremental a cada 6h
- Retenção de backup: 30 dias

---

### Seção 10: FAQ

**1. O que acontece se o uptime ficar abaixo do SLA?**
Você recebe créditos proporcionais automaticamente na próxima fatura.

**2. Como sei se houve downtime?**
Acesse https://status.midiaflow.com ou receba notificações por email.

**3. Posso cancelar a qualquer momento?**
Sim! Sem multas ou taxas. Cancele quando quiser.

**4. A garantia de 30 dias é real?**
Sim! Reembolso de 100% sem perguntas em até 7 dias úteis.

**5. Manutenções programadas contam no SLA?**
Não. Apenas downtime não planejado conta para o SLA.

**6. Como solicito compensação por downtime?**
Abra ticket em até 7 dias com evidências. Validamos em 48h.

---

### CTA Final

```
🛡️ Pronto para começar com confiança?

14 dias grátis. Sem cartão de crédito. Cancele quando quiser.

[Começar Grátis] [Ver Planos] [Falar com Vendas]
```

---

## 🎨 Design Guidelines

### Cores
- **Verde**: Garantias e uptime (confiança)
- **Azul**: Informações técnicas (profissionalismo)
- **Amarelo**: Avisos e manutenções (atenção)
- **Vermelho**: Downtime e incidentes (urgência)

### Ícones
- 🛡️ Garantias
- ⏱️ Uptime
- 💰 Compensação
- 📊 Monitoramento
- 🔒 Segurança
- 📞 Suporte

### Tipografia
- **Títulos**: Bold, 32px
- **Subtítulos**: Semibold, 24px
- **Corpo**: Regular, 16px
- **Destaque**: Semibold, 18px

---

## 📊 Métricas de Sucesso

**Objetivos:**
- Reduzir dúvidas sobre confiabilidade em 50%
- Aumentar conversão de trial para pago em 20%
- Reduzir tickets de suporte sobre SLA em 70%

**KPIs:**
- Tempo médio na página: >2min
- Taxa de rejeição: <30%
- Cliques em CTA: >15%

---

## 🚀 Próximos Passos

1. **@Lyra**: Revisar copywriting e tom de voz
2. **@Base**: Implementar página /sla no frontend
3. **@meumanus**: Configurar CloudWatch Alarms
4. **@produto**: Adicionar "Garantia de 30 dias" no /pricing

---

**Status**: ✅ Estrutura definida  
**Próxima ação**: Passar para @Lyra para copywriting

# 📚 Estrutura da Documentação Comercial - Mídiaflow

**Data**: 2025-01-30  
**Responsável**: @produto  
**Sprint**: 1.2 - Documentação Comercial

---

## 🎯 Objetivo

Criar documentação pública completa para novos usuários, reduzindo tickets de suporte e melhorando onboarding.

---

## 📋 Estrutura da Página /docs

### Navegação Principal

```
/docs
├── Início Rápido
├── Como Fazer Upload
├── Como Compartilhar Vídeos
└── FAQ
```

---

## 📖 Guia 1: Início Rápido

**Objetivo**: Usuário consegue fazer primeiro upload em 5 minutos

**Conteúdo**:

### Passo 1: Criar Conta (1 min)
- Acesse midiaflow.sstechnologies-cloud.com/register
- Preencha nome, email e senha
- Aceite os termos
- 14 dias grátis, sem cartão

### Passo 2: Fazer Login (30s)
- Email + senha
- 2FA (opcional, mas recomendado)

### Passo 3: Fazer Primeiro Upload (2 min)
- Clique em "Upload" ou arraste arquivo
- Aguarde conversão automática
- Vídeo pronto para compartilhar

### Passo 4: Compartilhar Vídeo (1 min)
- Copie link direto OU
- Copie código embed
- Cole onde quiser

### Passo 5: Acompanhar (30s)
- Veja visualizações no dashboard
- Monitore uso de storage e bandwidth

**Tempo total**: ~5 minutos

---

## 📖 Guia 2: Como Fazer Upload

**Objetivo**: Explicar todas as formas de upload e limites

**Conteúdo**:

### Métodos de Upload

#### 1. Drag & Drop (Recomendado)
- Arraste arquivo para área de upload
- Suporta múltiplos arquivos
- Barra de progresso em tempo real

#### 2. Clique para Selecionar
- Botão "Escolher Arquivo"
- Navegador de arquivos do sistema
- Selecione um ou vários

### Limites por Plano

| Plano | Upload Máximo | Storage | Bandwidth |
|-------|---------------|---------|-----------|
| Trial | 1 GB/arquivo | 10 GB | 20 GB/mês |
| Basic | 5 GB/arquivo | 25 GB | Ilimitado |
| Pro | 5 GB/arquivo | 200 GB | Ilimitado |
| Enterprise | Customizado | Customizado | Ilimitado |

### Formatos Suportados
- **Vídeo**: MP4, MOV, AVI, MKV, WebM
- **Conversão automática**: H.264 (1080p ou 4K)
- **Outros arquivos**: PDF, ZIP, imagens (bônus)

### Processo de Conversão

1. **Upload**: Arquivo enviado para S3
2. **Fila**: Entra na fila de conversão
3. **Conversão**: MediaConvert processa (5-15 min)
4. **Pronto**: Vídeo disponível em múltiplas resoluções

### Dicas de Upload

✅ **Faça**:
- Use Wi-Fi estável
- Vídeos até 5 GB (melhor performance)
- Formato MP4 (mais rápido)

❌ **Evite**:
- Upload via 4G/5G (pode falhar)
- Arquivos corrompidos
- Fechar navegador durante upload

### Troubleshooting

**Upload falhou?**
- Verifique conexão de internet
- Confirme tamanho do arquivo (limite do plano)
- Tente novamente em alguns minutos

**Conversão travada?**
- Aguarde até 15 minutos
- Verifique formato do arquivo
- Contate suporte se persistir

---

## 📖 Guia 3: Como Compartilhar Vídeos

**Objetivo**: Ensinar todas as formas de compartilhar

**Conteúdo**:

### Método 1: Link Direto

**Quando usar**: Compartilhar em redes sociais, email, WhatsApp

**Como fazer**:
1. Clique no vídeo no dashboard
2. Copie o link direto
3. Cole onde quiser

**Exemplo**:
```
https://midiaflow.sstechnologies-cloud.com/watch/abc123
```

### Método 2: Código Embed

**Quando usar**: Incorporar em sites, blogs, plataformas de curso

**Como fazer**:
1. Clique no vídeo no dashboard
2. Clique em "Embed"
3. Copie o código HTML
4. Cole no seu site

**Exemplo**:
```html
<iframe 
  src="https://midiaflow.sstechnologies-cloud.com/embed/abc123" 
  width="640" 
  height="360" 
  frameborder="0" 
  allowfullscreen>
</iframe>
```

### Método 3: Download

**Quando usar**: Enviar arquivo original

**Como fazer**:
1. Clique no vídeo no dashboard
2. Clique em "Download"
3. Arquivo original baixado

**Disponível em**: Basic, Pro, Enterprise

### Controle de Privacidade

#### Vídeos Privados (Padrão)
- Apenas você vê
- Link funciona apenas logado

#### Vídeos Públicos
- Qualquer pessoa com link pode ver
- Não aparece em buscas

#### Vídeos com Senha (Pro/Enterprise)
- Protegido por senha
- Você define a senha

### Domínio Personalizado (Pro/Enterprise)

Ao invés de:
```
https://midiaflow.sstechnologies-cloud.com/watch/abc123
```

Use seu domínio:
```
https://videos.suaempresa.com/abc123
```

---

## ❓ FAQ Público

**Objetivo**: Responder 15 perguntas mais comuns

**Categorias**:
1. Conta e Planos (5 perguntas)
2. Upload e Conversão (4 perguntas)
3. Compartilhamento (3 perguntas)
4. Técnico (3 perguntas)

### Conta e Planos

**1. Como funciona o trial de 14 dias?**
- Grátis, sem cartão de crédito
- 10 GB storage, 20 GB bandwidth
- Acesso a todas as funcionalidades
- Upgrade a qualquer momento

**2. Posso cancelar quando quiser?**
- Sim, sem multas ou taxas
- Cancele direto no dashboard
- Dados mantidos por 30 dias

**3. Como faço upgrade de plano?**
- Dashboard → Configurações → Planos
- Escolha novo plano
- Pagamento proporcional

**4. Quais formas de pagamento aceitam?**
- Cartão de crédito (mensal/anual)
- Boleto (apenas anual)
- PIX (apenas anual)

**5. Tem desconto para pagamento anual?**
- Sim, 20% de desconto
- Basic: R$ 479,04/ano (ao invés de R$ 598,80)
- Pro: R$ 959,04/ano (ao invés de R$ 1.198,80)

### Upload e Conversão

**6. Qual o tamanho máximo de upload?**
- Trial: 1 GB por arquivo
- Basic/Pro: 5 GB por arquivo
- Enterprise: Customizado

**7. Quanto tempo demora a conversão?**
- Vídeos curtos (<5 min): 2-5 minutos
- Vídeos médios (5-30 min): 5-10 minutos
- Vídeos longos (>30 min): 10-15 minutos

**8. Quais formatos são suportados?**
- Vídeo: MP4, MOV, AVI, MKV, WebM
- Conversão automática para H.264
- Outros arquivos: PDF, ZIP, imagens (bônus)

**9. Posso fazer upload de outros arquivos além de vídeos?**
- Sim! Bônus dos planos Basic e Pro
- Use como storage na nuvem
- Organize em pastas

### Compartilhamento

**10. Como compartilho meus vídeos?**
- Link direto (copiar e colar)
- Código embed (para sites)
- Download (arquivo original)

**11. Meus vídeos são públicos?**
- Não, privados por padrão
- Você controla quem vê
- Opção de senha (Pro/Enterprise)

**12. Posso usar meu próprio domínio?**
- Sim, em planos Pro e Enterprise
- Ex: videos.suaempresa.com
- Configuração simples via DNS

### Técnico

**13. Onde os vídeos são armazenados?**
- AWS S3 (Amazon)
- Múltiplas regiões (backup)
- CDN global (400+ localizações)

**14. Qual o uptime garantido?**
- Trial: 99.5%
- Basic: 99.9%
- Pro: 99.95%
- Enterprise: 99.99%

**15. Como funciona o suporte?**
- Trial: Email em 48h
- Basic: Email em 24h
- Pro: Email em 4h + Chat
- Enterprise: 24/7 + Gerente dedicado

---

## 📄 README_TECNICO.md

**Objetivo**: Documentação para desenvolvedores

**Conteúdo**:

### Arquitetura
- Frontend: Next.js 14 + TypeScript
- Backend: AWS Lambda (Node.js)
- Storage: S3 + CloudFront CDN
- Conversão: MediaConvert
- Auth: JWT + 2FA

### API (Pro/Enterprise)

#### Endpoints Principais
```
POST /api/upload - Upload de vídeo
GET /api/videos - Listar vídeos
GET /api/video/:id - Detalhes do vídeo
DELETE /api/video/:id - Deletar vídeo
```

#### Autenticação
```bash
curl -H "Authorization: Bearer YOUR_API_KEY" \
  https://api.midiaflow.com/videos
```

### Webhooks (Pro/Enterprise)

Receba notificações de eventos:
- `video.uploaded` - Upload completo
- `video.converted` - Conversão completa
- `video.deleted` - Vídeo deletado

### Limites de Rate
- Trial: 10 req/min
- Basic: 60 req/min
- Pro: 300 req/min
- Enterprise: Customizado

### SDKs Disponíveis
- JavaScript/Node.js
- Python
- PHP
- Ruby (em breve)

---

## 🎨 Design da Página /docs

### Layout
```
┌─────────────────────────────────────┐
│ Header (logo + navegação)           │
├──────────┬──────────────────────────┤
│ Sidebar  │ Conteúdo                 │
│          │                          │
│ - Início │ # Título                 │
│ - Upload │                          │
│ - Share  │ Texto explicativo...     │
│ - FAQ    │                          │
│          │ ## Subtítulo             │
│          │                          │
│          │ Mais conteúdo...         │
└──────────┴──────────────────────────┘
```

### Componentes
- Navegação lateral fixa (sticky)
- Breadcrumbs no topo
- Busca (opcional)
- Links âncora para seções
- Botão "Voltar ao topo"

---

## 📊 Métricas de Sucesso

**Objetivos**:
- Reduzir tickets de suporte em 50%
- Tempo médio na página: >3 min
- Taxa de rejeição: <20%

**KPIs**:
- Visualizações por guia
- Buscas mais comuns
- Links mais clicados

---

## ✅ Checklist de Entrega

### @produto (Estrutura)
- [x] Definir navegação principal
- [x] Criar outline dos 3 guias
- [x] Definir 15 perguntas FAQ
- [x] Especificar README_TECNICO.md

### @Lyra (Conteúdo)
- [ ] Escrever Guia 1: Início Rápido
- [ ] Escrever Guia 2: Como Fazer Upload
- [ ] Escrever Guia 3: Como Compartilhar
- [ ] Escrever FAQ (15 perguntas)
- [ ] Escrever README_TECNICO.md

### @Base (Implementação)
- [ ] Criar app/docs/page.tsx
- [ ] Implementar navegação lateral
- [ ] Implementar breadcrumbs
- [ ] Adicionar busca (opcional)
- [ ] Design responsivo

---

**Status**: ✅ Estrutura definida  
**Próxima ação**: @Lyra escrever conteúdo dos guias

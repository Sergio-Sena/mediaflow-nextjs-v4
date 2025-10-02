# Prompt para Replicação Completa do Mediaflow v4.2

> **📋 NOTA:** Este prompt foi criado usando o **Prompt Base Universal** e o **Persona Base**. Para criar prompts similares para outras aplicações, consulte:
> - `Prompt_Base_Universal.md` - Template genérico C.E.R.T.O
> - `Persona_Base.md` - Especialista em criação de aplicações

## 1. PAPEL E OBJETIVO (O P de C.E.R.T.O)

Você é um **Arquiteto de Software Full-Stack Sênior** especializado em sistemas de streaming, AWS Cloud Architecture e Next.js enterprise applications.

Seu objetivo principal é **replicar completamente o sistema Mediaflow v4.2** - uma plataforma profissional de streaming com upload inteligente, conversão de vídeo automática, CDN global e gerenciamento hierárquico de arquivos.

## 2. CONTEXTO E INFORMAÇÃO (O C de C.E.R.T.O)

### 2.1. Conhecimento Base (Sistema Atual)

```yaml
# MEDIAFLOW v4.2 - ESPECIFICAÇÕES TÉCNICAS
Sistema: "Plataforma de Streaming Profissional"
Status: "✅ PRODUÇÃO"
URL: "https://mediaflow.sstechnologies-cloud.com"
Performance: "Lighthouse 95+ | Uptime 99.9%"

# ARQUITETURA AWS
Frontend:
  - CDN: "CloudFront global (400+ edge locations)"
  - Hosting: "S3 Static Website"
  - SSL: "Certificado wildcard"
  - Domínio: "mediaflow.sstechnologies-cloud.com"

Backend:
  - API: "API Gateway + 6 Lambda Functions"
  - Storage: "3 S3 Buckets (uploads/processed/frontend)"
  - Vídeo: "AWS MediaConvert H.264 1080p"
  - Auth: "JWT com sessão persistente"

# FUNCIONALIDADES CORE
Upload:
  - Tamanho: "Até 5GB"
  - Método: "DirectUpload component com drag & drop"
  - Destino: "Upload direto S3 (bypass Next.js)"
  - Progress: "Tracking em tempo real"

Conversão:
  - Engine: "AWS MediaConvert"
  - Formato: "H.264 1080p automático"
  - Trigger: "Automático após upload"

Player:
  - Tipo: "Sequencial com navegação Previous/Next"
  - Navegação: "Entre vídeos da mesma pasta"
  - Controles: "Play/Pause/Volume/Fullscreen"

Gerenciamento:
  - Estrutura: "Navegação hierárquica por pastas"
  - Interface: "Breadcrumbs e seleção em lote"
  - Busca: "Global em todas as pastas"
  - Cleanup: "Automático de arquivos órfãos"

# DESIGN SYSTEM
Tema: "Neon Cyberpunk"
Cores: "Cyan, Purple, Pink gradients"
Animações: "Smooth transitions e hover effects"
Responsivo: "Mobile + Desktop otimizado"
Mode: "Dark Mode elegante"
```

### 2.2. Ambiente e Escopo

```yaml
# STACK TECNOLÓGICO
Frontend:
  - Framework: "Next.js 14 (App Router)"
  - Linguagem: "TypeScript 5.6"
  - Estilização: "CSS Modules + Tailwind CSS"
  - Componentes: "React 18 com hooks"

Backend:
  - Runtime: "Node.js 22+"
  - API: "Next.js API Routes + AWS Lambda"
  - Auth: "JWT com bcrypt"
  - Validação: "Zod schemas"

AWS Services:
  - Compute: "Lambda Functions (6 funções)"
  - Storage: "S3 (3 buckets)"
  - CDN: "CloudFront"
  - Media: "MediaConvert"
  - API: "API Gateway"
  - DNS: "Route 53"

# ESTRUTURA DE PASTAS
drive-online-clean-NextJs/
├── app/                    # Next.js App Router
│   ├── (auth)/            # Rotas de autenticação
│   ├── dashboard/         # Dashboard principal
│   └── globals.css        # Estilos globais
├── components/            # Componentes React
│   └── modules/           # Módulos principais
├── lib/                   # Clientes AWS e utilitários
├── aws-setup/             # Scripts de deploy AWS
│   └── lambda-functions/  # Funções Lambda
└── Prompt Base/           # Documentação de prompts
```

## 3. TAREFA DETALHADA E EXPECTATIVA (O T de C.E.R.T.O)

Siga estas etapas de raciocínio para executar a tarefa:

### 3.1. Raciocínio (Chain-of-Thought - CoT)

**Pense passo a passo** antes de gerar a resposta final:

1. **Analise a arquitetura AWS** - Identifique todos os serviços, buckets S3, funções Lambda e configurações de CDN necessárias
2. **Mapeie a estrutura Next.js** - Defina App Router, componentes modulares, API routes e sistema de autenticação JWT
3. **Implemente o sistema de upload** - DirectUpload component com drag & drop, progress tracking e upload direto S3
4. **Configure conversão de vídeo** - AWS MediaConvert com triggers automáticos e processamento H.264 1080p
5. **Desenvolva o player sequencial** - Navegação Previous/Next, controles completos e integração com estrutura de pastas
6. **Crie o gerenciador hierárquico** - Navegação por breadcrumbs, seleção em lote, busca global e cleanup automático
7. **Aplique o design system** - Tema neon cyberpunk, gradientes, animações e responsividade completa
8. **Configure infraestrutura** - CloudFront CDN, domínio customizado, SSL wildcard e monitoramento

### 3.2. Ação Principal

**Gere a estrutura completa do projeto Mediaflow v4.2** incluindo:
- Configuração AWS completa (Terraform/CloudFormation)
- Código Next.js 14 com TypeScript
- Componentes React modulares
- Sistema de autenticação JWT
- Upload direto S3 com progress tracking
- Player de vídeo sequencial
- Gerenciador de pastas hierárquico
- Design system neon cyberpunk
- Scripts de deploy e configuração

## 4. REGRAS E RESTRIÇÕES DE SAÍDA (O R de C.E.R.T.O)

O resultado DEVE aderir estritamente às seguintes regras:

1. **Arquitetura:** Use **exatamente** a mesma stack: Next.js 14, TypeScript 5.6, AWS (Lambda, S3, CloudFront, MediaConvert)
2. **Estrutura:** Mantenha a **estrutura de pastas idêntica** ao projeto original
3. **Funcionalidades:** Implemente **todas as funcionalidades** listadas no contexto (upload 5GB, conversão H.264, player sequencial, etc.)
4. **Design:** Replique o **tema neon cyberpunk** com gradientes cyan/purple/pink e animações suaves
5. **Performance:** Garanta **Lighthouse 95+** e otimizações para CDN global
6. **Segurança:** Implemente **JWT robusto**, validação de entrada e sanitização
7. **Código:** Use **TypeScript strict**, ESLint, Prettier e padrões enterprise
8. **Deploy:** Inclua **scripts completos** de configuração AWS e deploy automatizado
9. **Documentação:** Forneça **README detalhado** com setup, configuração e troubleshooting
10. **Idioma:** Todo código, comentários e documentação em **Português do Brasil**

## 5. ENTREGA (O E de C.E.R.T.O)

Após a etapa de **Raciocínio**, forneça:

### 5.1. Estrutura Completa do Projeto
- Todos os arquivos e pastas necessários
- Configurações AWS (Terraform/CloudFormation)
- Package.json com dependências exatas

### 5.2. Código Fonte Completo
- Componentes React TypeScript
- API Routes Next.js
- Funções Lambda AWS
- Configurações de build e deploy

### 5.3. Documentação Técnica
- README.md detalhado
- Guia de setup AWS
- Instruções de deploy
- Troubleshooting comum

### 5.4. Scripts de Automação
- Deploy automatizado
- Configuração de ambiente
- Backup e restore
- Monitoramento

---

## 📋 CHECKLIST DE VALIDAÇÃO

Antes de entregar, verifique se o sistema possui:

- [ ] ✅ Upload até 5GB com DirectUpload component
- [ ] ✅ Conversão automática H.264 1080p via MediaConvert
- [ ] ✅ Player sequencial com navegação Previous/Next
- [ ] ✅ Navegação hierárquica por pastas com breadcrumbs
- [ ] ✅ Gerenciador avançado com seleção em lote
- [ ] ✅ Busca global em todas as pastas
- [ ] ✅ Cleanup automático de arquivos órfãos
- [ ] ✅ CDN CloudFront global (400+ edge locations)
- [ ] ✅ SSL wildcard e domínio customizado
- [ ] ✅ Autenticação JWT robusta
- [ ] ✅ Design neon cyberpunk responsivo
- [ ] ✅ Performance Lighthouse 95+
- [ ] ✅ Monitoramento e analytics
- [ ] ✅ Deploy automatizado AWS
- [ ] ✅ Documentação completa em português

---

**🎯 OBJETIVO FINAL:** Sistema Mediaflow v4.2 100% funcional, replicando exatamente todas as funcionalidades, performance e design da versão em produção.
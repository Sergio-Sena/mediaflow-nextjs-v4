# 🚀 Prompt Inicial - Template Universal

## 📋 Como Usar Este Template

1. Copie este arquivo para `memoria/PROMPT_CONSOLIDADO.md` do novo projeto
2. Preencha todas as seções com informações do projeto
3. Use como contexto inicial para o chat

---

## 🎯 Contexto do Projeto

### Nome do Projeto
**[NOME_DO_PROJETO]**

### Descrição
**[Descreva em 2-3 linhas o que o projeto faz]**

Exemplo:
```
Sistema de gerenciamento de tarefas para equipes remotas com 
colaboração em tempo real, notificações push e integração com Slack.
```

---

## 🌐 Sistema em Produção (se aplicável)

### URLs
- **Produção**: [URL_PRODUCAO]
- **Staging**: [URL_STAGING]
- **Admin**: [URL_ADMIN]

### Credenciais (NÃO commitar)
- **Admin**: [admin-email] / [admin-password]
- **Teste**: [test-email] / [test-password]

### Status
- **Versão**: [X.X.X]
- **Status**: [Em Desenvolvimento / Produção / Manutenção]
- **Uptime**: [XX.X%]

---

## 🏗️ Arquitetura

### Stack Tecnológica

#### Frontend
```
Framework: [Next.js / React / Vue / Angular]
Linguagem: [TypeScript / JavaScript]
Estilo: [Tailwind / Styled Components / CSS Modules]
State: [Redux / Zustand / Context API]
```

#### Backend
```
Runtime: [Node.js / Python / Java / .NET]
Framework: [Express / FastAPI / Spring Boot]
API: [REST / GraphQL / tRPC]
Auth: [JWT / OAuth / Session]
```

#### Banco de Dados
```
Principal: [PostgreSQL / MySQL / MongoDB]
Cache: [Redis / Memcached]
Search: [Elasticsearch / Algolia]
```

#### Cloud / Infraestrutura
```
Provider: [AWS / Azure / GCP / Vercel]
Hosting: [S3 / EC2 / Lambda / Cloud Run]
CDN: [CloudFront / Cloudflare]
Storage: [S3 / Blob Storage / Cloud Storage]
```

---

## 🎯 Funcionalidades Implementadas

### v1.0 (MVP)
- [ ] [Funcionalidade 1]
- [ ] [Funcionalidade 2]
- [ ] [Funcionalidade 3]

### v1.1 (Atual)
- [ ] [Funcionalidade 4]
- [ ] [Funcionalidade 5]

### v2.0 (Próxima)
- [ ] [Funcionalidade 6]
- [ ] [Funcionalidade 7]

---

## 📁 Estrutura do Código

```
[nome-projeto]/
├── src/
│   ├── components/        # Componentes reutilizáveis
│   ├── pages/            # Páginas/rotas
│   ├── lib/              # Utilitários e helpers
│   ├── services/         # Integrações externas
│   └── styles/           # Estilos globais
├── tests/                # Testes automatizados
├── docs/                 # Documentação
├── memoria/              # Documentação do projeto
│   ├── PROMPT_CONSOLIDADO.md
│   └── METODO_DESENVOLVIMENTO.md
└── README.md
```

---

## 🔧 Setup Local

### Pré-requisitos
```bash
[Node.js XX+ / Python X.X+ / Java XX+]
[npm / yarn / pip / maven]
[Docker (opcional)]
```

### Instalação
```bash
# Clonar repositório
git clone [REPOSITORY_URL]
cd [PROJECT_NAME]

# Instalar dependências
[npm install / pip install -r requirements.txt]

# Configurar ambiente
cp .env.example .env.local
# Editar variáveis necessárias

# Iniciar desenvolvimento
[npm run dev / python manage.py runserver]
```

### Variáveis de Ambiente
```env
# Essenciais
DATABASE_URL=[url_do_banco]
API_KEY=[chave_api]
JWT_SECRET=[secret_key]

# Opcionais
REDIS_URL=[url_redis]
SMTP_HOST=[host_email]
```

---

## 🚀 Deploy

### Desenvolvimento
```bash
[comandos para deploy dev]
```

### Produção
```bash
[comandos para deploy prod]
```

---

## 💡 Decisões de Design Importantes

### 1. [Decisão Técnica 1]
- **Decisão**: [O que foi decidido]
- **Motivo**: [Por que foi decidido]
- **Alternativas**: [O que foi considerado]

Exemplo:
```
### 1. Autenticação JWT
- Decisão: JWT com refresh tokens
- Motivo: Stateless, escalável, suporta mobile
- Alternativas: Sessions (descartado por não escalar)
```

### 2. [Decisão Técnica 2]
- **Decisão**: [...]
- **Motivo**: [...]
- **Alternativas**: [...]

---

## 🐛 Problemas Conhecidos

### ✅ Resolvidos
- ~~[Problema 1]~~ → Fix: [Solução]
- ~~[Problema 2]~~ → Fix: [Solução]

### ⚠️ Pendentes
- [Problema 3] - Prioridade: [Alta/Média/Baixa]
- [Problema 4] - Prioridade: [Alta/Média/Baixa]

---

## 🎯 Roadmap

### Próxima Versão (vX.X)
- [ ] [Feature 1]
- [ ] [Feature 2]
- [ ] [Bug fix 1]

### Futuro (vX.X)
- [ ] [Feature 3]
- [ ] [Feature 4]

---

## 📊 Métricas

### Performance
- **Load Time**: [X.Xs]
- **Lighthouse**: [XX/100]
- **Bundle Size**: [XXX KB]

### Negócio
- **Usuários Ativos**: [XXX]
- **Uptime**: [XX.X%]
- **Conversão**: [XX%]

---

## 🔐 Segurança

### Implementado
- [ ] HTTPS/SSL
- [ ] Autenticação
- [ ] Autorização
- [ ] Rate limiting
- [ ] Input validation
- [ ] CORS configurado

### Melhorias Futuras
- [ ] [Melhoria 1]
- [ ] [Melhoria 2]

---

## 🧪 Testes

### Cobertura
- **Unit**: [XX%]
- **Integration**: [XX%]
- **E2E**: [XX%]

### Como Rodar
```bash
[npm test / pytest / mvn test]
```

---

## 📝 Documentação Adicional

### Links Úteis
- **API Docs**: [URL]
- **Design System**: [URL]
- **Wiki**: [URL]

### Contatos
- **Tech Lead**: [Nome] - [email]
- **Product Owner**: [Nome] - [email]

---

## 🎨 Design System

### Cores
```css
--primary: [#XXXXXX]
--secondary: [#XXXXXX]
--accent: [#XXXXXX]
--background: [#XXXXXX]
```

### Tipografia
```
Font Family: [Font Name]
Sizes: [12px, 14px, 16px, 20px, 24px]
```

---

## 📞 Suporte

### Em Caso de Problemas

1. Verificar logs: [onde estão os logs]
2. Consultar documentação: [link]
3. Abrir issue: [link do repositório]
4. Contatar: [email/slack]

---

## 🎓 Lições Aprendidas

### O Que Funcionou Bem
- [Lição 1]
- [Lição 2]

### O Que Pode Melhorar
- [Lição 3]
- [Lição 4]

---

**Versão**: [X.X.X] | **Última atualização**: [YYYY-MM-DD]

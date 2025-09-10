# 🎬 PROMPT PARA REFATORAÇÃO MEDIAFLOW NEXT.JS

## 📋 **CONTEXTO**
Preciso refatorar um sistema de streaming React+Vite para Next.js 14. Tenho toda a documentação e estrutura mapeada.

## 🎯 **OBJETIVO**
Criar projeto Next.js idêntico ao atual, mantendo 100% das funcionalidades:
- Sistema de streaming completo
- Upload multipart com progress
- Player de vídeo customizado
- Gerenciador de arquivos hierárquico
- Conversão automática de vídeos
- Autenticação JWT
- Design neon/cyberpunk

## 📁 **ARQUIVOS DE REFERÊNCIA**
Tenho na pasta `memoria/`:
- `MEDIAFLOW-NEXTJS-GUIDE.md` - Guia completo de migração
- `ESTRUTURA-COMPONENTES-REACT.md` - Mapeamento detalhado atual

## 🚀 **TAREFAS PRIORITÁRIAS**
1. **Setup Next.js 14** com App Router + TypeScript + Tailwind
2. **Migrar componentes** preservando arquitetura modular
3. **Criar API Routes** como proxy para AWS Lambda
4. **Implementar autenticação** com middleware
5. **Deploy Vercel** + configurar variáveis ambiente

## ⚙️ **CONFIGURAÇÕES AWS**
- **API Gateway**: `https://o9h6bz0ysl.execute-api.us-east-1.amazonaws.com`
- **Lambda Auth**: `auth-simple` (bypass ativo)
- **S3 Bucket**: `drive-online-frontend`
- **CloudFront**: `E1TK4C5GORRWUM`

## 🎨 **DESIGN SYSTEM**
- **Cores**: Neon cyan (#00ffff), Purple (#8b5cf6), Dark themes
- **Componentes**: Glass cards, backdrop blur, neon glows
- **Responsivo**: Mobile-first (320px-1440px)

## 📊 **FUNCIONALIDADES CRÍTICAS**
- ✅ Upload drag&drop com pastas
- ✅ Player modal com controles customizados  
- ✅ Navegação hierárquica de arquivos
- ✅ Conversão automática (.ts/.avi → .mp4)
- ✅ Busca avançada com filtros
- ✅ Storage stats em tempo real
- ✅ Limpeza automática de arquivos

## 🔧 **STACK TÉCNICA**
- **Frontend**: Next.js 14 + TypeScript + Tailwind CSS
- **Backend**: AWS Lambda Python (manter atual)
- **Deploy**: Vercel + AWS S3
- **Auth**: JWT + cookies + middleware

## 📝 **INSTRUÇÕES**
1. Leia os arquivos da pasta `memoria/` primeiro
2. Siga o guia `MEDIAFLOW-NEXTJS-GUIDE.md` exatamente
3. Use a estrutura de `ESTRUTURA-COMPONENTES-REACT.md` como referência
4. Mantenha a arquitetura modular
5. Preserve 100% das funcionalidades
6. Foque em performance e SEO

## 🎯 **RESULTADO ESPERADO**
- Projeto Next.js funcionando 100%
- Deploy em Vercel
- Performance 90+ Lighthouse
- Todas as funcionalidades migradas
- Código limpo e documentado

**Comece criando o projeto Next.js e seguindo o guia passo a passo.**
# 📤 Como Fazer Upload

Guia completo sobre upload de vídeos e arquivos no Mídiaflow.

---

## 🎯 Métodos de Upload

### Método 1: Arrastar e Soltar (Drag & Drop)

**Mais rápido e fácil!**

1. Abra o dashboard
2. Arraste o arquivo para a área de upload
3. Solte o arquivo
4. Upload inicia automaticamente

**Vantagens:**
- ✅ Suporta múltiplos arquivos
- ✅ Barra de progresso em tempo real
- ✅ Não precisa clicar em nada

---

### Método 2: Clique para Selecionar

**Tradicional e confiável**

1. Clique no botão **"Escolher Arquivo"**
2. Navegue até o arquivo no seu computador
3. Selecione um ou vários arquivos
4. Clique em **"Abrir"**

**Vantagens:**
- ✅ Familiar para todos
- ✅ Seleção múltipla (Ctrl/Cmd + clique)
- ✅ Funciona em qualquer navegador

---

## 📊 Limites por Plano

| Plano | Upload Máximo | Storage Total | Bandwidth |
|-------|---------------|---------------|-----------|
| **Trial** | 1 GB/arquivo | 10 GB | 20 GB/mês |
| **Basic** | 5 GB/arquivo | 25 GB | Ilimitado |
| **Pro** | 5 GB/arquivo | 200 GB | Ilimitado |
| **Enterprise** | Customizado | Customizado | Ilimitado |

**Dica:** Arquivos maiores que 5 GB? Entre em contato para plano Enterprise.

---

## 🎬 Formatos Suportados

### Vídeos (Conversão Automática)
- ✅ **MP4** (recomendado)
- ✅ **MOV** (Apple)
- ✅ **AVI** (Windows)
- ✅ **MKV** (alta qualidade)
- ✅ **WebM** (web)

**Conversão automática para:**
- H.264 (codec universal)
- Múltiplas resoluções (360p, 720p, 1080p, 4K*)
- Otimizado para streaming

*4K disponível no plano Pro

---

### Outros Arquivos (Bônus)

**Planos Basic e Pro incluem storage de qualquer arquivo:**

- 📄 **Documentos**: PDF, DOC, XLS, PPT
- 🖼️ **Imagens**: JPG, PNG, GIF, SVG
- 📦 **Compactados**: ZIP, RAR, 7Z
- 🎵 **Áudio**: MP3, WAV, AAC

**Use como storage na nuvem!**

---

## ⚙️ Processo de Conversão

### O que acontece após o upload?

**1. Upload (30s - 5min)**
- Arquivo enviado para AWS S3
- Criptografia automática
- Backup em múltiplas regiões

**2. Fila (instantâneo)**
- Entra na fila de conversão
- Prioridade por plano (Pro primeiro)

**3. Conversão (5-15min)**
- MediaConvert processa o vídeo
- Gera múltiplas resoluções
- Otimiza para streaming

**4. Distribuição (instantâneo)**
- Disponibilizado via CDN
- 400+ edge locations globais
- Pronto para assistir!

---

## ⏱️ Tempo de Conversão

| Duração do Vídeo | Tempo Estimado |
|------------------|----------------|
| Até 5 minutos | 2-5 minutos |
| 5-30 minutos | 5-10 minutos |
| 30-60 minutos | 10-15 minutos |
| Mais de 1 hora | 15-30 minutos |

**Fatores que influenciam:**
- Tamanho do arquivo
- Resolução original
- Formato do arquivo
- Fila de conversão

---

## ✅ Dicas para Upload Perfeito

### Faça

- ✅ Use **Wi-Fi estável** (não 4G/5G)
- ✅ Vídeos até **5 GB** (melhor performance)
- ✅ Formato **MP4** (conversão mais rápida)
- ✅ Resolução **1080p** (qualidade ideal)
- ✅ Mantenha navegador **aberto** durante upload

### Evite

- ❌ Upload via **conexão móvel** (pode falhar)
- ❌ Arquivos **corrompidos** ou incompletos
- ❌ **Fechar navegador** durante upload
- ❌ Vídeos com **DRM** ou proteção
- ❌ Formatos **exóticos** ou raros

---

## 🔧 Troubleshooting

### Upload Falhou?

**Possíveis causas:**
1. Conexão de internet instável
2. Arquivo maior que limite do plano
3. Formato não suportado
4. Navegador desatualizado

**Soluções:**
1. Verifique sua conexão
2. Confirme tamanho do arquivo
3. Converta para MP4
4. Atualize o navegador
5. Tente novamente

---

### Conversão Travada?

**O que fazer:**
1. Aguarde até **15 minutos**
2. Recarregue a página (F5)
3. Verifique formato do arquivo
4. Contate suporte se persistir

**Email:** suporte@midiaflow.com

---

### Vídeo Não Aparece?

**Checklist:**
1. Conversão terminou? (veja status)
2. Página atualizada? (F5)
3. Filtro ativo? (veja "Todos os vídeos")
4. Pasta correta? (veja navegação)

---

## 📱 Upload via Mobile

**Funciona em smartphones e tablets!**

### iOS (iPhone/iPad)
1. Abra Safari ou Chrome
2. Acesse o dashboard
3. Toque em "Escolher Arquivo"
4. Selecione da galeria ou grave novo

### Android
1. Abra Chrome ou Firefox
2. Acesse o dashboard
3. Toque em "Escolher Arquivo"
4. Selecione da galeria ou grave novo

**Dica:** Use Wi-Fi para uploads grandes.

---

## 🚀 Upload em Massa

**Precisa fazer upload de muitos vídeos?**

### Plano Pro/Enterprise
- API completa para automação
- Upload programático
- Integração com sistemas
- Webhooks para notificações

[Ver Documentação da API](/docs/api)

---

## 💡 Boas Práticas

### Organize Seus Vídeos
- Use **nomes descritivos**
- Crie **pastas por projeto**
- Adicione **tags** (em breve)
- Mantenha **backup local**

### Otimize Antes do Upload
- Comprima vídeos grandes
- Use resolução adequada (1080p é suficiente)
- Remova partes desnecessárias
- Converta para MP4 antes

### Monitore Seu Uso
- Acompanhe storage usado
- Verifique bandwidth mensal
- Faça upgrade quando necessário
- Delete vídeos antigos

---

## 🆘 Precisa de Ajuda?

- 📚 [Início Rápido](/docs/inicio-rapido)
- 📤 [Como Compartilhar](/docs/compartilhar)
- ❓ [FAQ](/docs/faq)
- 📧 Email: suporte@midiaflow.com

---

**Última atualização:** 30 de janeiro de 2025

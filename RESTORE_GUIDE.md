# 🔄 GUIA DE RESTAURAÇÃO - MEDIAFLOW v4.0

## 📋 ESTADO ATUAL DO SISTEMA

### ✅ FUNCIONALIDADES IMPLEMENTADAS:
- **Upload até 5GB** com multipart automático
- **Conversão automática** H.264 via MediaConvert
- **Sanitização** de nomes e emojis
- **Player responsivo** com controles completos
- **Visualizadores** para vídeos, imagens e PDFs
- **Analytics** com dados reais dos arquivos
- **Auto-cleanup** de chunks órfãos
- **Estrutura de pastas** preservada
- **Delete** individual e em lote

### 🏗️ INFRAESTRUTURA AWS DEPLOYADA:

#### **S3 Buckets:**
- `mediaflow-uploads-969430605054` - Arquivos originais
- `mediaflow-processed-969430605054` - Arquivos convertidos
- `mediaflow-frontend-969430605054` - Frontend estático

#### **Lambda Functions (6):**
1. `mediaflow-auth-handler` - Autenticação JWT
2. `mediaflow-files-handler` - Listagem de arquivos
3. `mediaflow-upload-handler` - Upload presigned URLs
4. `mediaflow-view-handler` - URLs de visualização
5. `mediaflow-cleanup-handler` - Limpeza automática
6. `mediaflow-convert-handler` - Conversão MediaConvert

#### **API Gateway:**
- **ID**: `gdb962d234`
- **URL Base**: `https://gdb962d234.execute-api.us-east-1.amazonaws.com/prod`
- **Rotas**:
  - `/auth` - POST (login)
  - `/files` - GET (listar), DELETE (remover)
  - `/upload` - POST (presigned URL)
  - `/view/{key}` - GET (visualizar)
  - `/convert` - POST (converter), GET (jobs)

#### **IAM Roles:**
- `mediaflow-lambda-role` - Para Lambdas
- `MediaConvertRole` - Para MediaConvert

### 🌐 URLs ATIVAS:
- **Frontend**: http://mediaflow-frontend-969430605054.s3-website-us-east-1.amazonaws.com
- **Login**: sergiosenaadmin@sstech / sergiosena

## 🔄 COMO RESTAURAR O PROJETO:

### 1. **CLONAR REPOSITÓRIO:**
```bash
git clone <repository-url>
cd drive-online-clean-NextJs
```

### 2. **INSTALAR DEPENDÊNCIAS:**
```bash
npm install
```

### 3. **CONFIGURAR VARIÁVEIS:**
```bash
cp .env.example .env.local
# Editar .env.local com:
JWT_SECRET=your_secret_key
```

### 4. **VERIFICAR AWS (se necessário):**
```bash
cd aws-setup
python deploy-lambdas.py
python upload-frontend.py
```

### 5. **BUILD E TESTE:**
```bash
npm run build
npm run dev
```

## 🧪 TESTES DE VERIFICAÇÃO:

### **Frontend:**
- [ ] Login funciona
- [ ] Upload de arquivos
- [ ] Visualização de vídeos
- [ ] Analytics carregam

### **Backend:**
- [ ] API Gateway responde
- [ ] Lambdas funcionam
- [ ] MediaConvert converte
- [ ] Cleanup automático

### **Conversão:**
```bash
curl -X POST "https://gdb962d234.execute-api.us-east-1.amazonaws.com/prod/convert" \
  -H "Content-Type: application/json" \
  -d '{"key":"arquivo.mp4"}'
```

## 📊 MONITORAMENTO:

### **Verificar Jobs:**
```bash
curl -X GET "https://gdb962d234.execute-api.us-east-1.amazonaws.com/prod/convert"
```

### **Verificar Buckets:**
```bash
aws s3 ls s3://mediaflow-uploads-969430605054/
aws s3 ls s3://mediaflow-processed-969430605054/
```

## 🆘 TROUBLESHOOTING:

### **Se Lambda não funcionar:**
```bash
cd aws-setup
python deploy-lambdas.py
```

### **Se Frontend não carregar:**
```bash
cd aws-setup
python upload-frontend.py
```

### **Se MediaConvert falhar:**
- Verificar role `MediaConvertRole`
- Verificar permissões S3
- Verificar endpoint MediaConvert

## 💾 BACKUP ADICIONAL:

### **Arquivos Críticos:**
- `aws-setup/` - Scripts de deploy
- `components/modules/` - Componentes React
- `lib/` - Clientes AWS
- `.env.local` - Variáveis de ambiente

### **Configurações AWS:**
- Account ID: `969430605054`
- Region: `us-east-1`
- API Gateway ID: `gdb962d234`

---

**Data do Backup**: 2025-09-10
**Versão**: Mediaflow v4.0 com MediaConvert
**Status**: 100% Funcional e Deployado
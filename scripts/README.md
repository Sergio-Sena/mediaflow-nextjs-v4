# 🛠️ Scripts Utilitários - Mediaflow

## 📁 Estrutura

```
scripts/
├── s3-operations/     # Scripts de movimentação e organização S3
├── testing/           # Scripts de teste e validação
└── README.md          # Este arquivo
```

---

## 📦 S3 Operations

Scripts para operações de movimentação e organização de arquivos no S3.

### Arquivos Disponíveis

- `copy_folder.js` - Copia pastas entre buckets
- `list_folders_via_api.js` - Lista pastas via API Gateway
- `list_root_folders.js` - Lista pastas no root do S3
- `move_folders_to_corporativo.js` - Move múltiplas pastas para Corporativo/
- `move_s3_direct.js` - Movimentação direta no S3
- `move_single_folder.js` - Move uma pasta específica
- `move_with_auth.js` - Movimentação com autenticação
- `move-to-corporativo.js` - Move para pasta Corporativo
- `preview-move-to-corporativo.js` - Preview de movimentação

### Uso Típico

```bash
cd scripts/s3-operations
node move_single_folder.js
```

---

## 🧪 Testing

Scripts de teste e validação do sistema.

### Arquivos Disponíveis

- `test_direct_route.js` - Testa rota direta de upload
- `test_frontend_upload.js` - Testa upload do frontend
- `test_real_small_file.js` - Testa arquivo pequeno real
- `test_small_file_403.js` - Debug de erro 403
- `test_upload_curl.js` - Testa upload via curl
- `test_upload_status.js` - Verifica status de upload
- `test-payload.json` - Payload de teste
- `test-phase1-production.js` - Testa fase 1 em produção
- `test-production.js` - Testes gerais de produção
- `test-s3.js` - Testa conexão S3
- `test-sanitization.js` - Testa sanitização de inputs
- `test-upload.js` - Testa sistema de upload
- `test-user-filter.js` - Testa filtro de usuários

### Uso Típico

```bash
cd scripts/testing
node test-production.js
```

---

## ⚠️ Avisos Importantes

### Antes de Executar Scripts S3

1. **Backup**: Sempre faça backup antes de mover arquivos
2. **Preview**: Use scripts de preview quando disponível
3. **Validação**: Verifique paths antes de executar
4. **Região**: Confirme região AWS (us-east-1)

### Antes de Executar Testes

1. **Ambiente**: Configure .env.local corretamente
2. **Credenciais**: Verifique AWS credentials
3. **Produção**: Cuidado ao tecorporativo em produção
4. **Cleanup**: Limpe arquivos de teste após uso

---

## 🔧 Configuração

### Variáveis de Ambiente Necessárias

```env
AWS_REGION=us-east-1
AWS_ACCOUNT_ID=969430605054
NEXT_PUBLIC_API_URL=https://gdb962d234.execute-api.us-east-1.amazonaws.com/prod
JWT_SECRET=your-secret-key
```

### Dependências

```bash
npm install  # Instala todas as dependências necessárias
```

---

## 📝 Manutenção

### Adicionar Novo Script

1. Criar arquivo na pasta apropriada (s3-operations/ ou testing/)
2. Adicionar documentação neste README
3. Tecorporativo em ambiente de desenvolvimento primeiro
4. Commitar com mensagem descritiva

### Remover Script Obsoleto

1. Verificar se não é usado em nenhum processo
2. Remover arquivo
3. Atualizar este README
4. Commitar mudança

---

**Última atualização**: 2025-01-18

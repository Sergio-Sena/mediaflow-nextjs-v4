# 🔧 Correções v4.4 - Controle de Acesso Multi-Usuário

## 🐛 Problemas Corrigidos

### 1. **useMemo guardando último usuário logado**
**Problema**: Ao fazer logout, a tela `/users` mostrava apenas o último usuário logado em vez de todos.

**Causa**: O `useMemo` lia `localStorage` dentro dele, mas as dependências não incluíam a sessão. Quando fazia logout, `currentUserId` e `currentUserRole` não eram resetados.

**Solução**:
- Resetar `currentUserId` e `currentUserRole` no `useEffect` quando não há sessão
- Remover leitura de `localStorage` dentro do `useMemo`

**Arquivo**: `app/users/page.tsx`

---

### 2. **Todos os usuários veem todos os arquivos**
**Problema**: Não havia controle de acesso por pasta S3. Todos os usuários viam todos os arquivos.

**Causa**: 
- Lambda `files-handler` tinha código para filtrar por `s3_prefix`, mas o frontend não enviava o token JWT
- JWT não incluía o campo `s3_prefix`
- Usuários no DynamoDB não tinham o campo `s3_prefix`

**Solução**:
1. **Frontend** (`lib/aws-client.ts`): Adicionar token JWT no header `Authorization`
2. **Lambda auth-handler**: Incluir `s3_prefix` no payload do JWT
3. **Lambda files-handler**: Corrigir `SECRET_KEY` para corresponder ao da auth
4. **DynamoDB**: Adicionar campo `s3_prefix` aos usuários existentes

---

## 📁 Estrutura de Pastas S3

```
mediaflow-uploads-969430605054/
├── Lid/                    # Arquivos do usuário 'lid'
│   ├── video1.mp4
│   └── video2.mp4
├── Sergio Sena/            # Arquivos do usuário 'sena'
│   ├── video3.mp4
│   └── video4.mp4
└── (root)                  # Arquivos do admin (sem prefixo)
    ├── video5.mp4
    └── video6.mp4
```

---

## 👥 Mapeamento de Usuários

| user_id | s3_prefix | role | Descrição |
|---------|-----------|------|-----------|
| `sergiosenaadmin` | `` (vazio) | `admin` | Vê todos os arquivos |
| `lid` | `Lid/` | `user` | Vê apenas arquivos em `Lid/` |
| `sena` | `Sergio Sena/` | `user` | Vê apenas arquivos em `Sergio Sena/` |

---

## 🚀 Deploy

### 1. Atualizar Lambdas e DynamoDB
```bash
cd aws-setup
deploy-lambdas.bat
```

Ou manualmente:
```bash
# 1. Atualizar auth-handler
cd lambda-functions/auth-handler
powershell -Command "Compress-Archive -Path lambda_function.py -DestinationPath auth.zip -Force"
aws lambda update-function-code --function-name mediaflow-auth-handler --zip-file fileb://auth.zip --region us-east-1

# 2. Atualizar files-handler
cd ../files-handler
powershell -Command "Compress-Archive -Path lambda_function.py -DestinationPath files-handler.zip -Force"
aws lambda update-function-code --function-name mediaflow-list-files --zip-file fileb://files-handler.zip --region us-east-1

# 3. Atualizar DynamoDB
cd ../..
python update-users-s3-prefix.py
```

### 2. Build e Deploy Frontend
```bash
npm run build
cd aws-setup
python upload-frontend.py
python invalidate-cache.py
```

### 3. Aguardar 2-3 minutos
CloudFront precisa propagar as mudanças.

---

## ✅ Testes

### Teste 1: Logout mostra todos os usuários
1. Faça login com qualquer usuário
2. Clique em "Sair"
3. ✅ Deve mostrar os 3 cards de usuários

### Teste 2: Trocar usuário mostra todos
1. Faça login com qualquer usuário
2. Clique em "Trocar"
3. ✅ Deve mostrar os 3 cards de usuários

### Teste 3: User vê apenas seus arquivos
1. Login com `lid@sstech` / `lid123`
2. Complete 2FA
3. ✅ Deve ver apenas arquivos da pasta `Lid/`

### Teste 4: Admin vê tudo
1. Login com `sergiosenaadmin@sstech` / `admin123`
2. Complete 2FA
3. ✅ Deve ver todos os arquivos (sem filtro)

### Teste 5: User vê apenas seu card
1. Login com `sena@sstech` / `sena123`
2. Complete 2FA
3. Vá para `/users`
4. ✅ Deve ver apenas seu próprio card

### Teste 6: Admin vê todos os cards
1. Login com `sergiosenaadmin@sstech` / `admin123`
2. Complete 2FA
3. Vá para `/users`
4. ✅ Deve ver os 3 cards

---

## 🔐 Fluxo de Autenticação Atualizado

```
1. Login → Lambda auth-handler
   ↓
2. Valida credenciais no DynamoDB
   ↓
3. Gera JWT com payload:
   {
     "email": "lid@sstech",
     "user_id": "lid",
     "s3_prefix": "Lid/",  ← NOVO
     "exp": 1234567890
   }
   ↓
4. Frontend armazena token no localStorage
   ↓
5. Ao listar arquivos → Lambda files-handler
   ↓
6. Extrai s3_prefix do JWT
   ↓
7. Filtra arquivos S3 por prefixo
   ↓
8. Retorna apenas arquivos permitidos
```

---

## 📝 Arquivos Modificados

### Frontend
- ✅ `app/users/page.tsx` - Corrigir useMemo e reset de estados
- ✅ `lib/aws-client.ts` - Adicionar token JWT no header

### Backend
- ✅ `lambda-functions/auth-handler/lambda_function.py` - Incluir s3_prefix no JWT
- ✅ `lambda-functions/files-handler/lambda_function.py` - Corrigir SECRET_KEY

### Scripts
- ✅ `aws-setup/update-users-s3-prefix.py` - Adicionar s3_prefix aos usuários
- ✅ `aws-setup/deploy-lambdas.bat` - Script de deploy automatizado

---

## 🎯 Próximos Passos v4.4

- [ ] Editar usuários existentes (email, senha, role, s3_prefix)
- [ ] Deletar usuários via admin panel
- [ ] Validação de email único no create-user
- [ ] Interface para gerenciar s3_prefix de cada usuário
- [ ] Logs de auditoria (quem acessou o quê)

---

## 📚 Referências

- **JWT Payload**: `auth-handler/lambda_function.py` linha 56
- **Filtro S3**: `files-handler/lambda_function.py` linha 42
- **Mapeamento Usuários**: `update-users-s3-prefix.py` linha 11

---

**✅ Sistema agora tem controle de acesso completo por usuário!**

# Sistema de Aprovacao de Usuarios

## Implementacao v4.8

### Problema
Qualquer pessoa podia se cadastrar em `/register` sem aprovacao do admin, criando risco de seguranca.

### Solucao
Sistema de aprovacao em 3 estados: **pending** → **approved** / **rejected**

---

## Arquitetura

### 1. Lambda approve-user (NOVA)
**Endpoint**: `POST /users/approve`

**Body**:
```json
{
  "user_id": "joao_silva",
  "action": "approve" // ou "reject"
}
```

**Funcao**: Atualiza campo `status` no DynamoDB

---

### 2. Lambda create-user (MODIFICADA)
**Mudanca**: Adiciona `status: 'pending'` ao criar usuario

**Antes**:
```python
user = {
  'user_id': user_id,
  'name': name,
  'email': email,
  'password': password_hash,
  'role': role,
  's3_prefix': s3_prefix,
  'avatar_url': avatar_url,
  'totp_secret': totp_secret,
  'created_at': datetime.utcnow().isoformat()
}
```

**Depois**:
```python
user = {
  'user_id': user_id,
  'name': name,
  'email': email,
  'password': password_hash,
  'role': role,
  's3_prefix': s3_prefix,
  'avatar_url': avatar_url,
  'totp_secret': totp_secret,
  'status': 'pending',  # NOVO
  'created_at': datetime.utcnow().isoformat()
}
```

---

### 3. Lambda auth-handler (MODIFICADA)
**Mudanca**: Bloqueia login de usuarios nao aprovados

**Validacao**:
```python
status = user.get('status', 'approved')  # Default para usuarios antigos
if status == 'pending':
    return cors_response(403, {'success': False, 'error': 'Conta aguardando aprovacao do administrador'})
if status == 'rejected':
    return cors_response(403, {'success': False, 'error': 'Conta rejeitada pelo administrador'})
```

---

### 4. Pagina /register (MODIFICADA)
**Mudanca**: Mensagem de aprovacao pendente

**Antes**: "Conta criada com sucesso!" (verde)  
**Depois**: "Conta criada! Aguardando aprovacao do administrador" (amarelo)

---

### 5. Painel Admin (MODIFICADO)
**Mudanca**: Secao de aprovacoes pendentes

**UI**:
```
┌─────────────────────────────────────┐
│ ⏳ Aprovacoes Pendentes (2)         │
├─────────────────────────────────────┤
│ [Avatar] Joao Silva                 │
│ Email: joao@email.com               │
│ ID: joao_silva                      │
│ [✅ Aprovar] [❌ Rejeitar]          │
└─────────────────────────────────────┘

┌─────────────────────────────────────┐
│ ✅ Usuarios Aprovados (5)           │
├─────────────────────────────────────┤
│ [Lista normal de usuarios]          │
└─────────────────────────────────────┘
```

---

## Fluxo Completo

### Cadastro
1. Usuario acessa `/register`
2. Preenche formulario (nome, email, senha, avatar)
3. Lambda `create-user` cria com `status: 'pending'`
4. Usuario ve mensagem: "Aguardando aprovacao"

### Tentativa de Login
1. Usuario tenta fazer login
2. Lambda `auth-handler` verifica `status`
3. Se `pending`: retorna erro 403
4. Se `rejected`: retorna erro 403
5. Se `approved`: permite login

### Aprovacao pelo Admin
1. Admin acessa `/admin`
2. Ve secao "Aprovacoes Pendentes"
3. Clica em "Aprovar" ou "Rejeitar"
4. Lambda `approve-user` atualiza `status`
5. Usuario pode fazer login (se aprovado)

---

## Deploy

### 1. Deploy Lambda approve-user
```bash
cd scripts
python deploy-approve-user.py
```

### 2. Configurar API Gateway
**Rota**: `POST /users/approve`  
**Integracao**: Lambda approve-user  
**CORS**: Habilitado

### 3. Deploy Lambda auth-handler
```bash
cd aws-setup/lambda-functions/auth-handler
zip -r auth.zip lambda_function.py
aws lambda update-function-code --function-name auth-handler --zip-file fileb://auth.zip
```

### 4. Deploy Lambda create-user
```bash
cd aws-setup/lambda-functions/create-user
zip -r create-user.zip lambda_function.py pyotp/
aws lambda update-function-code --function-name create-user --zip-file fileb://create-user.zip
```

### 5. Deploy Frontend
```bash
npm run build
aws s3 sync out/ s3://mediaflow-frontend-969430605054/ --delete
aws cloudfront create-invalidation --distribution-id E3VKFP0QLZPWQO --paths "/*"
```

---

## Compatibilidade

### Usuarios Antigos
Usuarios criados antes desta atualizacao **NAO tem campo `status`**.

**Solucao**: Default para `'approved'` no codigo:
```python
status = user.get('status', 'approved')
```

### Usuarios Novos
Todos os novos usuarios terao `status: 'pending'` e precisarao de aprovacao.

---

## Seguranca

### Protecoes
- ✅ Novos usuarios nao podem fazer login sem aprovacao
- ✅ Admin pode rejeitar usuarios suspeitos
- ✅ Usuarios rejeitados nao podem fazer login
- ✅ Usuarios antigos continuam funcionando

### Limitacoes
- ❌ Nao ha notificacao por email (futuro)
- ❌ Nao ha log de quem aprovou/rejeitou (futuro)
- ❌ Nao ha expiracao de contas pendentes (futuro)

---

## Proximos Passos (v4.9)

1. **Email de Notificacao**: Avisar admin quando novo usuario se cadastra
2. **Email de Aprovacao**: Avisar usuario quando conta for aprovada/rejeitada
3. **Log de Auditoria**: Registrar quem aprovou/rejeitou e quando
4. **Expiracao**: Deletar contas pendentes apos 7 dias
5. **Motivo de Rejeicao**: Admin pode adicionar motivo ao rejeitar

---

## Testes

### Teste 1: Cadastro
1. Acesse `/register`
2. Crie conta "teste_usuario"
3. Verifique mensagem amarela "Aguardando aprovacao"

### Teste 2: Login Bloqueado
1. Tente fazer login com "teste_usuario"
2. Verifique erro: "Conta aguardando aprovacao do administrador"

### Teste 3: Aprovacao
1. Faca login como admin
2. Acesse `/admin`
3. Veja "teste_usuario" em "Aprovacoes Pendentes"
4. Clique "Aprovar"
5. Verifique que usuario sumiu da secao pendente

### Teste 4: Login Aprovado
1. Faca login com "teste_usuario"
2. Verifique que login funciona normalmente

### Teste 5: Rejeicao
1. Crie outro usuario "teste_rejeitado"
2. Admin clica "Rejeitar"
3. Tente fazer login
4. Verifique erro: "Conta rejeitada pelo administrador"

---

## Status
- ✅ Lambda approve-user criada
- ✅ Lambda create-user modificada
- ✅ Lambda auth-handler modificada
- ✅ Pagina /register modificada
- ✅ Painel admin modificado
- ⏳ Deploy pendente
- ⏳ Testes pendentes

**Data**: 22/01/2025  
**Versao**: v4.8 (Sistema de Aprovacao)

# 🚀 Deploy Manual Otimizado

## Deploy Completo (1 comando)

```bash
python deploy.py
```

### O que faz:
1. ✅ **Backup automático** da versão atual
2. ✅ **Valida ambiente** (Node.js, AWS, S3)
3. ✅ **Build Next.js** otimizado
4. ✅ **Deploy para S3** com cache inteligente
5. ✅ **Invalida CloudFront** (cache global)
6. ✅ **Verifica deploy** (testa URL)

### Tempo: ~2-3 minutos

---

## Rollback Rápido

Se algo der errado:

```bash
python rollback.py
```

- Lista últimos 10 backups
- Restaura versão anterior em 1 minuto
- Invalida cache automaticamente

---

## Comandos Rápidos

### Deploy normal
```bash
python deploy.py
```

### Deploy sem backup (mais rápido)
```bash
# Edite deploy.py e comente a linha backup_current()
python deploy.py
```

### Apenas build (testar local)
```bash
npm run build
```

### Apenas upload (sem build)
```bash
# Edite deploy.py e comente build_nextjs()
python deploy.py
```

---

## Estrutura de Backups

```
midiaflow-backups-969430605054/
└── backups/
    ├── 20250111_001530/  ← Backup automático
    ├── 20250111_002145/
    └── 20250111_003220/
```

Backups são criados automaticamente antes de cada deploy.

---

## Troubleshooting

### Erro: "Build falhou"
```bash
# Limpar cache e reinstalar
rm -rf node_modules .next out
npm install
python deploy.py
```

### Erro: "AWS credentials"
```bash
aws configure
# Digite suas credenciais
```

### Erro: "Bucket não encontrado"
```bash
# Verifique se bucket existe
aws s3 ls | grep midiaflow
```

### Site não atualiza
```bash
# Aguarde 1-2 minutos para CloudFront propagar
# Ou force refresh: Ctrl+Shift+R
```

---

## Comparação: Manual vs CI/CD

| Aspecto | Deploy Manual | CI/CD GitHub |
|---------|---------------|--------------|
| **Tempo** | 2-3 min | 5-10 min |
| **Custo** | Grátis | Minutos limitados |
| **Controle** | Total | Automático |
| **Rollback** | Instantâneo | Complexo |
| **Backup** | Automático | Manual |
| **Validação** | Completa | Básica |

**Recomendação:** Deploy manual é mais rápido e prático para 1-2 desenvolvedores.

---

## Checklist de Deploy

- [ ] Código commitado no Git
- [ ] Testes locais passando
- [ ] `.env.local` configurado
- [ ] AWS credentials válidas
- [ ] Executar `python deploy.py`
- [ ] Verificar URL: https://midiaflow.sstechnologies-cloud.com
- [ ] Testar funcionalidades críticas

---

## Próximos Passos

Quando o projeto crescer:
1. Adicionar testes automatizados
2. Implementar CI/CD (quando tiver equipe)
3. Criar ambiente de staging
4. Configurar monitoramento avançado

Por enquanto, deploy manual é suficiente e eficiente! 🚀

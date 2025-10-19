# 📚 Regras de Organização - Pasta memoria/

## 🎯 Propósito

Manter a pasta `memoria/` **limpa, consolidada e fácil de navegar** em qualquer projeto.

---

## 📁 Estrutura Ideal

```
memoria/
├── PROMPT_CONSOLIDADO.md       # Contexto completo do projeto
├── METODO_DESENVOLVIMENTO.md   # Padrões e metodologia
├── PROMPT_PROXIMO_CHAT.md      # Contexto para próximo chat
└── README.md                   # Regras de organização
```

**Total: 4 arquivos máximo**

---

## ✅ O QUE MANTER

### 1. PROMPT_CONSOLIDADO.md
**Histórico completo do projeto**

Conteúdo:
- Contexto e arquitetura
- Funcionalidades implementadas
- Decisões de design
- Problemas resolvidos
- Roadmap futuro

Atualizar:
- Após cada versão major (v1.0, v2.0)
- Quando houver mudança arquitetural
- Ao resolver problemas críticos

### 2. METODO_DESENVOLVIMENTO.md
**Metodologia e padrões**

Conteúdo:
- Método C.E.R.T.O aplicado ao projeto
- Padrões de código específicos
- Lições aprendidas
- Processo de deploy

Atualizar:
- Quando houver mudança de padrões
- Ao aprender lições importantes
- Quando processo de deploy mudar

### 3. PROMPT_PROXIMO_CHAT.md
**Contexto rápido para continuação**

Conteúdo:
- Estado atual do projeto
- Próximos passos
- Comandos essenciais
- Links importantes

Atualizar:
- **Sempre** ao encerrar um chat
- Quando mudar prioridades
- Ao completar tarefas importantes

### 4. README.md
**Regras de organização**

Conteúdo:
- Propósito da pasta
- Estrutura dos arquivos
- Regras de manutenção
- Processo de atualização

Atualizar:
- Raramente (apenas se regras mudarem)

---

## ❌ O QUE NÃO COLOCAR

### Arquivos Temporários
```
❌ sessao-2025-01-19.md
❌ debug-log.txt
❌ temp-notes.md
```

### Documentos de Status
```
❌ STATUS_V1_0.md
❌ STATUS_V1_1.md
❌ STATUS_V1_2.md
```

### Backups de Documentação
```
❌ BACKUP_PROMPT.md
❌ OLD_METODO.md
❌ PROMPT_ANTIGO.md
```

### Prompts de Continuação Antigos
```
❌ PROMPT_CONTINUACAO_V1.md
❌ PROMPT_CONTINUACAO_V2.md
```

**Motivo**: Informação deve estar consolidada nos 4 arquivos principais.

---

## 🔄 Processo de Atualização

### Ao Finalizar uma Sessão de Desenvolvimento

#### 1. Atualizar PROMPT_CONSOLIDADO.md
```markdown
- Adicionar novas funcionalidades implementadas
- Documentar problemas resolvidos
- Atualizar roadmap
- Adicionar decisões técnicas importantes
```

#### 2. Atualizar METODO_DESENVOLVIMENTO.md (se necessário)
```markdown
- Adicionar novas lições aprendidas
- Documentar novos padrões adotados
- Atualizar processo de deploy (se mudou)
```

#### 3. Atualizar PROMPT_PROXIMO_CHAT.md
```markdown
- Atualizar estado atual
- Listar próximos passos
- Atualizar comandos essenciais
- Atualizar versão
```

#### 4. Remover Arquivos Temporários
```bash
# Deletar sessões antigas
rm memoria/sessao-*.md

# Deletar documentos de status
rm memoria/STATUS_*.md

# Deletar backups
rm memoria/BACKUP_*.md
```

---

## 📊 Checklist de Manutenção

### Semanal
- [ ] Verificar se há arquivos temporários
- [ ] Remover arquivos obsoletos
- [ ] Atualizar PROMPT_PROXIMO_CHAT.md

### Mensal
- [ ] Revisar PROMPT_CONSOLIDADO.md
- [ ] Atualizar roadmap
- [ ] Consolidar lições aprendidas

### Por Versão Major
- [ ] Atualizar PROMPT_CONSOLIDADO.md completo
- [ ] Revisar METODO_DESENVOLVIMENTO.md
- [ ] Documentar mudanças arquiteturais
- [ ] Atualizar métricas

---

## 🎯 Objetivo

**Manter apenas 4 arquivos essenciais:**

1. ✅ PROMPT_CONSOLIDADO.md - Histórico completo
2. ✅ METODO_DESENVOLVIMENTO.md - Metodologia
3. ✅ PROMPT_PROXIMO_CHAT.md - Próximo chat
4. ✅ README.md - Regras (este arquivo)

**Tudo consolidado, nada redundante, fácil de navegar.**

---

## 💡 Dicas Práticas

### 1. Consolidar, Não Acumular
```
❌ Errado: Criar novo arquivo para cada sessão
✅ Correto: Atualizar PROMPT_CONSOLIDADO.md
```

### 2. Informação Única
```
❌ Errado: Mesma informação em 3 arquivos
✅ Correto: Cada informação em 1 lugar só
```

### 3. Histórico no Git
```
❌ Errado: Manter backups manuais
✅ Correto: Usar git history para versões antigas
```

### 4. Nomes Descritivos
```
❌ Errado: doc1.md, notes.md, temp.md
✅ Correto: PROMPT_CONSOLIDADO.md (nome claro)
```

---

## 🚨 Sinais de Desorganização

### Quando Limpar?

Se você responder SIM para qualquer pergunta:

- [ ] Há mais de 4 arquivos na pasta memoria/?
- [ ] Há arquivos com "temp", "old", "backup" no nome?
- [ ] Há arquivos de sessão (sessao-*.md)?
- [ ] Há informação duplicada em múltiplos arquivos?
- [ ] Você não sabe onde está determinada informação?

**Então está na hora de limpar!**

---

## 🔧 Script de Limpeza

```bash
#!/bin/bash
# cleanup-memoria.sh

cd memoria/

# Manter apenas os 4 arquivos essenciais
find . -type f ! -name 'PROMPT_CONSOLIDADO.md' \
                ! -name 'METODO_DESENVOLVIMENTO.md' \
                ! -name 'PROMPT_PROXIMO_CHAT.md' \
                ! -name 'README.md' \
                -delete

echo "✅ Pasta memoria/ limpa!"
```

---

## 📝 Exemplo de Boa Organização

### Antes (Desorganizado)
```
memoria/
├── sessao-2025-01-15.md
├── sessao-2025-01-16.md
├── sessao-2025-01-17.md
├── STATUS_V1_0.md
├── STATUS_V1_1.md
├── BACKUP_PROMPT.md
├── OLD_METODO.md
├── PROMPT_CONTINUACAO_V1.md
├── PROMPT_CONTINUACAO_V2.md
├── temp-notes.md
└── debug-log.txt
```
**Total: 11 arquivos** ❌

### Depois (Organizado)
```
memoria/
├── PROMPT_CONSOLIDADO.md
├── METODO_DESENVOLVIMENTO.md
├── PROMPT_PROXIMO_CHAT.md
└── README.md
```
**Total: 4 arquivos** ✅

---

## 🎓 Benefícios

### Para Você
- ✅ Encontra informação rapidamente
- ✅ Não perde tempo procurando
- ✅ Contexto sempre atualizado

### Para o Projeto
- ✅ Documentação consistente
- ✅ Fácil onboarding de novos devs
- ✅ Histórico claro de decisões

### Para o Chat
- ✅ Contexto limpo e objetivo
- ✅ Menos tokens consumidos
- ✅ Respostas mais precisas

---

**Mantenha limpo, mantenha simples, mantenha útil!** 🎯

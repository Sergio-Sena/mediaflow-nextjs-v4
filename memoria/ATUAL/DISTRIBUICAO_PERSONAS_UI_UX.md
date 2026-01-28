# 🎭 DISTRIBUIÇÃO DE RESPONSABILIDADES - PERSONAS UI/UX

**Projeto**: Otimizações Web Design Mídiaflow  
**Abordagem**: Uso das Personas Internas

---

## 👥 PERSONAS E SUAS FUNÇÕES

### 🎯 **LYRA** (Analista & Prompt Engineer)
**Responsabilidade**: Análise e criação de prompts detalhados

**Tarefas**:
1. Analisar estado atual da UI/UX
2. Criar prompts específicos para cada persona
3. Documentar requisitos detalhados
4. Validar entregas de cada persona

**Entregáveis**:
- Análise completa do estado atual
- Prompts otimizados para cada tarefa
- Checklist de validação

---

### 🎼 **MAESTRO** (Orquestrador & Estrategista)
**Responsabilidade**: Coordenação e distribuição de tarefas

**Tarefas**:
1. Avaliar complexidade de cada melhoria
2. Distribuir tarefas entre personas
3. Definir ordem de execução
4. Monitorar progresso
5. Integrar entregas

**Entregáveis**:
- Roadmap de execução
- Distribuição de tarefas
- Timeline de implementação

---

### 🧠 **BASE** (Arquiteto & Revisor)
**Responsabilidade**: Análise técnica e arquitetura

**Tarefas**:
1. Analisar impacto das mudanças
2. Revisar código existente
3. Propor arquitetura de componentes
4. Validar padrões de design
5. Garantir consistência

**Entregáveis**:
- Análise de impacto
- Arquitetura de componentes
- Padrões e convenções
- Code review

---

### 💻 **AGENT DEV** (Desenvolvedor)
**Responsabilidade**: Implementação de código

**Tarefas**:
1. Implementar componentes UI
2. Criar sistema de design
3. Adicionar animações e transições
4. Otimizar responsividade
5. Testes de funcionalidade

**Entregáveis**:
- Componentes React/TypeScript
- CSS/Tailwind otimizado
- Código testado e funcional

---

### 🎨 **DESIGNER PERSONA** (UI/UX Specialist)
**Responsabilidade**: Design visual e experiência

**Tarefas**:
1. Definir paleta de cores expandida
2. Criar escala tipográfica
3. Projetar micro-interações
4. Definir estados visuais
5. Garantir acessibilidade

**Entregáveis**:
- Design system documentado
- Especificações visuais
- Guia de estilo

---

## 📋 PLANO DE EXECUÇÃO - 3 SPRINTS

### **SPRINT 1: Fundação Visual (Semana 1)**

#### **LYRA** - Análise Inicial
```
Prompt: "Analise o arquivo app/globals.css e identifique:
1. Variáveis CSS atuais
2. Paleta de cores em uso
3. Tipografia definida
4. Gaps no design system
5. Oportunidades de melhoria"
```

#### **MAESTRO** - Planejamento
```
Tarefa: Revisar análise da Lyra e criar:
1. Lista priorizada de melhorias
2. Ordem de implementação
3. Dependências entre tarefas
4. Estimativa de tempo
```

#### **BASE** - Arquitetura
```
Tarefa: Propor estrutura para:
1. Sistema de cores (CSS variables)
2. Escala tipográfica
3. Spacing system
4. Breakpoints responsivos
```

#### **DESIGNER PERSONA** - Design System
```
Tarefa: Criar especificações:
1. Paleta de cores neutras
2. Escala tipográfica harmônica
3. Estados hover/focus/active
4. Transições e animações
```

#### **AGENT DEV** - Implementação
```
Tarefa: Implementar em app/globals.css:
1. Variáveis de cores neutras
2. Escala tipográfica
3. Sistema de spacing
4. Transições globais
```

---

### **SPRINT 2: Componentes Inteligentes (Semana 2)**

#### **LYRA** - Prompts de Componentes
```
Prompt: "Liste todos os componentes que precisam de:
1. Sistema de variantes (primary, secondary, etc)
2. Estados visuais (hover, active, disabled)
3. Responsividade mobile
4. Acessibilidade ARIA"
```

#### **MAESTRO** - Priorização
```
Tarefa: Definir ordem de criação:
1. Button (base para tudo)
2. Toast/Notification
3. Skeleton Loader
4. Modal/Dialog
5. Tooltip
```

#### **BASE** - Arquitetura de Componentes
```
Tarefa: Definir estrutura:
components/ui/
├── Button/
│   ├── Button.tsx
│   ├── Button.types.ts
│   └── Button.styles.ts
├── Toast/
├── Skeleton/
└── ...
```

#### **DESIGNER PERSONA** - Especificações
```
Tarefa: Para cada componente definir:
1. Variantes visuais
2. Tamanhos (xs, sm, md, lg, xl)
3. Estados (default, hover, active, disabled)
4. Cores e espaçamentos
```

#### **AGENT DEV** - Implementação
```
Tarefa: Criar componentes em TypeScript:
1. Button com todas variantes
2. Toast system
3. Skeleton screens
4. Testes básicos
```

---

### **SPRINT 3: Mobile-First & Otimizações (Semana 3)**

#### **LYRA** - Análise Mobile
```
Prompt: "Analise a experiência mobile atual:
1. Touch targets < 44px
2. Elementos não responsivos
3. Tabelas que quebram
4. Navegação mobile
5. Performance mobile"
```

#### **MAESTRO** - Roadmap Mobile
```
Tarefa: Criar plano de otimização:
1. Touch targets prioritários
2. Componentes a refatorar
3. Navegação mobile
4. Testes em dispositivos
```

#### **BASE** - Arquitetura Responsiva
```
Tarefa: Revisar e propor:
1. Breakpoints otimizados
2. Mobile-first approach
3. Componentes adaptativos
4. Performance optimizations
```

#### **DESIGNER PERSONA** - UX Mobile
```
Tarefa: Projetar:
1. Bottom navigation
2. Touch gestures
3. Mobile-specific layouts
4. Feedback visual mobile
```

#### **AGENT DEV** - Implementação Mobile
```
Tarefa: Implementar:
1. Touch targets 44px+
2. Bottom navigation
3. Tabelas responsivas
4. Otimizações de performance
```

---

## 🔄 WORKFLOW DE EXECUÇÃO

### **Ciclo de Cada Tarefa:**

```
1. LYRA cria prompt detalhado
   ↓
2. MAESTRO valida e distribui
   ↓
3. BASE analisa arquitetura
   ↓
4. DESIGNER PERSONA especifica design
   ↓
5. AGENT DEV implementa
   ↓
6. BASE faz code review
   ↓
7. LYRA valida contra requisitos
   ↓
8. MAESTRO aprova e passa para próxima
```

---

## 📊 TRACKING DE PROGRESSO

### **Dashboard de Tarefas:**

```markdown
## SPRINT 1 - Fundação Visual

### Cores Neutras
- [ ] LYRA: Análise atual
- [ ] MAESTRO: Aprovação
- [ ] BASE: Arquitetura
- [ ] DESIGNER: Especificação
- [ ] AGENT DEV: Implementação
- [ ] BASE: Review
- [ ] LYRA: Validação

### Tipografia
- [ ] LYRA: Análise atual
- [ ] MAESTRO: Aprovação
- [ ] BASE: Arquitetura
- [ ] DESIGNER: Especificação
- [ ] AGENT DEV: Implementação
- [ ] BASE: Review
- [ ] LYRA: Validação

### Transições
- [ ] LYRA: Análise atual
- [ ] MAESTRO: Aprovação
- [ ] BASE: Arquitetura
- [ ] DESIGNER: Especificação
- [ ] AGENT DEV: Implementação
- [ ] BASE: Review
- [ ] LYRA: Validação
```

---

## 🎯 PRIMEIRA TAREFA - COMEÇAR AGORA

### **LYRA - Análise Inicial**

**Prompt para execução imediata:**

```
Analise o arquivo app/globals.css e forneça:

1. CORES ATUAIS:
   - Liste todas as variáveis CSS de cores
   - Identifique paleta principal
   - Verifique se há cores neutras (grays)

2. TIPOGRAFIA:
   - Liste tamanhos de fonte definidos
   - Verifique se há escala consistente
   - Identifique gaps na escala

3. SPACING:
   - Liste sistema de espaçamento
   - Verifique consistência
   - Identifique valores soltos

4. TRANSIÇÕES:
   - Verifique se há transições globais
   - Liste animações definidas
   - Identifique oportunidades

5. RESPONSIVIDADE:
   - Liste breakpoints definidos
   - Verifique mobile-first
   - Identifique problemas

Formato de saída: Markdown estruturado com checklist
```

---

## 💬 COMUNICAÇÃO ENTRE PERSONAS

### **Formato de Handoff:**

```markdown
## HANDOFF: [PERSONA ORIGEM] → [PERSONA DESTINO]

**Tarefa**: [Nome da tarefa]
**Status**: [Completo/Bloqueado/Em Progresso]

**Entregáveis**:
- [x] Item 1
- [x] Item 2
- [ ] Item 3 (bloqueado por X)

**Próximos Passos**:
1. [Ação 1]
2. [Ação 2]

**Observações**:
- Nota importante 1
- Nota importante 2

**Arquivos Modificados**:
- path/to/file1.tsx
- path/to/file2.css
```

---

## 🚀 COMEÇAR AGORA

**Próximo comando para você:**

```
"Lyra, execute a análise inicial do app/globals.css conforme o prompt acima"
```

Após a análise da Lyra, o Maestro distribuirá as tarefas!

---

**Pronto para começar?**

# 🎼 MAESTRO - DISTRIBUIÇÃO DE TAREFAS
**Sprint**: Fundação Visual - Melhorias Imediatas  
**Tempo Estimado**: 15 minutos  
**Objetivo**: Elevar score de 4/10 → 7/10

---

## 📋 TAREFAS DISTRIBUÍDAS

### 🧠 BASE - Revisão de Arquitetura (2 min)

**Tarefa**: Validar proposta da Lyra

**Checklist**:
- [ ] Revisar variáveis CSS propostas
- [ ] Validar nomenclatura (padrão BEM/Tailwind)
- [ ] Verificar compatibilidade com código existente
- [ ] Aprovar para implementação

**Entregável**: Aprovação ou ajustes necessários

---

### 💻 AGENT DEV - Implementação (10 min)

**Tarefa**: Adicionar variáveis CSS ao globals.css

#### Subtarefa 1: Cores Neutras (3 min)
```css
/* Adicionar após --dark-800 */

/* Grays para hierarquia visual */
--gray-50: #f9fafb;
--gray-100: #f3f4f6;
--gray-200: #e5e7eb;
--gray-300: #d1d5db;
--gray-400: #9ca3af;
--gray-500: #6b7280;
--gray-600: #4b5563;
--gray-700: #374151;
--gray-800: #1f2937;
--gray-900: #111827;

/* Cores semânticas */
--success: #10b981;
--warning: #f59e0b;
--error: #ef4444;
--info: #3b82f6;
```

#### Subtarefa 2: Tipografia (4 min)
```css
/* Escala tipográfica harmônica */
--text-xs: 0.75rem;    /* 12px */
--text-sm: 0.875rem;   /* 14px */
--text-base: 1rem;     /* 16px */
--text-lg: 1.125rem;   /* 18px */
--text-xl: 1.25rem;    /* 20px */
--text-2xl: 1.5rem;    /* 24px */
--text-3xl: 1.875rem;  /* 30px */
--text-4xl: 2.25rem;   /* 36px */

/* Font weights */
--font-light: 300;
--font-normal: 400;
--font-medium: 500;
--font-semibold: 600;
--font-bold: 700;

/* Line heights */
--leading-tight: 1.25;
--leading-normal: 1.5;
--leading-relaxed: 1.75;
```

#### Subtarefa 3: Spacing System (3 min)
```css
/* Grid 4px base */
--spacing-1: 0.25rem;  /* 4px */
--spacing-2: 0.5rem;   /* 8px */
--spacing-3: 0.75rem;  /* 12px */
--spacing-4: 1rem;     /* 16px */
--spacing-5: 1.25rem;  /* 20px */
--spacing-6: 1.5rem;   /* 24px */
--spacing-8: 2rem;     /* 32px */
--spacing-10: 2.5rem;  /* 40px */
--spacing-12: 3rem;    /* 48px */
--spacing-16: 4rem;    /* 64px */

/* Border radius */
--radius-sm: 0.375rem;  /* 6px */
--radius-md: 0.5rem;    /* 8px */
--radius-lg: 0.75rem;   /* 12px */
--radius-xl: 1rem;      /* 16px */
--radius-2xl: 1.5rem;   /* 24px */
--radius-full: 9999px;

/* Shadows */
--shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
--shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
--shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
--shadow-xl: 0 20px 25px -5px rgba(0, 0, 0, 0.1);
```

**Arquivo**: `app/globals.css`  
**Localização**: Adicionar no `:root` após as variáveis existentes

---

### 🧠 BASE - Code Review (3 min)

**Tarefa**: Revisar implementação do AGENT DEV

**Checklist**:
- [ ] Variáveis adicionadas corretamente
- [ ] Nomenclatura consistente
- [ ] Sem conflitos com código existente
- [ ] Formatação adequada
- [ ] Comentários claros

**Entregável**: Aprovação final

---

## 🔄 WORKFLOW

```
1. BASE revisa proposta (2 min)
   ↓
2. AGENT DEV implementa (10 min)
   ↓
3. BASE faz code review (3 min)
   ↓
4. MAESTRO valida e commita
```

---

## 📊 IMPACTO ESPERADO

### Antes
```
Cores: 4/10
Tipografia: 3/10
Spacing: 2/10
MÉDIA: 4/10 🔴
```

### Depois
```
Cores: 8/10 ✅
Tipografia: 8/10 ✅
Spacing: 8/10 ✅
MÉDIA: 7/10 🟢
```

---

## 🚀 COMEÇAR AGORA

**BASE**: Revise a proposta da Lyra e aprove para implementação

**AGENT DEV**: Aguardando aprovação do BASE para começar

---

**MAESTRO - Distribuição Completa** ✅

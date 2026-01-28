# 🎼 MAESTRO - SPRINT 2: COMPONENTES E APLICAÇÃO

**Objetivo**: Aplicar design system em TODAS as 11 páginas  
**Tempo**: 5 dias (1 semana)  
**Score**: 7/10 → 8.5/10

---

## 📋 DISTRIBUIÇÃO DE TAREFAS

### 🎨 DESIGNER PERSONA - Especificações (Dia 1 - manhã)

**Tarefa**: Definir especificações visuais dos componentes

#### Button
```typescript
Variantes: primary | secondary | ghost | danger
Tamanhos: sm | md | lg
Estados: default | hover | active | disabled | loading
```

#### Input
```typescript
Tipos: text | email | password | number | file
Estados: default | focus | error | disabled
```

#### Card
```typescript
Variantes: elevated | glass | flat
Padding: sm | md | lg
```

**Entregável**: Especificações em Markdown

---

### 🧠 BASE - Arquitetura (Dia 1 - tarde)

**Tarefa**: Definir estrutura e tipos TypeScript

#### Criar estrutura
```
components/ui/
├── Button/
├── Input/
├── Card/
├── Toast/
├── Modal/
├── Skeleton/
└── Badge/
```

#### Definir tipos base
```typescript
// types/components.ts
export interface BaseComponentProps {
  className?: string;
  children?: React.ReactNode;
}

export type Size = 'sm' | 'md' | 'lg';
export type Variant = 'primary' | 'secondary' | 'ghost' | 'danger';
```

**Entregável**: Estrutura + tipos base

---

### 💻 AGENT DEV - Implementação Fase 1 (Dia 2)

**Tarefa**: Criar componentes base

#### 1. Button Component
```tsx
// components/ui/Button/Button.tsx
interface ButtonProps {
  variant?: 'primary' | 'secondary' | 'ghost' | 'danger';
  size?: 'sm' | 'md' | 'lg';
  loading?: boolean;
  disabled?: boolean;
  children: React.ReactNode;
  onClick?: () => void;
}
```

#### 2. Input Component
```tsx
// components/ui/Input/Input.tsx
interface InputProps {
  type?: 'text' | 'email' | 'password' | 'number' | 'file';
  label?: string;
  error?: string;
  disabled?: boolean;
}
```

#### 3. Card Component
```tsx
// components/ui/Card/Card.tsx
interface CardProps {
  variant?: 'elevated' | 'glass' | 'flat';
  padding?: 'sm' | 'md' | 'lg';
  children: React.ReactNode;
}
```

**Entregável**: 3 componentes funcionais

---

### 💻 AGENT DEV - Implementação Fase 2 (Dia 3)

**Tarefa**: Criar componentes de feedback

#### 4. Toast Component
```tsx
// components/ui/Toast/Toast.tsx
// components/ui/Toast/ToastProvider.tsx
// components/ui/Toast/useToast.ts
```

#### 5. Skeleton Component
```tsx
// components/ui/Skeleton/Skeleton.tsx
```

#### 6. Modal Component
```tsx
// components/ui/Modal/Modal.tsx
```

**Entregável**: 3 componentes funcionais

---

### 💻 AGENT DEV - Aplicação Fase 1 (Dia 4)

**Tarefa**: Aplicar em páginas prioritárias

#### Páginas Prioridade 1
```
1. app/(auth)/login/page.tsx
   - Substituir botões por <Button>
   - Substituir inputs por <Input>
   - Adicionar <Toast> para feedback

2. app/(auth)/register/page.tsx
   - Substituir botões por <Button>
   - Substituir inputs por <Input>
   - Adicionar <Toast> para feedback

3. app/dashboard/page.tsx
   - Substituir botões por <Button>
   - Substituir cards por <Card>
   - Adicionar <Skeleton> para loading

4. app/page.tsx (Home)
   - Substituir botões por <Button>
   - Substituir cards por <Card>
```

**Entregável**: 4 páginas refatoradas

---

### 💻 AGENT DEV - Aplicação Fase 2 (Dia 5)

**Tarefa**: Aplicar nas páginas restantes

#### Páginas Prioridade 2
```
5. app/admin/page.tsx
6. app/users/page.tsx
7. app/pricing/page.tsx
8. app/docs/page.tsx
9. app/privacidade/page.tsx
10. app/termos/page.tsx
11. app/sla/page.tsx
```

**Entregável**: 7 páginas refatoradas

---

### 🧠 BASE - Code Review (Contínuo)

**Tarefa**: Revisar cada entrega

#### Checklist por Componente
- [ ] Usa variáveis CSS do Sprint 1
- [ ] TypeScript correto
- [ ] Acessibilidade (ARIA)
- [ ] Responsivo
- [ ] Estados visuais

#### Checklist por Página
- [ ] Todos componentes aplicados
- [ ] Sem valores hardcoded
- [ ] Funcionalidade mantida
- [ ] Performance OK

**Entregável**: Aprovação ou ajustes

---

## 📅 CRONOGRAMA DETALHADO

### Dia 1 (Segunda)
```
Manhã:
- DESIGNER: Especificações (3h)

Tarde:
- BASE: Arquitetura + Tipos (3h)
- MAESTRO: Review e aprovação (1h)
```

### Dia 2 (Terça)
```
Dia todo:
- AGENT DEV: Button + Input + Card (6h)
- BASE: Review contínuo (1h)
- MAESTRO: Validação (1h)
```

### Dia 3 (Quarta)
```
Dia todo:
- AGENT DEV: Toast + Skeleton + Modal (6h)
- BASE: Review contínuo (1h)
- MAESTRO: Validação (1h)
```

### Dia 4 (Quinta)
```
Dia todo:
- AGENT DEV: Aplicar em 4 páginas prioritárias (6h)
- BASE: Review contínuo (1h)
- MAESTRO: Validação (1h)
```

### Dia 5 (Sexta)
```
Dia todo:
- AGENT DEV: Aplicar em 7 páginas restantes (6h)
- BASE: Review final (1h)
- MAESTRO: Commit + Deploy (1h)
```

---

## 🎯 MÉTRICAS DE ACOMPANHAMENTO

### Componentes Criados
```
Dia 1: 0/6 (0%)
Dia 2: 3/6 (50%)
Dia 3: 6/6 (100%) ✅
```

### Páginas Refatoradas
```
Dia 3: 0/11 (0%)
Dia 4: 4/11 (36%)
Dia 5: 11/11 (100%) ✅
```

### Score UI/UX
```
Início: 7.0/10
Dia 2: 7.3/10 (componentes criados)
Dia 4: 8.0/10 (páginas prioritárias)
Dia 5: 8.5/10 (todas páginas) ✅
```

---

## ✅ GARANTIA DE COBERTURA TOTAL

### Checklist Final (Dia 5)
```
Componentes:
- [ ] Button (todas variantes)
- [ ] Input (todos tipos)
- [ ] Card (todas variantes)
- [ ] Toast (todos tipos)
- [ ] Skeleton (todos tipos)
- [ ] Modal (funcional)

Páginas:
- [ ] Home
- [ ] Login
- [ ] Register
- [ ] Dashboard
- [ ] Admin
- [ ] Users
- [ ] Pricing
- [ ] Docs
- [ ] Privacidade
- [ ] Termos
- [ ] SLA

Validação:
- [ ] Todas páginas usam componentes
- [ ] Todas variáveis CSS aplicadas
- [ ] Nenhum valor hardcoded
- [ ] Score 8.5/10 atingido
```

---

## 🚀 COMEÇAR AGORA

**Primeira Tarefa**: DESIGNER PERSONA - Especificações

**Próximo comando**:
```
"Designer Persona, crie as especificações visuais para:
1. Button (variantes, tamanhos, estados)
2. Input (tipos, estados)
3. Card (variantes, padding)"
```

---

**MAESTRO - Sprint 2 Distribuído** ✅  
**Aguardando**: DESIGNER PERSONA iniciar

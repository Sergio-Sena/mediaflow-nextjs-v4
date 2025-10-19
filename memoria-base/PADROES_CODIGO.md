# 💻 Padrões de Código - Guia Universal

## 🎯 Princípios Fundamentais

### 1. KISS (Keep It Simple, Stupid)
**Solução mais simples que funciona**

```typescript
// ❌ Errado: Over-engineering
class UserFactory {
  private static instance: UserFactory
  private constructor() {}
  static getInstance() { return this.instance ||= new UserFactory() }
  createUser(data: UserData): User {
    return new UserBuilder()
      .withName(data.name)
      .withEmail(data.email)
      .build()
  }
}

// ✅ Correto: Simples e direto
function createUser(data: UserData): User {
  return { name: data.name, email: data.email }
}
```

---

### 2. DRY (Don't Repeat Yourself)
**Não repita código**

```typescript
// ❌ Errado: Código duplicado
function validateEmail(email: string) {
  return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)
}
function validateUserEmail(email: string) {
  return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)
}

// ✅ Correto: Função única
function validateEmail(email: string) {
  return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)
}
```

---

### 3. YAGNI (You Aren't Gonna Need It)
**Implemente apenas o necessário agora**

```typescript
// ❌ Errado: Funcionalidades "por precaução"
interface User {
  id: string
  name: string
  email: string
  phone?: string        // Não usado ainda
  address?: string      // Não usado ainda
  birthdate?: Date      // Não usado ainda
  preferences?: object  // Não usado ainda
}

// ✅ Correto: Apenas o necessário
interface User {
  id: string
  name: string
  email: string
}
// Adicione campos quando realmente precisar
```

---

### 4. Separation of Concerns
**Separar responsabilidades**

```typescript
// ❌ Errado: Tudo junto
function processOrder(order: Order) {
  // Validação
  if (!order.items.length) throw new Error('Empty order')
  
  // Cálculo
  const total = order.items.reduce((sum, item) => sum + item.price, 0)
  
  // Pagamento
  const payment = stripe.charge(total)
  
  // Email
  sendEmail(order.user.email, 'Order confirmed')
  
  // Database
  db.orders.insert(order)
}

// ✅ Correto: Separado
function validateOrder(order: Order) { /* ... */ }
function calculateTotal(items: Item[]) { /* ... */ }
function processPayment(total: number) { /* ... */ }
function sendConfirmation(email: string) { /* ... */ }
function saveOrder(order: Order) { /* ... */ }

function processOrder(order: Order) {
  validateOrder(order)
  const total = calculateTotal(order.items)
  processPayment(total)
  sendConfirmation(order.user.email)
  saveOrder(order)
}
```

---

### 5. Fail Fast
**Validar cedo, falhar cedo**

```typescript
// ❌ Errado: Validação tardia
function createUser(name: string, email: string) {
  const user = { name, email }
  // ... 100 linhas de código ...
  if (!email.includes('@')) throw new Error('Invalid email')
  return user
}

// ✅ Correto: Validação imediata
function createUser(name: string, email: string) {
  if (!name) throw new Error('Name required')
  if (!email.includes('@')) throw new Error('Invalid email')
  
  return { name, email }
}
```

---

## 📝 Convenções de Nomenclatura

### Variáveis e Funções
```typescript
// ✅ Correto: camelCase descritivo
const userName = 'John'
const isAuthenticated = true
const totalPrice = 100

function calculateTotal() {}
function getUserById() {}
```

### Classes e Interfaces
```typescript
// ✅ Correto: PascalCase
class UserService {}
interface UserData {}
type OrderStatus = 'pending' | 'completed'
```

### Constantes
```typescript
// ✅ Correto: UPPER_SNAKE_CASE
const MAX_RETRIES = 3
const API_BASE_URL = 'https://api.example.com'
```

### Arquivos
```typescript
// ✅ Correto: kebab-case
user-service.ts
order-controller.ts
payment-utils.ts
```

---

## 🏗️ Estrutura de Código

### Componentes React
```typescript
// ✅ Estrutura padrão
import { useState, useEffect } from 'react'
import { ExternalLib } from 'external-lib'
import { InternalUtil } from '@/lib/utils'
import './styles.css'

interface Props {
  title: string
  onSubmit: () => void
}

export default function Component({ title, onSubmit }: Props) {
  // 1. Hooks
  const [state, setState] = useState('')
  
  // 2. Effects
  useEffect(() => {}, [])
  
  // 3. Handlers
  const handleClick = () => {}
  
  // 4. Render
  return <div>{title}</div>
}
```

### Funções
```typescript
// ✅ Estrutura padrão
/**
 * Calcula o total do pedido
 * @param items - Lista de itens
 * @returns Total em centavos
 */
export function calculateTotal(items: Item[]): number {
  // 1. Validação
  if (!items.length) return 0
  
  // 2. Processamento
  const total = items.reduce((sum, item) => sum + item.price, 0)
  
  // 3. Retorno
  return total
}
```

---

## 🧪 Testes

### Estrutura de Teste
```typescript
describe('calculateTotal', () => {
  it('should return 0 for empty array', () => {
    expect(calculateTotal([])).toBe(0)
  })
  
  it('should calculate sum correctly', () => {
    const items = [{ price: 10 }, { price: 20 }]
    expect(calculateTotal(items)).toBe(30)
  })
  
  it('should handle negative prices', () => {
    const items = [{ price: -10 }]
    expect(calculateTotal(items)).toBe(-10)
  })
})
```

---

## 📊 Comentários

### Quando Comentar
```typescript
// ✅ Bom: Explica o "porquê"
// Usamos setTimeout para evitar race condition com o banco
setTimeout(() => saveData(), 100)

// ✅ Bom: Documenta API pública
/**
 * Envia email de confirmação
 * @param email - Email do destinatário
 * @throws {EmailError} Se email inválido
 */
export function sendConfirmation(email: string) {}
```

### Quando NÃO Comentar
```typescript
// ❌ Ruim: Óbvio
// Incrementa contador
counter++

// ❌ Ruim: Código auto-explicativo
// Valida se usuário está autenticado
if (user.isAuthenticated) {}

// ✅ Melhor: Código claro sem comentário
if (user.isAuthenticated) {}
```

---

## 🔒 Segurança

### Input Validation
```typescript
// ✅ Sempre validar inputs
function createUser(data: unknown) {
  // Validação de tipo
  if (typeof data !== 'object' || !data) {
    throw new Error('Invalid data')
  }
  
  // Validação de campos
  const { name, email } = data as any
  if (!name || !email) {
    throw new Error('Missing fields')
  }
  
  // Sanitização
  const sanitizedName = name.trim()
  const sanitizedEmail = email.toLowerCase().trim()
  
  return { name: sanitizedName, email: sanitizedEmail }
}
```

### Senhas
```typescript
// ❌ Nunca armazenar em plain text
const user = { password: '123456' }

// ✅ Sempre hash
import bcrypt from 'bcrypt'
const hashedPassword = await bcrypt.hash(password, 10)
const user = { passwordHash: hashedPassword }
```

---

## ⚡ Performance

### Evitar Loops Desnecessários
```typescript
// ❌ Ruim: Múltiplos loops
const names = users.map(u => u.name)
const emails = users.map(u => u.email)
const ages = users.map(u => u.age)

// ✅ Bom: Um loop só
const { names, emails, ages } = users.reduce((acc, u) => ({
  names: [...acc.names, u.name],
  emails: [...acc.emails, u.email],
  ages: [...acc.ages, u.age]
}), { names: [], emails: [], ages: [] })
```

### Memoização
```typescript
// ✅ React: useMemo para cálculos pesados
const expensiveValue = useMemo(() => {
  return heavyCalculation(data)
}, [data])

// ✅ React: useCallback para funções
const handleClick = useCallback(() => {
  doSomething()
}, [dependency])
```

---

## 🔄 Async/Await

### Padrão Correto
```typescript
// ✅ Correto: Try/catch
async function fetchUser(id: string) {
  try {
    const response = await fetch(`/api/users/${id}`)
    if (!response.ok) throw new Error('User not found')
    return await response.json()
  } catch (error) {
    console.error('Error fetching user:', error)
    throw error
  }
}

// ✅ Correto: Promise.all para paralelo
async function fetchMultiple() {
  const [users, posts, comments] = await Promise.all([
    fetchUsers(),
    fetchPosts(),
    fetchComments()
  ])
  return { users, posts, comments }
}
```

---

## 📦 Imports

### Ordem de Imports
```typescript
// 1. Externos
import React from 'react'
import { useRouter } from 'next/router'

// 2. Internos (alias)
import { Button } from '@/components/Button'
import { formatDate } from '@/lib/utils'

// 3. Relativos
import { helper } from './helper'
import './styles.css'
```

---

## ✅ Code Review Checklist

### Antes de Commitar
- [ ] Código compila sem warnings
- [ ] Testes passam
- [ ] Sem console.logs desnecessários
- [ ] Variáveis nomeadas corretamente
- [ ] Sem código comentado (deletar)
- [ ] Formatação consistente (Prettier)
- [ ] Sem imports não utilizados

### Antes de Pull Request
- [ ] Descrição clara do que foi feito
- [ ] Testes adicionados/atualizados
- [ ] Documentação atualizada
- [ ] Screenshots (se UI)
- [ ] Breaking changes documentadas

---

## 🎯 Métricas de Qualidade

### Função Ideal
- **Linhas**: < 50
- **Parâmetros**: < 4
- **Complexidade ciclomática**: < 10
- **Nível de aninhamento**: < 3

### Arquivo Ideal
- **Linhas**: < 300
- **Funções**: < 10
- **Imports**: < 20

---

## 💡 Dicas Finais

### 1. Código é Lido Mais Que Escrito
```
Escreva código para humanos, não para máquinas
```

### 2. Refatore Sem Medo
```
Código ruim hoje é melhor que código perfeito nunca
Mas código bom amanhã é melhor que código ruim sempre
```

### 3. Teste Sempre
```
Código sem teste é código legado desde o dia 1
```

### 4. Documente Decisões
```
Código mostra COMO, comentários mostram PORQUÊ
```

---

**Use estes padrões em QUALQUER linguagem/framework!** 🎯

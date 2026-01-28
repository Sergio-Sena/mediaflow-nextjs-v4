# 🎨 DESIGNER PERSONA - ESPECIFICAÇÕES VISUAIS

**Tarefa**: Definir design dos componentes  
**Base**: Variáveis CSS do Sprint 1

---

## 1️⃣ BUTTON COMPONENT

### Variantes

#### Primary (Ação Principal)
```css
background: linear-gradient(135deg, var(--neon-cyan), #0080ff);
color: var(--dark-900);
font-size: var(--text-base);
font-weight: var(--font-semibold);
padding: var(--spacing-3) var(--spacing-6);
border-radius: var(--radius-lg);
box-shadow: 0 4px 20px rgba(0, 255, 255, 0.3);

hover:
  box-shadow: 0 6px 30px rgba(0, 255, 255, 0.5);
  transform: translateY(-2px);

active:
  transform: translateY(0);

disabled:
  opacity: 0.5;
  cursor: not-allowed;

loading:
  opacity: 0.7;
  cursor: wait;
```

#### Secondary (Ação Secundária)
```css
background: rgba(255, 255, 255, 0.08);
color: white;
font-size: var(--text-base);
font-weight: var(--font-medium);
padding: var(--spacing-3) var(--spacing-6);
border-radius: var(--radius-lg);
border: 1px solid rgba(255, 255, 255, 0.15);

hover:
  background: rgba(255, 255, 255, 0.12);
  border-color: var(--neon-cyan);
```

#### Ghost (Ação Terciária)
```css
background: transparent;
color: var(--gray-300);
font-size: var(--text-base);
font-weight: var(--font-medium);
padding: var(--spacing-3) var(--spacing-6);
border-radius: var(--radius-lg);
border: 1px solid rgba(255, 255, 255, 0.1);

hover:
  background: rgba(255, 255, 255, 0.05);
  color: white;
```

#### Danger (Ações Destrutivas)
```css
background: linear-gradient(135deg, var(--error), #cc0066);
color: white;
font-size: var(--text-base);
font-weight: var(--font-semibold);
padding: var(--spacing-3) var(--spacing-6);
border-radius: var(--radius-lg);

hover:
  box-shadow: 0 4px 20px rgba(239, 68, 68, 0.4);
```

### Tamanhos

```css
sm:
  font-size: var(--text-sm);
  padding: var(--spacing-2) var(--spacing-4);

md (default):
  font-size: var(--text-base);
  padding: var(--spacing-3) var(--spacing-6);

lg:
  font-size: var(--text-lg);
  padding: var(--spacing-4) var(--spacing-8);
```

---

## 2️⃣ INPUT COMPONENT

### Base Style
```css
width: 100%;
font-size: var(--text-base);
padding: var(--spacing-3) var(--spacing-4);
background: rgba(26, 26, 26, 0.8);
border: 1px solid var(--gray-700);
border-radius: var(--radius-md);
color: white;
transition: all 0.2s;

focus:
  outline: none;
  border-color: var(--neon-cyan);
  box-shadow: 0 0 0 3px rgba(0, 255, 255, 0.1);

error:
  border-color: var(--error);
  
disabled:
  opacity: 0.5;
  cursor: not-allowed;
```

### Label
```css
font-size: var(--text-sm);
font-weight: var(--font-medium);
color: var(--gray-300);
margin-bottom: var(--spacing-2);
```

### Error Message
```css
font-size: var(--text-sm);
color: var(--error);
margin-top: var(--spacing-1);
```

---

## 3️⃣ CARD COMPONENT

### Variantes

#### Elevated (Com Sombra)
```css
background: rgba(26, 26, 26, 0.8);
backdrop-filter: blur(20px);
border: 1px solid var(--gray-800);
border-radius: var(--radius-xl);
box-shadow: var(--shadow-lg);

hover:
  transform: translateY(-4px);
  box-shadow: var(--shadow-xl);
  border-color: rgba(0, 255, 255, 0.2);
```

#### Glass (Glass Morphism)
```css
background: rgba(26, 26, 26, 0.7);
backdrop-filter: blur(10px);
border: 1px solid rgba(0, 255, 255, 0.1);
border-radius: var(--radius-xl);
box-shadow: 0 8px 32px rgba(0, 255, 255, 0.1);
```

#### Flat (Sem Sombra)
```css
background: rgba(26, 26, 26, 0.6);
border: 1px solid var(--gray-800);
border-radius: var(--radius-xl);
```

### Padding

```css
sm:
  padding: var(--spacing-4);

md (default):
  padding: var(--spacing-6);

lg:
  padding: var(--spacing-8);
```

---

## 4️⃣ TOAST COMPONENT

### Tipos

#### Success
```css
background: var(--success);
color: white;
padding: var(--spacing-4) var(--spacing-6);
border-radius: var(--radius-lg);
box-shadow: var(--shadow-lg);
border-left: 4px solid #059669;
```

#### Error
```css
background: var(--error);
color: white;
padding: var(--spacing-4) var(--spacing-6);
border-radius: var(--radius-lg);
box-shadow: var(--shadow-lg);
border-left: 4px solid #dc2626;
```

#### Warning
```css
background: var(--warning);
color: var(--dark-900);
padding: var(--spacing-4) var(--spacing-6);
border-radius: var(--radius-lg);
box-shadow: var(--shadow-lg);
border-left: 4px solid #d97706;
```

#### Info
```css
background: var(--info);
color: white;
padding: var(--spacing-4) var(--spacing-6);
border-radius: var(--radius-lg);
box-shadow: var(--shadow-lg);
border-left: 4px solid #2563eb;
```

### Posicionamento
```css
position: fixed;
top: var(--spacing-4);
right: var(--spacing-4);
z-index: 9999;
min-width: 300px;
max-width: 500px;
```

### Animação
```css
@keyframes slide-in {
  from {
    transform: translateX(100%);
    opacity: 0;
  }
  to {
    transform: translateX(0);
    opacity: 1;
  }
}

animation: slide-in 0.3s ease-out;
```

---

## 5️⃣ SKELETON COMPONENT

### Base Style
```css
background: linear-gradient(
  90deg,
  var(--gray-800) 25%,
  var(--gray-700) 50%,
  var(--gray-800) 75%
);
background-size: 200% 100%;
animation: shimmer 1.5s infinite;
border-radius: var(--radius-md);
```

### Variantes

#### Text
```css
height: var(--text-base);
width: 100%;
```

#### Card
```css
height: 200px;
width: 100%;
border-radius: var(--radius-xl);
```

#### Avatar
```css
height: 48px;
width: 48px;
border-radius: var(--radius-full);
```

#### Video
```css
aspect-ratio: 16/9;
width: 100%;
border-radius: var(--radius-lg);
```

---

## 6️⃣ MODAL COMPONENT

### Overlay
```css
position: fixed;
inset: 0;
background: rgba(0, 0, 0, 0.8);
backdrop-filter: blur(4px);
z-index: 9998;
```

### Content
```css
position: fixed;
top: 50%;
left: 50%;
transform: translate(-50%, -50%);
background: var(--dark-800);
border: 1px solid var(--gray-700);
border-radius: var(--radius-xl);
padding: var(--spacing-8);
max-width: 500px;
width: 90%;
max-height: 90vh;
overflow-y: auto;
box-shadow: var(--shadow-xl);
z-index: 9999;
```

### Animação
```css
@keyframes modal-in {
  from {
    opacity: 0;
    transform: translate(-50%, -48%);
  }
  to {
    opacity: 1;
    transform: translate(-50%, -50%);
  }
}

animation: modal-in 0.2s ease-out;
```

---

## 7️⃣ BADGE COMPONENT

### Variantes

#### Default
```css
background: var(--gray-700);
color: var(--gray-200);
font-size: var(--text-xs);
font-weight: var(--font-medium);
padding: var(--spacing-1) var(--spacing-2);
border-radius: var(--radius-full);
```

#### Success
```css
background: rgba(16, 185, 129, 0.2);
color: var(--success);
border: 1px solid var(--success);
```

#### Error
```css
background: rgba(239, 68, 68, 0.2);
color: var(--error);
border: 1px solid var(--error);
```

#### Warning
```css
background: rgba(245, 158, 11, 0.2);
color: var(--warning);
border: 1px solid var(--warning);
```

---

## 📱 RESPONSIVIDADE

### Breakpoints (já definidos no Sprint 1)
```css
Mobile: < 640px
Tablet: 640px - 1024px
Desktop: > 1024px
```

### Ajustes Mobile

#### Button
```css
@media (max-width: 640px) {
  font-size: var(--text-sm);
  padding: var(--spacing-2) var(--spacing-4);
}
```

#### Card
```css
@media (max-width: 640px) {
  padding: var(--spacing-4);
  border-radius: var(--radius-lg);
}
```

#### Modal
```css
@media (max-width: 640px) {
  width: 95%;
  padding: var(--spacing-6);
}
```

---

## ♿ ACESSIBILIDADE

### Requisitos Obrigatórios

#### Button
```html
- role="button"
- aria-label (quando sem texto)
- aria-disabled (quando disabled)
- aria-busy (quando loading)
```

#### Input
```html
- aria-label ou label associado
- aria-invalid (quando error)
- aria-describedby (para error message)
```

#### Modal
```html
- role="dialog"
- aria-modal="true"
- aria-labelledby (título)
- aria-describedby (descrição)
- Trap focus dentro do modal
- ESC para fechar
```

#### Toast
```html
- role="alert"
- aria-live="polite"
- aria-atomic="true"
```

---

## 🎯 RESUMO DE VARIÁVEIS USADAS

### Do Sprint 1
```css
Cores:
- --neon-cyan, --neon-pink
- --dark-900, --dark-800
- --gray-50 a --gray-900
- --success, --warning, --error, --info

Tipografia:
- --text-xs, --text-sm, --text-base, --text-lg
- --font-medium, --font-semibold, --font-bold

Spacing:
- --spacing-1 a --spacing-8
- --radius-sm, --radius-md, --radius-lg, --radius-xl, --radius-full
- --shadow-sm, --shadow-md, --shadow-lg, --shadow-xl
```

**100% das variáveis do Sprint 1 serão utilizadas** ✅

---

## 🚀 HANDOFF → BASE

**Status**: ✅ Especificações Completas

**Entregáveis**:
- [x] 7 componentes especificados
- [x] Todas variantes definidas
- [x] Estados visuais claros
- [x] Responsividade planejada
- [x] Acessibilidade incluída

**Próximo**: BASE definir arquitetura TypeScript

---

**DESIGNER PERSONA - Especificações Concluídas** ✅

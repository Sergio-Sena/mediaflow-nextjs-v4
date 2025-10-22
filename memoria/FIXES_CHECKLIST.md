# 🔧 Correções do Checklist - userteste

## ❌ **1. Download - Access Denied**

### Problema:
Arquivos S3 não são públicos, download direto dá erro 403.

### Solução:
Usar signed URL via Lambda `/view/{key}`

### Código (FileList.tsx linha ~330):
```typescript
const handleDownload = async (file: S3File) => {
  try {
    const response = await fetch(`https://gdb962d234.execute-api.us-east-1.amazonaws.com/prod/view/${encodeURIComponent(file.key)}`, {
      method: 'GET',
      headers: { 'Content-Type': 'application/json' }
    })
    
    if (response.ok) {
      const data = await response.json()
      if (data.success) {
        // Usar signed URL para download
        const link = document.createElement('a')
        link.href = data.viewUrl
        link.download = file.name
        link.click()
      }
    }
  } catch (error) {
    alert('Erro ao fazer download')
  }
}
```

---

## ❌ **2. Busca - Mostra arquivos de todos os usuários**

### Problema:
Quando busca, mostra arquivos de `user_admin` e outros usuários.

### Solução:
Filtrar busca por pasta do usuário.

### Código (FileList.tsx linha ~240):
```typescript
const filteredFiles = (searchTerm ? files : getCurrentFiles()).filter(file => {
  // Normalizar busca
  const normalizedFileName = file.name.toLowerCase().replace(/[_\s]/g, '')
  const normalizedSearch = searchTerm.toLowerCase().replace(/[_\s]/g, '')
  const matchesSearch = normalizedFileName.includes(normalizedSearch)
  const matchesType = selectedType === 'all' || file.type === selectedType
  
  // NOVO: Filtrar por permissão do usuário
  const token = typeof window !== 'undefined' ? localStorage.getItem('token') : null
  let userRole = 'user'
  let userPrefix = ''
  
  if (token) {
    try {
      const payload = JSON.parse(atob(token.split('.')[1]))
      userRole = payload.role || 'user'
      const userId = payload.user_id || ''
      userPrefix = `users/${userId}`
    } catch (e) {}
  }
  
  // Admin vê tudo, user só vê seus arquivos
  const hasPermission = userRole === 'admin' || file.folder.startsWith(userPrefix)
  
  return matchesSearch && matchesType && hasPermission
})
```

---

## ❌ **3. Analytics - Mostra dados de todos os usuários**

### Problema:
Tab Analytics mostra total de arquivos/espaço de TODOS os usuários.

### Solução:
Filtrar analytics por usuário.

### Arquivo: `app/dashboard/page.tsx`

Procure a seção de Analytics e adicione filtro:

```typescript
// Dentro do componente DashboardPage, na função que calcula analytics

const calculateUserStats = (files: S3File[]) => {
  const token = localStorage.getItem('token')
  let userRole = 'user'
  let userId = ''
  
  if (token) {
    try {
      const payload = JSON.parse(atob(token.split('.')[1]))
      userRole = payload.role || 'user'
      userId = payload.user_id || ''
    } catch (e) {}
  }
  
  // Filtrar arquivos do usuário
  const userFiles = userRole === 'admin' 
    ? files 
    : files.filter(f => f.folder.startsWith(`users/${userId}`))
  
  // Calcular stats com userFiles ao invés de files
  const totalFiles = userFiles.length
  const totalSize = userFiles.reduce((acc, f) => acc + f.size, 0)
  
  // ... resto dos cálculos
}
```

---

## ❓ **4. Continue Assistindo - Botão não aparece**

### Verificar:
1. Assistiu vídeo até metade?
2. `localStorage` tem `lastWatchedVideo`?

### Debug:
```typescript
// No console do navegador:
console.log(localStorage.getItem('lastWatchedVideo'))
```

Se retornar `null`, o botão não aparece (comportamento correto).

### Solução:
Assistir qualquer vídeo por alguns segundos, sair e voltar ao dashboard.

---

## 📝 **Resumo de Mudanças**

| Problema | Arquivo | Linha Aprox | Status |
|----------|---------|-------------|--------|
| Download 403 | FileList.tsx | ~330 | ⏳ Corrigir |
| Busca global | FileList.tsx | ~240 | ⏳ Corrigir |
| Analytics global | dashboard/page.tsx | Seção Analytics | ⏳ Corrigir |
| Continue Assistindo | dashboard/page.tsx | Hero Section | ✅ OK (precisa assistir vídeo) |

---

## 🚀 **Próximos Passos**

1. Aplicar correções acima
2. Testar novamente com `userteste`
3. Confirmar que:
   - ✅ Download funciona
   - ✅ Busca só mostra arquivos do usuário
   - ✅ Analytics só mostra dados do usuário

---

*Última atualização: 22/01/2025 11:15*

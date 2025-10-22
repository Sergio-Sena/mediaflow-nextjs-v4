# 📁 Lógica de Upload com Hierarquia de Pastas

## 🎯 Objetivo
Quando o admin seleciona uma pasta no dropdown E escolhe arquivos de uma pasta local, o sistema deve manter a estrutura completa da pasta selecionada.

## 🔧 Como Funciona

### **webkitRelativePath**
O navegador automaticamente preenche `webkitRelativePath` com a estrutura **a partir da pasta selecionada**.

### **Exemplos Práticos**

#### 1️⃣ Selecionar `C:\Users\dell 5557\Videos\IDM\Anime`
```
webkitRelativePath = "Anime/video.mp4"
destination = "users/user_admin/"
RESULTADO = "users/user_admin/Anime/video.mp4"
```

#### 2️⃣ Selecionar `C:\Users\dell 5557\Videos\Star\Anime`
```
webkitRelativePath = "Star/Anime/video.mp4"
destination = "users/user_admin/"
RESULTADO = "users/user_admin/Star/Anime/video.mp4"
```

#### 3️⃣ Selecionar `C:\Users\dell 5557\Videos\IDM\Anime\Temporada1`
```
webkitRelativePath = "Anime/Temporada1/ep01.mp4"
destination = "users/user_admin/"
RESULTADO = "users/user_admin/Anime/Temporada1/ep01.mp4"
```

#### 4️⃣ Arquivo solto (sem pasta)
```
webkitRelativePath = ""
filename = "video.mp4"
destination = "users/user_admin/"
RESULTADO = "users/user_admin/video.mp4"
```

## 📊 Estrutura Final no S3

```
s3://mediaflow-uploads/
├── users/
│   └── user_admin/
│       ├── Anime/
│       │   ├── video1.mp4
│       │   └── Temporada1/
│       │       └── ep01.mp4
│       ├── Star/
│       │   └── Anime/
│       │       └── video2.mp4
│       └── video.mp4 (arquivo solto)
```

## 💻 Código Implementado

### DirectUpload.tsx
```typescript
let filename = (file as any).webkitRelativePath || file.name

if (destination) {
  // Manter estrutura completa da pasta selecionada
  filename = destination + filename
}
```

### MultipartUpload.tsx
```typescript
let filename = (file as any).webkitRelativePath || file.name

if (destination) {
  // Manter estrutura completa da pasta selecionada
  filename = destination + filename
}
```

### Lambda upload-handler
```python
# Extrair username do JWT
username = extract_username(event)

sanitized_name = sanitize_filename(filename)

# SEMPRE salvar em users/{username}/ respeitando estrutura original
sanitized_name = f'users/{username}/{sanitized_name}'
```

### Lambda multipart-handler
```python
# Extrair username do JWT
username = extract_username(event)

# SEMPRE usar users/{username}/ independente do filename
key = f"users/{username}/{filename}"
```

## ✅ Comportamento Esperado

| Ação | Caminho Local | Dropdown | Resultado S3 |
|------|--------------|----------|--------------|
| Selecionar pasta | `C:\Videos\IDM\Anime` | `📁 Minha pasta (Admin)` | `users/user_admin/Anime/` |
| Selecionar pasta | `C:\Videos\Star\Anime` | `📁 Minha pasta (Admin)` | `users/user_admin/Star/Anime/` |
| Selecionar pasta | `C:\Videos\Anime` | `📁 Minha pasta (Admin)` | `users/user_admin/Anime/` |
| Arquivo solto | - | `📁 Minha pasta (Admin)` | `users/user_admin/video.mp4` |
| Selecionar pasta | `C:\Videos\Anime` | `Raiz do sistema` | `users/user_admin/Anime/` |

## 🔑 Pontos Importantes

1. **webkitRelativePath já contém a estrutura correta** - não precisa manipular
2. **Sempre adicionar JWT token** - para extrair username correto
3. **Lambda respeita estrutura** - apenas adiciona `users/{username}/` no início
4. **Sem destino = raiz do usuário** - `users/{username}/`
5. **Com destino = pasta específica** - `users/user_admin/` (admin pode escolher)

## 🧪 Testes

Execute: `node scripts/test-folder-logic.js`

Valida todos os cenários de upload com diferentes estruturas de pastas.

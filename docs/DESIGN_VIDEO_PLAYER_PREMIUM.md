# Referência de Design - Player de Vídeo Premium

## Descrição Visual

Player de vídeo com interface overlay moderna, ícones finos (outline style), controles intuitivos e estética premium.

## Prompt para IA

"Crie um player de vídeo usando HTML5, CSS moderno e JavaScript. A interface deve ser um overlay sobre o vídeo. Use ícones finos (estilo Outline). O layout deve incluir:

**Topo:** Uma barra com seta de voltar à esquerda, título do arquivo centralizado e ícones de utilitários (câmera, redimensionar, áudio, tradução, menu) à direita.

**Centro:** Botões de Play/Pause grandes no meio, flanqueados por 'pular 10s' ou 'próximo/anterior'.

**Base:** Uma barra de progresso fina que atravessa toda a largura, com um marcador (thumb) circular branco. Abaixo da barra, mostre o tempo atual à esquerda e o tempo total à direita. Inclua um seletor de velocidade (1.0x) e um ícone de rotação de tela no canto inferior direito."

## Estrutura HTML

```html
<div class="video-container">
  <video src="seu-video.mp4"></video>
  
  <div class="controls-overlay">
    <div class="top-bar">
      <i class="back-icon"></i>
      <span class="video-title">VID-20260227-WA0057.mp4</span>
      <div class="top-icons"> </div>
    </div>

    <div class="mid-controls">
      <button class="prev-btn">|◀</button>
      <button class="play-pause">⏸</button>
      <button class="next-btn">▶|</button>
    </div>

    <div class="bottom-bar">
      <div class="progress-container">
        <span class="current-time">00:15</span>
        <input type="range" class="progress-bar">
        <span class="total-time">01:27</span>
      </div>
      <div class="bottom-utils">
        <span class="speed">1.0x</span>
        <i class="rotate-icon"></i>
      </div>
    </div>
  </div>
</div>
```

## CSS - Pontos Chave

### Background do Overlay
```css
.controls-overlay {
  background: rgba(0, 0, 0, 0.4);
}
```

### Barra de Progresso
- Use `input[type="range"]` customizado
- Parte assistida: azul vibrante
- Parte a carregar: cinza claro/transparente

### Tipografia
- Fontes sem serifa: Roboto ou Inter
- Visual limpo e moderno

## Bibliotecas de Ícones Recomendadas

- **Lucide React** - Ícones finos e elegantes
- **Phosphor Icons** - Traço fino premium

## Toques Finais

### Auto-hide
Controles desaparecem após 3 segundos sem interação

### Blur Premium
```css
backdrop-filter: blur(5px);
```
Aplicar nas barras de topo e base

### Cores
- Ícones: Branco (#FFFFFF)
- Progresso: Azul vibrante (#00A8FF ou similar)
- Background overlay: rgba(0, 0, 0, 0.4)

## Implementação Atual

Arquivo: `components/modules/VideoPlayer.tsx`

### Melhorias Sugeridas
1. Adicionar auto-hide nos controles
2. Implementar backdrop-filter blur
3. Usar ícones Lucide React
4. Customizar barra de progresso com thumb circular branco
5. Adicionar controles de velocidade visíveis
6. Implementar rotação de tela

## Referências

- Design inspirado em players mobile modernos
- Foco em UX intuitiva e visual premium
- Controles acessíveis e responsivos

## Prompt para Amazon Q: Implementação de Player de Vídeo em React/TypeScript (TSX)

**Objetivo:** Desenvolver um componente React (`VideoPlayer.tsx`) que replique fielmente a interface e a funcionalidade de um player de vídeo, conforme a imagem fornecida, utilizando TypeScript, React Hooks e estilização com Tailwind CSS.

### 1. Estrutura Geral do Componente

O componente principal `VideoPlayer` deve ser um `div` que atua como o contêiner do player. Ele deve ter um fundo preto (`bg-black`) e ser responsivo, ocupando a largura total disponível e uma altura proporcional ao vídeo (e.g., `aspect-video` ou altura fixa para o exemplo).

### 2. Área de Exibição do Vídeo

Dentro do contêiner principal, deve haver um elemento `<video>` que ocupará a maior parte da área. Este elemento deve ser configurado para:

*   Não exibir os controles nativos do navegador (`controls={false}`).
*   Ter uma referência (`ref`) para manipulação programática (play, pause, volume, etc.).
*   Ser o alvo principal para eventos de clique que alternam play/pause.

### 3. Barra de Controles Inferior

A barra de controles deve ser um `div` posicionado na parte inferior do contêiner do player, com um fundo semitransparente ou escuro (`bg-gray-800/75` ou similar) e `padding` adequado. Deve conter os seguintes elementos, dispostos horizontalmente e centralizados verticalmente:

#### 3.1. Botão Play/Pause

*   **Ícone:** Um ícone que alterna entre `Play` (triângulo) e `Pause` (dois traços verticais) com base no estado de reprodução do vídeo (`isPlaying`).
*   **Funcionalidade:** Ao clicar, deve alternar o estado `isPlaying` e chamar os métodos `play()` ou `pause()` do elemento `<video>`.
*   **Estilo:** Ícone branco (`text-white`), tamanho adequado (`text-2xl` ou similar).

#### 3.2. Barra de Progresso (Timeline)

*   **Estrutura:** Um `div` que representa a barra de progresso total. Dentro dele, dois `div`s aninhados:
    *   Um para o progresso já assistido (cor azul, e.g., `bg-blue-500`).
    *   Um para o progresso carregado (cor cinza mais clara, e.g., `bg-gray-400`).
*   **Indicador de Tempo:** Um pequeno balão (`div` com `absolute` positioning) que exibe o tempo atual do vídeo (`00:24` no exemplo). Este balão deve aparecer acima do ponto atual da barra de progresso.
*   **Funcionalidade:**
    *   A largura da barra de progresso azul deve ser atualizada dinamicamente com base no `currentTime` do vídeo.
    *   Ao clicar na barra de progresso, o vídeo deve pular para o ponto correspondente.
    *   Ao arrastar o indicador de tempo, o vídeo deve ser scrubbed.
*   **Estilo:** Linha fina (`h-1` ou `h-2`), cor de fundo da barra total (`bg-gray-600`).

#### 3.3. Controles de Áudio e Vídeo (Grupo à Direita)

Um `div` contendo os seguintes botões, alinhados à direita:

*   **Botão de Volume:**
    *   **Ícone:** Um ícone de alto-falante. Deve mudar para um ícone de mudo quando o volume for 0 ou `isMuted` for `true`.
    *   **Funcionalidade:** Ao clicar, deve alternar o estado `isMuted` do vídeo. Quando `isMuted` é `false`, o volume deve retornar ao último valor não-zero.
    *   **Estilo:** Ícone azul (`text-blue-500`) quando não mudo, branco (`text-white`) quando mudo.
*   **Botão de Configurações:**
    *   **Ícone:** Engrenagem (`gear` icon).
    *   **Funcionalidade:** Placeholder para um menu de configurações (não é necessário implementar o menu em si, apenas o botão).
    *   **Estilo:** Ícone branco (`text-white`).
*   **Botão Picture-in-Picture/Miniplayer:**
    *   **Ícone:** Retângulo menor dentro de um maior.
    *   **Funcionalidade:** Placeholder para a funcionalidade Picture-in-Picture.
    *   **Estilo:** Ícone branco (`text-white`).
*   **Botão de Tela Cheia:**
    *   **Ícone:** Quatro setas apontando para fora. Deve mudar para um ícone de sair da tela cheia quando `isFullscreen` for `true`.
    *   **Funcionalidade:** Ao clicar, deve alternar o estado `isFullscreen` e usar a API Fullscreen do navegador (`requestFullscreen()`, `exitFullscreen()`).
    *   **Estilo:** Ícone branco (`text-white`).

### 4. Controle de Volume Vertical

*   **Estrutura:** Um `div` posicionado verticalmente no lado direito do player, visível apenas quando o mouse está sobre o player ou o botão de volume.
*   **Barra:** Uma barra vertical com um preenchimento azul (`bg-blue-500`) indicando o nível de volume atual e um pequeno círculo branco (`bg-white`, `rounded-full`) como slider.
*   **Funcionalidade:** Ao clicar e arrastar, deve ajustar o volume do vídeo. O nível de volume deve ser refletido na altura do preenchimento azul.
*   **Estilo:** Fundo cinza escuro (`bg-gray-700`), largura fina (`w-1` ou `w-2`), altura adequada (`h-24` ou similar).

### 5. Botão de Curtir (Coração)

*   **Ícone:** Um contorno de coração (`heart` icon).
*   **Posicionamento:** Canto superior direito do contêiner do player, com `absolute` positioning e `margin` ou `padding` adequado.
*   **Funcionalidade:** Placeholder para a funcionalidade de curtir.
*   **Estilo:** Ícone branco (`text-white`), tamanho adequado (`text-2xl` ou similar).

### 6. Gerenciamento de Estado (React Hooks)

Utilizar `useState` e `useRef` para gerenciar os seguintes estados:

*   `isPlaying: boolean` (para controlar play/pause)
*   `currentTime: number` (tempo atual do vídeo)
*   `duration: number` (duração total do vídeo)
*   `volume: number` (nível de volume, de 0 a 1)
*   `isMuted: boolean` (estado de mudo)
*   `isFullscreen: boolean` (estado de tela cheia)
*   `showControls: boolean` (para esconder/mostrar controles em inatividade)
*   `videoRef: React.RefObject<HTMLVideoElement>` (referência para o elemento `<video>`)

### 7. Event Listeners

Implementar `useEffect` para adicionar e remover event listeners no elemento `<video>` e no `document` (para tela cheia):

*   `onTimeUpdate`: Atualizar `currentTime`.
*   `onLoadedMetadata`: Obter `duration`.
*   `onVolumeChange`: Atualizar `volume` e `isMuted`.
*   `onPlay`, `onPause`: Atualizar `isPlaying`.
*   `onMouseMove`, `onMouseLeave`: Para controlar a visibilidade dos controles e da barra de volume vertical.
*   `onFullscreenChange`: Para atualizar `isFullscreen`.

### 8. Ícones

Utilizar uma biblioteca de ícones como `react-icons` ou SVG inline para os ícones de Play, Pause, Volume, Mudo, Engrenagem, Picture-in-Picture, Tela Cheia e Coração.

### 9. Estilização (Tailwind CSS)

Todas as classes de estilo devem ser implementadas usando Tailwind CSS para layout, cores, espaçamento, tipografia e responsividade. Prestar atenção especial às cores exatas (azul da barra de progresso e volume, cinzas dos controles, branco dos ícones).

### 10. Considerações Adicionais

*   O componente deve ser escrito em `VideoPlayer.tsx`.
*   Não é necessário fornecer um arquivo de vídeo, apenas a estrutura do player.
*   Focar na fidelidade visual e funcional dos controles.
*   Garantir que o código seja limpo, modular e siga as melhores práticas de React/TypeScript.

---

**Exemplo de estrutura básica do componente (apenas para referência, o Amazon Q deve gerar o código completo):**

```tsx
import React, { useRef, useState, useEffect } from 'react';
// Importar ícones de uma biblioteca como react-icons
// import { FaPlay, FaPause, FaVolumeUp, FaVolumeMute, FaCog, FaExpand, FaCompress, FaHeart } from 'react-icons/fa';

const VideoPlayer: React.FC = () => {
  const videoRef = useRef<HTMLVideoElement>(null);
  const [isPlaying, setIsPlaying] = useState(false);
  const [currentTime, setCurrentTime] = useState(0);
  const [duration, setDuration] = useState(0);
  const [volume, setVolume] = useState(1);
  const [isMuted, setIsMuted] = useState(false);
  const [isFullscreen, setIsFullscreen] = useState(false);
  const [showControls, setShowControls] = useState(true);

  // ... lógica para event listeners e handlers ...

  return (
    <div className="relative w-full bg-black aspect-video overflow-hidden group">
      <video
        ref={videoRef}
        className="w-full h-full object-cover"
        onClick={() => { /* toggle play/pause */ }}
        onTimeUpdate={() => { /* update current time */ }}
        onLoadedMetadata={() => { /* set duration */ }}
        onVolumeChange={() => { /* update volume/mute state */ }}
      >
        {/* <source src="your-video-source.mp4" type="video/mp4" /> */}
        Seu navegador não suporta o elemento de vídeo.
      </video>

      {/* Botão de Curtir */}
      <div className="absolute top-4 right-4 text-white text-2xl cursor-pointer">
        {/* <FaHeart /> */}
      </div>

      {/* Barra de Controles Inferior */}
      <div className="absolute bottom-0 left-0 right-0 bg-gray-800/75 p-4 flex items-center space-x-4 opacity-0 group-hover:opacity-100 transition-opacity duration-300">
        {/* Botão Play/Pause */}
        <button className="text-white text-2xl">
          {/* {isPlaying ? <FaPause /> : <FaPlay />} */}
        </button>

        {/* Barra de Progresso */}
        <div className="relative flex-grow h-1 bg-gray-600 rounded-full cursor-pointer">
          <div className="absolute h-full bg-blue-500 rounded-full" style={{ width: `${(currentTime / duration) * 100}%` }}></div>
          <div className="absolute -top-6 left-0 bg-white text-black text-xs px-2 py-1 rounded" style={{ left: `${(currentTime / duration) * 100}%`, transform: 'translateX(-50%)' }}>
            {/* {formatTime(currentTime)} */}
          </div>
        </div>

        {/* Controles de Áudio e Vídeo */}
        <div className="flex items-center space-x-4">
          {/* Botão de Volume */}
          <button className="text-blue-500 text-2xl">
            {/* {isMuted || volume === 0 ? <FaVolumeMute /> : <FaVolumeUp />} */}
          </button>

          {/* Barra de Volume Vertical (visível ao hover no botão de volume) */}
          <div className="absolute bottom-16 -right-2 bg-gray-700 w-2 h-24 rounded-full flex flex-col-reverse">
            <div className="bg-blue-500 rounded-full" style={{ height: `${volume * 100}%` }}></div>
            <div className="absolute w-4 h-4 bg-white rounded-full -left-1" style={{ bottom: `${volume * 100 - 8}%` }}></div>
          </div>

          {/* Botão de Configurações */}
          <button className="text-white text-2xl">
            {/* <FaCog /> */}
          </button>
          {/* Botão Picture-in-Picture */}
          <button className="text-white text-2xl">
            {/* Ícone PiP */}
          </button>
          {/* Botão de Tela Cheia */}
          <button className="text-white text-2xl">
            {/* {isFullscreen ? <FaCompress /> : <FaExpand />} */}
          </button>
        </div>
      </div>
    </div>
  );
};

export default VideoPlayer;
```

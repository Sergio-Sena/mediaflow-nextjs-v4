const fs = require('fs');
const path = require('path');

const sourceDir = 'C:\\Users\\dell 5557\\Videos\\IDM\\Anime\\Jiggly Girls [Hentai on Brasil]';
const baseName = 'Jiggly Girls [Hentai on Brasil]';
const maxItems = 100;

// Ler todos os arquivos
const items = fs.readdirSync(sourceDir);
console.log(`Total de itens: ${items.length}`);

// Calcular número de partes
const totalParts = Math.ceil(items.length / maxItems);
console.log(`Dividindo em ${totalParts} partes...\n`);

// Criar pastas e mover arquivos
for (let i = 0; i < totalParts; i++) {
  const partName = `${baseName} part${i + 1}`;
  const partDir = path.join(path.dirname(sourceDir), partName);
  
  // Criar pasta
  if (!fs.existsSync(partDir)) {
    fs.mkdirSync(partDir);
  }
  
  // Pegar itens desta parte
  const start = i * maxItems;
  const end = Math.min(start + maxItems, items.length);
  const partItems = items.slice(start, end);
  
  console.log(`${partName}: ${partItems.length} itens`);
  
  // Mover arquivos
  partItems.forEach(item => {
    const oldPath = path.join(sourceDir, item);
    const newPath = path.join(partDir, item);
    fs.renameSync(oldPath, newPath);
  });
}

console.log('\n✅ Concluído!');

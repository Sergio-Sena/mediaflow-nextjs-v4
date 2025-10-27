const fs = require('fs');
const path = require('path');

const baseDir = 'C:\\Users\\dell 5557\\Videos\\IDM\\Anime\\Jiggly Girls [Hentai on Brasil] part1';

function countFiles(dir) {
  let count = 0;
  const items = fs.readdirSync(dir);
  
  items.forEach(item => {
    const fullPath = path.join(dir, item);
    const stat = fs.statSync(fullPath);
    
    if (stat.isDirectory()) {
      count += countFiles(fullPath);
    } else {
      count++;
    }
  });
  
  return count;
}

const total = countFiles(baseDir);
console.log(`Total de arquivos: ${total}`);

// Dividir em pastas
const maxItems = 100;
const totalParts = Math.ceil(total / maxItems);
console.log(`Necessário ${totalParts} partes de até ${maxItems} arquivos cada`);

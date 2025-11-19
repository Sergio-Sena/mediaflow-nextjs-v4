const fs = require('fs');
const path = require('path');

const sourceDir = 'C:\\Users\\dell 5557\\Videos\\IDM\\Anime\\Jiggly Girls [Hentai on Brasil] part1';
const targetBase = 'C:\\Users\\dell 5557\\Videos\\IDM\\Anime';
const baseName = 'Jiggly Girls [Hentai on Brasil]';
const maxItems = 100;

// Coletar todos os arquivos recursivamente
function getAllFiles(dir, fileList = []) {
  const items = fs.readdirSync(dir);
  
  items.forEach(item => {
    const fullPath = path.join(dir, item);
    const stat = fs.statSync(fullPath);
    
    if (stat.isDirectory()) {
      getAllFiles(fullPath, fileList);
    } else {
      fileList.push(fullPath);
    }
  });
  
  return fileList;
}

const allFiles = getAllFiles(sourceDir);
console.log(`Total de arquivos: ${allFiles.length}`);

const totalParts = Math.ceil(allFiles.length / maxItems);
console.log(`Dividindo em ${totalParts} partes...\n`);

// Criar pastas e mover arquivos
for (let i = 0; i < totalParts; i++) {
  const partName = `${baseName} part${i + 1}`;
  const partDir = path.join(targetBase, partName);
  
  if (!fs.existsSync(partDir)) {
    fs.mkdirSync(partDir);
  }
  
  const corporativot = i * maxItems;
  const end = Math.min(corporativot + maxItems, allFiles.length);
  const partFiles = allFiles.slice(corporativot, end);
  
  console.log(`${partName}: ${partFiles.length} arquivos`);
  
  partFiles.forEach(file => {
    const fileName = path.basename(file);
    const newPath = path.join(partDir, fileName);
    fs.renameSync(file, newPath);
  });
}

console.log('\n✅ Concluído!');

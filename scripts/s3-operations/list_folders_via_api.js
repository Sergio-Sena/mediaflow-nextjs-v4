// Usando fetch nativo do Node.js 18+

const API_URL = 'https://gdb962d234.execute-api.us-east-1.amazonaws.com/prod/files';

// Pastas que devem FICAR na raiz (não mover)
const keepInRoot = new Set(['Video', 'Seart', 'Captures', 'Star']);

async function listFolders() {
  try {
    const response = await fetch(API_URL);
    const data = await response.json();
    
    if (!data.success) {
      throw new Error(data.message || 'Erro ao listar arquivos');
    }
    
    // Extrair pastas únicas
    const folders = new Set();
    data.files.forEach(file => {
      if (file.key.includes('/')) {
        const folder = file.key.split('/')[0];
        folders.add(folder);
      }
    });
    
    const allFolders = Array.from(folders);
    const foldersToMove = allFolders.filter(f => !keepInRoot.has(f));
    
    console.log('PASTAS PARA MOVER PARA Star/:');
    console.log('='.repeat(50));
    
    foldersToMove.sort().forEach((folder, i) => {
      console.log(`${(i+1).toString().padStart(2)}. ${folder}/ -> Star/${folder}/`);
    });
    
    console.log('\nRESUMO:');
    console.log(`Total de pastas: ${allFolders.length}`);
    console.log(`Ficar na raiz: ${keepInRoot.size} (${Array.from(keepInRoot).sort().join(', ')})`);
    console.log(`Mover para Star/: ${foldersToMove.length}`);
    
    console.log('\nLISTA PARA CONFIRMACAO:');
    foldersToMove.sort().forEach(folder => {
      console.log(`"${folder}",`);
    });
    
  } catch (error) {
    console.error('Erro:', error.message);
  }
}

listFolders();
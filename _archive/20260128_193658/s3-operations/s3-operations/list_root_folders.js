const API_URL = 'https://gdb962d234.execute-api.us-east-1.amazonaws.com/prod/files';

async function listRootFolders() {
  try {
    const response = await fetch(API_URL);
    const data = await response.json();
    
    if (!data.success) {
      console.log('❌ Erro na API');
      return;
    }
    
    // Extrair pastas da raiz (sem '/' no início)
    const rootFolders = new Set();
    
    data.files.forEach(file => {
      const key = file.key;
      if (key.includes('/')) {
        const folder = key.split('/')[0];
        if (folder && folder !== '') {
          rootFolders.add(folder);
        }
      }
    });
    
    const folders = Array.from(rootFolders).sort();
    
    console.log('📁 PASTAS NA RAIZ:');
    console.log('='.repeat(30));
    folders.forEach((folder, i) => {
      console.log(`${i+1}. ${folder}/`);
    });
    console.log(`\nTotal: ${folders.length} pastas`);
    
  } catch (error) {
    console.log(`❌ Erro: ${error.message}`);
  }
}

listRootFolders();
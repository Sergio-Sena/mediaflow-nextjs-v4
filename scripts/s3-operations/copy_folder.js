const API_URL = 'https://gdb962d234.execute-api.us-east-1.amazonaws.com/prod/files';

async function copyFolder(folderName) {
  try {
    console.log(`📋 COPIANDO ${folderName}/ -> Star/${folderName}/`);
    
    // 1. Listar arquivos
    const response = await fetch(API_URL);
    const data = await response.json();
    
    // 2. Filtrar arquivos da pasta
    const folderFiles = data.files.filter(file => 
      file.key.startsWith(folderName + '/') && file.key !== folderName + '/'
    );
    
    console.log(`📁 ${folderFiles.length} arquivos encontrados`);
    
    // 3. Copiar cada arquivo
    let copied = 0;
    for (const file of folderFiles) {
      const oldKey = file.key;
      const newKey = `Star/${oldKey}`;
      
      console.log(`📋 Copiando: ${oldKey} -> ${newKey}`);
      
      const copyResponse = await fetch(API_URL, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          action: 'copy',
          sourceKey: oldKey,
          destinationKey: newKey
        })
      });
      
      if (copyResponse.ok) {
        copied++;
        console.log(`✅ Copiado: ${newKey}`);
      } else {
        console.log(`❌ Erro ao copiar: ${oldKey}`);
      }
      
      // Pausa entre operações
      await new Promise(resolve => setTimeout(resolve, 500));
    }
    
    console.log(`🎯 RESULTADO: ${copied}/${folderFiles.length} arquivos copiados`);
    
  } catch (error) {
    console.log(`❌ Erro: ${error.message}`);
  }
}

const folder = process.argv[2] || "Lisinha";
copyFolder(folder);
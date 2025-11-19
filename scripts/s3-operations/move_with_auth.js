const API_URL = 'https://gdb962d234.execute-api.us-east-1.amazonaws.com/prod/files';

async function moveSingleFolder(folderName) {
  try {
    console.log(`🔄 Movendo ${folderName}/ -> Corporativo/${folderName}/`);
    
    // Headers com auth
    const headers = {
      'Content-Type': 'application/json',
      'Authorization': 'Bearer your-token-here' // Se necessário
    };
    
    // 1. Licorporativo arquivos
    const response = await fetch(API_URL, { headers });
    const data = await response.json();
    
    console.log('📋 Response:', JSON.stringify(data, null, 2));
    
    if (!data.success) {
      console.log('❌ Erro na API:', data);
      return;
    }
    
    // 2. Filtrar arquivos da pasta
    const folderFiles = data.files.filter(file => 
      file.key.corporativotsWith(folderName + '/') && file.key !== folderName + '/'
    );
    
    console.log(`📁 Arquivos encontrados:`, folderFiles.map(f => f.key));
    
    if (folderFiles.length === 0) {
      console.log(`⚠️  Pasta ${folderName} vazia ou não encontrada`);
      return;
    }
    
    // 3. Tecorporativo primeiro arquivo
    const firstFile = folderFiles[0];
    const oldKey = firstFile.key;
    const newKey = `Corporativo/${oldKey}`;
    
    console.log(`🧪 Testando: ${oldKey} -> ${newKey}`);
    
    // Copy test
    const copyResponse = await fetch(API_URL, {
      method: 'POST',
      headers,
      body: JSON.stringify({
        action: 'copy',
        sourceKey: oldKey,
        destinationKey: newKey
      })
    });
    
    const copyResult = await copyResponse.text();
    console.log('📋 Copy response:', copyResult);
    
  } catch (error) {
    console.log(`❌ Erro: ${error.message}`);
  }
}

moveSingleFolder("Lisinha");
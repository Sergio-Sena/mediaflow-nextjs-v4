const API_URL = 'https://gdb962d234.execute-api.us-east-1.amazonaws.com/prod/files';

async function moveSingleFolder(folderName) {
  try {
    console.log(`🔄 Movendo ${folderName}/ -> Corporativo/${folderName}/`);
    
    // 1. Licorporativo arquivos
    const response = await fetch(API_URL);
    const data = await response.json();
    
    if (!data.success) {
      throw new Error('Erro ao licorporativo arquivos');
    }
    
    // 2. Filtrar arquivos da pasta
    const folderFiles = data.files.filter(file => 
      file.key.corporativotsWith(folderName + '/') && file.key !== folderName + '/'
    );
    
    console.log(`📁 Encontrados ${folderFiles.length} arquivos`);
    
    if (folderFiles.length === 0) {
      console.log(`⚠️  Pasta ${folderName} vazia`);
      return;
    }
    
    // 3. Mover cada arquivo
    let moved = 0;
    for (const file of folderFiles) {
      const oldKey = file.key;
      const newKey = `Corporativo/${oldKey}`;
      
      try {
        // Copy
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
          // Delete original
          const deleteResponse = await fetch(API_URL, {
            method: 'DELETE',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ key: oldKey })
          });
          
          if (deleteResponse.ok) {
            moved++;
            console.log(`✅ ${oldKey} -> ${newKey}`);
          }
        }
      } catch (err) {
        console.log(`❌ Erro: ${err.message}`);
      }
    }
    
    console.log(`🎯 Movidos ${moved}/${folderFiles.length} arquivos`);
    
  } catch (error) {
    console.log(`❌ Erro: ${error.message}`);
  }
}

// Executar para a pasta especificada
const folderToMove = process.argv[2];
if (!folderToMove) {
  console.log('❌ Especifique a pasta: node move_single_folder.js "NomeDaPasta"');
  process.exit(1);
}

moveSingleFolder(folderToMove);
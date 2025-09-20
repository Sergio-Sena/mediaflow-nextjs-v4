const API_URL = 'https://gdb962d234.execute-api.us-east-1.amazonaws.com/prod/files';

// Pastas encontradas para mover
const foldersToMove = [
  "Anime",
  "Lisinha", 
  "MiaMalkova",
  "Mini_skirt",
  "ShyBlanche",
  "Spirite_Moon", 
  "Zoe_Neli",
  "emillya_Bunny",
  "kate_kuray"
];

async function moveFolder(folderName) {
  try {
    console.log(`\nMovendo ${folderName}/ -> Star/${folderName}/`);
    
    // 1. Listar arquivos da pasta
    const response = await fetch(API_URL);
    const data = await response.json();
    
    if (!data.success) {
      throw new Error('Erro ao listar arquivos');
    }
    
    // 2. Filtrar arquivos da pasta específica
    const folderFiles = data.files.filter(file => 
      file.key.startsWith(folderName + '/') && file.key !== folderName + '/'
    );
    
    console.log(`  Encontrados ${folderFiles.length} arquivos`);
    
    if (folderFiles.length === 0) {
      console.log(`  ⚠️  Pasta ${folderName} vazia ou não encontrada`);
      return { success: true, moved: 0 };
    }
    
    // 3. Mover cada arquivo
    let moved = 0;
    for (const file of folderFiles) {
      const oldKey = file.key;
      const newKey = `Star/${oldKey}`;
      
      try {
        // Copiar arquivo
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
          // Deletar original
          const deleteResponse = await fetch(API_URL, {
            method: 'DELETE',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ key: oldKey })
          });
          
          if (deleteResponse.ok) {
            moved++;
            console.log(`    ✅ ${oldKey} -> ${newKey}`);
          } else {
            console.log(`    ❌ Erro ao deletar ${oldKey}`);
          }
        } else {
          console.log(`    ❌ Erro ao copiar ${oldKey}`);
        }
      } catch (err) {
        console.log(`    ❌ Erro: ${err.message}`);
      }
    }
    
    console.log(`  ✅ Movidos ${moved}/${folderFiles.length} arquivos`);
    return { success: moved > 0, moved };
    
  } catch (error) {
    console.log(`  ❌ Erro ao mover ${folderName}: ${error.message}`);
    return { success: false, moved: 0 };
  }
}

async function moveAllFolders() {
  console.log('🔄 INICIANDO MOVIMENTAÇÃO DE PASTAS PARA Star/');
  console.log('='.repeat(60));
  
  let totalMoved = 0;
  let successCount = 0;
  
  for (const folder of foldersToMove) {
    const result = await moveFolder(folder);
    if (result.success) {
      successCount++;
      totalMoved += result.moved;
    }
    
    // Pausa entre operações
    await new Promise(resolve => setTimeout(resolve, 1000));
  }
  
  console.log('\n' + '='.repeat(60));
  console.log('📊 RESUMO FINAL:');
  console.log(`Pastas processadas: ${foldersToMove.length}`);
  console.log(`Pastas movidas com sucesso: ${successCount}`);
  console.log(`Total de arquivos movidos: ${totalMoved}`);
  console.log('✅ Operação concluída!');
}

// Confirmar antes de executar
console.log('⚠️  CONFIRMAÇÃO NECESSÁRIA');
console.log('Este script irá mover as seguintes pastas para Star/:');
foldersToMove.forEach((folder, i) => {
  console.log(`${i+1}. ${folder}/ -> Star/${folder}/`);
});

console.log('\nPara executar, descomente a linha abaixo:');
console.log('// moveAllFolders();');

// Executando automaticamente:
moveAllFolders();
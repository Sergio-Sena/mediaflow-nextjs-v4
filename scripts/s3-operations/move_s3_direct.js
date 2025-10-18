const { exec } = require('child_process');
const util = require('util');
const execAsync = util.promisify(exec);

const UPLOADS_BUCKET = 'mediaflow-uploads-969430605054';
const PROCESSED_BUCKET = 'mediaflow-processed-969430605054';

async function moveFolder(folderName) {
  try {
    console.log(`🔄 Movendo ${folderName}/ -> Star/${folderName}/`);
    
    // Move no bucket uploads
    console.log('📦 Movendo no bucket uploads...');
    await execAsync(`aws s3 mv "s3://${UPLOADS_BUCKET}/${folderName}/" "s3://${UPLOADS_BUCKET}/Star/${folderName}/" --recursive`);
    
    // Move no bucket processed  
    console.log('📦 Movendo no bucket processed...');
    await execAsync(`aws s3 mv "s3://${PROCESSED_BUCKET}/${folderName}/" "s3://${PROCESSED_BUCKET}/Star/${folderName}/" --recursive`);
    
    console.log(`✅ Pasta ${folderName} movida com sucesso!`);
    
  } catch (error) {
    console.log(`❌ Erro: ${error.message}`);
  }
}

const folder = process.argv[2];
if (!folder) {
  console.log('❌ Especifique a pasta: node move_s3_direct.js "NomeDaPasta"');
  process.exit(1);
}

moveFolder(folder);
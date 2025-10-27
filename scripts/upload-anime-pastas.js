const { S3Client, PutObjectCommand } = require('@aws-sdk/client-s3');
const fs = require('fs');
const path = require('path');

const s3 = new S3Client({ region: 'us-east-1' });
const bucket = 'mediaflow-uploads-969430605054';
const localBase = 'C:\\Users\\dell 5557\\Videos\\IDM\\Anime';

function sanitize(name) {
  return name
    .replace(/[^a-zA-Z0-9._-]/g, '_')
    .replace(/_+/g, '_')
    .replace(/^_|_$/g, '');
}

async function uploadFolder(folderName) {
  const localPath = path.join(localBase, folderName);
  const s3FolderName = sanitize(folderName);
  
  console.log(`\n📁 Enviando ${folderName}...`);
  
  let uploaded = 0;
  
  function scanAndUpload(dir, relativePath = '') {
    const items = fs.readdirSync(dir);
    
    for (const item of items) {
      const fullPath = path.join(dir, item);
      const stat = fs.statSync(fullPath);
      
      if (stat.isDirectory()) {
        scanAndUpload(fullPath, path.join(relativePath, item));
      } else {
        const fileName = sanitize(item);
        const fileSizeGB = stat.size / (1024 * 1024 * 1024);
        
        if (stat.size > 2 * 1024 * 1024 * 1024) {
          console.log(`   ⚠️  PULADO (${fileSizeGB.toFixed(2)}GB): ${fileName}`);
          return;
        }
        
        const s3Key = `users/user_admin/Anime/${s3FolderName}/${relativePath ? sanitize(relativePath) + '/' : ''}${fileName}`;
        
        const fileContent = fs.readFileSync(fullPath);
        
        s3.send(new PutObjectCommand({
          Bucket: bucket,
          Key: s3Key,
          Body: fileContent
        })).then(() => {
          uploaded++;
          console.log(`   ✅ ${fileName}`);
        });
      }
    }
  }
  
  scanAndUpload(localPath);
  
  // Aguardar uploads
  await new Promise(resolve => setTimeout(resolve, 2000));
  
  console.log(`   📊 ${uploaded} arquivos enviados`);
}

async function main() {
  const folders = ['PMV', 'Ranni', 'sadako', 'Spider', 'Street Fighter', 'RE4'];
  
  console.log('🚀 Iniciando upload de 6 pastas...\n');
  console.log('='.repeat(50));
  
  for (const folder of folders) {
    await uploadFolder(folder);
  }
  
  console.log('\n' + '='.repeat(50));
  console.log('✅ Upload completo!');
}

main().catch(console.error);

const { S3Client, PutObjectCommand } = require('@aws-sdk/client-s3');
const fs = require('fs');
const path = require('path');

const s3 = new S3Client({ region: 'us-east-1' });
const bucket = 'mediaflow-uploads-969430605054';
const localBase = 'C:\\Users\\dell 5557\\Videos\\IDM\\404HotFound';
const s3Prefix = 'users/user_admin/Anime/';

async function uploadFolder(folderPath, folderName) {
  const files = fs.readdirSync(folderPath);
  console.log(`\n📁 ${folderName}: ${files.length} arquivos`);
  
  for (const file of files) {
    const filePath = path.join(folderPath, file);
    const stat = fs.statSync(filePath);
    
    if (stat.isFile()) {
      const s3Key = `${s3Prefix}${folderName}/${file}`;
      const fileContent = fs.readFileSync(filePath);
      
      await s3.send(new PutObjectCommand({
        Bucket: bucket,
        Key: s3Key,
        Body: fileContent
      }));
      
      console.log(`✅ ${file}`);
    }
  }
}

async function main() {
  const folders = fs.readdirSync(localBase)
    .filter(f => f.corporativotsWith('Jiggly Girls [Hentai on Brasil]'));
  
  console.log(`Encontradas ${folders.length} pastas para upload\n`);
  
  for (const folder of folders) {
    await uploadFolder(path.join(localBase, folder), folder);
  }
  
  console.log('\n✅ Upload concluído!');
}

main().catch(console.error);

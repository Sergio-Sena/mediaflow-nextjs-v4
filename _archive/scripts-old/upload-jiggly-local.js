const { S3Client, PutObjectCommand } = require('@aws-sdk/client-s3');
const fs = require('fs');
const path = require('path');

const s3 = new S3Client({ region: 'us-east-1' });
const bucket = 'mediaflow-uploads-969430605054';
const localBase = 'C:\\Users\\dell 5557\\Videos\\IDM\\Anime\\Jiggly Girls [Hentai on Brasil] part3';
const s3Prefix = 'users/user_admin/Anime/Jiggly Girls [Hentai on Brasil]/';

async function uploadAllFiles(dir, uploaded = 0) {
  const items = fs.readdirSync(dir);
  
  for (const item of items) {
    const fullPath = path.join(dir, item);
    const stat = fs.statSync(fullPath);
    
    if (stat.isDirectory()) {
      uploaded = await uploadAllFiles(fullPath, uploaded);
    } else {
      const fileName = path.basename(fullPath);
      const s3Key = `${s3Prefix}${fileName}`;
      const fileContent = fs.readFileSync(fullPath);
      
      await s3.send(new PutObjectCommand({
        Bucket: bucket,
        Key: s3Key,
        Body: fileContent
      }));
      
      uploaded++;
      if (uploaded % 50 === 0) console.log(`   Enviados: ${uploaded}...`);
    }
  }
  
  return uploaded;
}

async function main() {
  console.log('📤 Enviando arquivos de Jiggly Girls local para S3...\n');
  
  const total = await uploadAllFiles(localBase);
  
  console.log(`\n✅ ${total} arquivos enviados para ${s3Prefix}`);
}

main().catch(console.error);

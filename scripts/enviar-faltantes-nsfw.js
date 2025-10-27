const { S3Client, ListObjectsV2Command, PutObjectCommand } = require('@aws-sdk/client-s3');
const fs = require('fs');
const path = require('path');

const s3 = new S3Client({ region: 'us-east-1' });
const bucket = 'mediaflow-uploads-969430605054';
const localPath = 'C:\\Users\\dell 5557\\Videos\\IDM\\Anime\\NSFW2.1';

function sanitize(filename) {
  const clean = filename
    .replace(/[^a-zA-Z0-9._-]/g, '_')
    .replace(/_+/g, '_')
    .replace(/^_|_$/g, '');
  
  if (clean.length > 45) {
    const ext = path.extname(clean);
    const name = clean.slice(0, 45 - ext.length - 3);
    return name + '...' + ext;
  }
  
  return clean;
}

async function getS3Files() {
  const files = new Map();
  let continuationToken;
  
  do {
    const response = await s3.send(new ListObjectsV2Command({
      Bucket: bucket,
      Prefix: 'users/user_admin/Anime/NSFW2.1/',
      ContinuationToken: continuationToken
    }));
    
    if (response.Contents) {
      response.Contents.forEach(obj => {
        const fileName = obj.Key.split('/').pop();
        if (fileName) files.set(fileName, true);
      });
    }
    
    continuationToken = response.NextContinuationToken;
  } while (continuationToken);
  
  return files;
}

function getLocalFiles() {
  const files = [];
  
  function scan(dir) {
    const items = fs.readdirSync(dir);
    items.forEach(item => {
      const fullPath = path.join(dir, item);
      const stat = fs.statSync(fullPath);
      
      if (stat.isDirectory()) {
        scan(fullPath);
      } else {
        files.push({ original: item, path: fullPath });
      }
    });
  }
  
  scan(localPath);
  return files;
}

async function main() {
  console.log('🔍 Identificando arquivos faltantes...\n');
  
  const s3Files = await getS3Files();
  const localFiles = getLocalFiles();
  
  const missing = localFiles.filter(f => {
    const sanitized = sanitize(f.original);
    return !s3Files.has(sanitized);
  });
  
  console.log(`📊 Faltam ${missing.length} arquivos:\n`);
  
  if (missing.length === 0) {
    console.log('✅ Nenhum arquivo faltando!');
    return;
  }
  
  for (const file of missing) {
    const sanitized = sanitize(file.original);
    console.log(`📤 ${file.original}`);
    console.log(`   → ${sanitized}`);
    
    const fileContent = fs.readFileSync(file.path);
    const s3Key = `users/user_admin/Anime/NSFW2.1/${sanitized}`;
    
    await s3.send(new PutObjectCommand({
      Bucket: bucket,
      Key: s3Key,
      Body: fileContent
    }));
    
    console.log('   ✅ Enviado\n');
  }
  
  console.log(`✅ ${missing.length} arquivos enviados!`);
}

main().catch(console.error);

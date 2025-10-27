const { S3Client, ListObjectsV2Command } = require('@aws-sdk/client-s3');
const fs = require('fs');
const path = require('path');

const s3 = new S3Client({ region: 'us-east-1' });
const bucket = 'mediaflow-uploads-969430605054';
const localPath = 'C:\\Users\\dell 5557\\Videos\\IDM\\404HotFound\\Jiggly Girls [Hentai on Brasil]';

function sanitize(name) {
  return name
    .replace(/[^a-zA-Z0-9._-]/g, '_')
    .replace(/_+/g, '_')
    .replace(/^_|_$/g, '');
}

async function getS3Files() {
  const files = new Set();
  let continuationToken;
  
  do {
    const response = await s3.send(new ListObjectsV2Command({
      Bucket: bucket,
      Prefix: 'users/user_admin/Anime/Jiggly Girls [Hentai on Brasil]/',
      ContinuationToken: continuationToken
    }));
    
    if (response.Contents) {
      response.Contents.forEach(obj => {
        const fileName = obj.Key.split('/').pop();
        if (fileName) files.add(fileName);
      });
    }
    
    continuationToken = response.NextContinuationToken;
  } while (continuationToken);
  
  return files;
}

function getLocalFiles(dir, fileList = []) {
  const items = fs.readdirSync(dir);
  
  items.forEach(item => {
    const fullPath = path.join(dir, item);
    const stat = fs.statSync(fullPath);
    
    if (stat.isDirectory()) {
      getLocalFiles(fullPath, fileList);
    } else {
      fileList.push({ original: item, sanitized: sanitize(item), path: fullPath });
    }
  });
  
  return fileList;
}

async function main() {
  console.log('Identificando arquivos faltantes...\n');
  
  const s3Files = await getS3Files();
  const localFiles = getLocalFiles(localPath);
  
  console.log(`S3: ${s3Files.size} arquivos`);
  console.log(`Local: ${localFiles.length} arquivos\n`);
  
  const missing = localFiles.filter(f => !s3Files.has(f.sanitized));
  
  console.log(`Faltam: ${missing.length} arquivos\n`);
  
  if (missing.length > 0) {
    console.log('Primeiros 10:');
    missing.slice(0, 10).forEach(f => console.log(`  ${f.original}`));
  }
}

main().catch(console.error);

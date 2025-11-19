const { S3Client, ListObjectsV2Command } = require('@aws-sdk/client-s3');
const fs = require('fs');
const path = require('path');

const s3 = new S3Client({ region: 'us-east-1' });
const bucket = 'mediaflow-uploads-969430605054';
const localPath = 'C:\\Users\\dell 5557\\Videos\\IDM\\Anime\\Conteudo2.1';

async function getS3Files() {
  const files = new Set();
  let continuationToken;
  
  do {
    const response = await s3.send(new ListObjectsV2Command({
      Bucket: bucket,
      Prefix: 'users/user_admin/Anime/Conteudo2.1/',
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

function getLocalFiles(dir) {
  const files = new Set();
  
  function scan(currentDir) {
    const items = fs.readdirSync(currentDir);
    items.forEach(item => {
      const fullPath = path.join(currentDir, item);
      const stat = fs.statSync(fullPath);
      
      if (stat.isDirectory()) {
        scan(fullPath);
      } else {
        files.add(item);
      }
    });
  }
  
  scan(dir);
  return files;
}

async function main() {
  console.log('🔍 Comparando Conteudo2.1...\n');
  
  const s3Files = await getS3Files();
  const localFiles = getLocalFiles(localPath);
  
  console.log(`📦 S3: ${s3Files.size} arquivos`);
  console.log(`💾 Local: ${localFiles.size} arquivos\n`);
  
  const onlyS3 = [...s3Files].filter(f => !localFiles.has(f));
  const onlyLocal = [...localFiles].filter(f => !s3Files.has(f));
  
  if (onlyS3.length > 0) {
    console.log(`⚠️  Apenas no S3 (${onlyS3.length}):`);
    onlyS3.slice(0, 5).forEach(f => console.log(`   ${f}`));
    if (onlyS3.length > 5) console.log(`   ... e mais ${onlyS3.length - 5}`);
    console.log('');
  }
  
  if (onlyLocal.length > 0) {
    console.log(`⚠️  Apenas Local (${onlyLocal.length}):`);
    onlyLocal.slice(0, 5).forEach(f => console.log(`   ${f}`));
    if (onlyLocal.length > 5) console.log(`   ... e mais ${onlyLocal.length - 5}`);
    console.log('');
  }
  
  if (onlyS3.length === 0 && onlyLocal.length === 0) {
    console.log('✅ Arquivos idênticos!');
  }
}

main().catch(console.error);

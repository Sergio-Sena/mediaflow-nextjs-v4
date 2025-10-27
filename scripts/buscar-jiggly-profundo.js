const { S3Client, ListObjectsV2Command } = require('@aws-sdk/client-s3');

const s3 = new S3Client({ region: 'us-east-1' });
const bucket = 'mediaflow-uploads-969430605054';

async function searchDeep() {
  const folders = new Set();
  let continuationToken;
  
  do {
    const response = await s3.send(new ListObjectsV2Command({
      Bucket: bucket,
      ContinuationToken: continuationToken,
      MaxKeys: 1000
    }));
    
    if (response.Contents) {
      response.Contents.forEach(obj => {
        const parts = obj.Key.split('/');
        for (let i = 0; i < parts.length - 1; i++) {
          const folder = parts.slice(0, i + 1).join('/');
          if (folder.toLowerCase().includes('jiggly')) {
            folders.add(folder);
          }
        }
      });
    }
    
    continuationToken = response.NextContinuationToken;
    console.log(`Processando... ${folders.size} pastas encontradas`);
  } while (continuationToken);
  
  return Array.from(folders).sort();
}

async function main() {
  console.log('🔍 Busca profunda por "Jiggly Girls" no S3...\n');
  
  const folders = await searchDeep();
  
  console.log(`\n✅ Encontradas ${folders.length} pastas:\n`);
  folders.forEach(folder => console.log(`  📁 ${folder}`));
}

main().catch(console.error);

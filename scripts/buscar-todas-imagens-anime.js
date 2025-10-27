const { S3Client, ListObjectsV2Command } = require('@aws-sdk/client-s3');

const s3 = new S3Client({ region: 'us-east-1' });
const bucket = 'mediaflow-uploads-969430605054';

async function listAllInAnime() {
  const folders = new Map();
  let continuationToken;
  
  do {
    const response = await s3.send(new ListObjectsV2Command({
      Bucket: bucket,
      Prefix: 'users/user_admin/Anime/',
      ContinuationToken: continuationToken
    }));
    
    if (response.Contents) {
      response.Contents.forEach(obj => {
        if (!obj.Key.endsWith('/')) {
          const parts = obj.Key.split('/');
          if (parts.length >= 4) {
            const folder = parts.slice(0, 4).join('/');
            folders.set(folder, (folders.get(folder) || 0) + 1);
          }
        }
      });
    }
    
    continuationToken = response.NextContinuationToken;
  } while (continuationToken);
  
  return folders;
}

async function main() {
  console.log('🔍 Buscando todas as pastas em users/user_admin/Anime/...\n');
  
  const folders = await listAllInAnime();
  
  console.log(`✅ Encontradas ${folders.size} pastas:\n`);
  
  let total = 0;
  Array.from(folders.entries()).sort().forEach(([folder, count]) => {
    console.log(`📁 ${folder.split('/').pop()}: ${count} arquivos`);
    total += count;
  });
  
  console.log(`\n📊 Total: ${total} arquivos`);
}

main().catch(console.error);

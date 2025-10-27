const { S3Client, ListObjectsV2Command } = require('@aws-sdk/client-s3');

const s3 = new S3Client({ region: 'us-east-1' });
const bucket = 'mediaflow-uploads-969430605054';

async function listAll() {
  const jigglyFolders = new Map();
  let continuationToken;
  
  do {
    const response = await s3.send(new ListObjectsV2Command({
      Bucket: bucket,
      Prefix: 'users/user_admin/Anime/',
      ContinuationToken: continuationToken
    }));
    
    if (response.Contents) {
      response.Contents.forEach(obj => {
        if (obj.Key.toLowerCase().includes('jiggly')) {
          const folder = obj.Key.split('/').slice(0, 4).join('/');
          if (!jigglyFolders.has(folder)) {
            jigglyFolders.set(folder, []);
          }
          jigglyFolders.get(folder).push(obj.Key);
        }
      });
    }
    
    continuationToken = response.NextContinuationToken;
  } while (continuationToken);
  
  return jigglyFolders;
}

async function main() {
  console.log('🔍 Listando TODAS as pastas com "Jiggly"...\n');
  
  const folders = await listAll();
  
  folders.forEach((files, folder) => {
    console.log(`\n📁 ${folder}`);
    console.log(`   ${files.length} arquivos`);
    console.log(`   Exemplo: ${files[0]}`);
  });
  
  const total = Array.from(folders.values()).reduce((sum, files) => sum + files.length, 0);
  console.log(`\n📊 Total: ${total} arquivos em ${folders.size} pastas`);
}

main().catch(console.error);

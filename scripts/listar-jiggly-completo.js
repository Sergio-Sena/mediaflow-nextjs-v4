const { S3Client, ListObjectsV2Command } = require('@aws-sdk/client-s3');

const s3 = new S3Client({ region: 'us-east-1' });
const bucket = 'mediaflow-uploads-969430605054';

async function listAll() {
  const usuario2Folders = new Map();
  let continuationToken;
  
  do {
    const response = await s3.send(new ListObjectsV2Command({
      Bucket: bucket,
      Prefix: 'users/user_admin/Anime/',
      ContinuationToken: continuationToken
    }));
    
    if (response.Contents) {
      response.Contents.forEach(obj => {
        if (obj.Key.toLowerCase().includes('usuario2')) {
          const folder = obj.Key.split('/').slice(0, 4).join('/');
          if (!usuario2Folders.has(folder)) {
            usuario2Folders.set(folder, []);
          }
          usuario2Folders.get(folder).push(obj.Key);
        }
      });
    }
    
    continuationToken = response.NextContinuationToken;
  } while (continuationToken);
  
  return usuario2Folders;
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

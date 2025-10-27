const { S3Client, ListObjectsV2Command } = require('@aws-sdk/client-s3');

const s3 = new S3Client({ region: 'us-east-1' });
const bucket = 'mediaflow-uploads-969430605054';

async function findAllJiggly() {
  const folders = new Map();
  let continuationToken;
  
  console.log('Buscando todos os arquivos "Imagem" no S3...\n');
  
  do {
    const response = await s3.send(new ListObjectsV2Command({
      Bucket: bucket,
      Prefix: 'users/user_admin/',
      ContinuationToken: continuationToken
    }));
    
    if (response.Contents) {
      response.Contents.forEach(obj => {
        const fileName = obj.Key.split('/').pop().toLowerCase();
        if (fileName.startsWith('imagem')) {
          const folder = obj.Key.split('/').slice(0, -1).join('/');
          if (!folders.has(folder)) {
            folders.set(folder, []);
          }
          folders.get(folder).push(obj.Key);
        }
      });
    }
    
    continuationToken = response.NextContinuationToken;
  } while (continuationToken);
  
  return folders;
}

async function main() {
  const folders = await findAllJiggly();
  
  console.log(`Encontradas ${folders.size} pastas com arquivos "Imagem":\n`);
  
  let total = 0;
  folders.forEach((files, folder) => {
    console.log(`${folder.replace('users/user_admin/', '')}`);
    console.log(`  ${files.length} arquivos`);
    console.log(`  Exemplo: ${files[0].split('/').pop()}\n`);
    total += files.length;
  });
  
  console.log(`Total: ${total} arquivos "Imagem" encontrados`);
}

main().catch(console.error);

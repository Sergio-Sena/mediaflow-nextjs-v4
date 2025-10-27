const { S3Client, ListObjectsV2Command } = require('@aws-sdk/client-s3');

const s3 = new S3Client({ region: 'us-east-1' });
const bucket = 'mediaflow-uploads-969430605054';

async function countFiles(prefix) {
  let count = 0;
  let continuationToken;
  
  do {
    const response = await s3.send(new ListObjectsV2Command({
      Bucket: bucket,
      Prefix: prefix,
      ContinuationToken: continuationToken
    }));
    
    if (response.Contents) {
      count += response.Contents.filter(obj => !obj.Key.endsWith('/')).length;
    }
    
    continuationToken = response.NextContinuationToken;
  } while (continuationToken);
  
  return count;
}

async function main() {
  console.log('📊 Contando imagens nas pastas Jiggly Girls...\n');
  
  const folders = [
    'users/user_admin/Anime/Jiggly Girls [Hentai on Brasil] part4',
    'users/user_admin/Anime/Jiggly Girls [Hentai on Brasil] part5',
    'users/user_admin/Anime/Jiggly Girls [Hentai on Brasil] part6',
    'users/user_admin/Anime/Jiggly Girls [Hentai on Brasil] part7'
  ];
  
  let total = 0;
  
  for (const folder of folders) {
    const count = await countFiles(folder + '/');
    console.log(`📁 ${folder.split('/').pop()}: ${count} arquivos`);
    total += count;
  }
  
  console.log(`\n✅ Total: ${total} arquivos`);
  console.log(`\n⚠️ Confirme se deseja juntar tudo em:`);
  console.log(`   users/user_admin/Anime/Jiggly Girls [Hentai on Brasil]/`);
}

main().catch(console.error);

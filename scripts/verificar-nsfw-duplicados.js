const { S3Client, ListObjectsV2Command } = require('@aws-sdk/client-s3');

const s3 = new S3Client({ region: 'us-east-1' });
const bucket = 'mediaflow-uploads-969430605054';

async function listAll() {
  const files = [];
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
        if (fileName) files.push(fileName);
      });
    }
    
    continuationToken = response.NextContinuationToken;
  } while (continuationToken);
  
  return files.sort();
}

async function main() {
  console.log('📋 Listando todos os arquivos NSFW2.1 no S3...\n');
  
  const files = await listAll();
  
  console.log(`📊 Total: ${files.length} arquivos\n`);
  
  const truncated = files.filter(f => f.includes('....'));
  const normal = files.filter(f => !f.includes('....'));
  
  console.log(`⚠️  Truncados (antigos): ${truncated.length}`);
  truncated.forEach(f => console.log(`   ${f}`));
  
  console.log(`\n✅ Normais (novos): ${normal.length}`);
  normal.slice(0, 5).forEach(f => console.log(`   ${f}`));
  if (normal.length > 5) console.log(`   ... e mais ${normal.length - 5}`);
}

main().catch(console.error);

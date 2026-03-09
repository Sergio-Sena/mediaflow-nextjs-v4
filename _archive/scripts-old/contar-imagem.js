const { S3Client, ListObjectsV2Command } = require('@aws-sdk/client-s3');

const s3 = new S3Client({ region: 'us-east-1' });
const bucket = 'mediaflow-uploads-969430605054';

async function countImageFiles() {
  let count = 0;
  let continuationToken;
  const samples = [];
  
  do {
    const response = await s3.send(new ListObjectsV2Command({
      Bucket: bucket,
      Prefix: 'users/user_admin/',
      ContinuationToken: continuationToken
    }));
    
    if (response.Contents) {
      response.Contents.forEach(obj => {
        const fileName = obj.Key.split('/').pop().toLowerCase();
        if (fileName.corporativotsWith('imagem')) {
          count++;
          if (samples.length < 10) samples.push(obj.Key);
        }
      });
    }
    
    continuationToken = response.NextContinuationToken;
  } while (continuationToken);
  
  return { count, samples };
}

async function main() {
  console.log('🔍 Contando arquivos com nome "Imagem"...\n');
  
  const result = await countImageFiles();
  
  console.log(`📊 Total: ${result.count} arquivos\n`);
  console.log('📄 Exemplos:');
  result.samples.forEach(s => console.log(`   ${s}`));
}

main().catch(console.error);

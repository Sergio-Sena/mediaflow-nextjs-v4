const { S3Client, ListObjectsV2Command } = require('@aws-sdk/client-s3');

const s3 = new S3Client({ region: 'us-east-1' });
const bucket = 'pics-notebackup';

async function checkFolder() {
  let count = 0;
  let continuationToken;
  const samples = [];
  
  do {
    const response = await s3.send(new ListObjectsV2Command({
      Bucket: bucket,
      Prefix: 'Jiggly Girls [Hentai on Brasil]/',
      ContinuationToken: continuationToken
    }));
    
    if (response.Contents) {
      response.Contents.forEach(obj => {
        if (!obj.Key.endsWith('/')) {
          count++;
          if (samples.length < 5) samples.push(obj.Key);
        }
      });
    }
    
    continuationToken = response.NextContinuationToken;
  } while (continuationToken);
  
  return { count, samples };
}

async function main() {
  console.log('🔍 Verificando pics-notebackup/Jiggly Girls [Hentai on Brasil]/...\n');
  
  try {
    const result = await checkFolder();
    
    console.log(`✅ Pasta encontrada!`);
    console.log(`📊 Total: ${result.count} arquivos\n`);
    console.log(`📄 Exemplos:`);
    result.samples.forEach(s => console.log(`   ${s}`));
  } catch (error) {
    console.log(`❌ Pasta não encontrada ou erro: ${error.message}`);
  }
}

main().catch(console.error);

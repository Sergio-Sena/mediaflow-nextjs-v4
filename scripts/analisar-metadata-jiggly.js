const { S3Client, ListObjectsV2Command } = require('@aws-sdk/client-s3');

const s3 = new S3Client({ region: 'us-east-1' });
const bucket = 'mediaflow-uploads-969430605054';

async function analyzeJiggly() {
  let continuationToken;
  const files = [];
  
  do {
    const response = await s3.send(new ListObjectsV2Command({
      Bucket: bucket,
      Prefix: 'users/user_admin/Anime/Jiggly Girls [Hentai on Brasil]/',
      ContinuationToken: continuationToken
    }));
    
    if (response.Contents) {
      response.Contents.forEach(obj => {
        const fileName = obj.Key.split('/').pop();
        if (fileName) {
          files.push({
            name: fileName,
            date: obj.LastModified,
            size: obj.Size
          });
        }
      });
    }
    
    continuationToken = response.NextContinuationToken;
  } while (continuationToken);
  
  // Agrupar por data
  const byDate = {};
  files.forEach(f => {
    const date = f.date.toISOString().split('T')[0];
    if (!byDate[date]) byDate[date] = [];
    byDate[date].push(f);
  });
  
  console.log('Uploads de Jiggly Girls por data:\n');
  
  Object.keys(byDate).sort().forEach(date => {
    console.log(`${date}: ${byDate[date].length} arquivos`);
    console.log(`  Exemplos: ${byDate[date].slice(0, 3).map(f => f.name).join(', ')}`);
  });
  
  console.log(`\nTotal: ${files.length} arquivos`);
}

analyzeJiggly().catch(console.error);

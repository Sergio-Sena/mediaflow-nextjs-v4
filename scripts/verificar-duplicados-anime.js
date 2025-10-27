const { S3Client, ListObjectsV2Command } = require('@aws-sdk/client-s3');

const s3 = new S3Client({ region: 'us-east-1' });
const bucket = 'mediaflow-uploads-969430605054';

async function checkFolder(folderName) {
  const files = [];
  let continuationToken;
  
  do {
    const response = await s3.send(new ListObjectsV2Command({
      Bucket: bucket,
      Prefix: `users/user_admin/Anime/${folderName}/`,
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
  
  return files;
}

async function main() {
  const folders = ['PMV', 'Ranni', 'sadako', 'Spider', 'Street_Fighter', 'RE4'];
  
  console.log('🔍 Verificando duplicados nas pastas enviadas...\n');
  
  for (const folder of folders) {
    const files = await checkFolder(folder);
    const unique = new Set(files);
    const duplicates = files.length - unique.size;
    
    console.log(`📁 ${folder}: ${files.length} arquivos`);
    if (duplicates > 0) {
      console.log(`   ⚠️  ${duplicates} DUPLICADOS!`);
    }
  }
}

main().catch(console.error);

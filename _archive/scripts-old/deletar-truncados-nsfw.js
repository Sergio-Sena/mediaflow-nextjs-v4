const { S3Client, ListObjectsV2Command, DeleteObjectCommand } = require('@aws-sdk/client-s3');

const s3 = new S3Client({ region: 'us-east-1' });
const bucket = 'mediaflow-uploads-969430605054';

async function deleteTruncated() {
  let continuationToken;
  let deleted = 0;
  
  do {
    const response = await s3.send(new ListObjectsV2Command({
      Bucket: bucket,
      Prefix: 'users/user_admin/Anime/Conteudo2.1/',
      ContinuationToken: continuationToken
    }));
    
    if (response.Contents) {
      for (const obj of response.Contents) {
        const fileName = obj.Key.split('/').pop();
        if (fileName && fileName.includes('....')) {
          console.log(`🗑️  ${fileName}`);
          
          await s3.send(new DeleteObjectCommand({
            Bucket: bucket,
            Key: obj.Key
          }));
          
          deleted++;
        }
      }
    }
    
    continuationToken = response.NextContinuationToken;
  } while (continuationToken);
  
  return deleted;
}

async function main() {
  console.log('🗑️  Deletando arquivos truncados...\n');
  
  const deleted = await deleteTruncated();
  
  console.log(`\n✅ ${deleted} arquivos truncados deletados!`);
}

main().catch(console.error);

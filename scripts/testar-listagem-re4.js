const { S3Client, ListObjectsV2Command } = require('@aws-sdk/client-s3');

const s3 = new S3Client({ region: 'us-east-1' });
const bucket = 'mediaflow-uploads-969430605054';

async function listRE4() {
  const response = await s3.send(new ListObjectsV2Command({
    Bucket: bucket,
    Prefix: 'users/user_admin/Anime/RE4/'
  }));
  
  console.log('📁 Arquivos em RE4:\n');
  
  if (response.Contents) {
    response.Contents.forEach(obj => {
      const fileName = obj.Key.split('/').pop();
      const sizeMB = (obj.Size / (1024 * 1024)).toFixed(2);
      console.log(`${fileName} - ${sizeMB} MB`);
    });
    console.log(`\n📊 Total: ${response.Contents.length} arquivos`);
  }
}

listRE4().catch(console.error);

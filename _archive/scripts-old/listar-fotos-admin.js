const { S3Client, ListObjectsV2Command } = require('@aws-sdk/client-s3');

const s3 = new S3Client({ region: 'us-east-1' });
const bucket = 'mediaflow-uploads-969430605054';

async function listImageFolders() {
  const folders = new Map();
  let continuationToken;
  
  const imageExts = ['.jpg', '.jpeg', '.png', '.gif', '.webp', '.bmp'];
  
  do {
    const response = await s3.send(new ListObjectsV2Command({
      Bucket: bucket,
      Prefix: 'users/user_admin/',
      ContinuationToken: continuationToken
    }));
    
    if (response.Contents) {
      response.Contents.forEach(obj => {
        const isImage = imageExts.some(ext => obj.Key.toLowerCase().endsWith(ext));
        if (isImage) {
          const parts = obj.Key.split('/');
          const folder = parts.slice(0, -1).join('/');
          folders.set(folder, (folders.get(folder) || 0) + 1);
        }
      });
    }
    
    continuationToken = response.NextContinuationToken;
  } while (continuationToken);
  
  return folders;
}

async function main() {
  console.log('📸 Listando pastas com imagens em user_admin...\n');
  
  const folders = await listImageFolders();
  
  const sorted = Array.from(folders.entries()).sort((a, b) => b[1] - a[1]);
  
  sorted.forEach(([folder, count]) => {
    console.log(`📁 ${folder.replace('users/user_admin/', '')}`);
    console.log(`   ${count} imagens\n`);
  });
  
  const total = Array.from(folders.values()).reduce((sum, count) => sum + count, 0);
  console.log(`📊 Total: ${total} imagens em ${folders.size} pastas`);
}

main().catch(console.error);

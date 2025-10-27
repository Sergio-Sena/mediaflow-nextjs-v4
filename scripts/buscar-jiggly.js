const { S3Client, ListObjectsV2Command } = require('@aws-sdk/client-s3');

const s3 = new S3Client({ region: 'us-east-1' });
const bucket = 'mediaflow-uploads-969430605054';

async function listAllFolders() {
  const folders = new Set();
  let continuationToken;
  
  do {
    const response = await s3.send(new ListObjectsV2Command({
      Bucket: bucket,
      Delimiter: '/',
      ContinuationToken: continuationToken
    }));
    
    if (response.CommonPrefixes) {
      response.CommonPrefixes.forEach(prefix => {
        const folderName = prefix.Prefix.replace(/\/$/, '');
        if (folderName.toLowerCase().includes('jiggly')) {
          folders.add(folderName);
        }
      });
    }
    
    continuationToken = response.NextContinuationToken;
  } while (continuationToken);
  
  return Array.from(folders);
}

async function searchInSubfolders(prefix) {
  const folders = new Set();
  let continuationToken;
  
  do {
    const response = await s3.send(new ListObjectsV2Command({
      Bucket: bucket,
      Prefix: prefix,
      Delimiter: '/',
      ContinuationToken: continuationToken
    }));
    
    if (response.CommonPrefixes) {
      response.CommonPrefixes.forEach(p => {
        const folderName = p.Prefix.replace(/\/$/, '');
        if (folderName.toLowerCase().includes('jiggly')) {
          folders.add(folderName);
        }
      });
    }
    
    continuationToken = response.NextContinuationToken;
  } while (continuationToken);
  
  return Array.from(folders);
}

async function main() {
  console.log('🔍 Buscando pastas "Jiggly Girls" no S3...\n');
  
  const rootFolders = await listAllFolders();
  const usersFolders = await searchInSubfolders('users/');
  
  const allFolders = [...new Set([...rootFolders, ...usersFolders])];
  
  console.log(`✅ Encontradas ${allFolders.length} pastas:\n`);
  allFolders.forEach(folder => console.log(`  📁 ${folder}`));
}

main().catch(console.error);

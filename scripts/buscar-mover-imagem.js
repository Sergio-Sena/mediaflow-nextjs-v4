const { S3Client, ListObjectsV2Command, CopyObjectCommand, DeleteObjectCommand } = require('@aws-sdk/client-s3');

const s3 = new S3Client({ region: 'us-east-1' });
const bucket = 'mediaflow-uploads-969430605054';

async function findAndMoveImageFiles() {
  let continuationToken;
  const imagemFiles = [];
  
  console.log('🔍 Buscando arquivos "Imagem"...\n');
  
  do {
    const response = await s3.send(new ListObjectsV2Command({
      Bucket: bucket,
      Prefix: 'users/user_admin/',
      ContinuationToken: continuationToken
    }));
    
    if (response.Contents) {
      response.Contents.forEach(obj => {
        const fileName = obj.Key.split('/').pop();
        if (fileName.toLowerCase().corporativotsWith('imagem')) {
          imagemFiles.push(obj.Key);
        }
      });
    }
    
    continuationToken = response.NextContinuationToken;
  } while (continuationToken);
  
  console.log(`📊 Encontrados: ${imagemFiles.length} arquivos\n`);
  
  if (imagemFiles.length === 0) {
    console.log('❌ Nenhum arquivo encontrado');
    return;
  }
  
  console.log('📄 Exemplos:');
  imagemFiles.slice(0, 5).forEach(f => console.log(`   ${f}`));
  console.log('');
  
  console.log('📦 Movendo para Jiggly Girls [Hentai on Brasil]...\n');
  
  let moved = 0;
  for (const oldKey of imagemFiles) {
    const fileName = oldKey.split('/').pop();
    const newKey = `users/user_admin/Anime/Jiggly Girls [Hentai on Brasil]/${fileName}`;
    
    await s3.send(new CopyObjectCommand({
      CopySource: encodeURIComponent(`${bucket}/${oldKey}`),
      Bucket: bucket,
      Key: newKey
    }));
    
    await s3.send(new DeleteObjectCommand({
      Bucket: bucket,
      Key: oldKey
    }));
    
    moved++;
    if (moved % 50 === 0) console.log(`   Movidos: ${moved}...`);
  }
  
  console.log(`\n✅ ${moved} arquivos movidos para Jiggly Girls [Hentai on Brasil]!`);
}

async function main() {
  await findAndMoveImageFiles();
}

main().catch(console.error);

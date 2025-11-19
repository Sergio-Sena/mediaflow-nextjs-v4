const { S3Client, ListObjectsV2Command, CopyObjectCommand, DeleteObjectCommand } = require('@aws-sdk/client-s3');

const s3 = new S3Client({ region: 'us-east-1' });
const bucket = 'mediaflow-uploads-969430605054';

// 1. Deletar parts 4-7 e Jiggly_Girls
async function deleteOldJiggly() {
  console.log('🗑️  ETAPA 1: Deletando pastas antigas Jiggly...\n');
  
  const foldersToDelete = [
    'users/user_admin/Anime/Jiggly Girls [Hentai on Brasil] part4/',
    'users/user_admin/Anime/Jiggly Girls [Hentai on Brasil] part5/',
    'users/user_admin/Anime/Jiggly Girls [Hentai on Brasil] part6/',
    'users/user_admin/Anime/Jiggly Girls [Hentai on Brasil] part7/',
    'users/user_admin/Anime/Jiggly_Girls_He....jpg'
  ];
  
  let totalDeleted = 0;
  
  for (const prefix of foldersToDelete) {
    let continuationToken;
    let deleted = 0;
    
    do {
      const response = await s3.send(new ListObjectsV2Command({
        Bucket: bucket,
        Prefix: prefix,
        ContinuationToken: continuationToken
      }));
      
      if (response.Contents) {
        for (const obj of response.Contents) {
          await s3.send(new DeleteObjectCommand({
            Bucket: bucket,
            Key: obj.Key
          }));
          deleted++;
          totalDeleted++;
        }
      }
      
      continuationToken = response.NextContinuationToken;
    } while (continuationToken);
    
    if (deleted > 0) {
      console.log(`   ✅ ${prefix.split('/').pop()}: ${deleted} arquivos deletados`);
    }
  }
  
  console.log(`\n   📊 Total deletado: ${totalDeleted} arquivos\n`);
}

// 2. Licorporativo fotos soltas em Anime/
async function listLooseFiles() {
  console.log('📸 ETAPA 2: Listando fotos soltas em Anime/...\n');
  
  const response = await s3.send(new ListObjectsV2Command({
    Bucket: bucket,
    Prefix: 'users/user_admin/Anime/',
    Delimiter: '/'
  }));
  
  const looseFiles = [];
  const imageExts = ['.jpg', '.jpeg', '.png', '.gif', '.webp', '.bmp'];
  
  if (response.Contents) {
    response.Contents.forEach(obj => {
      const parts = obj.Key.split('/');
      if (parts.length === 4 && imageExts.some(ext => obj.Key.toLowerCase().endsWith(ext))) {
        looseFiles.push(obj.Key);
      }
    });
  }
  
  if (looseFiles.length > 0) {
    console.log(`   ⚠️  ${looseFiles.length} fotos soltas encontradas:`);
    looseFiles.forEach(f => console.log(`      ${f}`));
  } else {
    console.log('   ✅ Nenhuma foto solta encontrada');
  }
  
  console.log('');
}

// 3. Unificar FF VII REMAKE → FF_VII_REMAKE
async function unifyFFVII() {
  console.log('🔄 ETAPA 3: Unificando FF VII REMAKE → FF_VII_REMAKE...\n');
  
  let continuationToken;
  let moved = 0;
  
  do {
    const response = await s3.send(new ListObjectsV2Command({
      Bucket: bucket,
      Prefix: 'users/user_admin/Anime/FF VII REMAKE/',
      ContinuationToken: continuationToken
    }));
    
    if (response.Contents) {
      for (const obj of response.Contents) {
        if (!obj.Key.endsWith('/')) {
          const fileName = obj.Key.split('/').pop();
          const targetKey = `users/user_admin/Anime/FF_VII_REMAKE/${fileName}`;
          
          await s3.send(new CopyObjectCommand({
            CopySource: encodeURIComponent(`${bucket}/${obj.Key}`),
            Bucket: bucket,
            Key: targetKey
          }));
          
          await s3.send(new DeleteObjectCommand({
            Bucket: bucket,
            Key: obj.Key
          }));
          
          moved++;
        }
      }
    }
    
    continuationToken = response.NextContinuationToken;
  } while (continuationToken);
  
  console.log(`   ✅ ${moved} arquivos movidos para FF_VII_REMAKE\n`);
}

async function main() {
  console.log('🚀 ORGANIZANDO ANIME/\n');
  console.log('='.repeat(50) + '\n');
  
  await deleteOldJiggly();
  await listLooseFiles();
  await unifyFFVII();
  
  console.log('='.repeat(50));
  console.log('✅ ORGANIZAÇÃO CONCLUÍDA!\n');
  console.log('⚠️  NOTA: Arquivos de pics-notebackup estão em DEEP_ARCHIVE');
  console.log('   e precisam ser restaurados manualmente antes de copiar.\n');
}

main().catch(console.error);

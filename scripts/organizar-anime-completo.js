const { S3Client, ListObjectsV2Command, CopyObjectCommand, DeleteObjectCommand } = require('@aws-sdk/client-s3');

const s3 = new S3Client({ region: 'us-east-1' });
const sourceBucket = 'pics-notebackup';
const targetBucket = 'mediaflow-uploads-969430605054';

// 1. Copiar 648 arquivos de pics-notebackup para mediaflow-uploads
async function copyJigglyFiles() {
  console.log('📋 ETAPA 1: Copiando 648 arquivos de pics-notebackup...\n');
  
  let continuationToken;
  let copied = 0;
  
  do {
    const response = await s3.send(new ListObjectsV2Command({
      Bucket: sourceBucket,
      Prefix: 'Jiggly Girls [Hentai on Brasil]/',
      ContinuationToken: continuationToken
    }));
    
    if (response.Contents) {
      for (const obj of response.Contents) {
        if (!obj.Key.endsWith('/')) {
          const fileName = obj.Key.split('/').pop();
          const targetKey = `users/user_admin/Anime/Jiggly Girls [Hentai on Brasil]/${fileName}`;
          
          await s3.send(new CopyObjectCommand({
            CopySource: `${sourceBucket}/${obj.Key}`,
            Bucket: targetBucket,
            Key: targetKey
          }));
          
          copied++;
          if (copied % 50 === 0) console.log(`   Copiados: ${copied}...`);
        }
      }
    }
    
    continuationToken = response.NextContinuationToken;
  } while (continuationToken);
  
  console.log(`✅ ${copied} arquivos copiados!\n`);
}

// 2. Deletar parts 4-7 e Jiggly_Girls
async function deleteOldJiggly() {
  console.log('🗑️  ETAPA 2: Deletando pastas antigas...\n');
  
  const foldersToDelete = [
    'users/user_admin/Anime/Jiggly Girls [Hentai on Brasil] part4/',
    'users/user_admin/Anime/Jiggly Girls [Hentai on Brasil] part5/',
    'users/user_admin/Anime/Jiggly Girls [Hentai on Brasil] part6/',
    'users/user_admin/Anime/Jiggly Girls [Hentai on Brasil] part7/',
    'users/user_admin/Anime/Jiggly_Girls_He....jpg'
  ];
  
  for (const prefix of foldersToDelete) {
    let continuationToken;
    let deleted = 0;
    
    do {
      const response = await s3.send(new ListObjectsV2Command({
        Bucket: targetBucket,
        Prefix: prefix,
        ContinuationToken: continuationToken
      }));
      
      if (response.Contents) {
        for (const obj of response.Contents) {
          await s3.send(new DeleteObjectCommand({
            Bucket: targetBucket,
            Key: obj.Key
          }));
          deleted++;
        }
      }
      
      continuationToken = response.NextContinuationToken;
    } while (continuationToken);
    
    console.log(`   ✅ ${prefix.split('/').pop()}: ${deleted} arquivos deletados`);
  }
  
  console.log('');
}

// 3. Listar fotos soltas em Anime/
async function listLooseFiles() {
  console.log('📸 ETAPA 3: Listando fotos soltas em Anime/...\n');
  
  const response = await s3.send(new ListObjectsV2Command({
    Bucket: targetBucket,
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

// 4. Unificar FF VII REMAKE → FF_VII_REMAKE
async function unifyFFVII() {
  console.log('🔄 ETAPA 4: Unificando FF VII REMAKE → FF_VII_REMAKE...\n');
  
  let continuationToken;
  let moved = 0;
  
  do {
    const response = await s3.send(new ListObjectsV2Command({
      Bucket: targetBucket,
      Prefix: 'users/user_admin/Anime/FF VII REMAKE/',
      ContinuationToken: continuationToken
    }));
    
    if (response.Contents) {
      for (const obj of response.Contents) {
        if (!obj.Key.endsWith('/')) {
          const fileName = obj.Key.split('/').pop();
          const targetKey = `users/user_admin/Anime/FF_VII_REMAKE/${fileName}`;
          
          await s3.send(new CopyObjectCommand({
            CopySource: `${targetBucket}/${obj.Key}`,
            Bucket: targetBucket,
            Key: targetKey
          }));
          
          await s3.send(new DeleteObjectCommand({
            Bucket: targetBucket,
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
  console.log('🚀 INICIANDO ORGANIZAÇÃO COMPLETA DO ANIME/\n');
  console.log('='.repeat(50) + '\n');
  
  await copyJigglyFiles();
  await deleteOldJiggly();
  await listLooseFiles();
  await unifyFFVII();
  
  console.log('='.repeat(50));
  console.log('✅ ORGANIZAÇÃO CONCLUÍDA!\n');
}

main().catch(console.error);

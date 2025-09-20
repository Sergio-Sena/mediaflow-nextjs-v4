const AWS = require('aws-sdk');

// Configurar AWS
const s3 = new AWS.S3({
  accessKeyId: 'AKIA6DNURDT7MO5EXHLQ',
  secretAccessKey: '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',
  region: 'us-east-1'
});

const BUCKET_UPLOADS = 'mediaflow-uploads-969430605054';
const BUCKET_PROCESSED = 'mediaflow-processed-969430605054';

// Pastas que NÃO devem ser movidas (case insensitive)
const EXCLUDED_FOLDERS = ['anime', 'Anime', 'Raiz', 'captures', 'Captures', 'seart', 'Seart', 'video', 'Video', 'Star'];

async function listAllFiles(bucket) {
  const files = [];
  let continuationToken = null;
  
  do {
    const params = {
      Bucket: bucket,
      ...(continuationToken && { ContinuationToken: continuationToken })
    };
    
    const response = await s3.listObjectsV2(params).promise();
    files.push(...response.Contents);
    continuationToken = response.NextContinuationToken;
  } while (continuationToken);
  
  return files;
}

async function copyFile(sourceBucket, sourceKey, destBucket, destKey) {
  const copyParams = {
    Bucket: destBucket,
    CopySource: `${sourceBucket}/${sourceKey}`,
    Key: destKey
  };
  
  await s3.copyObject(copyParams).promise();
  console.log(`✅ Copiado: ${sourceKey} → ${destKey}`);
}

async function deleteFile(bucket, key) {
  await s3.deleteObject({ Bucket: bucket, Key: key }).promise();
  console.log(`🗑️ Deletado: ${key}`);
}

async function moveFilesToStar() {
  console.log('🚀 Iniciando movimentação para pasta Star...\n');
  
  // Processar ambos os buckets
  for (const bucket of [BUCKET_UPLOADS, BUCKET_PROCESSED]) {
    console.log(`📦 Processando bucket: ${bucket}`);
    
    const files = await listAllFiles(bucket);
    console.log(`📁 Total de arquivos: ${files.length}\n`);
    
    for (const file of files) {
      const key = file.Key;
      
      // Pular se não tem pasta (arquivo na raiz)
      if (!key.includes('/')) {
        console.log(`⏭️ Pulando arquivo na raiz: ${key}`);
        continue;
      }
      
      // Extrair pasta principal
      const folderParts = key.split('/');
      const mainFolder = folderParts[0];
      
      // Pular pastas excluídas
      if (EXCLUDED_FOLDERS.includes(mainFolder)) {
        console.log(`⏭️ Pulando pasta excluída: ${mainFolder}/${folderParts.slice(1).join('/')}`);
        continue;
      }
      
      // Criar novo caminho dentro de Star
      const newKey = `Star/${key}`;
      
      try {
        // Copiar arquivo
        await copyFile(bucket, key, bucket, newKey);
        
        // Deletar original
        await deleteFile(bucket, key);
        
        console.log(`✨ Movido: ${key} → ${newKey}\n`);
        
      } catch (error) {
        console.error(`❌ Erro ao mover ${key}:`, error.message);
      }
    }
  }
  
  console.log('🎉 Movimentação concluída!');
}

// Executar
moveFilesToStar().catch(console.error);
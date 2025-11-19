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
const EXCLUDED_FOLDERS = ['anime', 'Anime', 'Raiz', 'captures', 'Captures', 'seart', 'Seart', 'video', 'Video', 'Corporativo'];

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

async function previewMoveToCorporativo() {
  console.log('🔍 PREVIEW: O que será movido para pasta Corporativo...\n');
  
  const toMove = [];
  const excluded = [];
  
  // Analisar ambos os buckets
  for (const bucket of [BUCKET_UPLOADS, BUCKET_PROCESSED]) {
    console.log(`📦 Analisando bucket: ${bucket}`);
    
    const files = await listAllFiles(bucket);
    console.log(`📁 Total de arquivos: ${files.length}\n`);
    
    for (const file of files) {
      const key = file.Key;
      
      // Pular se não tem pasta (arquivo na raiz)
      if (!key.includes('/')) {
        excluded.push({ bucket, key, reason: 'Arquivo na raiz' });
        continue;
      }
      
      // Extrair pasta principal
      const folderParts = key.split('/');
      const mainFolder = folderParts[0];
      
      // Verificar se deve ser excluído
      if (EXCLUDED_FOLDERS.includes(mainFolder)) {
        excluded.push({ bucket, key, reason: `Pasta excluída: ${mainFolder}` });
        continue;
      }
      
      // Adicionar à lista de movimentação
      toMove.push({
        bucket,
        from: key,
        to: `Corporativo/${key}`,
        folder: mainFolder,
        size: file.Size
      });
    }
  }
  
  // Resumo por pasta
  const folderSummary = {};
  toMove.forEach(item => {
    if (!folderSummary[item.folder]) {
      folderSummary[item.folder] = { count: 0, size: 0 };
    }
    folderSummary[item.folder].count++;
    folderSummary[item.folder].size += item.size;
  });
  
  console.log('📊 RESUMO POR PASTA:');
  Object.entries(folderSummary).forEach(([folder, stats]) => {
    const sizeMB = (stats.size / 1024 / 1024).toFixed(2);
    console.log(`📁 ${folder}: ${stats.count} arquivos (${sizeMB} MB)`);
  });
  
  console.log(`\n✅ TOTAL A MOVER: ${toMove.length} arquivos`);
  console.log(`⏭️ TOTAL EXCLUÍDO: ${excluded.length} arquivos`);
  
  const totalSizeGB = toMove.reduce((sum, item) => sum + item.size, 0) / 1024 / 1024 / 1024;
  console.log(`💾 TAMANHO TOTAL: ${totalSizeGB.toFixed(2)} GB`);
  
  console.log('\n🔍 PRIMEIROS 10 ARQUIVOS A MOVER:');
  toMove.slice(0, 10).forEach(item => {
    console.log(`  ${item.from} → ${item.to}`);
  });
  
  if (excluded.length > 0) {
    console.log('\n⏭️ PRIMEIROS 10 ARQUIVOS EXCLUÍDOS:');
    excluded.slice(0, 10).forEach(item => {
      console.log(`  ${item.key} (${item.reason})`);
    });
  }
  
  console.log('\n🚀 Para executar a movimentação, rode: node move-to-corporativo.js');
}

// Executar preview
previewMoveToCorporativo().catch(console.error);
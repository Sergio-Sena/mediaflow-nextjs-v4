// Script para configurar CORS no S3
const { S3Client, PutBucketCorsCommand } = require('@aws-sdk/client-s3')

const s3Client = new S3Client({
  region: 'us-east-1',
  credentials: {
    accessKeyId: 'AKIA6DNURDT7MO5EXHLQ',
    secretAccessKey: '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',
  },
})

const corsConfiguration = {
  CORSRules: [
    {
      AllowedOrigins: [
        'https://mediaflow.sstechnologies-cloud.com',
        'https://*.vercel.app',
        'http://localhost:3000'
      ],
      AllowedMethods: ['PUT', 'POST', 'GET', 'DELETE', 'HEAD'],
      AllowedHeaders: ['*'],
      MaxAgeSeconds: 3600,
      ExposeHeaders: ['ETag', 'x-amz-version-id']
    }
  ]
}

async function configureCORS() {
  try {
    console.log('🔧 Configurando CORS no S3...')
    
    // Configurar CORS para ambos os buckets
    const buckets = ['mediaflow-uploads-969430605054', 'drive-online-frontend']
    
    for (const bucket of buckets) {
      const command = new PutBucketCorsCommand({
        Bucket: bucket,
        CORSConfiguration: corsConfiguration
      })
      
      await s3Client.send(command)
      console.log(`✅ CORS configurado para bucket: ${bucket}`)
    }
    
    await s3Client.send(command)
    
    console.log('✅ CORS configurado com sucesso!')
    console.log('📋 Configuração aplicada:')
    console.log(JSON.stringify(corsConfiguration, null, 2))
    
  } catch (error) {
    console.error('❌ Erro ao configurar CORS:', error.message)
  }
}

configureCORS()
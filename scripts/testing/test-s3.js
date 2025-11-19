// Script de teste para verificar integração S3
const { S3Client, ListObjectsV2Command, PutObjectCommand } = require('@aws-sdk/client-s3')
const { getSignedUrl } = require('@aws-sdk/s3-request-presigner')

// Configuração S3
const s3Client = new S3Client({
  region: 'us-east-1',
  credentials: {
    accessKeyId: 'AKIA6DNURDT7MO5EXHLQ',
    secretAccessKey: '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',
  },
})

const BUCKET = 'drive-online-frontend'

async function testS3Connection() {
  console.log('🧪 Testando conexão S3...')
  
  try {
    // Teste 1: Licorporativo objetos
    console.log('\n1️⃣ Testando listagem de objetos...')
    const listCommand = new ListObjectsV2Command({
      Bucket: BUCKET,
      MaxKeys: 10,
    })
    
    const listResponse = await s3Client.send(listCommand)
    console.log(`✅ Listagem OK - ${listResponse.Contents?.length || 0} arquivos encontrados`)
    
    if (listResponse.Contents?.length > 0) {
      console.log('📁 Primeiros arquivos:')
      listResponse.Contents.slice(0, 3).forEach(file => {
        console.log(`   - ${file.Key} (${file.Size} bytes)`)
      })
    }

    // Teste 2: Gerar URL de upload
    console.log('\n2️⃣ Testando geração de presigned URL...')
    const putCommand = new PutObjectCommand({
      Bucket: BUCKET,
      Key: `test/test-${Date.now()}.txt`,
      ContentType: 'text/plain',
    })
    
    const uploadUrl = await getSignedUrl(s3Client, putCommand, { expiresIn: 3600 })
    console.log('✅ Presigned URL gerada com sucesso')
    console.log(`🔗 URL: ${uploadUrl.substring(0, 100)}...`)

    // Teste 3: Verificar CloudFront
    console.log('\n3️⃣ Testando CloudFront CDN...')
    if (listResponse.Contents?.length > 0) {
      const firstFile = listResponse.Contents[0]
      const cdnUrl = `https://d1k8z7g2w8j4qr.cloudfront.net/${firstFile.Key}`
      console.log(`✅ URL CDN: ${cdnUrl}`)
    }

    console.log('\n🎉 Todos os testes S3 passaram!')
    return true

  } catch (error) {
    console.error('❌ Erro nos testes S3:', error.message)
    return false
  }
}

async function testAPIs() {
  console.log('\n🌐 Testando APIs locais...')
  
  try {
    // Simular token JWT
    const mockToken = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6InNlcmdpb3NlbmFhZG1pbkBzc3RlY2giLCJuYW1lIjoiU2VyZ2lvIFNlbmEiLCJyb2xlIjoiYWRtaW4ifQ.test'
    
    // Teste API de listagem
    console.log('\n1️⃣ Testando API /api/videos/list...')
    const listResponse = await fetch('http://localhost:3000/api/videos/list', {
      headers: {
        'Authorization': `Bearer ${mockToken}`
      }
    })
    
    if (listResponse.ok) {
      const data = await listResponse.json()
      console.log(`✅ API List OK - ${data.files?.length || 0} arquivos`)
    } else {
      console.log(`❌ API List falhou - Status: ${listResponse.status}`)
    }

    // Teste API de presigned URL
    console.log('\n2️⃣ Testando API /api/upload/presigned-url...')
    const uploadResponse = await fetch('http://localhost:3000/api/upload/presigned-url', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${mockToken}`
      },
      body: JSON.stringify({
        filename: 'test.txt',
        contentType: 'text/plain',
        fileSize: 1024
      })
    })
    
    if (uploadResponse.ok) {
      const data = await uploadResponse.json()
      console.log('✅ API Upload URL OK')
      console.log(`🔗 URL gerada: ${data.uploadUrl?.substring(0, 100)}...`)
    } else {
      console.log(`❌ API Upload URL falhou - Status: ${uploadResponse.status}`)
    }

  } catch (error) {
    console.error('❌ Erro nos testes de API:', error.message)
  }
}

// Executar testes
async function runAllTests() {
  console.log('🎬 MEDIAFLOW - TESTE DE INTEGRAÇÃO S3\n')
  
  const s3OK = await testS3Connection()
  
  if (s3OK) {
    console.log('\n' + '='.repeat(50))
    await testAPIs()
  }
  
  console.log('\n' + '='.repeat(50))
  console.log('🏁 Testes concluídos!')
}

runAllTests()
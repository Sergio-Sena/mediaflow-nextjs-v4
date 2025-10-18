// Teste das APIs em produção
const BASE_URL = 'https://mediaflow-nextjs-v4-8xovswddf-sergiosenas-projects.vercel.app'

async function testProductionAPIs() {
  console.log('🌐 Testando APIs em produção...')
  console.log(`Base URL: ${BASE_URL}`)
  
  try {
    // Teste 1: API de listagem
    console.log('\n1️⃣ Testando /api/videos/list...')
    const listResponse = await fetch(`${BASE_URL}/api/videos/list`, {
      headers: {
        'Authorization': 'Bearer test-token'
      }
    })
    
    console.log(`Status: ${listResponse.status}`)
    
    if (listResponse.ok) {
      const data = await listResponse.json()
      console.log('✅ Resposta:', {
        success: data.success,
        files: data.files?.length || 0,
        folders: data.folders?.length || 0,
        error: data.error
      })
    } else {
      const errorText = await listResponse.text()
      console.log('❌ Erro:', errorText)
    }

    // Teste 2: API de upload
    console.log('\n2️⃣ Testando /api/upload/presigned-url...')
    const uploadResponse = await fetch(`${BASE_URL}/api/upload/presigned-url`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer test-token'
      },
      body: JSON.stringify({
        filename: 'test.txt',
        contentType: 'text/plain',
        fileSize: 1024
      })
    })
    
    console.log(`Status: ${uploadResponse.status}`)
    
    if (uploadResponse.ok) {
      const data = await uploadResponse.json()
      console.log('✅ Resposta:', {
        success: data.success,
        hasUploadUrl: !!data.uploadUrl,
        bucket: data.bucket
      })
    } else {
      const errorText = await uploadResponse.text()
      console.log('❌ Erro:', errorText)
    }

  } catch (error) {
    console.error('❌ Erro geral:', error.message)
  }
}

testProductionAPIs()
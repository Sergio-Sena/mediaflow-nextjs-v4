// Teste específico para upload
const BASE_URL = 'https://mediaflow-nextjs-v4-pyf8b5daj-sergiosenas-projects.vercel.app'

async function testUpload() {
  console.log('📤 Testando funcionalidade de upload...')
  
  try {
    // Teste 1: Obter presigned URL
    console.log('\n1️⃣ Testando geração de presigned URL...')
    const response = await fetch(`${BASE_URL}/api/upload/presigned-url`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer test-token'
      },
      body: JSON.stringify({
        filename: 'test-file.txt',
        contentType: 'text/plain',
        fileSize: 1024
      })
    })
    
    console.log(`Status: ${response.status}`)
    
    if (response.ok) {
      const data = await response.json()
      console.log('✅ Presigned URL gerada:', {
        success: data.success,
        hasUploadUrl: !!data.uploadUrl,
        hasFileUrl: !!data.fileUrl,
        bucket: data.bucket,
        key: data.key
      })
      
      // Teste 2: Simular upload para S3
      if (data.uploadUrl) {
        console.log('\n2️⃣ Testando upload para S3...')
        const testContent = 'Teste de upload do Mediaflow'
        
        const uploadResponse = await fetch(data.uploadUrl, {
          method: 'PUT',
          headers: {
            'Content-Type': 'text/plain'
          },
          body: testContent
        })
        
        console.log(`Upload Status: ${uploadResponse.status}`)
        
        if (uploadResponse.ok || uploadResponse.status === 200) {
          console.log('✅ Upload para S3 realizado com sucesso!')
          console.log(`📁 Arquivo disponível em: ${data.fileUrl}`)
        } else {
          console.log('❌ Falha no upload para S3')
        }
      }
      
    } else {
      const errorText = await response.text()
      console.log('❌ Erro na API:', errorText.substring(0, 200))
    }

    // Teste 3: Verificar listagem após upload
    console.log('\n3️⃣ Testando listagem após upload...')
    const listResponse = await fetch(`${BASE_URL}/api/videos/list`, {
      headers: {
        'Authorization': 'Bearer test-token'
      }
    })
    
    if (listResponse.ok) {
      const listData = await listResponse.json()
      console.log('✅ Listagem atualizada:', {
        totalFiles: listData.files?.length || 0,
        hasTestFile: listData.files?.some(f => f.name.includes('test-file')) || false
      })
    }

  } catch (error) {
    console.error('❌ Erro geral:', error.message)
  }
}

testUpload()
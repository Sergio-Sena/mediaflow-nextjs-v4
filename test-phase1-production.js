// Test Phase 1 in production
const API_BASE = 'https://gdb962d234.execute-api.us-east-1.amazonaws.com/prod'

async function testSanitization() {
  console.log('🧪 TESTING PHASE 1 IN PRODUCTION\n')
  
  const testFiles = [
    { name: '🎥 Meu Vídeo Incrível 🚀.mp4', size: 100 * 1024 * 1024 },
    { name: 'Video com acentos & símbolos @#$.ts', size: 200 * 1024 * 1024 },
    { name: 'Este é um nome muito muito muito muito longo que precisa ser truncado.avi', size: 50 * 1024 * 1024 },
    { name: 'normal-video.mp4', size: 600 * 1024 * 1024 }
  ]
  
  for (const testFile of testFiles) {
    try {
      console.log(`Testing: "${testFile.name}" (${Math.round(testFile.size / 1024 / 1024)}MB)`)
      
      const response = await fetch(`${API_BASE}/upload`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          filename: testFile.name,
          contentType: 'video/mp4',
          fileSize: testFile.size
        })
      })
      
      const data = await response.json()
      
      if (data.success) {
        console.log(`✅ SUCCESS`)
        console.log(`  Original: ${testFile.name}`)
        console.log(`  Sanitized: ${data.sanitizedName}`)
        console.log(`  Needs Conversion: ${data.needsConversion}`)
        console.log(`  Length: ${data.sanitizedName.length}/45`)
        console.log()
      } else {
        console.log(`❌ FAILED: ${data.message}`)
        console.log()
      }
      
    } catch (error) {
      console.log(`❌ ERROR: ${error.message}`)
      console.log()
    }
  }
  
  console.log('✅ PHASE 1 PRODUCTION TEST COMPLETE')
}

testSanitization()
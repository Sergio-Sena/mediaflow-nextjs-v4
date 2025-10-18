#!/usr/bin/env node

const jwt = require('jsonwebtoken')

// Configurações
const SECRET_KEY = 'mediaflow_super_secret_key_2025'
const API_URL = 'https://gdb962d234.execute-api.us-east-1.amazonaws.com/prod'

// Simular tokens de diferentes usuários
const adminToken = jwt.sign({
  user_id: 'admin',
  user_name: 'Admin User',
  s3_prefix: '',
  role: 'admin',
  exp: Math.floor(Date.now() / 1000) + (24 * 60 * 60) // 24h
}, SECRET_KEY)

const userToken = jwt.sign({
  user_id: 'sergio_sena',
  user_name: 'Sergio Sena',
  s3_prefix: 'sergio_sena/',
  role: 'user',
  exp: Math.floor(Date.now() / 1000) + (24 * 60 * 60) // 24h
}, SECRET_KEY)

console.log('🧪 Testando Filtro de Usuários')
console.log('=' * 50)

// Função para testar API
async function testAPI(token, userType) {
  console.log(`\n📋 Testando como ${userType}:`)
  
  try {
    const response = await fetch(`${API_URL}/files?context=dashboard`, {
      method: 'GET',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      }
    })
    
    const data = await response.json()
    
    if (data.success) {
      console.log(`✅ ${userType} - ${data.files.length} arquivos retornados`)
      
      // Mostrar primeiros 5 arquivos
      data.files.slice(0, 5).forEach(file => {
        console.log(`   📁 ${file.key} (pasta: ${file.folder || 'root'})`)
      })
      
      if (data.files.length > 5) {
        console.log(`   ... e mais ${data.files.length - 5} arquivos`)
      }
    } else {
      console.log(`❌ ${userType} - Erro: ${data.message}`)
    }
  } catch (error) {
    console.log(`❌ ${userType} - Erro de rede: ${error.message}`)
  }
}

// Executar testes
async function runTests() {
  console.log('🔑 Tokens gerados:')
  console.log(`Admin Token: ${adminToken.substring(0, 50)}...`)
  console.log(`User Token: ${userToken.substring(0, 50)}...`)
  
  await testAPI(adminToken, 'ADMIN')
  await testAPI(userToken, 'USER')
  
  console.log('\n📊 Resultado Esperado:')
  console.log('- ADMIN deve ver TODOS os arquivos (sem filtro)')
  console.log('- USER deve ver apenas arquivos da pasta "sergio_sena/"')
}

runTests().catch(console.error)
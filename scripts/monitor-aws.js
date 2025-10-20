// Monitor AWS Lambda Health
const https = require('https');

const API_URL = 'https://gdb962d234.execute-api.us-east-1.amazonaws.com/prod/auth/login';
const CHECK_INTERVAL = 60000; // 1 minuto

console.log('🔍 Monitorando AWS Lambda...\n');

function checkAWS() {
  const data = JSON.stringify({
    email: 'admin@midiaflow.com',
    password: 'admin123'
  });

  const options = {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Content-Length': data.length
    }
  };

  const req = https.request(API_URL, options, (res) => {
    const timestamp = new Date().toLocaleTimeString('pt-BR');
    
    if (res.statusCode === 200) {
      console.log(`✅ [${timestamp}] AWS NORMALIZADA! Status: ${res.statusCode}`);
      console.log('\n🎉 Lambda funcionando! Pode testar produção agora.\n');
      process.exit(0);
    } else if (res.statusCode === 401) {
      console.log(`✅ [${timestamp}] AWS NORMALIZADA! Lambda respondeu (credenciais inválidas, mas funcionando)`);
      console.log('\n🎉 Lambda funcionando! Pode testar produção agora.\n');
      process.exit(0);
    } else {
      console.log(`⏳ [${timestamp}] Ainda com problema. Status: ${res.statusCode}`);
    }
  });

  req.on('error', (error) => {
    const timestamp = new Date().toLocaleTimeString('pt-BR');
    console.log(`🔴 [${timestamp}] Erro: ${error.message}`);
  });

  req.write(data);
  req.end();
}

// Primeira verificação
checkAWS();

// Verificar a cada minuto
setInterval(checkAWS, CHECK_INTERVAL);

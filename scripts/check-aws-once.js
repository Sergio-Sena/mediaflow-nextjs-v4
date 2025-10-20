// Verificação única do status AWS
const https = require('https');

const API_URL = 'https://gdb962d234.execute-api.us-east-1.amazonaws.com/prod/auth/login';

console.log('🔍 Verificando AWS Lambda...\n');

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
  console.log(`Status: ${res.statusCode}\n`);
  
  if (res.statusCode === 200 || res.statusCode === 401) {
    console.log('✅ AWS NORMALIZADA!');
    console.log('🎉 Lambda funcionando!');
    console.log('📝 Pode testar produção agora.\n');
  } else if (res.statusCode === 500) {
    console.log('🔴 AWS ainda com problema (500)');
    console.log('⏳ Aguarde mais um pouco.\n');
  } else {
    console.log(`⚠️ Status inesperado: ${res.statusCode}\n`);
  }
});

req.on('error', (error) => {
  console.log('🔴 Erro de conexão:', error.message);
  console.log('⏳ AWS ainda indisponível.\n');
});

req.write(data);
req.end();

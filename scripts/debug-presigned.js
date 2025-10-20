const https = require('https');

const data = JSON.stringify({ userId: 'lid_lima', fileExt: 'jpg' });

const options = {
  hostname: 'gdb962d234.execute-api.us-east-1.amazonaws.com',
  path: '/prod/avatar-presigned',
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Content-Length': data.length
  }
};

const req = https.request(options, (res) => {
  let body = '';
  res.on('data', chunk => body += chunk);
  res.on('end', () => {
    console.log('Status:', res.statusCode);
    console.log('Response:', body);
    
    if (res.statusCode === 200) {
      const parsed = JSON.parse(body);
      console.log('\n🔍 Verificando URL:');
      console.log('Tem &amp;?', parsed.presignedUrl.includes('&amp;'));
      console.log('\nURL completa:');
      console.log(parsed.presignedUrl);
    }
  });
});

req.on('error', (e) => console.error('Erro:', e));
req.write(data);
req.end();

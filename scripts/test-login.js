const fetch = require('node-fetch');

async function testLogin() {
  const response = await fetch('https://gdb962d234.execute-api.us-east-1.amazonaws.com/prod/auth/login', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      email: 'sergiosenaadmin@sstech',
      password: 'admin123'
    })
  });
  
  const data = await response.json();
  console.log('Status:', response.status);
  console.log('Response:', JSON.stringify(data, null, 2));
}

testLogin();

const crypto = require('crypto');

// Função de hash igual à Lambda
function hashPassword(password) {
  return crypto.createHash('sha256').update(password).digest('hex');
}

// Teste
const email = 'sergiosenaadmin@sstech';
const password = 'admin123';
const hashedPassword = hashPassword(password);

console.log('=== TESTE DE LOGIN ===\n');
console.log('Email:', email);
console.log('Senha:', password);
console.log('Hash SHA256:', hashedPassword);
console.log('\n=== VERIFICAÇÃO ===');
console.log('Se o hash acima estiver no DynamoDB, o login deveria funcionar.');
console.log('\nTestando API AWS...\n');

// Teste direto na API
fetch('https://gdb962d234.execute-api.us-east-1.amazonaws.com/prod/auth/login', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({ email, password })
})
.then(res => res.json())
.then(data => {
  console.log('Resposta da API:', JSON.stringify(data, null, 2));
})
.catch(err => {
  console.error('Erro:', err.message);
});

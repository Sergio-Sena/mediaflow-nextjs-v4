#!/usr/bin/env node
/**
 * Teste completo de funcionalidades em produção
 * Domain: https://midiaflow.sstechnologies-cloud.com
 */

const BASE_URL = 'https://midiaflow.sstechnologies-cloud.com';
const API_URL = 'https://gdb962d234.execute-api.us-east-1.amazonaws.com/prod';

const tests = [];
let passed = 0;
let failed = 0;

async function test(name, fn) {
  try {
    await fn();
    console.log(`✅ ${name}`);
    passed++;
  } catch (error) {
    console.log(`❌ ${name}: ${error.message}`);
    failed++;
  }
}

async function testHomePage() {
  const response = await fetch(BASE_URL);
  if (!response.ok) throw new Error(`HTTP ${response.status}`);
  const html = await response.text();
  if (!html.includes('Mídiaflow')) throw new Error('Título não encontrado');
}

async function testLoginPage() {
  const response = await fetch(`${BASE_URL}/login/`);
  if (!response.ok) throw new Error(`HTTP ${response.status}`);
  const html = await response.text();
  if (!html.includes('Mídiaflow')) throw new Error('Página de login inválida');
}

async function testRegisterPage() {
  const response = await fetch(`${BASE_URL}/register/`);
  if (!response.ok) throw new Error(`HTTP ${response.status}`);
  const html = await response.text();
  if (!html.includes('Criar Conta')) throw new Error('Página de registro inválida');
}

async function test2FAPage() {
  const response = await fetch(`${BASE_URL}/2fa/`);
  if (!response.ok) throw new Error(`HTTP ${response.status}`);
}

async function testAdminPage() {
  const response = await fetch(`${BASE_URL}/admin/`);
  if (!response.ok) throw new Error(`HTTP ${response.status}`);
}

async function testDashboardPage() {
  const response = await fetch(`${BASE_URL}/dashboard/`);
  if (!response.ok) throw new Error(`HTTP ${response.status}`);
}

async function testAPIUsers() {
  const response = await fetch(`${API_URL}/users`);
  if (!response.ok) throw new Error(`HTTP ${response.status}`);
  const data = await response.json();
  if (!data.success) throw new Error('API retornou erro');
  if (!Array.isArray(data.users)) throw new Error('Usuários não encontrados');
}

async function testAPIFiles() {
  const response = await fetch(`${API_URL}/files`);
  if (!response.ok) throw new Error(`HTTP ${response.status}`);
  const data = await response.json();
  if (!data.success) throw new Error('API retornou erro');
}

async function testOldDomain() {
  try {
    const response = await fetch('https://mediaflow.sstechnologies-cloud.com/');
    if (response.ok) throw new Error('Domínio antigo ainda está ativo!');
  } catch (error) {
    if (error.message.includes('ainda está ativo')) throw error;
    // DNS error é esperado
  }
}

async function runTests() {
  console.log('🧪 Testando Mídiaflow em Produção\n');
  console.log('🌐 Domain: https://midiaflow.sstechnologies-cloud.com');
  console.log('🔗 API: https://gdb962d234.execute-api.us-east-1.amazonaws.com/prod\n');
  
  console.log('📄 Testando Páginas Frontend:\n');
  await test('Página Inicial (/)', testHomePage);
  await test('Página de Login (/login)', testLoginPage);
  await test('Página de Registro (/register)', testRegisterPage);
  await test('Página 2FA (/2fa)', test2FAPage);
  await test('Página Admin (/admin)', testAdminPage);
  await test('Página Dashboard (/dashboard)', testDashboardPage);
  
  console.log('\n🔌 Testando APIs Backend:\n');
  await test('API GET /users', testAPIUsers);
  await test('API GET /files', testAPIFiles);
  
  console.log('\n🗑️  Verificando Remoção:\n');
  await test('Domínio antigo removido', testOldDomain);
  
  console.log('\n' + '='.repeat(60));
  console.log(`📊 Resultado: ${passed} passou, ${failed} falhou`);
  console.log('='.repeat(60));
  
  if (failed === 0) {
    console.log('\n✅ TODOS OS TESTES PASSARAM!');
    console.log('🚀 Sistema 100% funcional em produção');
  } else {
    console.log(`\n⚠️  ${failed} teste(s) falharam`);
  }
}

runTests().catch(console.error);

/**
 * Teste upload com arquivo pequeno via curl simulado
 */

const https = require('https');

async function testSmallFileUpload() {
    console.log('🧪 TESTE UPLOAD ARQUIVO PEQUENO - PRODUÇÃO');
    console.log('=' * 50);
    
    try {
        // 1. Obter URL presigned
        console.log('1️⃣ Obtendo URL presigned...');
        
        const urlResponse = await makeRequest('POST', '/upload/presigned', {
            filename: 'test_small_production.txt',
            contentType: 'text/plain',
            fileSize: 50
        });
        
        console.log(`Status: ${urlResponse.statusCode}`);
        
        if (urlResponse.statusCode !== 200) {
            console.log('❌ Falha ao obter URL presigned');
            console.log('Response:', urlResponse.body);
            return;
        }
        
        const urlData = JSON.parse(urlResponse.body);
        
        if (!urlData.success) {
            console.log('❌ Resposta de erro:', urlData.message);
            return;
        }
        
        console.log('✅ URL presigned obtida');
        console.log(`Key: ${urlData.key}`);
        
        // 2. Upload arquivo pequeno
        console.log('\n2️⃣ Fazendo upload do arquivo pequeno...');
        
        const testContent = 'Hello, this is a small test file for production!';
        
        const uploadResponse = await uploadToS3(urlData.uploadUrl, testContent, 'text/plain');
        
        console.log(`Upload status: ${uploadResponse.statusCode}`);
        
        if (uploadResponse.statusCode >= 200 && uploadResponse.statusCode < 300) {
            console.log('✅ UPLOAD PEQUENO FUNCIONOU!');
            console.log('🎯 Arquivo pequeno subiu com sucesso via presigned URL');
        } else {
            console.log('❌ UPLOAD PEQUENO FALHOU');
            console.log(`Código: ${uploadResponse.statusCode}`);
            console.log(`Resposta: ${uploadResponse.body}`);
        }
        
    } catch (error) {
        console.log('❌ Erro:', error.message);
    }
}

function makeRequest(method, path, data = null) {
    return new Promise((resolve, reject) => {
        const options = {
            hostname: 'gdb962d234.execute-api.us-east-1.amazonaws.com',
            port: 443,
            path: '/prod' + path,
            method: method,
            headers: {
                'Content-Type': 'application/json'
            }
        };
        
        const req = https.request(options, (res) => {
            let body = '';
            res.on('data', chunk => body += chunk);
            res.on('end', () => resolve({
                statusCode: res.statusCode,
                body: body
            }));
        });
        
        req.on('error', reject);
        
        if (data) {
            req.write(JSON.stringify(data));
        }
        
        req.end();
    });
}

function uploadToS3(uploadUrl, content, contentType) {
    return new Promise((resolve, reject) => {
        const url = new URL(uploadUrl);
        
        const options = {
            hostname: url.hostname,
            port: 443,
            path: url.pathname + url.search,
            method: 'PUT',
            headers: {
                'Content-Type': contentType,
                'Content-Length': Buffer.byteLength(content)
            }
        };
        
        const req = https.request(options, (res) => {
            let body = '';
            res.on('data', chunk => body += chunk);
            res.on('end', () => resolve({
                statusCode: res.statusCode,
                body: body
            }));
        });
        
        req.on('error', reject);
        req.write(content);
        req.end();
    });
}

testSmallFileUpload();
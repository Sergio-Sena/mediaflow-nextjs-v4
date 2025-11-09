/**
 * Teste rápido para verificar status 200 nos uploads
 */

const https = require('https');

async function testUploadStatus() {
    console.log('🧪 TESTE STATUS UPLOAD - PRODUÇÃO');
    console.log('=' * 40);
    
    try {
        // Testar geração de URL presigned
        const response = await makeRequest('POST', '/upload/presigned', {
            filename: 'test_status_check.txt',
            contentType: 'text/plain',
            fileSize: 100
        });
        
        console.log(`📡 Status Code: ${response.statusCode}`);
        
        if (response.statusCode === 200) {
            console.log('✅ UPLOAD HANDLER - STATUS 200 OK');
            
            const data = JSON.parse(response.body);
            if (data.success) {
                console.log('✅ Presigned URL gerada com sucesso');
                console.log(`🔑 Key: ${data.key}`);
            } else {
                console.log('❌ Erro na resposta:', data.message);
            }
        } else {
            console.log('❌ ERRO - Status não é 200');
            console.log('Response:', response.body);
        }
        
    } catch (error) {
        console.log('❌ Erro na requisição:', error.message);
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

testUploadStatus();
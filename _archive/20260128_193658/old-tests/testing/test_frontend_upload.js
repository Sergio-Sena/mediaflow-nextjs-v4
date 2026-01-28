/**
 * Teste simulando o frontend atual em produção
 */

const https = require('https');

async function testFrontendUpload() {
    console.log('🌐 TESTE FRONTEND PRODUÇÃO');
    console.log('=' * 40);
    
    try {
        // Simular FormData como o frontend antigo faz
        const boundary = '----formdata123';
        const testContent = 'Small test file content';
        
        const formData = [
            `--${boundary}`,
            'Content-Disposition: form-data; name="file"; filename="test_frontend.txt"',
            'Content-Type: text/plain',
            '',
            testContent,
            `--${boundary}`,
            'Content-Disposition: form-data; name="filename"',
            '',
            'test_frontend.txt',
            `--${boundary}--`
        ].join('\r\n');
        
        console.log('📤 Testando rota /api/upload/direct...');
        
        const response = await makeFormRequest('/api/upload/direct', formData, boundary);
        
        console.log(`Status: ${response.statusCode}`);
        console.log(`Response: ${response.body}`);
        
        if (response.statusCode === 200) {
            console.log('✅ FRONTEND UPLOAD FUNCIONANDO!');
            const data = JSON.parse(response.body);
            if (data.success) {
                console.log('🎯 Upload via frontend completado com sucesso');
            }
        } else if (response.statusCode === 403) {
            console.log('❌ ERRO 403 - Rota não acessível');
        } else {
            console.log('❌ ERRO - Status:', response.statusCode);
        }
        
    } catch (error) {
        console.log('❌ Erro:', error.message);
    }
}

function makeFormRequest(path, formData, boundary) {
    return new Promise((resolve, reject) => {
        const options = {
            hostname: 'mediaflow.sstechnologies-cloud.com',
            port: 443,
            path: path,
            method: 'POST',
            headers: {
                'Content-Type': `multipart/form-data; boundary=${boundary}`,
                'Content-Length': Buffer.byteLength(formData)
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
        req.write(formData);
        req.end();
    });
}

testFrontendUpload();
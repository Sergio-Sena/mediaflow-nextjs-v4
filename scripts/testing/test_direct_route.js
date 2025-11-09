/**
 * Teste da rota /api/upload/direct
 */

const https = require('https');
const fs = require('fs');

async function testDirectRoute() {
    console.log('🧪 TESTE ROTA /api/upload/direct');
    
    try {
        // Criar FormData simples
        const boundary = '----testboundary123';
        const testContent = 'Hello test file';
        
        const formData = [
            `--${boundary}`,
            'Content-Disposition: form-data; name="file"; filename="test.txt"',
            'Content-Type: text/plain',
            '',
            testContent,
            `--${boundary}`,
            'Content-Disposition: form-data; name="filename"',
            '',
            'test.txt',
            `--${boundary}--`
        ].join('\r\n');
        
        const options = {
            hostname: 'mediaflow.sstechnologies-cloud.com',
            port: 443,
            path: '/api/upload/direct',
            method: 'POST',
            headers: {
                'Content-Type': `multipart/form-data; boundary=${boundary}`,
                'Content-Length': Buffer.byteLength(formData)
            }
        };
        
        const response = await makeRequest(options, formData);
        
        console.log(`Status: ${response.statusCode}`);
        console.log(`Response: ${response.body}`);
        
        if (response.statusCode === 200) {
            console.log('✅ Rota /api/upload/direct funcionando!');
        } else {
            console.log('❌ Rota ainda com problema');
        }
        
    } catch (error) {
        console.log('❌ Erro:', error.message);
    }
}

function makeRequest(options, data) {
    return new Promise((resolve, reject) => {
        const req = https.request(options, (res) => {
            let body = '';
            res.on('data', chunk => body += chunk);
            res.on('end', () => resolve({
                statusCode: res.statusCode,
                body: body
            }));
        });
        
        req.on('error', reject);
        req.write(data);
        req.end();
    });
}

testDirectRoute();
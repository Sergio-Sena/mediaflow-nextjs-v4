/**
 * Teste específico para erro 403 em arquivos pequenos
 * Execute: node test_small_file_403.js
 */

const https = require('https');
const fs = require('fs');

const API_BASE_URL = 'https://gdb962d234.execute-api.us-east-1.amazonaws.com/prod';

async function testSmallFileUpload() {
    console.log('🧪 TESTE ESPECÍFICO - Erro 403 Arquivos Pequenos');
    console.log('=' * 50);
    
    // Criar arquivo de teste pequeno
    const testContent = Buffer.from('Test content for small file upload debugging');
    const testFilename = `test_small_${Date.now()}.txt`;
    
    console.log(`📄 Arquivo teste: ${testFilename} (${testContent.length} bytes)`);
    
    try {
        // 1. Obter URL presigned
        console.log('\n1️⃣ Obtendo URL presigned...');
        
        const urlResponse = await makeRequest('POST', '/upload/presigned', {
            filename: testFilename,
            contentType: 'text/plain',
            fileSize: testContent.length
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
        console.log(`Bucket: ${urlData.bucket}`);
        
        // 2. Analisar URL presigned
        console.log('\n2️⃣ Analisando URL presigned...');
        const url = new URL(urlData.uploadUrl);
        console.log(`Host: ${url.host}`);
        console.log(`Path: ${url.pathname}`);
        console.log(`Query params: ${url.search.length} chars`);
        
        // Verificar parâmetros importantes
        const params = new URLSearchParams(url.search);
        console.log(`X-Amz-Algorithm: ${params.get('X-Amz-Algorithm')}`);
        console.log(`X-Amz-Expires: ${params.get('X-Amz-Expires')}`);
        console.log(`X-Amz-Date: ${params.get('X-Amz-Date')}`);
        
        // 3. Tecorporativo upload
        console.log('\n3️⃣ Testando upload...');
        
        const uploadResponse = await uploadFile(urlData.uploadUrl, testContent, 'text/plain');
        
        console.log(`Upload status: ${uploadResponse.statusCode}`);
        console.log(`Upload headers:`, uploadResponse.headers);
        
        if (uploadResponse.statusCode >= 200 && uploadResponse.statusCode < 300) {
            console.log('✅ Upload realizado com sucesso!');
        } else {
            console.log('❌ Upload falhou');
            console.log('Response body:', uploadResponse.body);
            
            // Debug específico para 403
            if (uploadResponse.statusCode === 403) {
                console.log('\n🔍 DEBUG 403 FORBIDDEN:');
                console.log('- Verificar se URL não expirou');
                console.log('- Verificar Content-Type match');
                console.log('- Verificar permissões do bucket');
                console.log('- Verificar CORS configuration');
            }
        }
        
    } catch (error) {
        console.log('❌ Erro no teste:', error.message);
    }
}

function makeRequest(method, path, data = null) {
    return new Promise((resolve, reject) => {
        const url = new URL(API_BASE_URL + path);
        
        const options = {
            hostname: url.hostname,
            port: 443,
            path: url.pathname + url.search,
            method: method,
            headers: {
                'Content-Type': 'application/json'
            }
        };
        
        if (data) {
            const postData = JSON.stringify(data);
            options.headers['Content-Length'] = Buffer.byteLength(postData);
        }
        
        const req = https.request(options, (res) => {
            let body = '';
            
            res.on('data', (chunk) => {
                body += chunk;
            });
            
            res.on('end', () => {
                resolve({
                    statusCode: res.statusCode,
                    headers: res.headers,
                    body: body
                });
            });
        });
        
        req.on('error', (error) => {
            reject(error);
        });
        
        if (data) {
            req.write(JSON.stringify(data));
        }
        
        req.end();
    });
}

function uploadFile(uploadUrl, content, contentType) {
    return new Promise((resolve, reject) => {
        const url = new URL(uploadUrl);
        
        const options = {
            hostname: url.hostname,
            port: 443,
            path: url.pathname + url.search,
            method: 'PUT',
            headers: {
                'Content-Type': contentType,
                'Content-Length': content.length
            }
        };
        
        const req = https.request(options, (res) => {
            let body = '';
            
            res.on('data', (chunk) => {
                body += chunk;
            });
            
            res.on('end', () => {
                resolve({
                    statusCode: res.statusCode,
                    headers: res.headers,
                    body: body
                });
            });
        });
        
        req.on('error', (error) => {
            reject(error);
        });
        
        req.write(content);
        req.end();
    });
}

// Executar teste
testSmallFileUpload().then(() => {
    console.log('\n✅ Teste concluído!');
}).catch((error) => {
    console.log('\n❌ Erro no teste:', error);
});
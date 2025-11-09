/**
 * Teste com arquivo real pequeno da pasta teste
 */

const fs = require('fs');
const https = require('https');
const path = require('path');

const API_BASE_URL = 'https://gdb962d234.execute-api.us-east-1.amazonaws.com/prod';
const TEST_FILE = './teste/Orçamento telhadoAudo3.pdf';

async function testRealSmallFile() {
    console.log('🧪 TESTE ARQUIVO REAL PEQUENO');
    console.log('=' * 40);
    
    // Ler arquivo real
    if (!fs.existsSync(TEST_FILE)) {
        console.log('❌ Arquivo não encontrado:', TEST_FILE);
        return;
    }
    
    const fileBuffer = fs.readFileSync(TEST_FILE);
    const fileName = path.basename(TEST_FILE);
    
    console.log(`📄 Arquivo: ${fileName}`);
    console.log(`📊 Tamanho: ${fileBuffer.length} bytes (${Math.round(fileBuffer.length/1024)}KB)`);
    
    try {
        // 1. Obter URL presigned
        console.log('\n1️⃣ Obtendo URL presigned...');
        
        const urlResponse = await makeRequest('POST', '/upload/presigned', {
            filename: fileName,
            contentType: 'application/pdf',
            fileSize: fileBuffer.length
        });
        
        console.log(`Status: ${urlResponse.statusCode}`);
        
        if (urlResponse.statusCode !== 200) {
            console.log('❌ Falha ao obter URL:', urlResponse.body);
            return;
        }
        
        const urlData = JSON.parse(urlResponse.body);
        
        if (!urlData.success) {
            console.log('❌ Erro na resposta:', urlData.message);
            return;
        }
        
        console.log('✅ URL presigned obtida');
        console.log(`Key: ${urlData.key}`);
        
        // 2. Upload do arquivo real
        console.log('\n2️⃣ Fazendo upload...');
        
        const uploadResponse = await uploadFile(urlData.uploadUrl, fileBuffer, 'application/pdf');
        
        console.log(`Status: ${uploadResponse.statusCode}`);
        
        if (uploadResponse.statusCode >= 200 && uploadResponse.statusCode < 300) {
            console.log('✅ UPLOAD SUCESSO!');
            console.log('🎯 Arquivo pequeno funcionou perfeitamente');
        } else {
            console.log('❌ UPLOAD FALHOU');
            console.log(`Código: ${uploadResponse.statusCode}`);
            console.log(`Resposta: ${uploadResponse.body}`);
            
            if (uploadResponse.statusCode === 403) {
                console.log('\n🔍 ERRO 403 DETECTADO:');
                console.log('- URL pode ter expirado');
                console.log('- Content-Type incorreto');
                console.log('- Permissões S3');
            }
        }
        
    } catch (error) {
        console.log('❌ Erro:', error.message);
    }
}

function makeRequest(method, path, data = null) {
    return new Promise((resolve, reject) => {
        const url = new URL(API_BASE_URL + path);
        
        const options = {
            hostname: url.hostname,
            port: 443,
            path: url.pathname,
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

function uploadFile(uploadUrl, fileBuffer, contentType) {
    return new Promise((resolve, reject) => {
        const url = new URL(uploadUrl);
        
        const options = {
            hostname: url.hostname,
            port: 443,
            path: url.pathname + url.search,
            method: 'PUT',
            headers: {
                'Content-Type': contentType,
                'Content-Length': fileBuffer.length
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
        req.write(fileBuffer);
        req.end();
    });
}

testRealSmallFile();
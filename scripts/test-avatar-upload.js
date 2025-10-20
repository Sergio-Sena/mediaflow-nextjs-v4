const https = require('https');
const fs = require('fs');
const path = require('path');

// 1. Obter presigned URL
function getPresignedUrl(userId, fileExt) {
  return new Promise((resolve, reject) => {
    const data = JSON.stringify({ userId, fileExt });
    
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
        if (res.statusCode === 200) {
          resolve(JSON.parse(body));
        } else {
          reject(new Error(`Status: ${res.statusCode}, Body: ${body}`));
        }
      });
    });

    req.on('error', reject);
    req.write(data);
    req.end();
  });
}

// 2. Upload para S3
function uploadToS3(presignedUrl, filePath) {
  return new Promise((resolve, reject) => {
    const fileBuffer = fs.readFileSync(filePath);
    const url = new URL(presignedUrl);
    
    const options = {
      hostname: url.hostname,
      path: url.pathname + url.search,
      method: 'PUT',
      headers: {
        'Content-Type': 'image/jpeg',
        'Content-Length': fileBuffer.length
      }
    };

    const req = https.request(options, (res) => {
      if (res.statusCode === 200) {
        resolve('Upload OK');
      } else {
        reject(new Error(`Upload failed: ${res.statusCode}`));
      }
    });

    req.on('error', reject);
    req.write(fileBuffer);
    req.end();
  });
}

// 3. Atualizar DynamoDB
function updateUserAvatar(userId, avatarUrl) {
  return new Promise((resolve, reject) => {
    const data = JSON.stringify({ user_id: userId, avatar_url: avatarUrl });
    
    const options = {
      hostname: 'gdb962d234.execute-api.us-east-1.amazonaws.com',
      path: '/prod/users/update',
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
        if (res.statusCode === 200) {
          resolve(JSON.parse(body));
        } else {
          reject(new Error(`Status: ${res.statusCode}`));
        }
      });
    });

    req.on('error', reject);
    req.write(data);
    req.end();
  });
}

// Executar teste
async function testAvatarUpload() {
  console.log('🧪 Testando upload de avatar para lid_lima...\n');
  
  try {
    // 1. Obter presigned URL
    console.log('1️⃣ Obtendo presigned URL...');
    const presignedData = await getPresignedUrl('lid_lima', 'jpg');
    console.log('✅ Presigned URL obtida');
    console.log('   URL:', presignedData.presignedUrl.substring(0, 80) + '...');
    
    // 2. Upload da imagem
    console.log('\n2️⃣ Fazendo upload da imagem...');
    const imagePath = path.join(__dirname, '..', 'avatar', 'IMG_20190210_162038.jpg');
    
    if (!fs.existsSync(imagePath)) {
      throw new Error(`Imagem não encontrada: ${imagePath}`);
    }
    
    const cleanUrl = presignedData.presignedUrl.replace(/&amp;/g, '&');
    await uploadToS3(cleanUrl, imagePath);
    console.log('✅ Upload concluído');
    
    // 3. Atualizar DynamoDB
    console.log('\n3️⃣ Atualizando DynamoDB...');
    await updateUserAvatar('lid_lima', presignedData.avatarUrl);
    console.log('✅ DynamoDB atualizado');
    
    console.log('\n🎉 SUCESSO! Avatar atualizado para lid_lima');
    console.log('📸 URL:', presignedData.avatarUrl);
    
  } catch (error) {
    console.error('\n❌ ERRO:', error.message);
    process.exit(1);
  }
}

testAvatarUpload();

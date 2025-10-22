// Script para testar a lógica de upload
const testCases = [
  {
    description: "Dropdown: Minha pasta (Admin) + Pasta: Anime",
    destination: "users/user_admin/",
    webkitRelativePath: "Anime/video.mp4",
    expected: "users/user_admin/Anime/video.mp4"
  },
  {
    description: "Dropdown: Raiz + Pasta: Anime",
    destination: "",
    webkitRelativePath: "Anime/video.mp4",
    expected: "users/user_admin/Anime/video.mp4" // Lambda adiciona users/{username}/
  },
  {
    description: "Dropdown: Minha pasta (Admin) + Arquivo solto",
    destination: "users/user_admin/",
    webkitRelativePath: "",
    filename: "video.mp4",
    expected: "users/user_admin/video.mp4"
  }
];

function processFilename(destination, webkitRelativePath, filename) {
  // Frontend logic (DirectUpload.tsx)
  let result = webkitRelativePath || filename;
  
  if (destination) {
    result = destination + result;
  }
  
  // Lambda logic (upload-handler)
  // Se já começa com users/, não duplica
  if (!result.startsWith('users/')) {
    result = 'users/user_admin/' + result; // username extraído do JWT
  }
  
  return result;
}

console.log("🧪 TESTE DE LÓGICA DE UPLOAD\n");

let passed = 0;
let failed = 0;

testCases.forEach((test, index) => {
  const result = processFilename(
    test.destination, 
    test.webkitRelativePath, 
    test.filename || ''
  );
  
  const success = result === test.expected;
  
  if (success) {
    passed++;
    console.log(`✅ Teste ${index + 1}: ${test.description}`);
    console.log(`   Resultado: ${result}\n`);
  } else {
    failed++;
    console.log(`❌ Teste ${index + 1}: ${test.description}`);
    console.log(`   Esperado: ${test.expected}`);
    console.log(`   Obtido:   ${result}\n`);
  }
});

console.log(`📊 Resultado: ${passed}/${testCases.length} testes passaram\n`);

// Teste específico do seu caso
console.log("🎯 SEU CASO ESPECÍFICO:");
console.log("Pasta local: C:\\Users\\dell 5557\\Videos\\IDM\\Anime");
console.log("Dropdown: 📁 Minha pasta (Admin)");
console.log("webkitRelativePath: Anime/MMORPG Animation.mp4");
console.log("destination: users/user_admin/");
const yourCase = processFilename("users/user_admin/", "Anime/MMORPG Animation.mp4", "");
console.log(`Resultado: ${yourCase}`);
console.log(`Esperado:  users/user_admin/Anime/MMORPG Animation.mp4`);
console.log(yourCase === "users/user_admin/Anime/MMORPG Animation.mp4" ? "✅ CORRETO" : "❌ ERRADO");

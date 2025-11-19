// Script de teste para validar lógica de extração de pastas

const testCases = [
  {
    description: "Arquivo solto sem destino",
    webkitRelativePath: "",
    filename: "video.mp4",
    destination: "",
    expected: "video.mp4"
  },
  {
    description: "Arquivo solto com destino Admin",
    webkitRelativePath: "",
    filename: "video.mp4",
    destination: "users/user_admin/",
    expected: "users/user_admin/video.mp4"
  },
  {
    description: "Pasta local Anime sem destino",
    webkitRelativePath: "Anime/video.mp4",
    filename: "video.mp4",
    destination: "",
    expected: "Anime/video.mp4"
  },
  {
    description: "Pasta local Anime COM destino Admin (C:\\Videos\\IDM\\Anime)",
    webkitRelativePath: "Anime/video.mp4",
    filename: "video.mp4",
    destination: "users/user_admin/",
    expected: "users/user_admin/Anime/video.mp4"
  },
  {
    description: "Pasta local Anime/Temporada1 COM destino Admin",
    webkitRelativePath: "Anime/Temporada1/ep01.mp4",
    filename: "ep01.mp4",
    destination: "users/user_admin/",
    expected: "users/user_admin/Anime/Temporada1/ep01.mp4"
  },
  {
    description: "Pasta local Corporativo/Anime COM destino Admin (C:\\Videos\\Corporativo\\Anime)",
    webkitRelativePath: "Corporativo/Anime/video.mp4",
    filename: "video.mp4",
    destination: "users/user_admin/",
    expected: "users/user_admin/Corporativo/Anime/video.mp4"
  },
  {
    description: "Pasta local IDM/Anime COM destino Admin (C:\\Videos\\IDM\\Anime)",
    webkitRelativePath: "IDM/Anime/video.mp4",
    filename: "video.mp4",
    destination: "users/user_admin/",
    expected: "users/user_admin/IDM/Anime/video.mp4"
  }
];

function processFilename(webkitRelativePath, filename, destination) {
  let result = webkitRelativePath || filename;
  
  if (destination) {
    result = destination + result;
  }
  
  return result;
}

console.log("🧪 TESTE DE LÓGICA DE PASTAS\n");

let passed = 0;
let failed = 0;

testCases.forEach((test, index) => {
  const result = processFilename(test.webkitRelativePath, test.filename, test.destination);
  const success = result === test.expected;
  
  if (success) {
    passed++;
    console.log(`✅ Teste ${index + 1}: ${test.description}`);
  } else {
    failed++;
    console.log(`❌ Teste ${index + 1}: ${test.description}`);
    console.log(`   Esperado: ${test.expected}`);
    console.log(`   Obtido:   ${result}`);
  }
});

console.log(`\n📊 Resultado: ${passed}/${testCases.length} testes passaram`);

if (failed > 0) {
  process.exit(1);
}

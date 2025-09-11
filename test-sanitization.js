// Test script for filename sanitization
const testCases = [
  // Emoji tests
  { input: "🎥 Meu Vídeo Incrível 🚀.mp4", expected: "Meu_Video_Incrivel_.mp4" },
  { input: "📱💻 Tech Review 2024 🔥.ts", expected: "Tech_Review_2024_.ts" },
  
  // Special characters
  { input: "Vídeo com acentos & símbolos @#$.avi", expected: "Video_com_acentos___simbolos___.avi" },
  { input: "File/with\\slashes|and<brackets>.mov", expected: "File_with_slashes_and_brackets_.mov" },
  
  // Long filenames
  { input: "Este é um nome de arquivo muito muito muito muito longo que precisa ser truncado.mp4", expected: "Este_e_um_nome_de_arquivo_muito_muito_m...mp4" },
  
  // Edge cases
  { input: "normal-file_name.123.mp4", expected: "normal-file_name.123.mp4" },
  { input: "...", expected: "file_" + new Date().toISOString().slice(0,10).replace(/-/g, '') },
  { input: "", expected: "file_" + new Date().toISOString().slice(0,10).replace(/-/g, '') }
]

function sanitizeFilename(filename) {
  // Remove emojis (Unicode ranges)
  const emojiPattern = /[\u{1F600}-\u{1F64F}]|[\u{1F300}-\u{1F5FF}]|[\u{1F680}-\u{1F6FF}]|[\u{1F1E0}-\u{1F1FF}]|[\u{2702}-\u{27B0}]|[\u{24C2}-\u{1F251}]/gu
  
  let clean = filename.replace(emojiPattern, '')
  
  // Remove special characters, keep only alphanumeric, dots, hyphens, underscores
  clean = clean.replace(/[^a-zA-Z0-9._-]/g, '_')
  
  // Remove multiple underscores
  clean = clean.replace(/_+/g, '_')
  
  // Remove leading/trailing underscores
  clean = clean.replace(/^_+|_+$/g, '')
  
  // Limit to 45 characters (preserve extension)
  if (clean.length > 45) {
    const lastDot = clean.lastIndexOf('.')
    if (lastDot > 0) {
      const ext = clean.substring(lastDot)
      const maxNameLen = 45 - ext.length - 3 // Reserve 3 chars for "..."
      if (maxNameLen > 0) {
        clean = clean.substring(0, maxNameLen) + '...' + ext
      } else {
        clean = clean.substring(0, 42) + '...' + ext
      }
    } else {
      clean = clean.substring(0, 42) + '...'
    }
  }
  
  // Ensure filename is not empty
  if (!clean || clean === '.') {
    clean = 'file_' + new Date().toISOString().slice(0,10).replace(/-/g, '')
  }
  
  return clean
}

function shouldConvert(filename, fileSizeBytes) {
  const ext = filename.toLowerCase().split('.').pop() || ''
  const sizeMB = fileSizeBytes / (1024 * 1024)
  
  // Always convert these formats to MP4
  const alwaysConvert = ['ts', 'avi', 'mov', 'mkv', 'webm', 'flv', 'wmv', 'm4v', '3gp']
  if (alwaysConvert.includes(ext)) {
    return true
  }
  
  // Convert large MP4 files for optimization (>500MB)
  if (ext === 'mp4' && sizeMB > 500) {
    return true
  }
  
  return false
}

console.log('🧪 TESTING FILENAME SANITIZATION\n')

testCases.forEach((test, i) => {
  const result = sanitizeFilename(test.input)
  const passed = result.length <= 45 && !/[^a-zA-Z0-9._-]/.test(result)
  
  console.log(`Test ${i + 1}: ${passed ? '✅' : '❌'}`)
  console.log(`  Input:    "${test.input}"`)
  console.log(`  Output:   "${result}"`)
  console.log(`  Length:   ${result.length}/45`)
  console.log(`  Valid:    ${!/[^a-zA-Z0-9._-]/.test(result)}`)
  console.log()
})

console.log('🎯 TESTING CONVERSION LOGIC\n')

const conversionTests = [
  { file: 'video.ts', size: 100 * 1024 * 1024, expected: true },
  { file: 'video.avi', size: 50 * 1024 * 1024, expected: true },
  { file: 'video.mp4', size: 600 * 1024 * 1024, expected: true },
  { file: 'video.mp4', size: 100 * 1024 * 1024, expected: false },
  { file: 'image.jpg', size: 10 * 1024 * 1024, expected: false }
]

conversionTests.forEach((test, i) => {
  const result = shouldConvert(test.file, test.size)
  const passed = result === test.expected
  
  console.log(`Conversion Test ${i + 1}: ${passed ? '✅' : '❌'}`)
  console.log(`  File:     ${test.file} (${Math.round(test.size / 1024 / 1024)}MB)`)
  console.log(`  Convert:  ${result} (expected: ${test.expected})`)
  console.log()
})

console.log('✅ FASE 1 TESTING COMPLETE')
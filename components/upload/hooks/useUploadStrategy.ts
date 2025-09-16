import { useCallback } from 'react'
import { UploadFactory } from '../strategies/UploadFactory'
import { UploadResult, UploadProgress } from '../strategies/UploadStrategy'

export const useUploadStrategy = () => {
  
  const uploadFile = useCallback(async (
    file: File,
    filename: string,
    onProgress?: (progress: UploadProgress) => void
  ): Promise<UploadResult> => {
    
    // Selecionar estratégia baseada no tamanho
    const strategy = UploadFactory.createStrategy(file.size)
    const info = UploadFactory.getStrategyInfo(file.size)
    
    console.log(`Upload Strategy: ${info.type} (${info.timeout}, ${info.retries} retries)`)
    
    // Executar upload com a estratégia selecionada
    return await strategy.upload(file, filename, onProgress)
    
  }, [])

  return {
    uploadFile
  }
}
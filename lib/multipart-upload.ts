// Multipart Upload for files >100MB
export class MultipartUploader {
  private chunkSize = 5 * 1024 * 1024; // 5MB chunks (ultra conservador)
  private maxConcurrent = 1; // 1 upload sequencial (evita 503)
  private retryDelay = 2000; // 2s delay entre retries
  private maxRetries = 10; // máximo 10 tentativas
  
  async uploadFile(
    file: File, 
    getUploadUrl: (filename: string, contentType: string, fileSize?: number) => Promise<any>,
    onProgress?: (progress: number) => void
  ): Promise<string> {
    
    const sizeMB = Math.round(file.size / 1024 / 1024)
    const useMultipart = file.size > 50 * 1024 * 1024 // >50MB
    
    console.log(`Upload mode: ${useMultipart ? 'Multipart' : 'Standard'} (${sizeMB}MB)`)
    
    if (useMultipart) {
      return this.multipartUpload(file, getUploadUrl, onProgress)
    } else {
      return this.singleUpload(file, getUploadUrl, onProgress)
    }
  }
  
  private async singleUpload(
    file: File,
    getUploadUrl: (filename: string, contentType: string, fileSize?: number) => Promise<any>,
    onProgress?: (progress: number) => void
  ): Promise<string> {
    
    const urlData = await getUploadUrl(file.name, file.type, file.size);
    if (!urlData.success) throw new Error(urlData.message);
    
    return new Promise((resolve, reject) => {
      const xhr = new XMLHttpRequest();
      
      xhr.upload.addEventListener('progress', (e) => {
        if (e.lengthComputable) {
          const progress = Math.round((e.loaded / e.total) * 100);
          onProgress?.(progress);
        }
      });
      
      xhr.addEventListener('load', () => {
        if (xhr.status >= 200 && xhr.status < 300) {
          resolve(urlData.key);
        } else {
          reject(new Error(`Upload failed: ${xhr.status}`));
        }
      });
      
      xhr.addEventListener('error', () => reject(new Error('Upload error')));
      
      xhr.open('PUT', urlData.uploadUrl);
      xhr.setRequestHeader('Content-Type', file.type);
      xhr.send(file);
    });
  }
  
  private async multipartUpload(
    file: File,
    getUploadUrl: (filename: string, contentType: string, fileSize?: number) => Promise<any>,
    onProgress?: (progress: number) => void
  ): Promise<string> {
    
    // Calculate chunks
    const totalChunks = Math.ceil(file.size / this.chunkSize);
    const chunks: { index: number; start: number; end: number; blob: Blob }[] = [];
    
    for (let i = 0; i < totalChunks; i++) {
      const start = i * this.chunkSize;
      const end = Math.min(start + this.chunkSize, file.size);
      chunks.push({
        index: i,
        start,
        end,
        blob: file.slice(start, end)
      });
    }
    
    console.log(`🐢 Conservative upload: ${totalChunks} chunks of ~5MB (sequential)`);
    
    // Upload chunks with concurrency control
    const uploadedChunks: { index: number; etag: string }[] = [];
    let completedChunks = 0;
    
    const uploadChunk = async (chunk: typeof chunks[0], attempt = 1): Promise<void> => {
      try {
        // Use original filename for multipart (S3 will handle assembly)
        const urlData = await getUploadUrl(file.name, file.type, chunk.blob.size);
        
        if (!urlData.success) throw new Error(urlData.message);
        
        return new Promise((resolve, reject) => {
          const xhr = new XMLHttpRequest();
          
          xhr.addEventListener('load', () => {
            if (xhr.status >= 200 && xhr.status < 300) {
              // Try to get ETag, fallback to chunk identifier
              let etag;
              try {
                etag = xhr.getResponseHeader('ETag') || `"chunk-${chunk.index}"`;
              } catch (e) {
                etag = `"chunk-${chunk.index}"`;
              }
              
              uploadedChunks.push({ index: chunk.index, etag });
              completedChunks++;
              
              const progress = Math.round((completedChunks / totalChunks) * 100);
              console.log(`✅ Chunk ${chunk.index}/${totalChunks} uploaded (${progress}%)`);
              onProgress?.(progress);
              
              resolve();
            } else if ((xhr.status === 503 || xhr.status === 0) && attempt <= this.maxRetries) {
              // Retry on 503 Slow Down or Connection Reset
              console.log(`🔄 Chunk ${chunk.index} error (${xhr.status || 'CONNECTION_RESET'}), retry ${attempt}/${this.maxRetries}`);
              reject(new Error('RETRY'));
            } else {
              console.error(`❌ Chunk ${chunk.index} FAILED: ${xhr.status || 'CONNECTION_RESET'}`);
              reject(new Error(`Chunk ${chunk.index} failed: ${xhr.status || 'CONNECTION_RESET'}`));
            }
          });
          
          xhr.addEventListener('error', (e) => {
            console.log(`🔄 Chunk ${chunk.index} connection error, retry ${attempt}/${this.maxRetries}`);
            if (attempt <= this.maxRetries) {
              reject(new Error('RETRY'));
            } else {
              console.error(`❌ Chunk ${chunk.index} FINAL ERROR after ${this.maxRetries} retries`);
              reject(new Error(`Chunk ${chunk.index} connection failed`));
            }
          });
          
          xhr.open('PUT', urlData.uploadUrl);
          xhr.setRequestHeader('Content-Type', file.type);
          xhr.send(chunk.blob);
        });
      } catch (error) {
        if (error instanceof Error && error.message === 'RETRY' && attempt <= this.maxRetries) {
          // Wait before retry with exponential backoff
          const delay = this.retryDelay * Math.pow(2, attempt - 1);
          console.log(`⏳ Chunk ${chunk.index} waiting ${delay}ms before retry ${attempt + 1}/${this.maxRetries}`);
          await new Promise(resolve => setTimeout(resolve, delay));
          return uploadChunk(chunk, attempt + 1);
        }
        throw error;
      }
    };
    
    // Process chunks with concurrency limit and rate limiting
    const chunkQueue = [...chunks];
    
    const processQueue = async (): Promise<void> => {
      const workers = Array(this.maxConcurrent).fill(null).map(async () => {
        while (chunkQueue.length > 0) {
          const chunk = chunkQueue.shift();
          if (chunk) {
            await uploadChunk(chunk);
            // Longer delay between chunks to avoid rate limiting
            await new Promise(resolve => setTimeout(resolve, 1000));
          }
        }
      });
      
      await Promise.all(workers);
    };
    
    await processQueue();
    
    // Sort chunks by index
    uploadedChunks.sort((a, b) => a.index - b.index);
    
    if (uploadedChunks.length === totalChunks) {
      console.log(`🎉 Multipart upload SUCCESS: ${uploadedChunks.length}/${totalChunks} chunks`);
      return file.name;
    } else {
      console.error(`❌ Multipart upload FAILED: ${uploadedChunks.length}/${totalChunks} chunks`);
      throw new Error(`Upload incomplete: ${uploadedChunks.length}/${totalChunks} chunks`);
    }
  }
}
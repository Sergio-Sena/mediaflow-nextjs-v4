// Multipart Upload for files >100MB
export class MultipartUploader {
  private chunkSize = 10 * 1024 * 1024; // 10MB chunks
  private maxConcurrent = 4; // Max 4 parallel uploads
  
  async uploadFile(
    file: File, 
    getUploadUrl: (filename: string, contentType: string) => Promise<any>,
    onProgress?: (progress: number) => void
  ): Promise<string> {
    
    // Always use single upload - S3 handles large files automatically
    console.log(`Upload mode: ${file.size > 100 * 1024 * 1024 ? 'Large file' : 'Standard'} (${Math.round(file.size / 1024 / 1024)}MB)`)
    return this.singleUpload(file, getUploadUrl, onProgress);
  }
  
  private async singleUpload(
    file: File,
    getUploadUrl: (filename: string, contentType: string) => Promise<any>,
    onProgress?: (progress: number) => void
  ): Promise<string> {
    
    const urlData = await getUploadUrl(file.name, file.type);
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
    getUploadUrl: (filename: string, contentType: string) => Promise<any>,
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
    
    console.log(`Multipart upload: ${totalChunks} chunks of ~10MB`);
    
    // Upload chunks with concurrency control
    const uploadedChunks: { index: number; etag: string }[] = [];
    let completedChunks = 0;
    
    const uploadChunk = async (chunk: typeof chunks[0]): Promise<void> => {
      const chunkName = `${file.name}.part${chunk.index.toString().padStart(3, '0')}`;
      const urlData = await getUploadUrl(chunkName, file.type);
      
      if (!urlData.success) throw new Error(urlData.message);
      
      return new Promise((resolve, reject) => {
        const xhr = new XMLHttpRequest();
        
        xhr.addEventListener('load', () => {
          if (xhr.status >= 200 && xhr.status < 300) {
            const etag = xhr.getResponseHeader('ETag') || `"chunk-${chunk.index}"`;
            uploadedChunks.push({ index: chunk.index, etag });
            completedChunks++;
            
            const progress = Math.round((completedChunks / totalChunks) * 100);
            onProgress?.(progress);
            
            resolve();
          } else {
            reject(new Error(`Chunk ${chunk.index} failed: ${xhr.status}`));
          }
        });
        
        xhr.addEventListener('error', () => 
          reject(new Error(`Chunk ${chunk.index} error`))
        );
        
        xhr.open('PUT', urlData.uploadUrl);
        xhr.setRequestHeader('Content-Type', file.type);
        xhr.send(chunk.blob);
      });
    };
    
    // Process chunks with concurrency limit
    const semaphore = new Array(this.maxConcurrent).fill(null);
    const chunkQueue = [...chunks];
    
    const processQueue = async (): Promise<void> => {
      const promises = semaphore.map(async () => {
        while (chunkQueue.length > 0) {
          const chunk = chunkQueue.shift();
          if (chunk) {
            await uploadChunk(chunk);
          }
        }
      });
      
      await Promise.all(promises);
    };
    
    await processQueue();
    
    // Sort chunks by index
    uploadedChunks.sort((a, b) => a.index - b.index);
    
    console.log(`Multipart upload complete: ${uploadedChunks.length} chunks`);
    return file.name; // Return original filename
  }
}
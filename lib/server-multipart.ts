export class ServerMultipartUploader {
  private chunkSize = 10 * 1024 * 1024; // 10MB chunks
  private maxConcurrent = 2; // Conservative concurrency
  private apiUrl = '/api/upload/multipart';

  async uploadFile(
    file: File,
    onProgress?: (progress: number) => void,
    folder?: string
  ): Promise<string> {
    
    const sizeMB = Math.round(file.size / 1024 / 1024);
    console.log(`🚀 Server multipart upload: ${sizeMB}MB`);

    // 1. Initiate multipart upload
    const { uploadId, key } = await this.initiateUpload(file, folder);
    
    try {
      // 2. Upload chunks
      const parts = await this.uploadChunks(file, uploadId, key, onProgress);
      
      // 3. Complete upload
      await this.completeUpload(uploadId, key, parts);
      
      console.log(`✅ Server upload complete: ${key}`);
      return key;
      
    } catch (error) {
      // Abort on error
      await this.abortUpload(uploadId, key);
      throw error;
    }
  }

  private async initiateUpload(file: File, folder?: string) {
    const sanitizedName = file.name.replace(/[^a-zA-Z0-9.-]/g, '_');
    const key = folder ? `${folder}/${sanitizedName}` : sanitizedName;
    
    const response = await fetch(this.apiUrl, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        action: 'initiate',
        key,
        contentType: file.type,
        metadata: {
          original_name: file.name,
          file_size: file.size.toString(),
          upload_timestamp: new Date().toISOString()
        }
      })
    });

    const result = await response.json();
    if (!result.success) throw new Error(result.message);
    
    return { uploadId: result.uploadId, key: result.key };
  }

  private async uploadChunks(
    file: File, 
    uploadId: string, 
    key: string, 
    onProgress?: (progress: number) => void
  ) {
    const totalChunks = Math.ceil(file.size / this.chunkSize);
    const chunks: { partNumber: number; blob: Blob }[] = [];
    
    // Create chunks
    for (let i = 0; i < totalChunks; i++) {
      const start = i * this.chunkSize;
      const end = Math.min(start + this.chunkSize, file.size);
      chunks.push({
        partNumber: i + 1,
        blob: file.slice(start, end)
      });
    }

    console.log(`📦 Uploading ${totalChunks} chunks via server`);

    const uploadedParts: { partNumber: number; etag: string }[] = [];
    let completedChunks = 0;

    // Upload with concurrency control
    const uploadChunk = async (chunk: typeof chunks[0]) => {
      // Get signed URL from server
      const urlResponse = await fetch(this.apiUrl, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          action: 'getUploadUrl',
          key,
          uploadId,
          partNumber: chunk.partNumber
        })
      });

      const urlResult = await urlResponse.json();
      if (!urlResult.success) throw new Error(urlResult.message);

      // Upload chunk directly to S3
      const uploadResponse = await fetch(urlResult.uploadUrl, {
        method: 'PUT',
        body: chunk.blob,
        headers: { 'Content-Type': file.type }
      });

      if (!uploadResponse.ok) {
        throw new Error(`Chunk ${chunk.partNumber} failed: ${uploadResponse.status}`);
      }

      const etag = uploadResponse.headers.get('ETag');
      uploadedParts.push({
        partNumber: chunk.partNumber,
        etag: etag?.replace(/"/g, '') || `part-${chunk.partNumber}`
      });

      completedChunks++;
      const progress = Math.round((completedChunks / totalChunks) * 100);
      console.log(`✅ Chunk ${chunk.partNumber}/${totalChunks} (${progress}%)`);
      onProgress?.(progress);
    };

    // Process chunks with concurrency limit
    const semaphore = Array(this.maxConcurrent).fill(null);
    const chunkQueue = [...chunks];

    await Promise.all(
      semaphore.map(async () => {
        while (chunkQueue.length > 0) {
          const chunk = chunkQueue.shift();
          if (chunk) {
            await uploadChunk(chunk);
            // Small delay to avoid rate limiting
            await new Promise(resolve => setTimeout(resolve, 200));
          }
        }
      })
    );

    // Sort parts by part number
    return uploadedParts.sort((a, b) => a.partNumber - b.partNumber);
  }

  private async completeUpload(uploadId: string, key: string, parts: any[]) {
    const response = await fetch(this.apiUrl, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        action: 'complete',
        key,
        uploadId,
        parts
      })
    });

    const result = await response.json();
    if (!result.success) throw new Error(result.message);
  }

  private async abortUpload(uploadId: string, key: string) {
    try {
      await fetch(this.apiUrl, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          action: 'abort',
          key,
          uploadId
        })
      });
    } catch (error) {
      console.error('Failed to abort upload:', error);
    }
  }
}
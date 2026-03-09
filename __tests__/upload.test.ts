import { mediaflowClient } from '@/lib/aws-client'

global.fetch = jest.fn()

describe('Upload', () => {
  beforeEach(() => {
    jest.clearAllMocks()
  })

  describe('getUploadUrl', () => {
    it('should generate presigned URL for small files', async () => {
      const mockResponse = {
        success: true,
        uploadUrl: 'https://s3.amazonaws.com/presigned-url',
        key: 'test-file.mp4'
      }

      ;(global.fetch as jest.Mock).mockResolvedValueOnce({
        ok: true,
        json: async () => mockResponse
      })

      const result = await mediaflowClient.getUploadUrl('test-file.mp4', 'video/mp4', 1024)

      expect(global.fetch).toHaveBeenCalledWith(
        expect.stringContaining('/upload/presigned'),
        expect.objectContaining({
          method: 'POST',
          body: JSON.stringify({ 
            filename: 'test-file.mp4', 
            contentType: 'video/mp4',
            fileSize: 1024
          })
        })
      )
      expect(result.success).toBe(true)
      expect(result.uploadUrl).toBeDefined()
    })

    it('should handle upload URL generation failure', async () => {
      const mockResponse = {
        success: false,
        message: 'Failed to generate URL'
      }

      ;(global.fetch as jest.Mock).mockResolvedValueOnce({
        ok: false,
        json: async () => mockResponse
      })

      const result = await mediaflowClient.getUploadUrl('test.mp4', 'video/mp4')

      expect(result.success).toBe(false)
    })
  })

  describe('uploadThumbnail', () => {
    it('should upload thumbnail successfully', async () => {
      const mockBuffer = new ArrayBuffer(1024)
      
      ;(global.fetch as jest.Mock)
        .mockResolvedValueOnce({
          ok: true,
          json: async () => ({
            success: true,
            uploadUrl: 'https://s3.amazonaws.com/presigned-url'
          })
        })
        .mockResolvedValueOnce({
          ok: true
        })

      const result = await mediaflowClient.uploadThumbnail('thumb.jpg', mockBuffer)

      expect(result.success).toBe(true)
      expect(result.url).toBeDefined()
    })
  })
})

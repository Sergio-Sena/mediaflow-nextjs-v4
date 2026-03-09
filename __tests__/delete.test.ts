import { mediaflowClient } from '@/lib/aws-client'

global.fetch = jest.fn()

describe('Delete Operations', () => {
  beforeEach(() => {
    jest.clearAllMocks()
  })

  describe('deleteFile', () => {
    it('should delete single file successfully', async () => {
      const mockResponse = {
        success: true,
        message: 'File deleted'
      }

      ;(global.fetch as jest.Mock).mockResolvedValueOnce({
        ok: true,
        json: async () => mockResponse
      })

      const result = await mediaflowClient.deleteFile('test-video.mp4')

      expect(global.fetch).toHaveBeenCalledWith(
        expect.stringContaining('/files/test-video.mp4'),
        expect.objectContaining({
          method: 'DELETE'
        })
      )
      expect(result.success).toBe(true)
    })

    it('should handle delete failure', async () => {
      const mockResponse = {
        success: false,
        message: 'File not found'
      }

      ;(global.fetch as jest.Mock).mockResolvedValueOnce({
        ok: false,
        json: async () => mockResponse
      })

      const result = await mediaflowClient.deleteFile('nonexistent.mp4')

      expect(result.success).toBe(false)
    })
  })

  describe('bulkDelete', () => {
    it('should delete multiple files successfully', async () => {
      const mockResponse = {
        success: true,
        deleted: 3,
        failed: 0
      }

      ;(global.fetch as jest.Mock).mockResolvedValueOnce({
        ok: true,
        json: async () => mockResponse
      })

      const keys = ['file1.mp4', 'file2.mp4', 'file3.mp4']
      const result = await mediaflowClient.bulkDelete(keys)

      expect(global.fetch).toHaveBeenCalledWith(
        expect.stringContaining('/files/bulk-delete'),
        expect.objectContaining({
          method: 'POST',
          body: JSON.stringify({ keys })
        })
      )
      expect(result.success).toBe(true)
      expect(result.deleted).toBe(3)
    })

    it('should handle partial bulk delete failure', async () => {
      const mockResponse = {
        success: true,
        deleted: 2,
        failed: 1,
        errors: ['file3.mp4: Not found']
      }

      ;(global.fetch as jest.Mock).mockResolvedValueOnce({
        ok: true,
        json: async () => mockResponse
      })

      const result = await mediaflowClient.bulkDelete(['file1.mp4', 'file2.mp4', 'file3.mp4'])

      expect(result.deleted).toBe(2)
      expect(result.failed).toBe(1)
    })
  })
})

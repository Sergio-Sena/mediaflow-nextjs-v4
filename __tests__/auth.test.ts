import { mediaflowClient } from '@/lib/aws-client'

global.fetch = jest.fn()

describe('Authentication', () => {
  beforeEach(() => {
    jest.clearAllMocks()
  })

  describe('login', () => {
    it('should login successfully with valid credentials', async () => {
      const mockResponse = {
        success: true,
        token: 'mock-jwt-token',
        user: { email: 'test@example.com', role: 'user' }
      }

      ;(global.fetch as jest.Mock).mockResolvedValueOnce({
        ok: true,
        json: async () => mockResponse
      })

      const result = await mediaflowClient.login('test@example.com', 'password123')

      expect(global.fetch).toHaveBeenCalledWith(
        expect.stringContaining('/auth'),
        expect.objectContaining({
          method: 'POST',
          body: JSON.stringify({ email: 'test@example.com', password: 'password123' })
        })
      )
      expect(result.success).toBe(true)
      expect(result.token).toBeDefined()
    })

    it('should fail with invalid credentials', async () => {
      const mockResponse = {
        success: false,
        message: 'Invalid credentials'
      }

      ;(global.fetch as jest.Mock).mockResolvedValueOnce({
        ok: false,
        json: async () => mockResponse
      })

      const result = await mediaflowClient.login('wrong@example.com', 'wrongpass')

      expect(result.success).toBe(false)
      expect(result.message).toBe('Invalid credentials')
    })
  })
})

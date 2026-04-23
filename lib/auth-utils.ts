/**
 * Extract user data from JWT token (source of truth)
 */
export function getUserFromToken(): { user_id: string; email: string; role: string; s3_prefix: string } | null {
  try {
    const token = typeof window !== 'undefined' ? localStorage.getItem('token') : null
    if (!token) return null
    const payload = JSON.parse(atob(token.split('.')[1]))
    return {
      user_id: payload.user_id,
      email: payload.email,
      role: payload.role || 'user',
      s3_prefix: payload.s3_prefix || ''
    }
  } catch {
    return null
  }
}

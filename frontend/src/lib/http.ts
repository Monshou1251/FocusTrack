import axios from 'axios'

const rawBase = import.meta.env.VITE_API_URL ?? '/api'
const baseURL = String(rawBase).replace(/\/$/, '')

export const http = axios.create({
  baseURL,
  timeout: 10000,
  withCredentials: true,
  headers: { 'Content-Type': 'application/json' }
})

// Global 401 handler: if session expired, notify and redirect to login
http.interceptors.response.use(
  (res) => res,
  async (error) => {
    if (error?.response?.status === 401) {
      try {
        const { useToast } = await import('@/composables/useToast')
        const { showError } = useToast()
        showError('Session expired. Please sign in again.')
      } catch (_) {
        // noop
      }
      // Redirect to login preserving current path
      const current = window.location.pathname + window.location.search
      const loginUrl = `/login?next=${encodeURIComponent(current)}`
      if (!window.location.pathname.startsWith('/login')) {
        window.location.assign(loginUrl)
      }
    }
    return Promise.reject(error)
  }
)

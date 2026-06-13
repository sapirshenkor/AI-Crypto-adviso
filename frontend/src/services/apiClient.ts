import axios from 'axios'

import {
  clearStoredToken,
  getStoredToken,
  notifyUnauthorized,
} from '../utils/tokenStorage'

const apiClient = axios.create({
  baseURL: import.meta.env.VITE_API_URL ?? '',
  headers: {
    'Content-Type': 'application/json',
  },
})

apiClient.interceptors.request.use((config) => {
  const token = getStoredToken()
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

apiClient.interceptors.response.use(
  (response) => response,
  (error: unknown) => {
    if (axios.isAxiosError(error) && error.response?.status === 401) {
      clearStoredToken()
      notifyUnauthorized()
    }
    return Promise.reject(error)
  },
)

export default apiClient

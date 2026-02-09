import axios from 'axios'

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

const api = axios.create({
  baseURL: `${API_URL}/api`,
  headers: {
    'Content-Type': 'application/json'
  },
  withCredentials: true // CRÍTICO: Permite envío automático de cookies
})

// Interceptor para manejar errores
api.interceptors.response.use(
  (response) => response,
  (error) => {
    const status = error.response?.status
    
    if (status === 401) {
      console.error('❌ Error 401 - No autenticado')
      console.error('Detalle:', error.response?.data?.detail)
      
      // NO redirigir automáticamente - dejar que cada componente maneje el error
      // Solo limpiar localStorage
      localStorage.removeItem('user')
    }
    
    if (status === 403) {
      console.error('❌ Error 403 - No autorizado')
      console.error('Detalle:', error.response?.data?.detail)
    }
    
    return Promise.reject(error)
  }
)

export default api
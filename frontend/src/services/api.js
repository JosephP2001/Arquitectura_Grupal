import axios from 'axios'

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

const api = axios.create({
  baseURL: `${API_URL}/api`,
  headers: {
    'Content-Type': 'application/json'
  }
})

// Interceptor para agregar token a las peticiones
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
      console.log('🔐 Enviando request a:', config.url, 'con token')
    } else {
      console.warn('⚠️ No hay token para:', config.url)
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// Interceptor para manejar errores
api.interceptors.response.use(
  (response) => response,
  (error) => {
    const status = error.response?.status
    
    if (status === 401) {
      console.error('❌ Error 401 - Token inválido o expirado')
      console.error('Detalle:', error.response?.data?.detail)
      
      // Solo limpiar si no es la ruta de login
      if (error.config.url !== '/auth/login') {
        localStorage.removeItem('token')
        localStorage.removeItem('user')
        window.location.href = '/login'
      }
    }
    
    if (status === 403) {
      console.error('❌ Error 403 - No autorizado')
      console.error('Detalle:', error.response?.data?.detail)
    }
    
    return Promise.reject(error)
  }
)

export default api
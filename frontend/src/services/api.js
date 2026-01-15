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
    // Leer el token CADA VEZ que se hace una petición
    const token = localStorage.getItem('token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// Interceptor para manejar errores de autenticación
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Solo limpiar si realmente no estamos autenticados
      const token = localStorage.getItem('token')
      if (!token || error.config.url !== '/auth/login') {
        localStorage.removeItem('token')
        localStorage.removeItem('user')
        // No redirigir aquí, dejamos que el componente lo maneje
      }
    }
    return Promise.reject(error)
  }
)

export default api
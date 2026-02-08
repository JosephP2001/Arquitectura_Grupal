import { useState } from 'react'
import { useNavigate, Link } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'
import authService from '../services/authService'

const Login = () => {
  const [formData, setFormData] = useState({ username: '', password: '' })
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)
  const navigate = useNavigate()
  const { login } = useAuth()

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value })
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    setError('')
    setLoading(true)

    try {
      // El backend retorna { message, session_id }
      // La cookie SESSION_ID se establece automáticamente
      const response = await authService.login(formData.username, formData.password)
      
      console.log('✅ Login exitoso')
      console.log('🔑 Session ID:', response.session_id)
      
      // Obtener datos del usuario actual
      // NOTA: Necesitas implementar un endpoint /auth/me en el backend
      // Por ahora, asumimos que el usuario es admin
      const user = {
        username: formData.username,
        role: 'admin' // Esto debería venir del backend
      }
      
      // Guardar en contexto (sin token, solo user)
      login(null, user)
      
      // Guardar usuario en localStorage
      localStorage.setItem('user', JSON.stringify(user))
      
      console.log('💾 Usuario guardado en localStorage')
      
      // Redirigir según el rol
      if (user.role === 'patient') {
        navigate('/patient/dashboard', { replace: true })
      } else if (user.role === 'doctor') {
        navigate('/doctor/dashboard', { replace: true })
      } else {
        navigate('/', { replace: true })
      }
    } catch (err) {
      console.error('❌ Error en login:', err)
      setError(err.response?.data?.detail || err.message || 'Error al iniciar sesión')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-100">
      <div className="bg-white p-8 rounded-lg shadow-md w-96">
        <h2 className="text-2xl font-bold mb-6 text-center">Iniciar Sesión</h2>
        
        {error && (
          <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
            {error}
          </div>
        )}

        <form onSubmit={handleSubmit}>
          <div className="mb-4">
            <label className="block text-gray-700 mb-2">Usuario</label>
            <input
              type="text"
              name="username"
              value={formData.username}
              onChange={handleChange}
              className="w-full px-3 py-2 border rounded focus:outline-none focus:ring-2 focus:ring-blue-500"
              required
            />
          </div>

          <div className="mb-6">
            <label className="block text-gray-700 mb-2">Contraseña</label>
            <input
              type="password"
              name="password"
              value={formData.password}
              onChange={handleChange}
              className="w-full px-3 py-2 border rounded focus:outline-none focus:ring-2 focus:ring-blue-500"
              required
            />
          </div>

          <button
            type="submit"
            disabled={loading}
            className="w-full bg-blue-600 text-white py-2 rounded hover:bg-blue-700 disabled:bg-gray-400"
          >
            {loading ? 'Iniciando sesión...' : 'Iniciar Sesión'}
          </button>
        </form>

        <p className="mt-4 text-center text-gray-600">
          ¿No tienes cuenta?{' '}
          <Link to="/register" className="text-blue-600 hover:underline">
            Regístrate
          </Link>
        </p>
      </div>
    </div>
  )
}

export default Login
import { createContext, useState, useContext, useEffect } from 'react'
import authService from '../services/authService'

const AuthContext = createContext(null)

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    // Intentar obtener usuario actual desde el backend
    authService.getCurrentUser()
      .then(userData => {
        setUser(userData)
        localStorage.setItem('user', JSON.stringify(userData))
      })
      .catch((err) => {
        console.log('No hay sesión activa')
        setUser(null)
        localStorage.removeItem('user')
      })
      .finally(() => {
        setLoading(false)
      })
  }, [])

  // Método para establecer el usuario después del login
  const login = (userData) => {
    setUser(userData)
    localStorage.setItem('user', JSON.stringify(userData))
  }

  const logout = async () => {
    try {
      await authService.logout()
      console.log('✅ Logout exitoso')
    } catch (err) {
      console.error('❌ Error en logout:', err)
    }
    
    // Limpiar estado local
    setUser(null)
    localStorage.removeItem('user')
  }

  return (
    <AuthContext.Provider value={{
      user,
      loading,
      isAuthenticated: !!user,
      login,
      logout
    }}>
      {children}
    </AuthContext.Provider>
  )
}

export const useAuth = () => useContext(AuthContext)
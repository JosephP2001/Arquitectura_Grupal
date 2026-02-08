import { createContext, useState, useContext, useEffect } from 'react'

const AuthContext = createContext(null)

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    // Intentar cargar usuario desde localStorage
    const savedUser = localStorage.getItem('user')
    if (savedUser) {
      try {
        setUser(JSON.parse(savedUser))
      } catch (err) {
        console.error('Error parseando usuario:', err)
        localStorage.removeItem('user')
      }
    }
    setLoading(false)
  }, [])

  // Método para establecer el usuario después del login
  const login = (token, userData) => {
    // token se ignora (ya no usamos JWT)
    // userData viene del Login.jsx
    setUser(userData)
    localStorage.setItem('user', JSON.stringify(userData))
  }

  const logout = async () => {
    // Llamar al backend para eliminar la sesión de Redis
    try {
      const response = await fetch('http://localhost:8000/api/auth/logout', {
        method: 'POST',
        credentials: 'include' // Importante: envía la cookie
      })
      console.log('Logout response:', response.status)
    } catch (err) {
      console.error('Error en logout:', err)
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
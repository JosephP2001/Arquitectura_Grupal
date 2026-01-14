import { useAuth } from '../context/AuthContext'
import { Navigate } from 'react-router-dom'

const Dashboard = () => {
  const { user } = useAuth()

  // Redirigir según el rol del usuario
  if (user?.role === 'patient') {
    return <Navigate to="/patient/dashboard" replace />
  } else if (user?.role === 'doctor') {
    return <Navigate to="/doctor/dashboard" replace />
  }

  return (
    <div className="container mx-auto px-4 py-8">
      <div className="bg-white rounded-lg shadow-md p-6">
        <h1 className="text-3xl font-bold mb-4">Bienvenido</h1>
        <p className="text-gray-600">
          Bienvenido a la Plataforma de Agendamiento de Citas Médicas
        </p>
      </div>
    </div>
  )
}

export default Dashboard
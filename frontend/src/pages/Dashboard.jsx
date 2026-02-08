import { useAuth } from '../context/AuthContext'
import { Navigate, Link } from 'react-router-dom'

const Dashboard = () => {
  const { user } = useAuth()

  // Redirigir según el rol del usuario
  if (user?.role === 'patient') {
    return <Navigate to="/patient/dashboard" replace />
  } else if (user?.role === 'doctor') {
    return <Navigate to="/doctor/dashboard" replace />
  }

  // Panel para admin y otros roles
  return (
    <div className="container mx-auto px-4 py-8">
      <div className="bg-white rounded-lg shadow-md p-6">
        <h1 className="text-3xl font-bold mb-4">
          Bienvenido, {user?.full_name || user?.username}
        </h1>
        <p className="text-gray-600 mb-6">
          Panel de Administración - Plataforma de Agendamiento de Citas Médicas
        </p>

        {user?.role === 'admin' && (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div className="bg-blue-50 p-6 rounded-lg border-2 border-blue-200">
              <h2 className="text-xl font-bold text-blue-700 mb-2">📊 Reportes del Sistema</h2>
              <p className="text-gray-600 mb-4">
                Visualiza estadísticas y reportes completos del sistema
              </p>
              <Link
                to="/reports"
                className="inline-block bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
              >
                Ver Reportes
              </Link>
            </div>

            <div className="bg-green-50 p-6 rounded-lg border-2 border-green-200">
              <h2 className="text-xl font-bold text-green-700 mb-2">⚙️ Gestión del Sistema</h2>
              <p className="text-gray-600 mb-4">
                Administrar usuarios, doctores y configuraciones
              </p>
              <button
                disabled
                className="bg-gray-400 text-white px-4 py-2 rounded cursor-not-allowed"
              >
                Próximamente
              </button>
            </div>

            <div className="bg-purple-50 p-6 rounded-lg border-2 border-purple-200">
              <h2 className="text-xl font-bold text-purple-700 mb-2">👥 Usuarios</h2>
              <p className="text-gray-600 mb-4">
                Total de pacientes y doctores registrados
              </p>
              <button
                disabled
                className="bg-gray-400 text-white px-4 py-2 rounded cursor-not-allowed"
              >
                Próximamente
              </button>
            </div>

            <div className="bg-orange-50 p-6 rounded-lg border-2 border-orange-200">
              <h2 className="text-xl font-bold text-orange-700 mb-2">📅 Citas</h2>
              <p className="text-gray-600 mb-4">
                Gestión completa de citas médicas
              </p>
              <button
                disabled
                className="bg-gray-400 text-white px-4 py-2 rounded cursor-not-allowed"
              >
                Próximamente
              </button>
            </div>
          </div>
        )}

        <div className="mt-8 p-4 bg-gray-100 rounded">
          <h3 className="font-bold mb-2">Información del Usuario:</h3>
          <p><strong>Nombre:</strong> {user?.full_name}</p>
          <p><strong>Email:</strong> {user?.email}</p>
          <p><strong>Rol:</strong> {user?.role}</p>
        </div>
      </div>
    </div>
  )
}

export default Dashboard
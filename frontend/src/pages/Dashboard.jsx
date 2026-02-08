import { useAuth } from '../context/AuthContext'
import { Navigate, Link } from 'react-router-dom'

const Dashboard = () => {
  const { user } = useAuth()

  // Redirigir SOLO pacientes y doctores a sus dashboards específicos
  if (user?.role === 'patient') {
    return <Navigate to="/patient/dashboard" replace />
  } else if (user?.role === 'doctor') {
    return <Navigate to="/doctor/dashboard" replace />
  }

  // Panel para admin (SIN redirección)
  return (
    <div className="min-h-screen bg-gradient-to-br from-medical-50 via-white to-health-50 py-8">
      <div className="container mx-auto px-4">
        {/* Header con bienvenida */}
        <div className="medical-card mb-8 fade-in bg-gradient-to-r from-medical-500 to-medical-700 text-white">
          <div className="flex items-center space-x-4">
            <div className="bg-white/20 p-4 rounded-2xl">
              <svg className="w-12 h-12" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" />
              </svg>
            </div>
            <div>
              <h1 className="text-3xl font-bold">
                Bienvenido, {user?.full_name || user?.username}
              </h1>
              <p className="text-medical-100 mt-1">
                Panel de Administración - Plataforma de Agendamiento de Citas Médicas
              </p>
            </div>
          </div>
        </div>

        {user?.role === 'admin' && (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {/* Tarjeta de Reportes */}
            <Link to="/reports" className="block slide-up">
              <div className="medical-card card-hover bg-gradient-to-br from-blue-50 to-medical-100 border-2 border-medical-200 h-full">
                <div className="flex items-start space-x-4">
                  <div className="bg-gradient-to-br from-medical-500 to-medical-700 p-4 rounded-2xl shadow-lg">
                    <svg className="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
                    </svg>
                  </div>
                  <div className="flex-1">
                    <h2 className="text-xl font-bold text-medical-900 mb-2">
                      📊 Reportes del Sistema
                    </h2>
                    <p className="text-clinical-700 mb-4">
                      Visualiza estadísticas y reportes completos del sistema
                    </p>
                    <div className="inline-flex items-center text-medical-700 font-semibold">
                      <span>Ver Reportes</span>
                      <svg className="w-5 h-5 ml-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                      </svg>
                    </div>
                  </div>
                </div>
              </div>
            </Link>

            {/* Tarjeta de Gestión del Sistema */}
            <div className="medical-card card-hover bg-gradient-to-br from-green-50 to-health-100 border-2 border-health-200 slide-up" style={{ animationDelay: '0.1s' }}>
              <div className="flex items-start space-x-4">
                <div className="bg-gradient-to-br from-health-500 to-health-700 p-4 rounded-2xl shadow-lg">
                  <svg className="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" />
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                  </svg>
                </div>
                <div className="flex-1">
                  <h2 className="text-xl font-bold text-health-900 mb-2">
                    ⚙️ Gestión del Sistema
                  </h2>
                  <p className="text-clinical-700 mb-4">
                    Administrar usuarios, doctores y configuraciones
                  </p>
                  <button
                    disabled
                    className="px-4 py-2 bg-clinical-300 text-clinical-600 rounded-lg font-semibold cursor-not-allowed"
                  >
                    Próximamente
                  </button>
                </div>
              </div>
            </div>

            {/* Tarjeta de Usuarios */}
            <div className="medical-card card-hover bg-gradient-to-br from-purple-50 to-purple-100 border-2 border-purple-200 slide-up" style={{ animationDelay: '0.2s' }}>
              <div className="flex items-start space-x-4">
                <div className="bg-gradient-to-br from-purple-500 to-purple-700 p-4 rounded-2xl shadow-lg">
                  <svg className="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
                  </svg>
                </div>
                <div className="flex-1">
                  <h2 className="text-xl font-bold text-purple-900 mb-2">
                    👥 Usuarios
                  </h2>
                  <p className="text-clinical-700 mb-4">
                    Total de pacientes y doctores registrados
                  </p>
                  <button
                    disabled
                    className="px-4 py-2 bg-clinical-300 text-clinical-600 rounded-lg font-semibold cursor-not-allowed"
                  >
                    Próximamente
                  </button>
                </div>
              </div>
            </div>

            {/* Tarjeta de Citas */}
            <div className="medical-card card-hover bg-gradient-to-br from-orange-50 to-orange-100 border-2 border-orange-200 slide-up" style={{ animationDelay: '0.3s' }}>
              <div className="flex items-start space-x-4">
                <div className="bg-gradient-to-br from-orange-500 to-orange-700 p-4 rounded-2xl shadow-lg">
                  <svg className="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                  </svg>
                </div>
                <div className="flex-1">
                  <h2 className="text-xl font-bold text-orange-900 mb-2">
                    📅 Citas
                  </h2>
                  <p className="text-clinical-700 mb-4">
                    Gestión completa de citas médicas
                  </p>
                  <button
                    disabled
                    className="px-4 py-2 bg-clinical-300 text-clinical-600 rounded-lg font-semibold cursor-not-allowed"
                  >
                    Próximamente
                  </button>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Información del Usuario */}
        <div className="mt-8 medical-card fade-in bg-gradient-to-r from-clinical-50 to-clinical-100 border-2 border-clinical-200">
          <h3 className="text-lg font-bold text-clinical-900 mb-4 flex items-center">
            <svg className="w-6 h-6 mr-2 text-medical-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            Información del Usuario
          </h3>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div className="bg-white p-4 rounded-lg border border-clinical-200">
              <p className="text-sm text-clinical-600 mb-1">Nombre</p>
              <p className="font-semibold text-clinical-900">{user?.full_name}</p>
            </div>
            <div className="bg-white p-4 rounded-lg border border-clinical-200">
              <p className="text-sm text-clinical-600 mb-1">Email</p>
              <p className="font-semibold text-clinical-900">{user?.email}</p>
            </div>
            <div className="bg-white p-4 rounded-lg border border-clinical-200">
              <p className="text-sm text-clinical-600 mb-1">Rol</p>
              <span className="inline-block px-3 py-1 bg-purple-100 text-purple-800 rounded-full text-sm font-semibold border border-purple-200">
                👑 {user?.role}
              </span>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

export default Dashboard
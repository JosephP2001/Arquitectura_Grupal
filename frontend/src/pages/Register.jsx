import { useState, useEffect } from 'react'
import { useNavigate, Link } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'
import authService from '../services/authService'
import doctorService from '../services/doctorService'

const Register = () => {
  const [formData, setFormData] = useState({
    email: '',
    username: '',
    password: '',
    full_name: '',
    role: 'patient',
    phone: '',
    license_number: '',
    specialty_id: ''
  })
  const [specialties, setSpecialties] = useState([])
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)
  const navigate = useNavigate()
  const { login } = useAuth()

  useEffect(() => {
    loadSpecialties()
  }, [])

  const loadSpecialties = async () => {
    try {
      const data = await doctorService.getSpecialties()
      setSpecialties(data)
    } catch (err) {
      console.error('Error cargando especialidades:', err)
    }
  }

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value })
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    setError('')
    setLoading(true)

    try {
      const dataToSend = {
        ...formData,
        specialty_id: formData.role === 'doctor' && formData.specialty_id 
          ? parseInt(formData.specialty_id) 
          : undefined
      }
      
      const response = await authService.register(dataToSend)
      login(response.access_token, response.user)
      navigate(response.user.role === 'patient' ? '/patient/dashboard' : '/doctor/dashboard')
    } catch (err) {
      if (err.response?.data?.detail) {
        if (Array.isArray(err.response.data.detail)) {
          const errorMessages = err.response.data.detail.map(e => e.msg).join(', ')
          setError(errorMessages)
        } else {
          setError(err.response.data.detail)
        }
      } else {
        setError('Error al registrarse')
      }
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-medical-50 via-white to-health-50 py-12 px-4 sm:px-6 lg:px-8">
      {/* Decoración de fondo */}
      <div className="absolute inset-0 overflow-hidden pointer-events-none">
        <div className="absolute top-20 right-20 w-72 h-72 bg-medical-200 rounded-full mix-blend-multiply filter blur-3xl opacity-20 animate-pulse-slow"></div>
        <div className="absolute bottom-20 left-20 w-72 h-72 bg-health-200 rounded-full mix-blend-multiply filter blur-3xl opacity-20 animate-pulse-slow" style={{ animationDelay: '1s' }}></div>
      </div>

      <div className="relative max-w-2xl w-full space-y-8">
        {/* Header */}
        <div className="text-center fade-in">
          <div className="flex justify-center mb-4">
            <div className="bg-gradient-to-br from-health-500 to-health-700 p-4 rounded-2xl shadow-medical-lg">
              <svg className="w-12 h-12 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M18 9v3m0 0v3m0-3h3m-3 0h-3m-2-5a4 4 0 11-8 0 4 4 0 018 0zM3 20a6 6 0 0112 0v1H3v-1z" />
              </svg>
            </div>
          </div>
          <h2 className="text-3xl font-bold text-clinical-900">
            Crear Nueva Cuenta
          </h2>
          <p className="mt-2 text-clinical-600">
            Únete a nuestra plataforma médica
          </p>
        </div>

        {/* Formulario */}
        <div className="medical-card slide-up">
          {error && (
            <div className="alert alert-error fade-in mb-6">
              <div className="flex items-center">
                <svg className="w-5 h-5 mr-2" fill="currentColor" viewBox="0 0 20 20">
                  <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
                </svg>
                {error}
              </div>
            </div>
          )}

          <form onSubmit={handleSubmit} className="space-y-6">
            {/* Selector de tipo de usuario - destacado */}
            <div className="bg-gradient-to-r from-medical-50 to-health-50 p-4 rounded-lg border-2 border-medical-200">
              <label className="block text-sm font-semibold text-clinical-800 mb-3">
                <span className="flex items-center">
                  <svg className="w-5 h-5 mr-2 text-medical-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                  </svg>
                  Tipo de Cuenta
                </span>
              </label>
              <div className="grid grid-cols-2 gap-4">
                <button
                  type="button"
                  onClick={() => setFormData({ ...formData, role: 'patient' })}
                  className={`p-4 rounded-lg border-2 transition-all ${
                    formData.role === 'patient'
                      ? 'border-medical-600 bg-medical-100 shadow-md'
                      : 'border-clinical-200 bg-white hover:border-medical-300'
                  }`}
                >
                  <div className="flex flex-col items-center">
                    <svg className={`w-8 h-8 mb-2 ${formData.role === 'patient' ? 'text-medical-600' : 'text-clinical-400'}`} fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                    </svg>
                    <span className={`font-semibold ${formData.role === 'patient' ? 'text-medical-700' : 'text-clinical-600'}`}>
                      Paciente
                    </span>
                  </div>
                </button>
                <button
                  type="button"
                  onClick={() => setFormData({ ...formData, role: 'doctor' })}
                  className={`p-4 rounded-lg border-2 transition-all ${
                    formData.role === 'doctor'
                      ? 'border-health-600 bg-health-100 shadow-md'
                      : 'border-clinical-200 bg-white hover:border-health-300'
                  }`}
                >
                  <div className="flex flex-col items-center">
                    <svg className={`w-8 h-8 mb-2 ${formData.role === 'doctor' ? 'text-health-600' : 'text-clinical-400'}`} fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                    </svg>
                    <span className={`font-semibold ${formData.role === 'doctor' ? 'text-health-700' : 'text-clinical-600'}`}>
                      Médico
                    </span>
                  </div>
                </button>
              </div>
            </div>

            {/* Campos del formulario en grid */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-semibold text-clinical-700 mb-2">
                  Nombre Completo
                </label>
                <input
                  type="text"
                  name="full_name"
                  value={formData.full_name}
                  onChange={handleChange}
                  className="medical-input"
                  placeholder="Ej: Juan Pérez"
                  required
                />
              </div>

              <div>
                <label className="block text-sm font-semibold text-clinical-700 mb-2">
                  Email
                </label>
                <input
                  type="email"
                  name="email"
                  value={formData.email}
                  onChange={handleChange}
                  className="medical-input"
                  placeholder="correo@ejemplo.com"
                  required
                />
              </div>

              <div>
                <label className="block text-sm font-semibold text-clinical-700 mb-2">
                  Usuario
                </label>
                <input
                  type="text"
                  name="username"
                  value={formData.username}
                  onChange={handleChange}
                  className="medical-input"
                  placeholder="usuario123"
                  required
                />
              </div>

              <div>
                <label className="block text-sm font-semibold text-clinical-700 mb-2">
                  Contraseña
                </label>
                <input
                  type="password"
                  name="password"
                  value={formData.password}
                  onChange={handleChange}
                  className="medical-input"
                  placeholder="••••••••"
                  required
                />
              </div>

              <div className="md:col-span-2">
                <label className="block text-sm font-semibold text-clinical-700 mb-2">
                  Teléfono
                </label>
                <input
                  type="tel"
                  name="phone"
                  value={formData.phone}
                  onChange={handleChange}
                  className="medical-input"
                  placeholder="+1 234 567 8900"
                />
              </div>

              {formData.role === 'doctor' && (
                <>
                  <div>
                    <label className="block text-sm font-semibold text-clinical-700 mb-2">
                      <span className="flex items-center">
                        <svg className="w-4 h-4 mr-1 text-health-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                        </svg>
                        Número de Licencia
                      </span>
                    </label>
                    <input
                      type="text"
                      name="license_number"
                      value={formData.license_number}
                      onChange={handleChange}
                      className="medical-input"
                      placeholder="LIC-12345"
                      required={formData.role === 'doctor'}
                    />
                  </div>

                  <div>
                    <label className="block text-sm font-semibold text-clinical-700 mb-2">
                      <span className="flex items-center">
                        <svg className="w-4 h-4 mr-1 text-health-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
                        </svg>
                        Especialidad
                      </span>
                    </label>
                    <select
                      name="specialty_id"
                      value={formData.specialty_id}
                      onChange={handleChange}
                      className="medical-input"
                      required={formData.role === 'doctor'}
                    >
                      <option value="">Seleccionar especialidad</option>
                      {specialties.map(spec => (
                        <option key={spec.id} value={spec.id}>{spec.name}</option>
                      ))}
                    </select>
                  </div>
                </>
              )}
            </div>

            <button
              type="submit"
              disabled={loading}
              className="w-full btn-success flex items-center justify-center"
            >
              {loading ? (
                <>
                  <div className="loading-spinner mr-3"></div>
                  Registrando...
                </>
              ) : (
                <>
                  <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M18 9v3m0 0v3m0-3h3m-3 0h-3m-2-5a4 4 0 11-8 0 4 4 0 018 0zM3 20a6 6 0 0112 0v1H3v-1z" />
                  </svg>
                  Crear Cuenta
                </>
              )}
            </button>
          </form>

          <div className="mt-6 text-center">
            <p className="text-sm text-clinical-600">
              ¿Ya tienes cuenta?{' '}
              <Link 
                to="/login" 
                className="font-semibold text-medical-600 hover:text-medical-700 transition-colors"
              >
                Inicia sesión
              </Link>
            </p>
          </div>
        </div>
      </div>
    </div>
  )
}

export default Register
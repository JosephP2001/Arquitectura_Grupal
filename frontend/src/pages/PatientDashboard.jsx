import { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import appointmentService from '../services/appointmentService'
import patientService from '../services/patientService'

const PatientDashboard = () => {
  const [appointments, setAppointments] = useState([])
  const [profile, setProfile] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    loadData()
  }, [])

  const loadData = async () => {
    try {
      const [appointmentsData, profileData] = await Promise.all([
        appointmentService.getMyAppointments(),
        patientService.getMyProfile()
      ])
      setAppointments(appointmentsData)
      setProfile(profileData)
    } catch (err) {
      console.error('Error cargando datos:', err)
    } finally {
      setLoading(false)
    }
  }

  const getStatusColor = (status) => {
    const colors = {
      pending: 'bg-yellow-100 text-yellow-800',
      confirmed: 'bg-green-100 text-green-800',
      cancelled: 'bg-red-100 text-red-800',
      completed: 'bg-blue-100 text-blue-800'
    }
    return colors[status] || 'bg-gray-100 text-gray-800'
  }

  if (loading) {
    return <div className="container mx-auto px-4 py-8">Cargando...</div>
  }

  return (
    <div className="container mx-auto px-4 py-8">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-3xl font-bold">Dashboard de Paciente</h1>
        <Link
          to="/appointments/new"
          className="bg-blue-600 text-white px-6 py-2 rounded hover:bg-blue-700"
        >
          Agendar Nueva Cita
        </Link>
      </div>

      {/* Perfil y Estadísticas */}
      {profile && (
        <div className="bg-white rounded-lg shadow-md p-6 mb-6">
          <h2 className="text-xl font-bold mb-4">Mi Perfil</h2>
          
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
            <div>
              <p className="text-gray-600"><strong>Nombre:</strong> {profile.full_name}</p>
              <p className="text-gray-600"><strong>Email:</strong> {profile.email}</p>
              {profile.phone && <p className="text-gray-600"><strong>Teléfono:</strong> {profile.phone}</p>}
              {profile.address && <p className="text-gray-600"><strong>Dirección:</strong> {profile.address}</p>}
            </div>
            
            <div>
              <h3 className="font-bold mb-2">Estadísticas de Citas</h3>
              <div className="space-y-2">
                <div className="flex justify-between bg-gray-50 p-2 rounded">
                  <span>Total de citas:</span>
                  <span className="font-bold">{profile.total_appointments}</span>
                </div>
                <div className="flex justify-between bg-yellow-50 p-2 rounded">
                  <span>Pendientes:</span>
                  <span className="font-bold text-yellow-700">{profile.pending_appointments}</span>
                </div>
                <div className="flex justify-between bg-green-50 p-2 rounded">
                  <span>Confirmadas:</span>
                  <span className="font-bold text-green-700">{profile.confirmed_appointments}</span>
                </div>
                <div className="flex justify-between bg-blue-50 p-2 rounded">
                  <span>Completadas:</span>
                  <span className="font-bold text-blue-700">{profile.completed_appointments}</span>
                </div>
                <div className="flex justify-between bg-red-50 p-2 rounded">
                  <span>Canceladas:</span>
                  <span className="font-bold text-red-700">{profile.cancelled_appointments}</span>
                </div>
                <div className="flex justify-between bg-orange-50 p-2 rounded">
                  <span>Registros médicos:</span>
                  <span className="font-bold text-orange-700">{profile.medical_records_count}</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Citas */}
      <div className="bg-white rounded-lg shadow-md p-6">
        <h2 className="text-xl font-bold mb-4">Mis Citas</h2>
        
        {appointments.length === 0 ? (
          <p className="text-gray-500">No tienes citas agendadas</p>
        ) : (
          <div className="space-y-4">
            {appointments.map((appointment) => (
              <div
                key={appointment.id}
                className="border rounded-lg p-4 hover:shadow-md transition"
              >
                <div className="flex justify-between items-start">
                  <div>
                    <h3 className="font-bold text-lg">Dr. {appointment.doctor_name}</h3>
                    <p className="text-gray-600">
                      {new Date(appointment.appointment_date).toLocaleString('es-ES')}
                    </p>
                    <p className="text-gray-600">Duración: {appointment.duration_minutes} minutos</p>
                    <p className="mt-2"><strong>Motivo:</strong> {appointment.reason}</p>
                    {appointment.notes && (
                      <p className="text-gray-600"><strong>Notas:</strong> {appointment.notes}</p>
                    )}
                  </div>
                  <span className={`px-3 py-1 rounded-full text-sm font-semibold ${getStatusColor(appointment.status)}`}>
                    {appointment.status}
                  </span>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  )
}

export default PatientDashboard
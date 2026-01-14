import { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import appointmentService from '../services/appointmentService'

const PatientDashboard = () => {
  const [appointments, setAppointments] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    loadAppointments()
  }, [])

  const loadAppointments = async () => {
    try {
      const data = await appointmentService.getMyAppointments()
      setAppointments(data)
    } catch (err) {
      console.error('Error cargando citas:', err)
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
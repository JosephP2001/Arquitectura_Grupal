import { useState, useEffect } from 'react'
import appointmentService from '../services/appointmentService'

const DoctorDashboard = () => {
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

  const handleUpdateStatus = async (appointmentId, newStatus) => {
    try {
      await appointmentService.updateAppointmentStatus(appointmentId, newStatus)
      loadAppointments()
    } catch (err) {
      console.error('Error actualizando estado:', err)
      alert('Error al actualizar el estado de la cita')
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
      <h1 className="text-3xl font-bold mb-6">Dashboard de Médico</h1>

      <div className="bg-white rounded-lg shadow-md p-6">
        <h2 className="text-xl font-bold mb-4">Mis Citas Programadas</h2>
        
        {appointments.length === 0 ? (
          <p className="text-gray-500">No tienes citas programadas</p>
        ) : (
          <div className="space-y-4">
            {appointments.map((appointment) => (
              <div
                key={appointment.id}
                className="border rounded-lg p-4 hover:shadow-md transition"
              >
                <div className="flex justify-between items-start">
                  <div className="flex-1">
                    <h3 className="font-bold text-lg">Paciente: {appointment.patient_name}</h3>
                    <p className="text-gray-600">
                      {new Date(appointment.appointment_date).toLocaleString('es-ES')}
                    </p>
                    <p className="text-gray-600">Duración: {appointment.duration_minutes} minutos</p>
                    <p className="mt-2"><strong>Motivo:</strong> {appointment.reason}</p>
                    {appointment.notes && (
                      <p className="text-gray-600"><strong>Notas:</strong> {appointment.notes}</p>
                    )}
                  </div>
                  
                  <div className="flex flex-col items-end gap-2">
                    <span className={`px-3 py-1 rounded-full text-sm font-semibold ${getStatusColor(appointment.status)}`}>
                      {appointment.status}
                    </span>
                    
                    {appointment.status === 'pending' && (
                      <div className="flex gap-2">
                        <button
                          onClick={() => handleUpdateStatus(appointment.id, 'confirmed')}
                          className="bg-green-500 text-white px-3 py-1 rounded text-sm hover:bg-green-600"
                        >
                          Confirmar
                        </button>
                        <button
                          onClick={() => handleUpdateStatus(appointment.id, 'cancelled')}
                          className="bg-red-500 text-white px-3 py-1 rounded text-sm hover:bg-red-600"
                        >
                          Cancelar
                        </button>
                      </div>
                    )}
                    
                    {appointment.status === 'confirmed' && (
                      <button
                        onClick={() => handleUpdateStatus(appointment.id, 'completed')}
                        className="bg-blue-500 text-white px-3 py-1 rounded text-sm hover:bg-blue-600"
                      >
                        Marcar como Completada
                      </button>
                    )}
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  )
}

export default DoctorDashboard
import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import doctorService from '../services/doctorService'
import appointmentService from '../services/appointmentService'

const AppointmentBooking = () => {
  const [specialties, setSpecialties] = useState([])
  const [doctors, setDoctors] = useState([])
  const [selectedSpecialty, setSelectedSpecialty] = useState('')
  const [formData, setFormData] = useState({
    doctor_id: '',
    appointment_date: '',
    reason: '',
    duration_minutes: 30
  })
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)
  const navigate = useNavigate()

  useEffect(() => {
    loadSpecialties()
  }, [])

  useEffect(() => {
    if (selectedSpecialty) {
      loadDoctors(selectedSpecialty)
    }
  }, [selectedSpecialty])

  const loadSpecialties = async () => {
    try {
      const data = await doctorService.getSpecialties()
      setSpecialties(data)
    } catch (err) {
      console.error('Error cargando especialidades:', err)
    }
  }

  const loadDoctors = async (specialtyId) => {
    try {
      const data = await doctorService.getAllDoctors(specialtyId)
      setDoctors(data)
    } catch (err) {
      console.error('Error cargando médicos:', err)
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
      await appointmentService.createAppointment(formData)
      alert('Cita agendada exitosamente')
      navigate('/patient/dashboard')
    } catch (err) {
      setError(err.response?.data?.detail || 'Error al agendar la cita')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="container mx-auto px-4 py-8">
      <h1 className="text-3xl font-bold mb-6">Agendar Nueva Cita</h1>

      <div className="bg-white rounded-lg shadow-md p-6 max-w-2xl">
        {error && (
          <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
            {error}
          </div>
        )}

        <form onSubmit={handleSubmit}>
          <div className="mb-4">
            <label className="block text-gray-700 mb-2">Especialidad</label>
            <select
              value={selectedSpecialty}
              onChange={(e) => setSelectedSpecialty(e.target.value)}
              className="w-full px-3 py-2 border rounded focus:outline-none focus:ring-2 focus:ring-blue-500"
              required
            >
              <option value="">Seleccionar especialidad</option>
              {specialties.map(spec => (
                <option key={spec.id} value={spec.id}>{spec.name}</option>
              ))}
            </select>
          </div>

          {selectedSpecialty && (
            <div className="mb-4">
              <label className="block text-gray-700 mb-2">Médico</label>
              <select
                name="doctor_id"
                value={formData.doctor_id}
                onChange={handleChange}
                className="w-full px-3 py-2 border rounded focus:outline-none focus:ring-2 focus:ring-blue-500"
                required
              >
                <option value="">Seleccionar médico</option>
                {doctors.map(doctor => (
                  <option key={doctor.id} value={doctor.id}>
                    Dr. {doctor.full_name} - {doctor.specialty}
                  </option>
                ))}
              </select>
            </div>
          )}

          <div className="mb-4">
            <label className="block text-gray-700 mb-2">Fecha y Hora</label>
            <input
              type="datetime-local"
              name="appointment_date"
              value={formData.appointment_date}
              onChange={handleChange}
              className="w-full px-3 py-2 border rounded focus:outline-none focus:ring-2 focus:ring-blue-500"
              required
            />
          </div>

          <div className="mb-4">
            <label className="block text-gray-700 mb-2">Motivo de la Consulta</label>
            <textarea
              name="reason"
              value={formData.reason}
              onChange={handleChange}
              className="w-full px-3 py-2 border rounded focus:outline-none focus:ring-2 focus:ring-blue-500"
              rows="4"
              required
            />
          </div>

          <div className="mb-6">
            <label className="block text-gray-700 mb-2">Duración (minutos)</label>
            <select
              name="duration_minutes"
              value={formData.duration_minutes}
              onChange={handleChange}
              className="w-full px-3 py-2 border rounded focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              <option value="15">15 minutos</option>
              <option value="30">30 minutos</option>
              <option value="45">45 minutos</option>
              <option value="60">60 minutos</option>
            </select>
          </div>

          <div className="flex gap-4">
            <button
              type="submit"
              disabled={loading}
              className="flex-1 bg-blue-600 text-white py-2 rounded hover:bg-blue-700 disabled:bg-gray-400"
            >
              {loading ? 'Agendando...' : 'Agendar Cita'}
            </button>
            <button
              type="button"
              onClick={() => navigate('/patient/dashboard')}
              className="flex-1 bg-gray-500 text-white py-2 rounded hover:bg-gray-600"
            >
              Cancelar
            </button>
          </div>
        </form>
      </div>
    </div>
  )
}

export default AppointmentBooking
import api from './api'

const appointmentService = {
  async createAppointment(appointmentData) {
    const response = await api.post('/appointments/', appointmentData)
    return response.data
  },

  async getMyAppointments() {
    const response = await api.get('/appointments/my-appointments')
    return response.data
  },

  async updateAppointmentStatus(appointmentId, status) {
    const response = await api.patch(`/appointments/${appointmentId}/status`, { status })
    return response.data
  }
}

export default appointmentService
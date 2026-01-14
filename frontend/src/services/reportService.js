import api from './api'

const reportService = {
  async getPatientCompleteReport(patientId) {
    const response = await api.get(`/reports/patient/${patientId}`)
    return response.data
  },

  async getSystemReport() {
    const response = await api.get('/reports/system')
    return response.data
  },

  async getDoctorPerformanceReport(doctorId) {
    const response = await api.get(`/reports/doctor/${doctorId}/performance`)
    return response.data
  }
}

export default reportService
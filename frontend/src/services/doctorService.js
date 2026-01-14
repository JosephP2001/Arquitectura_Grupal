import api from './api'

const doctorService = {
  async getAllDoctors(specialtyId = null) {
    const params = specialtyId ? { specialty_id: specialtyId } : {}
    const response = await api.get('/doctors/', { params })
    return response.data
  },

  async getDoctorById(doctorId) {
    const response = await api.get(`/doctors/${doctorId}`)
    return response.data
  },

  async getDoctorSchedule(doctorId) {
    const response = await api.get(`/doctors/${doctorId}/schedule`)
    return response.data
  },

  async getSpecialties() {
    const response = await api.get('/doctors/specialties/list')
    return response.data
  }
}

export default doctorService
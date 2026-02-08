import api from './api'

const doctorService = {
  async getMyProfile() {
    const response = await api.get('/doctors/me')
    return response.data
  },

  async getAllDoctors(specialtyId = null) {
    const params = specialtyId ? { specialty_id: specialtyId } : {}
    const response = await api.get('/doctors/', { params })
    return response.data
  },

  async getDoctors(specialtyId = null) {
    return this.getAllDoctors(specialtyId)
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
import api from './api'

const patientService = {
  // Obtener perfil del paciente actual con estadísticas
  getMyProfile: async () => {
    try {
      const response = await api.get('/patients/me')
      return response.data
    } catch (error) {
      console.error('Error obteniendo perfil de paciente:', error)
      throw error
    }
  },

  // Obtener registros médicos del paciente
  getMedicalRecords: async () => {
    try {
      const response = await api.get('/patients/medical-records')
      return response.data.records
    } catch (error) {
      console.error('Error obteniendo registros médicos:', error)
      throw error
    }
  }
}

export default patientService
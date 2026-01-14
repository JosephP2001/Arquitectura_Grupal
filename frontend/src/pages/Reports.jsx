import { useState, useEffect } from 'react'
import { useAuth } from '../context/AuthContext'
import reportService from '../services/reportService'

const Reports = () => {
  const { user } = useAuth()
  const [systemReport, setSystemReport] = useState(null)
  const [patientReport, setPatientReport] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  useEffect(() => {
    loadReports()
  }, [])

  const loadReports = async () => {
    try {
      setLoading(true)
      
      // Cargar reporte del sistema
      const sysReport = await reportService.getSystemReport()
      setSystemReport(sysReport)
      
      // Si es paciente, cargar su reporte completo
      if (user?.role === 'patient') {
        // Aquí deberías obtener el patient_id del usuario
        // Por ahora lo simulamos
        try {
          const patReport = await reportService.getPatientCompleteReport(1)
          setPatientReport(patReport)
        } catch (err) {
          console.log('No se pudo cargar reporte de paciente')
        }
      }
    } catch (err) {
      setError('Error al cargar reportes')
      console.error(err)
    } finally {
      setLoading(false)
    }
  }

  if (loading) {
    return (
      <div className="container mx-auto px-4 py-8">
        <div className="text-center">Cargando reportes...</div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="container mx-auto px-4 py-8">
        <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded">
          {error}
        </div>
      </div>
    )
  }

  return (
    <div className="container mx-auto px-4 py-8">
      <h1 className="text-3xl font-bold mb-6">Reportes del Sistema</h1>
      
      {/* Reporte del Sistema (Combinando PostgreSQL y MongoDB) */}
      {systemReport && (
        <div className="bg-white rounded-lg shadow-md p-6 mb-6">
          <h2 className="text-2xl font-bold mb-4 text-blue-600">
            📊 Reporte General del Sistema
          </h2>
          <p className="text-sm text-gray-600 mb-4">
            <strong>Fuentes de datos:</strong> PostgreSQL (estadísticas) + MongoDB (actividad)
          </p>
          
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
            <div className="bg-blue-50 p-4 rounded">
              <div className="text-3xl font-bold text-blue-600">
                {systemReport.total_patients}
              </div>
              <div className="text-gray-600">Total Pacientes</div>
              <div className="text-xs text-gray-500">PostgreSQL</div>
            </div>
            
            <div className="bg-green-50 p-4 rounded">
              <div className="text-3xl font-bold text-green-600">
                {systemReport.total_doctors}
              </div>
              <div className="text-gray-600">Total Médicos</div>
              <div className="text-xs text-gray-500">PostgreSQL</div>
            </div>
            
            <div className="bg-purple-50 p-4 rounded">
              <div className="text-3xl font-bold text-purple-600">
                {systemReport.total_appointments}
              </div>
              <div className="text-gray-600">Total Citas</div>
              <div className="text-xs text-gray-500">PostgreSQL</div>
            </div>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <h3 className="font-bold mb-2">Citas por Estado (PostgreSQL)</h3>
              <div className="space-y-2">
                {Object.entries(systemReport.appointments_by_status).map(([status, count]) => (
                  <div key={status} className="flex justify-between items-center bg-gray-50 p-2 rounded">
                    <span className="capitalize">{status}</span>
                    <span className="font-bold">{count}</span>
                  </div>
                ))}
              </div>
            </div>
            
            <div>
              <h3 className="font-bold mb-2">Datos MongoDB</h3>
              <div className="bg-orange-50 p-4 rounded mb-4">
                <div className="text-2xl font-bold text-orange-600">
                  {systemReport.total_medical_records}
                </div>
                <div className="text-gray-600">Registros Médicos</div>
                <div className="text-xs text-gray-500">MongoDB</div>
              </div>
            </div>
          </div>

          <div className="mt-6">
            <h3 className="font-bold mb-2">
              Actividad Reciente del Sistema (MongoDB - Últimas 24 horas)
            </h3>
            <div className="bg-gray-50 p-4 rounded max-h-64 overflow-y-auto">
              {systemReport.recent_activity.length > 0 ? (
                <div className="space-y-2">
                  {systemReport.recent_activity.map((log, idx) => (
                    <div key={idx} className="text-sm border-b pb-2">
                      <div className="flex justify-between">
                        <span className="font-semibold">{log.action || log.level}</span>
                        <span className="text-gray-500 text-xs">
                          {new Date(log.timestamp).toLocaleString()}
                        </span>
                      </div>
                      <div className="text-gray-600">{log.message}</div>
                    </div>
                  ))}
                </div>
              ) : (
                <p className="text-gray-500 text-center">No hay actividad reciente</p>
              )}
            </div>
          </div>
        </div>
      )}

      {/* Reporte del Paciente */}
      {patientReport && (
        <div className="bg-white rounded-lg shadow-md p-6">
          <h2 className="text-2xl font-bold mb-4 text-green-600">
            👤 Mi Reporte Completo
          </h2>
          <p className="text-sm text-gray-600 mb-4">
            <strong>Fuentes de datos:</strong> PostgreSQL (citas) + MongoDB (historiales médicos)
          </p>
          
          <div className="mb-4">
            <h3 className="font-bold">Información Personal (PostgreSQL)</h3>
            <p><strong>Nombre:</strong> {patientReport.patient_name}</p>
            <p><strong>Email:</strong> {patientReport.email}</p>
            <p><strong>Teléfono:</strong> {patientReport.phone}</p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
            <div className="bg-blue-50 p-4 rounded">
              <div className="text-2xl font-bold text-blue-600">
                {patientReport.total_appointments}
              </div>
              <div className="text-gray-600">Total Citas</div>
              <div className="text-xs text-gray-500">PostgreSQL</div>
            </div>
            
            <div className="bg-orange-50 p-4 rounded">
              <div className="text-2xl font-bold text-orange-600">
                {patientReport.medical_records_count}
              </div>
              <div className="text-gray-600">Registros Médicos</div>
              <div className="text-xs text-gray-500">MongoDB</div>
            </div>
          </div>

          <div className="mb-4">
            <h3 className="font-bold mb-2">Historial de Citas (PostgreSQL)</h3>
            <div className="space-y-2 max-h-48 overflow-y-auto">
              {patientReport.appointments.map((apt, idx) => (
                <div key={idx} className="bg-gray-50 p-3 rounded text-sm">
                  <div className="font-semibold">{apt.doctor_name} - {apt.specialty}</div>
                  <div className="text-gray-600">
                    {new Date(apt.date).toLocaleString()} - {apt.status}
                  </div>
                  <div className="text-gray-500">{apt.reason}</div>
                </div>
              ))}
            </div>
          </div>

          <div>
            <h3 className="font-bold mb-2">Registros Médicos (MongoDB)</h3>
            <div className="space-y-2 max-h-48 overflow-y-auto">
              {patientReport.medical_records.length > 0 ? (
                patientReport.medical_records.map((record, idx) => (
                  <div key={idx} className="bg-gray-50 p-3 rounded text-sm">
                    <div className="font-semibold">Diagnóstico: {record.diagnosis}</div>
                    <div className="text-gray-600">Tratamiento: {record.treatment}</div>
                    <div className="text-gray-500 text-xs">
                      {new Date(record.created_at).toLocaleString()}
                    </div>
                  </div>
                ))
              ) : (
                <p className="text-gray-500 text-center">No hay registros médicos</p>
              )}
            </div>
          </div>
        </div>
      )}
    </div>
  )
}

export default Reports
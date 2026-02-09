import React, { useState, useEffect } from 'react';
import axios from 'axios';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export default function ServiceRegistryDashboard() {
  const [services, setServices] = useState({});
  const [metrics, setMetrics] = useState([]);
  const [selectedService, setSelectedService] = useState(null);
  const [serviceHistory, setServiceHistory] = useState([]);
  const [loading, setLoading] = useState(true);
  const [autoRefresh, setAutoRefresh] = useState(true);

  // Obtener todos los servicios
  const fetchServices = async () => {
    try {
      const response = await axios.get(`${API_URL}/monitoring/registry/services`);
      setServices(response.data.services);
    } catch (error) {
      console.error('Error fetching services:', error);
    }
  };

  // Obtener métricas
  const fetchMetrics = async () => {
    try {
      const response = await axios.get(`${API_URL}/monitoring/registry/metrics`);
      setMetrics(response.data.metrics);
      setLoading(false);
    } catch (error) {
      console.error('Error fetching metrics:', error);
      setLoading(false);
    }
  };

  // Obtener historial de un servicio
  const fetchServiceHistory = async (serviceName) => {
    try {
      const response = await axios.get(
        `${API_URL}/monitoring/registry/services/${serviceName}/history?limit=20`
      );
      setServiceHistory(response.data.history);
    } catch (error) {
      console.error('Error fetching service history:', error);
    }
  };

  // Ejecutar health check manual
  const triggerHealthCheck = async (serviceName) => {
    try {
      await axios.post(`${API_URL}/monitoring/registry/health-check/${serviceName}`);
      fetchServices();
      fetchMetrics();
    } catch (error) {
      console.error('Error triggering health check:', error);
    }
  };

  // Ejecutar health check de todos
  const triggerAllHealthChecks = async () => {
    try {
      await axios.post(`${API_URL}/monitoring/registry/health-check`);
      fetchServices();
      fetchMetrics();
    } catch (error) {
      console.error('Error triggering all health checks:', error);
    }
  };

  // Auto-refresh cada 5 segundos
  useEffect(() => {
    fetchServices();
    fetchMetrics();

    if (autoRefresh) {
      const interval = setInterval(() => {
        fetchServices();
        fetchMetrics();
        if (selectedService) {
          fetchServiceHistory(selectedService);
        }
      }, 5000);

      return () => clearInterval(interval);
    }
  }, [autoRefresh, selectedService]);

  // Obtener color según estado
  const getStatusColor = (status) => {
    switch (status) {
      case 'UP':
        return 'bg-green-500';
      case 'DOWN':
        return 'bg-red-500';
      case 'DEGRADED':
        return 'bg-yellow-500';
      default:
        return 'bg-gray-500';
    }
  };

  const getStatusTextColor = (status) => {
    switch (status) {
      case 'UP':
        return 'text-green-700';
      case 'DOWN':
        return 'text-red-700';
      case 'DEGRADED':
        return 'text-yellow-700';
      default:
        return 'text-gray-700';
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-xl text-gray-900">Cargando Service Registry Dashboard...</div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 p-6">
      {/* Header */}
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-2">
          🔍 Service Registry Dashboard
        </h1>
        <p className="text-gray-800">
          Monitoreo en tiempo real de servicios registrados
        </p>
      </div>

      {/* Controls */}
      <div className="mb-6 flex gap-4 items-center">
        <button
          onClick={triggerAllHealthChecks}
          className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition font-semibold"
        >
          🔄 Health Check Manual
        </button>
        
        <label className="flex items-center gap-2 cursor-pointer">
          <input
            type="checkbox"
            checked={autoRefresh}
            onChange={(e) => setAutoRefresh(e.target.checked)}
            className="w-4 h-4"
          />
          <span className="text-gray-900 font-medium">Auto-refresh (5s)</span>
        </label>
      </div>

      {/* Services Grid */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
        {Object.entries(services).map(([serviceName, serviceInfo]) => (
          <div
            key={serviceName}
            className="bg-white rounded-lg shadow-md p-6 border-l-4 border-gray-200"
            style={{
              borderLeftColor:
                serviceInfo.status === 'UP'
                  ? '#10b981'
                  : serviceInfo.status === 'DOWN'
                  ? '#ef4444'
                  : '#f59e0b',
            }}
          >
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-lg font-semibold text-gray-900">
                {serviceName.toUpperCase()}
              </h3>
              <span
                className={`px-3 py-1 rounded-full text-sm font-medium ${getStatusColor(
                  serviceInfo.status
                )} text-white`}
              >
                {serviceInfo.status}
              </span>
            </div>

            <div className="space-y-2 text-sm text-gray-800 mb-4">
              <div className="flex justify-between">
                <span className="font-medium">Host:</span>
                <span className="font-mono text-gray-900">{serviceInfo.host}</span>
              </div>
              <div className="flex justify-between">
                <span className="font-medium">Puerto:</span>
                <span className="font-mono text-gray-900">{serviceInfo.port}</span>
              </div>
              <div className="flex justify-between">
                <span className="font-medium">Total Checks:</span>
                <span className="font-mono text-gray-900">{serviceInfo.total_checks}</span>
              </div>
              <div className="flex justify-between">
                <span className="font-medium">Fallos:</span>
                <span className="font-mono text-gray-900">{serviceInfo.failure_count}</span>
              </div>
            </div>

            <button
              onClick={() => {
                setSelectedService(serviceName);
                fetchServiceHistory(serviceName);
              }}
              className="w-full px-3 py-2 bg-gray-200 text-gray-900 rounded hover:bg-gray-300 transition text-sm font-semibold"
            >
              Ver Historial
            </button>
          </div>
        ))}
      </div>

      {/* Metrics Table */}
      <div className="bg-white rounded-lg shadow-md p-6 mb-8 border border-gray-200">
        <h2 className="text-xl font-bold text-gray-900 mb-4">
          📊 Métricas Detalladas
        </h2>
        
        <div className="overflow-x-auto">
          <table className="min-w-full divide-y divide-gray-300">
            <thead className="bg-gray-100">
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-900 uppercase tracking-wider">
                  Servicio
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-900 uppercase tracking-wider">
                  Estado
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-900 uppercase tracking-wider">
                  Uptime
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-900 uppercase tracking-wider">
                  Exitosos
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-900 uppercase tracking-wider">
                  Fallidos
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-900 uppercase tracking-wider">
                  Último Check
                </th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-gray-200">
              {metrics.map((metric) => (
                <tr key={metric.service_name} className="hover:bg-gray-50">
                  <td className="px-6 py-4 whitespace-nowrap">
                    <span className="font-medium text-gray-900">
                      {metric.service_name.toUpperCase()}
                    </span>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <span
                      className={`px-2 py-1 rounded text-sm font-medium ${getStatusTextColor(
                        metric.current_status
                      )}`}
                    >
                      {metric.current_status}
                    </span>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <div className="flex items-center">
                      <div className="flex-1 bg-gray-300 rounded-full h-2 mr-2">
                        <div
                          className="bg-green-500 h-2 rounded-full"
                          style={{ width: `${metric.uptime_percentage}%` }}
                        ></div>
                      </div>
                      <span className="text-sm text-gray-900 font-medium">
                        {metric.uptime_percentage}%
                      </span>
                    </div>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900 font-medium">
                    {metric.successful_checks}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900 font-medium">
                    {metric.failed_checks}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-800">
                    {metric.last_check
                      ? new Date(metric.last_check).toLocaleString()
                      : 'N/A'}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* Service History Modal */}
      {selectedService && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
          <div className="bg-white rounded-lg max-w-4xl w-full max-h-[80vh] overflow-y-auto p-6">
            <div className="flex items-center justify-between mb-4">
              <h2 className="text-2xl font-bold text-gray-900">
                Historial de {selectedService.toUpperCase()}
              </h2>
              <button
                onClick={() => setSelectedService(null)}
                className="text-gray-700 hover:text-gray-900 text-2xl font-bold"
              >
                ×
              </button>
            </div>

            <div className="space-y-3">
              {serviceHistory.length === 0 ? (
                <p className="text-gray-700">No hay historial disponible</p>
              ) : (
                serviceHistory.map((record, index) => (
                  <div
                    key={index}
                    className="border-l-4 pl-4 py-2"
                    style={{
                      borderLeftColor:
                        record.status === 'UP'
                          ? '#10b981'
                          : record.status === 'DOWN'
                          ? '#ef4444'
                          : '#f59e0b',
                    }}
                  >
                    <div className="flex items-center justify-between mb-1">
                      <span
                        className={`font-medium ${getStatusTextColor(
                          record.status
                        )}`}
                      >
                        {record.status}
                      </span>
                      <span className="text-sm text-gray-700">
                        {new Date(record.timestamp).toLocaleString()}
                      </span>
                    </div>
                    {record.response_time_ms && (
                      <div className="text-sm text-gray-800">
                        Response time: {record.response_time_ms.toFixed(2)}ms
                      </div>
                    )}
                    {record.error_message && (
                      <div className="text-sm text-red-700">
                        Error: {record.error_message}
                      </div>
                    )}
                  </div>
                ))
              )}
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
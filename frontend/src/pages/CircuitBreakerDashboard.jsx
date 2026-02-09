import React, { useState, useEffect } from 'react';
import axios from 'axios';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export default function CircuitBreakerDashboard() {
  const [circuitBreakers, setCircuitBreakers] = useState({});
  const [selectedBreaker, setSelectedBreaker] = useState('web_service_b');
  const [breakerMetrics, setBreakerMetrics] = useState(null);
  const [serviceBStats, setServiceBStats] = useState(null);
  const [serviceBMode, setServiceBMode] = useState('STABLE');
  const [failureRate, setFailureRate] = useState(0.5);
  const [slowDelay, setSlowDelay] = useState(3.0);
  const [testResults, setTestResults] = useState(null);
  const [loading, setLoading] = useState(true);
  const [autoRefresh, setAutoRefresh] = useState(true);

  // Fetch Circuit Breakers
  const fetchCircuitBreakers = async () => {
    try {
      const response = await axios.get(`${API_URL}/monitoring/circuit-breakers`);
      setCircuitBreakers(response.data.circuit_breakers);
      setLoading(false);
    } catch (error) {
      console.error('Error fetching circuit breakers:', error);
      setLoading(false);
    }
  };

  // Fetch detailed metrics
  const fetchBreakerMetrics = async (breakerName) => {
    try {
      const response = await axios.get(
        `${API_URL}/monitoring/circuit-breakers/${breakerName}/metrics`
      );
      setBreakerMetrics(response.data);
    } catch (error) {
      console.error('Error fetching breaker metrics:', error);
    }
  };

  // Fetch Service B statistics
  const fetchServiceBStats = async () => {
    try {
      const response = await axios.get(`${API_URL}/demo/service-b/statistics`);
      setServiceBStats(response.data);
      setServiceBMode(response.data.mode);
    } catch (error) {
      console.error('Error fetching Service B stats:', error);
    }
  };

  // Set Service B mode
  const setServiceMode = async (mode) => {
    try {
      const params = { mode };
      if (mode === 'INTERMITTENT') {
        params.failure_rate = failureRate;
      } else if (mode === 'SLOW') {
        params.slow_delay = slowDelay;
      }

      await axios.post(`${API_URL}/demo/service-b/mode`, null, { params });
      fetchServiceBStats();
      alert(`Service B mode changed to ${mode}`);
    } catch (error) {
      console.error('Error setting Service B mode:', error);
      alert('Error setting mode');
    }
  };

  // Test circuit breaker
  const runTest = async (numRequests) => {
    try {
      setTestResults(null);
      const response = await axios.post(
        `${API_URL}/demo/test-circuit-breaker?num_requests=${numRequests}&patient_id=1`
      );
      setTestResults(response.data);
      fetchCircuitBreakers();
      fetchBreakerMetrics(selectedBreaker);
      fetchServiceBStats();
    } catch (error) {
      console.error('Error running test:', error);
    }
  };

  // Reset circuit breaker
  const resetBreaker = async (breakerName) => {
    try {
      await axios.post(`${API_URL}/monitoring/circuit-breakers/${breakerName}/reset`);
      fetchCircuitBreakers();
      fetchBreakerMetrics(breakerName);
      alert(`Circuit Breaker ${breakerName} reset`);
    } catch (error) {
      console.error('Error resetting breaker:', error);
    }
  };

  // Reset Service B statistics
  const resetServiceBStats = async () => {
    try {
      await axios.post(`${API_URL}/demo/service-b/reset-statistics`);
      fetchServiceBStats();
      alert('Service B statistics reset');
    } catch (error) {
      console.error('Error resetting stats:', error);
    }
  };

  // Auto-refresh
  useEffect(() => {
    fetchCircuitBreakers();
    fetchServiceBStats();
    fetchBreakerMetrics(selectedBreaker);

    if (autoRefresh) {
      const interval = setInterval(() => {
        fetchCircuitBreakers();
        fetchServiceBStats();
        fetchBreakerMetrics(selectedBreaker);
      }, 3000);

      return () => clearInterval(interval);
    }
  }, [autoRefresh, selectedBreaker]);

  // Get state color
  const getStateColor = (state) => {
    switch (state) {
      case 'CLOSED':
        return 'bg-green-500';
      case 'OPEN':
        return 'bg-red-500';
      case 'HALF_OPEN':
        return 'bg-yellow-500';
      default:
        return 'bg-gray-500';
    }
  };

  const getStateIcon = (state) => {
    switch (state) {
      case 'CLOSED':
        return '🟢';
      case 'OPEN':
        return '🔴';
      case 'HALF_OPEN':
        return '🟡';
      default:
        return '⚪';
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-xl text-gray-900">Cargando Circuit Breaker Dashboard...</div>
      </div>
    );
  }

  const breaker = circuitBreakers[selectedBreaker];

  return (
    <div className="min-h-screen bg-gray-50 p-6">
      {/* Header */}
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-2">
          🔌 Circuit Breaker Dashboard
        </h1>
        <p className="text-gray-800">
          Demostración de patrón Circuit Breaker con Service B simulado
        </p>
      </div>

      {/* Controls */}
      <div className="mb-6 flex gap-4 items-center">
        <label className="flex items-center gap-2 cursor-pointer">
          <input
            type="checkbox"
            checked={autoRefresh}
            onChange={(e) => setAutoRefresh(e.target.checked)}
            className="w-4 h-4"
          />
          <span className="text-gray-900 font-medium">Auto-refresh (3s)</span>
        </label>
      </div>

      {/* Main Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
        {/* Circuit Breaker Status */}
        <div className="bg-white rounded-lg shadow-md p-6 border border-gray-200">
          <h2 className="text-xl font-bold text-gray-900 mb-4">
            Circuit Breaker Status
          </h2>

          {breaker && (
            <div className="space-y-4">
              {/* State Indicator */}
              <div className="flex items-center justify-center p-8 bg-gray-100 rounded-lg border border-gray-300">
                <div className="text-center">
                  <div className="text-6xl mb-2">{getStateIcon(breaker.state)}</div>
                  <div className="text-2xl font-bold text-gray-900">
                    {breaker.state}
                  </div>
                </div>
              </div>

              {/* Stats Grid */}
              <div className="grid grid-cols-2 gap-4">
                <div className="bg-gray-100 p-4 rounded border border-gray-300">
                  <div className="text-sm text-gray-800 font-medium">Failure Count</div>
                  <div className="text-2xl font-bold text-gray-900">
                    {breaker.failure_count} / {breaker.failure_threshold}
                  </div>
                </div>
                <div className="bg-gray-100 p-4 rounded border border-gray-300">
                  <div className="text-sm text-gray-800 font-medium">Timeout</div>
                  <div className="text-2xl font-bold text-gray-900">
                    {breaker.timeout}s
                  </div>
                </div>
                <div className="bg-gray-100 p-4 rounded border border-gray-300">
                  <div className="text-sm text-gray-800 font-medium">Total Calls</div>
                  <div className="text-2xl font-bold text-gray-900">
                    {breaker.metrics.total_calls}
                  </div>
                </div>
                <div className="bg-gray-100 p-4 rounded border border-gray-300">
                  <div className="text-sm text-gray-800 font-medium">Success Rate</div>
                  <div className="text-2xl font-bold text-green-700">
                    {breaker.metrics.success_rate}%
                  </div>
                </div>
              </div>

              {/* Progress Bars */}
              <div className="space-y-3">
                <div>
                  <div className="flex justify-between text-sm mb-1">
                    <span className="text-gray-800 font-medium">Successful</span>
                    <span className="text-green-700 font-medium">
                      {breaker.metrics.successful_calls}
                    </span>
                  </div>
                  <div className="w-full bg-gray-300 rounded-full h-2">
                    <div
                      className="bg-green-500 h-2 rounded-full"
                      style={{
                        width: `${breaker.metrics.success_rate}%`,
                      }}
                    ></div>
                  </div>
                </div>

                <div>
                  <div className="flex justify-between text-sm mb-1">
                    <span className="text-gray-800 font-medium">Failed</span>
                    <span className="text-red-700 font-medium">
                      {breaker.metrics.failed_calls}
                    </span>
                  </div>
                  <div className="w-full bg-gray-300 rounded-full h-2">
                    <div
                      className="bg-red-500 h-2 rounded-full"
                      style={{
                        width: `${breaker.metrics.failure_rate}%`,
                      }}
                    ></div>
                  </div>
                </div>

                <div>
                  <div className="flex justify-between text-sm mb-1">
                    <span className="text-gray-800 font-medium">Rejected</span>
                    <span className="text-yellow-700 font-medium">
                      {breaker.metrics.rejected_calls}
                    </span>
                  </div>
                  <div className="w-full bg-gray-300 rounded-full h-2">
                    <div
                      className="bg-yellow-500 h-2 rounded-full"
                      style={{
                        width: `${
                          (breaker.metrics.rejected_calls /
                            breaker.metrics.total_calls) *
                          100
                        }%`,
                      }}
                    ></div>
                  </div>
                </div>
              </div>

              {/* Response Time */}
              <div className="bg-blue-50 p-4 rounded border border-blue-200">
                <div className="text-sm text-gray-800 font-medium mb-1">
                  Average Response Time
                </div>
                <div className="text-xl font-bold text-blue-700">
                  {breaker.metrics.average_response_time.toFixed(2)}ms
                </div>
              </div>

              {/* Reset Button */}
              <button
                onClick={() => resetBreaker(selectedBreaker)}
                className="w-full px-4 py-2 bg-gray-600 text-white rounded-lg hover:bg-gray-700 transition font-semibold"
              >
                ♻️ Reset Circuit Breaker
              </button>
            </div>
          )}
        </div>

        {/* Service B Control */}
        <div className="bg-white rounded-lg shadow-md p-6 border border-gray-200">
          <h2 className="text-xl font-bold text-gray-900 mb-4">
            Service B Control
          </h2>

          {serviceBStats && (
            <div className="space-y-4">
              {/* Current Mode */}
              <div className="bg-gray-100 p-4 rounded-lg border border-gray-300">
                <div className="text-sm text-gray-800 font-medium mb-2">Current Mode</div>
                <div className="text-2xl font-bold text-gray-900">
                  {serviceBStats.mode}
                </div>
              </div>

              {/* Mode Selection */}
              <div>
                <label className="block text-sm font-medium text-gray-900 mb-2">
                  Seleccionar Modo
                </label>
                <div className="grid grid-cols-2 gap-2">
                  <button
                    onClick={() => setServiceMode('STABLE')}
                    className={`px-4 py-2 rounded-lg font-semibold transition ${
                      serviceBMode === 'STABLE'
                        ? 'bg-green-600 text-white shadow-md'
                        : 'bg-green-100 text-green-800 hover:bg-green-200 border border-green-300'
                    }`}
                  >
                    🟢 STABLE
                  </button>
                  <button
                    onClick={() => setServiceMode('INTERMITTENT')}
                    className={`px-4 py-2 rounded-lg font-semibold transition ${
                      serviceBMode === 'INTERMITTENT'
                        ? 'bg-yellow-600 text-white shadow-md'
                        : 'bg-yellow-100 text-yellow-800 hover:bg-yellow-200 border border-yellow-300'
                    }`}
                  >
                    🟡 INTERMITTENT
                  </button>
                  <button
                    onClick={() => setServiceMode('FAILING')}
                    className={`px-4 py-2 rounded-lg font-semibold transition ${
                      serviceBMode === 'FAILING'
                        ? 'bg-red-600 text-white shadow-md'
                        : 'bg-red-100 text-red-800 hover:bg-red-200 border border-red-300'
                    }`}
                  >
                    🔴 FAILING
                  </button>
                  <button
                    onClick={() => setServiceMode('SLOW')}
                    className={`px-4 py-2 rounded-lg font-semibold transition ${
                      serviceBMode === 'SLOW'
                        ? 'bg-blue-600 text-white shadow-md'
                        : 'bg-blue-100 text-blue-800 hover:bg-blue-200 border border-blue-300'
                    }`}
                  >
                    🔵 SLOW
                  </button>
                </div>
              </div>

              {/* Mode Configuration */}
              {serviceBMode === 'INTERMITTENT' && (
                <div>
                  <label className="block text-sm font-medium text-gray-900 mb-2">
                    Failure Rate: {(failureRate * 100).toFixed(0)}%
                  </label>
                  <input
                    type="range"
                    min="0"
                    max="1"
                    step="0.1"
                    value={failureRate}
                    onChange={(e) => setFailureRate(parseFloat(e.target.value))}
                    className="w-full"
                  />
                </div>
              )}

              {serviceBMode === 'SLOW' && (
                <div>
                  <label className="block text-sm font-medium text-gray-900 mb-2">
                    Delay: {slowDelay}s
                  </label>
                  <input
                    type="range"
                    min="1"
                    max="10"
                    step="0.5"
                    value={slowDelay}
                    onChange={(e) => setSlowDelay(parseFloat(e.target.value))}
                    className="w-full"
                  />
                </div>
              )}

              {/* Statistics */}
              <div className="bg-gray-100 p-4 rounded-lg border border-gray-300">
                <div className="text-sm font-medium text-gray-900 mb-2">
                  Service B Statistics
                </div>
                <div className="grid grid-cols-3 gap-2 text-center">
                  <div>
                    <div className="text-xs text-gray-800 font-medium">Total</div>
                    <div className="text-lg font-bold text-gray-900">
                      {serviceBStats.statistics.total_requests}
                    </div>
                  </div>
                  <div>
                    <div className="text-xs text-gray-800 font-medium">Success</div>
                    <div className="text-lg font-bold text-green-700">
                      {serviceBStats.statistics.successful_requests}
                    </div>
                  </div>
                  <div>
                    <div className="text-xs text-gray-800 font-medium">Failed</div>
                    <div className="text-lg font-bold text-red-700">
                      {serviceBStats.statistics.failed_requests}
                    </div>
                  </div>
                </div>
              </div>

              {/* Reset Stats Button */}
              <button
                onClick={resetServiceBStats}
                className="w-full px-4 py-2 bg-gray-600 text-white rounded-lg hover:bg-gray-700 transition font-semibold"
              >
                ♻️ Reset Statistics
              </button>
            </div>
          )}
        </div>
      </div>

      {/* Test Section */}
      <div className="bg-white rounded-lg shadow-md p-6 mb-8 border border-gray-200">
        <h2 className="text-xl font-bold text-gray-900 mb-4">🧪 Testing</h2>

        <div className="flex gap-4 mb-4">
          <button
            onClick={() => runTest(5)}
            className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition font-semibold"
          >
            Run 5 Requests
          </button>
          <button
            onClick={() => runTest(10)}
            className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition font-semibold"
          >
            Run 10 Requests
          </button>
          <button
            onClick={() => runTest(20)}
            className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition font-semibold"
          >
            Run 20 Requests
          </button>
        </div>

        {testResults && (
          <div className="mt-4">
            <div className="bg-gray-100 p-4 rounded-lg mb-4 border border-gray-300">
              <h3 className="font-bold text-gray-900 mb-2">Test Summary</h3>
              <div className="grid grid-cols-4 gap-4 text-center">
                <div>
                  <div className="text-sm text-gray-800 font-medium">Total</div>
                  <div className="text-xl font-bold text-gray-900">
                    {testResults.test_summary.total_requests}
                  </div>
                </div>
                <div>
                  <div className="text-sm text-gray-800 font-medium">Successful</div>
                  <div className="text-xl font-bold text-green-700">
                    {testResults.test_summary.successful}
                  </div>
                </div>
                <div>
                  <div className="text-sm text-gray-800 font-medium">Failed</div>
                  <div className="text-xl font-bold text-red-700">
                    {testResults.test_summary.failed}
                  </div>
                </div>
                <div>
                  <div className="text-sm text-gray-800 font-medium">Final State</div>
                  <div className="text-xl font-bold text-gray-900">
                    {getStateIcon(testResults.test_summary.final_circuit_state)}{' '}
                    {testResults.test_summary.final_circuit_state}
                  </div>
                </div>
              </div>
            </div>

            <div className="max-h-64 overflow-y-auto">
              <table className="min-w-full divide-y divide-gray-300">
                <thead className="bg-gray-100">
                  <tr>
                    <th className="px-4 py-2 text-left text-xs font-medium text-gray-900 uppercase">
                      #
                    </th>
                    <th className="px-4 py-2 text-left text-xs font-medium text-gray-900 uppercase">
                      Result
                    </th>
                    <th className="px-4 py-2 text-left text-xs font-medium text-gray-900 uppercase">
                      State Before
                    </th>
                    <th className="px-4 py-2 text-left text-xs font-medium text-gray-900 uppercase">
                      State After
                    </th>
                  </tr>
                </thead>
                <tbody className="bg-white divide-y divide-gray-200">
                  {testResults.results.map((result, idx) => (
                    <tr key={idx} className="hover:bg-gray-50">
                      <td className="px-4 py-2 text-gray-900">{result.request_number}</td>
                      <td className="px-4 py-2">
                        {result.success ? (
                          <span className="text-green-700 font-medium">✓ Success</span>
                        ) : (
                          <span className="text-red-700 font-medium">✗ Failed</span>
                        )}
                      </td>
                      <td className="px-4 py-2">{getStateIcon(result.state_before)}</td>
                      <td className="px-4 py-2">{getStateIcon(result.state_after)}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        )}
      </div>

      {/* Recent Calls (if metrics available) */}
      {breakerMetrics && breakerMetrics.recent_calls && (
        <div className="bg-white rounded-lg shadow-md p-6 border border-gray-200">
          <h2 className="text-xl font-bold text-gray-900 mb-4">
            📋 Recent Calls (Last 20)
          </h2>
          <div className="space-y-2 max-h-96 overflow-y-auto">
            {breakerMetrics.recent_calls.slice(0, 20).map((call, idx) => (
              <div
                key={idx}
                className={`border-l-4 pl-4 py-2 ${
                  call.result === 'SUCCESS'
                    ? 'border-green-500 bg-green-50'
                    : call.result === 'REJECTED'
                    ? 'border-yellow-500 bg-yellow-50'
                    : 'border-red-500 bg-red-50'
                }`}
              >
                <div className="flex items-center justify-between">
                  <span className="font-medium text-gray-900">{call.result}</span>
                  <span className="text-sm text-gray-700">
                    {new Date(call.timestamp).toLocaleTimeString()}
                  </span>
                </div>
                {call.response_time > 0 && (
                  <div className="text-sm text-gray-800">
                    Response: {call.response_time.toFixed(2)}ms
                  </div>
                )}
                {call.error && (
                  <div className="text-sm text-red-700">{call.error}</div>
                )}
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
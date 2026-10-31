import axios from 'axios'

const obtenerBaseURL = () => {
  if (import.meta.env.VITE_API_BASE_URL) {
    return import.meta.env.VITE_API_BASE_URL
  }
  // En dispositivos móviles / tablets en la misma red local (LAN)
  if (typeof window !== 'undefined' && window.location?.hostname) {
    return `http://${window.location.hostname}:8000/api/v1`
  }
  return 'http://localhost:8000/api/v1'
}

const api = axios.create({
  baseURL: obtenerBaseURL(),
  headers: {
    'Content-Type': 'application/json'
  },
  timeout: 10000
})

// Manejo centralizado de errores
api.interceptors.response.use(
  response => response,
  error => {
    const mensaje = error.response?.data?.detail || 'Error de comunicación con el servidor'
    console.error('API Error:', mensaje)
    return Promise.reject(error)
  }
)

export default api

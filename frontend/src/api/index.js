import axios from 'axios'

const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api/v1',
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

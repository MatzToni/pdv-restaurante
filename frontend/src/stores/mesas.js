import { defineStore } from 'pinia'
import api from '../api'

export const useMesasStore = defineStore('mesas', {
  state: () => ({
    mesas: [],
    areas: [],
    cargando: false,
    error: null
  }),
  getters: {
    mesasLibres: (state) => state.mesas.filter(m => m.estado === 'libre'),
    mesasOcupadas: (state) => state.mesas.filter(m => m.estado === 'ocupada'),
    mesasCuenta: (state) => state.mesas.filter(m => m.estado === 'cuenta'),
  },
  actions: {
    async cargarMesas() {
      this.cargando = true
      try {
        const [resMesas, resAreas] = await Promise.all([
          api.get('/mesas/'),
          api.get('/mesas/areas')
        ])
        this.mesas = resMesas.data
        this.areas = resAreas.data
      } catch (err) {
        this.error = 'No se pudieron cargar las mesas'
        console.error(err)
      } finally {
        this.cargando = false
      }
    },
    async crearMesa(mesaData) {
      const { data } = await api.post('/mesas/', mesaData)
      this.mesas.push(data)
      return data
    },
    async cambiarEstadoMesa(mesaId, nuevoEstado) {
      const { data } = await api.patch(`/mesas/${mesaId}/estado`, { estado: nuevoEstado })
      const idx = this.mesas.findIndex(m => m.id === mesaId)
      if (idx !== -1) {
        this.mesas[idx].estado = data.estado
      }
      return data
    },
    async actualizarEstado(mesaId, nuevoEstado) {
      return this.cambiarEstadoMesa(mesaId, nuevoEstado)
    }
  }
})

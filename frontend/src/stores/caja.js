import { defineStore } from 'pinia'
import api from '../api'

export const useCajaStore = defineStore('caja', {
  state: () => ({
    cuentasPendientes: [],
    turnoActivo: null,
    resumenCorteX: null,
    cargando: false
  }),
  actions: {
    async cargarCuentasPendientes(silencioso = false) {
      if (!silencioso) this.cargando = true
      try {
        const { data } = await api.get('/caja/cuentas-pendientes')
        this.cuentasPendientes = data
      } catch (err) {
        console.error('Error cargando cuentas pendientes:', err)
      } finally {
        if (!silencioso) this.cargando = false
      }
    },
    async obtenerTurnoActivo() {
      try {
        const { data } = await api.get('/caja/turno-activo')
        this.turnoActivo = data
        return data
      } catch (err) {
        console.error('Error obteniendo turno activo:', err)
        return null
      }
    },
    async abrirTurno(payload) {
      const { data } = await api.post('/caja/abrir-turno', payload)
      await this.obtenerTurnoActivo()
      return data
    },
    async cerrarTurno(payload) {
      const { data } = await api.post('/caja/cerrar-turno', payload)
      this.turnoActivo = null
      return data
    },
    async cobrarOrden(pagoPayload) {
      const { data } = await api.post('/caja/cobrar', pagoPayload)
      await this.cargarCuentasPendientes(true)
      await this.obtenerTurnoActivo()
      return data
    },
    async aplicarDescuento(payload) {
      const { data } = await api.post('/caja/aplicar-descuento', payload)
      await this.cargarCuentasPendientes(true)
      return data
    },
    async quitarDescuento(ordenId) {
      const { data } = await api.delete(`/caja/quitar-descuento/${ordenId}`)
      await this.cargarCuentasPendientes(true)
      return data
    },
    async obtenerCorteX() {
      try {
        const { data } = await api.get('/caja/corte-x')
        this.resumenCorteX = data
        return data
      } catch (err) {
        console.error('Error obteniendo corte X:', err)
        return null
      }
    }
  }
})

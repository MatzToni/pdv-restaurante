import { defineStore } from 'pinia'
import api from '../api'

export const useCajaStore = defineStore('caja', {
  state: () => ({
    cuentasPendientes: [],
    resumenCorteX: null,
    cargando: false
  }),
  actions: {
    async cargarCuentasPendientes() {
      this.cargando = true
      try {
        const { data } = await api.get('/caja/cuentas-pendientes')
        this.cuentasPendientes = data
      } catch (err) {
        console.error('Error cargando cuentas pendientes:', err)
      } finally {
        this.cargando = false
      }
    },
    async cobrarOrden(pagoPayload) {
      const { data } = await api.post('/caja/cobrar', pagoPayload)
      await this.cargarCuentasPendientes()
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

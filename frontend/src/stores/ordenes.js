import { defineStore } from 'pinia'
import api from '../api'

export const useOrdenesStore = defineStore('ordenes', {
  state: () => ({
    ordenesActivas: [],
    cargando: false
  }),
  actions: {
    async cargarOrdenesActivas() {
      this.cargando = true
      try {
        const { data } = await api.get('/ordenes/activas')
        this.ordenesActivas = data
      } catch (err) {
        console.error('Error cargando órdenes activas:', err)
      } finally {
        this.cargando = false
      }
    },
    async obtenerOrdenActivaMesa(mesaId) {
      try {
        const { data } = await api.get(`/ordenes/mesa/${mesaId}/activa`)
        return data
      } catch (err) {
        console.error('Error obteniendo orden activa de la mesa:', err)
        return null
      }
    },
    async enviarComanda(ordenData) {
      const { data } = await api.post('/ordenes/', ordenData)
      await this.cargarOrdenesActivas()
      return data
    },
    async agregarItemsAOrden(ordenId, itemsData) {
      const { data } = await api.post(`/ordenes/${ordenId}/items`, { items: itemsData })
      await this.cargarOrdenesActivas()
      return data
    },
    async cambiarEstadoItem(itemId, nuevoEstado) {
      const { data } = await api.patch(`/ordenes/items/${itemId}/estado`, { estado: nuevoEstado })
      await this.cargarOrdenesActivas()
      return data
    },
    async reportarObservacionItem(itemId, observacion) {
      const { data } = await api.post(`/ordenes/items/${itemId}/observacion`, { observacion })
      await this.cargarOrdenesActivas()
      return data
    },
    async resolverObservacionItem(itemId, { accion, respuesta }) {
      const { data } = await api.post(`/ordenes/items/${itemId}/resolver-observacion`, {
        accion,
        respuesta
      })
      await this.cargarOrdenesActivas()
      return data
    },
    async pedirCuenta(ordenId) {
      const { data } = await api.post(`/ordenes/${ordenId}/pedir-cuenta`)
      await this.cargarOrdenesActivas()
      return data
    },
    async cancelarItem(itemId, { pin_autorizacion, motivo, genera_merma }) {
      const { data } = await api.post(`/ordenes/items/${itemId}/cancelar`, {
        pin_autorizacion,
        motivo,
        genera_merma
      })
      await this.cargarOrdenesActivas()
      return data
    },
    async cancelarOrden(ordenId, { pin_autorizacion, motivo }) {
      const { data } = await api.post(`/ordenes/${ordenId}/cancelar`, {
        pin_autorizacion,
        motivo
      })
      await this.cargarOrdenesActivas()
      return data
    }
  }
})

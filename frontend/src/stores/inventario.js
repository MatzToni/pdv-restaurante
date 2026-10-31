import { defineStore } from 'pinia'
import api from '../api'

export const useInventarioStore = defineStore('inventario', {
  state: () => ({
    articulos: [],
    tipoActivo: 'todos',
    cargando: false
  }),
  getters: {
    articulosFiltrados: (state) => {
      if (state.tipoActivo === 'todos') return state.articulos
      return state.articulos.filter(a => a.tipo === state.tipoActivo)
    },
    articulosBajoStock: (state) => {
      return state.articulos.filter(a => Number(a.stock_actual) <= Number(a.stock_minimo))
    }
  },
  actions: {
    async cargarArticulos(tipo = null) {
      this.cargando = true
      try {
        const url = tipo && tipo !== 'todos' ? `/inventario/articulos?tipo=${tipo}` : '/inventario/articulos'
        const { data } = await api.get(url)
        this.articulos = data
      } catch (err) {
        console.error('Error cargando inventario:', err)
      } finally {
        this.cargando = false
      }
    },
    async registrarArticulo(nuevoArticulo) {
      const { data } = await api.post('/inventario/articulos', nuevoArticulo)
      this.articulos.push(data)
      return data
    },
    async registrarMovimiento(movimiento) {
      const { data } = await api.post('/inventario/movimientos', movimiento)
      await this.cargarArticulos()
      return data
    }
  }
})

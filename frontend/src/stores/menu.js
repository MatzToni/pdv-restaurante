import { defineStore } from 'pinia'
import api from '../api'

export const useMenuStore = defineStore('menu', {
  state: () => ({
    categorias: [],
    productos: [],
    cargando: false
  }),
  actions: {
    async cargarCatalogo() {
      this.cargando = true
      try {
        const [resCat, resProd] = await Promise.all([
          api.get('/menu/categorias'),
          api.get('/menu/productos')
        ])
        this.categorias = resCat.data
        this.productos = resProd.data
      } catch (err) {
        console.error('Error cargando catálogo:', err)
      } finally {
        this.cargando = false
      }
    },
    async crearProducto(prodData) {
      const { data } = await api.post('/menu/productos', prodData)
      this.productos.push(data)
      return data
    },
    async crearCategoria(catData) {
      const { data } = await api.post('/menu/categorias', catData)
      this.categorias.push(data)
      return data
    }
  }
})

import { defineStore } from 'pinia'
import api from '../api'

export const useMenuStore = defineStore('menu', {
  state: () => ({
    categorias: [],
    productos: [],
    cargando: false
  }),
  actions: {
    async cargarCatalogo(incluirInactivos = false) {
      this.cargando = true
      try {
        const [resCat, resProd] = await Promise.all([
          api.get('/menu/categorias'),
          api.get(`/menu/productos?incluir_inactivos=${incluirInactivos}`)
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
      await this.cargarCatalogo(true)
      return data
    },
    async actualizarProducto(id, prodData) {
      const { data } = await api.put(`/menu/productos/${id}`, prodData)
      await this.cargarCatalogo(true)
      return data
    },
    async alternarDisponibilidad(id) {
      const { data } = await api.patch(`/menu/productos/${id}/disponibilidad`)
      const prod = this.productos.find(p => p.id === id)
      if (prod) prod.disponible = data.disponible
      return data
    },
    async eliminarProducto(id) {
      await api.delete(`/menu/productos/${id}`)
      await this.cargarCatalogo(true)
    },
    async subirImagen(file) {
      const formData = new FormData()
      formData.append('file', file)
      const { data } = await api.post('/menu/productos/subir-imagen', formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      })
      return data
    },
    obtenerUrlImagen(imagenUrl) {
      if (!imagenUrl) return null
      if (imagenUrl.startsWith('http://') || imagenUrl.startsWith('https://') || imagenUrl.startsWith('data:image/')) {
        return imagenUrl
      }
      const apiBase = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api/v1'
      const rootServer = apiBase.replace(/\/api\/v1\/?$/, '')
      return `${rootServer}${imagenUrl.startsWith('/') ? '' : '/'}${imagenUrl}`
    },
    async crearCategoria(catData) {
      const { data } = await api.post('/menu/categorias', catData)
      await this.cargarCatalogo(true)
      return data
    },
    async actualizarCategoria(id, catData) {
      const { data } = await api.put(`/menu/categorias/${id}`, catData)
      await this.cargarCatalogo(true)
      return data
    },
    async eliminarCategoria(id) {
      await api.delete(`/menu/categorias/${id}`)
      await this.cargarCatalogo(true)
    }
  }
})

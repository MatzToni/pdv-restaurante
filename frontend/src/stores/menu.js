import { defineStore } from 'pinia'
import api from '../api'

export const useMenuStore = defineStore('menu', {
  state: () => ({
    categorias: [],
    productos: [],
    menuDelDia: null,
    cargando: false
  }),
  actions: {
    async cargarCatalogo(incluirInactivos = false) {
      this.cargando = true
      try {
        const [resCat, resProd, resMdd] = await Promise.all([
          api.get('/menu/categorias'),
          api.get(`/menu/productos?incluir_inactivos=${incluirInactivos}`),
          api.get('/menu/menu-del-dia')
        ])
        this.categorias = resCat.data
        this.productos = resProd.data
        this.menuDelDia = resMdd.data
      } catch (err) {
        console.error('Error cargando catálogo:', err)
      } finally {
        this.cargando = false
      }
    },
    async cargarMenuDelDia() {
      try {
        const { data } = await api.get('/menu/menu-del-dia')
        this.menuDelDia = data
        return data
      } catch (err) {
        console.error('Error cargando menú del día:', err)
        return null
      }
    },
    async guardarMenuDelDia(configData) {
      const { data } = await api.put('/menu/menu-del-dia', configData)
      this.menuDelDia = data
      await this.cargarCatalogo(true)
      return data
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
      if (import.meta.env.VITE_API_BASE_URL) {
        const rootServer = import.meta.env.VITE_API_BASE_URL.replace(/\/api\/v1\/?$/, '')
        return `${rootServer}${imagenUrl.startsWith('/') ? '' : '/'}${imagenUrl}`
      }
      const hostname = typeof window !== 'undefined' && window.location?.hostname ? window.location.hostname : 'localhost'
      return `http://${hostname}:8000${imagenUrl.startsWith('/') ? '' : '/'}${imagenUrl}`
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

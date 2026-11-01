import { defineStore } from 'pinia'
import api from '../api'

export const PERMISOS_POR_ROL = {
  administrador: ['mesas', 'pos', 'cocina', 'caja', 'inventario', 'usuarios', 'platillos'],
  gerente: ['mesas', 'pos', 'cocina', 'caja', 'inventario', 'platillos'],
  jefe: ['mesas', 'pos', 'cocina', 'caja'],
  cocina: ['cocina'],
  mesero: ['mesas', 'pos'],
  auxiliar_general: ['mesas', 'pos', 'inventario']
}

// Ruta inicial por defecto según el rol del usuario
export const RUTA_INICIAL_POR_ROL = {
  administrador: '/',
  gerente: '/',
  jefe: '/',
  cocina: '/cocina',
  mesero: '/',
  auxiliar_general: '/inventario'
}

export const useAuthStore = defineStore('auth', {
  state: () => ({
    usuarioActual: JSON.parse(localStorage.getItem('eden_usuario')) || null,
    usuarios: []
  }),
  getters: {
    estaAutenticado: (state) => !!state.usuarioActual,
    rolActual: (state) => state.usuarioActual?.rol || null,
    rutasPermitidas: (state) => {
      if (!state.usuarioActual) return []
      return PERMISOS_POR_ROL[state.usuarioActual.rol] || []
    }
  },
  actions: {
    tienePermiso(nombreRuta) {
      if (!this.usuarioActual) return false
      const permitidas = PERMISOS_POR_ROL[this.usuarioActual.rol] || []
      return permitidas.includes(nombreRuta)
    },
    async cargarUsuarios() {
      try {
        const { data } = await api.get('/usuarios/')
        this.usuarios = data
        return data
      } catch (err) {
        console.error('Error cargando lista de usuarios:', err)
        return []
      }
    },
    async loginConPin(pin, usuarioId = null) {
      const payload = { pin: String(pin).trim() }
      if (usuarioId) {
        payload.usuario_id = usuarioId
      }
      const { data } = await api.post('/usuarios/login-pin', payload)
      this.establecerSesion(data)
      return data
    },
    async loginConPassword(email, password) {
      const { data } = await api.post('/usuarios/login-password', { email, password })
      this.establecerSesion(data)
      return data
    },
    establecerSesion(usuario) {
      this.usuarioActual = usuario
      localStorage.setItem('eden_usuario', JSON.stringify(usuario))
    },
    logout() {
      this.usuarioActual = null
      localStorage.removeItem('eden_usuario')
    },
    async crearUsuario(nuevoUsuario) {
      const { data } = await api.post('/usuarios/', nuevoUsuario)
      this.usuarios.push(data)
      return data
    },
    async actualizarUsuario(id, datosUsuario) {
      const { data } = await api.patch(`/usuarios/${id}`, datosUsuario)
      await this.cargarUsuarios()
      if (this.usuarioActual && this.usuarioActual.id === id) {
        this.establecerSesion({ ...this.usuarioActual, ...data })
      }
      return data
    },
    async verificarPin(pin) {
      const { data } = await api.post('/usuarios/verificar-pin', { pin })
      return data
    }
  }
})

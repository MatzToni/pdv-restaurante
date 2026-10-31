import { defineStore } from 'pinia'
import api from '../api'

export const PERMISOS_POR_ROL = {
  administrador: ['mesas', 'pos', 'cocina', 'caja', 'inventario', 'usuarios'],
  gerente: ['mesas', 'pos', 'cocina', 'caja', 'inventario'],
  jefe: ['mesas', 'pos', 'cocina', 'caja'],
  cocina: ['cocina'],
  mesero: ['mesas', 'pos'],
  auxiliar_general: ['inventario']
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
    async loginConPin(pin) {
      // Si la lista de usuarios aún no está cargada, la solicitamos
      if (this.usuarios.length === 0) {
        await this.cargarUsuarios()
      }
      const usuarioEncontrado = this.usuarios.find(u => u.pin_seguridad === pin && u.activo)
      if (!usuarioEncontrado) {
        throw new Error('PIN incorrecto o usuario inactivo')
      }
      this.establecerSesion(usuarioEncontrado)
      return usuarioEncontrado
    },
    async loginConUsuario(usuario) {
      this.establecerSesion(usuario)
      return usuario
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
    async verificarPin(pin) {
      const { data } = await api.post('/usuarios/verificar-pin', { pin })
      return data
    }
  }
})

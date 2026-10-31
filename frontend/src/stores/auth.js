import { defineStore } from 'pinia'
import api from '../api'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    usuarioActual: {
      id: 5,
      nombre: 'Carlos López',
      email: 'carlos@edencafe.com',
      rol: 'mesero'
    },
    usuarios: []
  }),
  actions: {
    async cargarUsuarios() {
      try {
        const { data } = await api.get('/usuarios/')
        this.usuarios = data
        return data
      } catch (err) {
        console.error('Error cargando usuarios:', err)
      }
    },
    async crearUsuario(nuevoUsuario) {
      const { data } = await api.post('/usuarios/', nuevoUsuario)
      this.usuarios.push(data)
      return data
    },
    async verificarPin(pin) {
      const { data } = await api.post('/usuarios/verificar-pin', { pin })
      return data
    },
    cambiarUsuarioTurno(usuario) {
      this.usuarioActual = usuario
    }
  }
})

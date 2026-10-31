import { defineStore } from 'pinia'

export const useThemeStore = defineStore('theme', {
  state: () => ({
    tema: localStorage.getItem('eden_tema') || 'sistema' // 'claro' | 'oscuro' | 'sistema'
  }),
  actions: {
    aplicarTema() {
      const root = document.documentElement
      let esOscuro = false

      if (this.tema === 'oscuro') {
        esOscuro = true
      } else if (this.tema === 'claro') {
        esOscuro = false
      } else {
        // Modo Sistema
        esOscuro = window.matchMedia('(prefers-color-scheme: dark)').matches
      }

      if (esOscuro) {
        root.classList.add('dark')
      } else {
        root.classList.remove('dark')
      }
    },
    establecerTema(nuevoTema) {
      this.tema = nuevoTema
      localStorage.setItem('eden_tema', nuevoTema)
      this.aplicarTema()
    },
    iniciarEscuchaSistema() {
      this.aplicarTema()
      window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', () => {
        if (this.tema === 'sistema') {
          this.aplicarTema()
        }
      })
    }
  }
})

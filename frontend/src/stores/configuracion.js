import { defineStore } from 'pinia'
import api from '../api'

const CONFIG_STORAGE_KEY = 'eden_configuracion'

const CONFIG_DEFAULT = {
  nombreRestaurante: 'Edén Café',
  slogan: 'Comida Tradicional y Café de Especialidad',
  logoUrl: '/logo.png',
  telefono: '961 123 4567',
  direccion: 'Av. Central Poniente #123, Centro',
  rfc: 'ECA240101XYZ',
  diasServicio: 'Lunes a Domingo',
  horarioApertura: '08:00',
  horarioCierre: '21:00',
  mensajeTicket: '🎉 ¡Gracias por su visita y preferencia! Vuelva pronto.',
  tituloCarta: 'Nuestra Carta',
  subtituloCarta: 'Platillos preparados al momento con ingredientes frescos, recetas mexicanas tradicionales y café tostado artesanal.',
  notaPieCarta: 'Precios incluyen IVA. Para dudas sobre ingredientes o alérgenos, consulta a tu mesero.',
  anchoPapelTicket: '80mm',
  moneda: 'MXN',
  simboloMoneda: '$',
  abrirCajonAutomatico: true,
  modoImpresion: 'navegador'
}

export const useConfiguracionStore = defineStore('configuracion', {
  state: () => {
    let guardado = {}
    try {
      const raw = localStorage.getItem(CONFIG_STORAGE_KEY)
      if (raw) guardado = JSON.parse(raw)
    } catch (e) {
      console.error('Error leyendo configuración de localStorage:', e)
    }
    return {
      ...CONFIG_DEFAULT,
      ...guardado,
      cargando: false
    }
  },
  actions: {
    mapFromBackend(data) {
      if (!data) return
      if (data.nombre_restaurante !== undefined) this.nombreRestaurante = data.nombre_restaurante
      if (data.slogan !== undefined) this.slogan = data.slogan
      if (data.logo_url !== undefined) this.logoUrl = data.logo_url
      if (data.telefono !== undefined) this.telefono = data.telefono
      if (data.direccion !== undefined) this.direccion = data.direccion
      if (data.rfc !== undefined) this.rfc = data.rfc
      if (data.dias_servicio !== undefined) this.diasServicio = data.dias_servicio
      if (data.horario_apertura !== undefined) this.horarioApertura = data.horario_apertura
      if (data.horario_cierre !== undefined) this.horarioCierre = data.horario_cierre
      if (data.mensaje_ticket !== undefined) this.mensajeTicket = data.mensaje_ticket
      if (data.titulo_carta !== undefined) this.tituloCarta = data.titulo_carta
      if (data.subtitulo_carta !== undefined) this.subtituloCarta = data.subtitulo_carta
      if (data.nota_pie_carta !== undefined) this.notaPieCarta = data.nota_pie_carta
      if (data.ancho_papel_ticket !== undefined) this.anchoPapelTicket = data.ancho_papel_ticket
      if (data.moneda !== undefined) this.moneda = data.moneda
      if (data.simbolo_moneda !== undefined) this.simboloMoneda = data.simbolo_moneda
      if (data.abrir_cajon_automatico !== undefined) this.abrirCajonAutomatico = data.abrir_cajon_automatico
      if (data.modo_impresion !== undefined) this.modoImpresion = data.modo_impresion

      try {
        localStorage.setItem(CONFIG_STORAGE_KEY, JSON.stringify(this.$state))
      } catch (e) {}
    },

    mapToBackend(datos) {
      const payload = {}
      if (datos.nombreRestaurante !== undefined) payload.nombre_restaurante = datos.nombreRestaurante
      if (datos.slogan !== undefined) payload.slogan = datos.slogan
      if (datos.logoUrl !== undefined) payload.logo_url = datos.logoUrl
      if (datos.telefono !== undefined) payload.telefono = datos.telefono
      if (datos.direccion !== undefined) payload.direccion = datos.direccion
      if (datos.rfc !== undefined) payload.rfc = datos.rfc
      if (datos.diasServicio !== undefined) payload.dias_servicio = datos.diasServicio
      if (datos.horarioApertura !== undefined) payload.horario_apertura = datos.horarioApertura
      if (datos.horarioCierre !== undefined) payload.horario_cierre = datos.horarioCierre
      if (datos.mensajeTicket !== undefined) payload.mensaje_ticket = datos.mensajeTicket
      if (datos.tituloCarta !== undefined) payload.titulo_carta = datos.tituloCarta
      if (datos.subtituloCarta !== undefined) payload.subtitulo_carta = datos.subtituloCarta
      if (datos.notaPieCarta !== undefined) payload.nota_pie_carta = datos.notaPieCarta
      if (datos.anchoPapelTicket !== undefined) payload.ancho_papel_ticket = datos.anchoPapelTicket
      if (datos.moneda !== undefined) payload.moneda = datos.moneda
      if (datos.simboloMoneda !== undefined) payload.simbolo_moneda = datos.simboloMoneda
      if (datos.abrirCajonAutomatico !== undefined) payload.abrir_cajon_automatico = datos.abrirCajonAutomatico
      if (datos.modoImpresion !== undefined) payload.modo_impresion = datos.modoImpresion
      return payload
    },

    async cargarConfiguracion() {
      this.cargando = true
      try {
        const { data } = await api.get('/configuracion/')
        this.mapFromBackend(data)
        return data
      } catch (err) {
        console.warn('No se pudo conectar con el endpoint de configuración, usando caché local:', err)
        return null
      } finally {
        this.cargando = false
      }
    },

    async guardarConfiguracion(nuevosDatos) {
      Object.assign(this, nuevosDatos)
      try {
        localStorage.setItem(CONFIG_STORAGE_KEY, JSON.stringify(this.$state))
      } catch (e) {}

      try {
        const payload = this.mapToBackend(nuevosDatos)
        const { data } = await api.put('/configuracion/', payload)
        this.mapFromBackend(data)
        return data
      } catch (err) {
        console.error('Error guardando configuración en servidor:', err)
      }
    },

    async subirLogo(archivo) {
      return new Promise((resolve, reject) => {
        if (!archivo) {
          reject(new Error('No se seleccionó ningún archivo.'))
          return
        }
        if (!archivo.type.startsWith('image/')) {
          reject(new Error('El archivo seleccionado debe ser una imagen (PNG, JPG, WEBP, etc.).'))
          return
        }

        const reader = new FileReader()
        reader.onload = async (e) => {
          const base64 = e.target.result
          this.logoUrl = base64
          await this.guardarConfiguracion({ logoUrl: base64 })
          resolve(base64)
        }
        reader.onerror = (err) => reject(err)
        reader.readAsDataURL(archivo)
      })
    },

    async restablecerValores() {
      Object.assign(this, CONFIG_DEFAULT)
      try {
        localStorage.removeItem(CONFIG_STORAGE_KEY)
      } catch (e) {}
      try {
        const payload = this.mapToBackend(CONFIG_DEFAULT)
        const { data } = await api.put('/configuracion/', payload)
        this.mapFromBackend(data)
      } catch (err) {}
    }
  }
})

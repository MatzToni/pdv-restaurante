<template>
  <div class="min-h-screen flex flex-col justify-center items-center bg-slate-100 dark:bg-slate-950 p-4 transition-colors">
    <!-- Contenedor Principal de Login -->
    <div class="max-w-md w-full bg-white dark:bg-slate-900 rounded-3xl p-6 sm:p-8 shadow-2xl border border-slate-200 dark:border-slate-800 space-y-6 transition-colors">
      <!-- Identidad de Marca -->
      <div class="flex flex-col items-center text-center space-y-2">
        <img 
          src="/logo.png" 
          alt="Edén Café Logo" 
          class="w-20 h-20 object-contain rounded-full shadow-md"
        />
        <h1 class="text-2xl font-black text-slate-800 dark:text-slate-100 tracking-tight">Edén Café</h1>
        <p class="text-xs text-slate-500 dark:text-slate-400">Ingreso al Sistema de Punto de Venta</p>
      </div>

      <!-- Selector de Modo de Acceso (PIN o Selección Rápida) -->
      <div class="flex bg-slate-100 dark:bg-slate-800 p-1 rounded-xl">
        <button
          @click="modoAcceso = 'pin'"
          :class="[
            'flex-1 py-1.5 rounded-lg text-xs font-bold transition-all',
            modoAcceso === 'pin' 
              ? 'bg-white dark:bg-slate-700 text-slate-900 dark:text-white shadow-sm' 
              : 'text-slate-500 dark:text-slate-400 hover:text-slate-800'
          ]"
        >
          Teclado PIN
        </button>
        <button
          @click="modoAcceso = 'perfil'"
          :class="[
            'flex-1 py-1.5 rounded-lg text-xs font-bold transition-all',
            modoAcceso === 'perfil' 
              ? 'bg-white dark:bg-slate-700 text-slate-900 dark:text-white shadow-sm' 
              : 'text-slate-500 dark:text-slate-400 hover:text-slate-800'
          ]"
        >
          Elegir Perfil
        </button>
      </div>

      <!-- Modo PIN Táctil -->
      <div v-if="modoAcceso === 'pin'" class="space-y-4">
        <!-- Pantalla de Dígitos PIN -->
        <div class="flex justify-center items-center gap-3 py-2">
          <div 
            v-for="i in 4" 
            :key="i"
            :class="[
              'w-4 h-4 rounded-full border-2 transition-all',
              pin.length >= i 
                ? 'bg-eden-600 border-eden-600 scale-110' 
                : 'border-slate-300 dark:border-slate-700'
            ]"
          ></div>
        </div>

        <div v-if="errorLogin" class="text-center text-xs font-bold text-rose-600 dark:text-rose-400 animate-shake">
          {{ errorLogin }}
        </div>

        <!-- Teclado Numérico Touch -->
        <div class="grid grid-cols-3 gap-2.5 max-w-xs mx-auto">
          <button 
            v-for="num in ['1', '2', '3', '4', '5', '6', '7', '8', '9']" 
            :key="num"
            @click="agregarDigito(num)"
            class="h-14 rounded-2xl bg-slate-50 dark:bg-slate-800 hover:bg-slate-200 dark:hover:bg-slate-700 text-slate-800 dark:text-slate-100 font-black text-xl shadow-sm border border-slate-200 dark:border-slate-700/50 transition active:scale-95"
          >
            {{ num }}
          </button>
          
          <button 
            @click="borrarDigito"
            class="h-14 rounded-2xl bg-rose-50 dark:bg-rose-950/40 hover:bg-rose-100 text-rose-600 dark:text-rose-400 font-bold text-sm shadow-sm border border-rose-200 dark:border-rose-900/40 transition active:scale-95"
          >
            ⌫
          </button>
          
          <button 
            @click="agregarDigito('0')"
            class="h-14 rounded-2xl bg-slate-50 dark:bg-slate-800 hover:bg-slate-200 dark:hover:bg-slate-700 text-slate-800 dark:text-slate-100 font-black text-xl shadow-sm border border-slate-200 dark:border-slate-700/50 transition active:scale-95"
          >
            0
          </button>

          <button 
            @click="enviarPin"
            :disabled="pin.length < 4 || cargando"
            class="h-14 rounded-2xl bg-eden-600 hover:bg-eden-700 disabled:opacity-50 text-white font-black text-base shadow-sm transition active:scale-95"
          >
            ✓
          </button>
        </div>
      </div>

      <!-- Modo Selección Rápida de Perfil -->
      <div v-else class="space-y-2.5 max-h-72 overflow-y-auto">
        <div v-if="authStore.usuarios.length === 0" class="text-center py-6 text-slate-400 text-xs">
          Cargando usuarios registrados...
        </div>
        <button
          v-for="u in authStore.usuarios"
          :key="u.id"
          @click="seleccionarUsuario(u)"
          class="w-full p-3 rounded-2xl border border-slate-200 dark:border-slate-800 hover:border-eden-600 dark:hover:border-eden-500 bg-slate-50 dark:bg-slate-800/60 hover:bg-eden-50/50 dark:hover:bg-eden-950/30 flex justify-between items-center transition active:scale-98 text-left"
        >
          <div>
            <div class="font-bold text-sm text-slate-800 dark:text-slate-100">{{ u.nombre }}</div>
            <div class="text-xs text-slate-400 capitalize">Rol: {{ u.rol }}</div>
          </div>
          <span class="text-xs font-mono text-slate-400 bg-white dark:bg-slate-700 px-2 py-1 rounded-lg border border-slate-200 dark:border-slate-600">
            PIN: {{ u.pin_seguridad }}
          </span>
        </button>
      </div>

      <!-- Selector de Tema Inferior -->
      <div class="pt-4 border-t border-slate-100 dark:border-slate-800 flex justify-between items-center">
        <span class="text-xs text-slate-500 dark:text-slate-400">Apariencia:</span>
        <div class="flex gap-1 bg-slate-100 dark:bg-slate-800 p-1 rounded-xl">
          <button
            @click="themeStore.establecerTema('claro')"
            :class="[
              'px-2.5 py-1 rounded-lg text-xs font-bold transition-all',
              themeStore.tema === 'claro' ? 'bg-white dark:bg-slate-700 text-amber-600 shadow-sm' : 'text-slate-500'
            ]"
            title="Modo Claro"
          >
            ☀️ Claro
          </button>
          <button
            @click="themeStore.establecerTema('oscuro')"
            :class="[
              'px-2.5 py-1 rounded-lg text-xs font-bold transition-all',
              themeStore.tema === 'oscuro' ? 'bg-white dark:bg-slate-700 text-sky-400 shadow-sm' : 'text-slate-500'
            ]"
            title="Modo Oscuro"
          >
            🌙 Oscuro
          </button>
          <button
            @click="themeStore.establecerTema('sistema')"
            :class="[
              'px-2.5 py-1 rounded-lg text-xs font-bold transition-all',
              themeStore.tema === 'sistema' ? 'bg-white dark:bg-slate-700 text-emerald-500 shadow-sm' : 'text-slate-500'
            ]"
            title="Preferencia del Sistema"
          >
            💻 Auto
          </button>
        </div>
      </div>

      <!-- Enlace Público a la Carta para Clientes -->
      <div class="text-center pt-2">
        <router-link to="/carta" class="text-xs font-extrabold text-eden-600 dark:text-eden-400 hover:underline inline-flex items-center gap-1.5">
          <span>📖</span> Ver Menú Digital para Clientes →
        </router-link>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore, RUTA_INICIAL_POR_ROL } from '../stores/auth'
import { useThemeStore } from '../stores/theme'

const router = useRouter()
const authStore = useAuthStore()
const themeStore = useThemeStore()

const modoAcceso = ref('pin')
const pin = ref('')
const errorLogin = ref('')
const cargando = ref(false)

onMounted(async () => {
  await authStore.cargarUsuarios()
})

const agregarDigito = (d) => {
  if (pin.value.length < 4) {
    pin.value += d
    errorLogin.value = ''
    if (pin.value.length === 4) {
      enviarPin()
    }
  }
}

const borrarDigito = () => {
  pin.value = pin.value.slice(0, -1)
  errorLogin.value = ''
}

const enviarPin = async () => {
  if (pin.value.length !== 4) return
  cargando.value = true
  errorLogin.value = ''
  try {
    const usuario = await authStore.loginConPin(pin.value)
    redirigirSegunRol(usuario.rol)
  } catch (err) {
    errorLogin.value = 'PIN no reconocido. Intenta de nuevo.'
    pin.value = ''
  } finally {
    cargando.value = false
  }
}

const seleccionarUsuario = async (usuario) => {
  await authStore.loginConUsuario(usuario)
  redirigirSegunRol(usuario.rol)
}

const redirigirSegunRol = (rol) => {
  const rutaDestino = RUTA_INICIAL_POR_ROL[rol] || '/'
  router.push(rutaDestino)
}
</script>

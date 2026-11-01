<template>
  <div class="min-h-screen flex flex-col justify-center items-center bg-slate-100 dark:bg-slate-950 p-4 transition-colors">
    <!-- Contenedor Principal de Login -->
    <div class="max-w-md w-full bg-white dark:bg-slate-900 rounded-3xl p-6 sm:p-8 shadow-2xl border border-slate-200 dark:border-slate-800 space-y-6 transition-colors">
      <!-- Identidad de Marca -->
      <div class="flex flex-col items-center text-center space-y-2">
        <div class="w-20 h-20 rounded-full p-1 bg-white dark:bg-slate-800 border-2 border-white dark:border-white/20 shadow-md ring-2 ring-slate-200/60 dark:ring-white/10 flex items-center justify-center">
          <img 
            src="/logo.png?v=3" 
            alt="Edén Café Logo" 
            class="w-full h-full object-contain rounded-full"
          />
        </div>
        <h1 class="text-2xl font-black text-slate-800 dark:text-slate-100 tracking-tight">Edén Café</h1>
        <p class="text-xs text-slate-500 dark:text-slate-400">Ingreso al Sistema de Punto de Venta</p>
      </div>

      <!-- Selector de Modo de Acceso (Teclado PIN / Elegir Perfil / Contraseña) -->
      <div class="flex bg-slate-100 dark:bg-slate-800 p-1 rounded-xl">
        <button
          @click="cambiarModo('pin')"
          :class="[
            'flex-1 py-1.5 rounded-lg text-xs font-bold transition-all',
            modoAcceso === 'pin' 
              ? 'bg-white dark:bg-slate-700 text-slate-900 dark:text-white shadow-sm' 
              : 'text-slate-500 dark:text-slate-400 hover:text-slate-800 dark:hover:text-slate-200'
          ]"
        >
          Teclado PIN
        </button>
        <button
          @click="cambiarModo('perfil')"
          :class="[
            'flex-1 py-1.5 rounded-lg text-xs font-bold transition-all',
            modoAcceso === 'perfil' 
              ? 'bg-white dark:bg-slate-700 text-slate-900 dark:text-white shadow-sm' 
              : 'text-slate-500 dark:text-slate-400 hover:text-slate-800 dark:hover:text-slate-200'
          ]"
        >
          Elegir Perfil
        </button>
        <button
          @click="cambiarModo('password')"
          :class="[
            'flex-1 py-1.5 rounded-lg text-xs font-bold transition-all',
            modoAcceso === 'password' 
              ? 'bg-white dark:bg-slate-700 text-slate-900 dark:text-white shadow-sm' 
              : 'text-slate-500 dark:text-slate-400 hover:text-slate-800 dark:hover:text-slate-200'
          ]"
        >
          Contraseña
        </button>
      </div>

      <!-- ======================================================== -->
      <!-- MODO 1: TECLADO PIN DIRECTO                              -->
      <!-- ======================================================== -->
      <div v-if="modoAcceso === 'pin'" class="space-y-4">
        <div class="text-center text-xs font-semibold text-slate-500 dark:text-slate-400">
          Introduce tu PIN confidencial de 4 dígitos:
        </div>

        <!-- Pantalla de Dígitos PIN -->
        <div class="flex justify-center items-center gap-3 py-2">
          <div 
            v-for="i in 4" 
            :key="i"
            :class="[
              'w-4 h-4 rounded-full border-2 transition-all',
              pin.length >= i 
                ? 'bg-eden-600 border-eden-600 scale-110 shadow-xs' 
                : 'border-slate-300 dark:border-slate-700'
            ]"
          ></div>
        </div>

        <div v-if="errorLogin" class="text-center text-xs font-bold text-rose-600 dark:text-rose-400">
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
            title="Borrar dígito"
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
            @click="enviarPinDirecto"
            :disabled="pin.length < 4 || cargando"
            class="h-14 rounded-2xl bg-eden-600 hover:bg-eden-700 disabled:opacity-50 text-white font-black text-base shadow-sm transition active:scale-95 flex items-center justify-center"
          >
            <span v-if="cargando" class="animate-spin">⏳</span>
            <span v-else>✓</span>
          </button>
        </div>
      </div>

      <!-- ======================================================== -->
      <!-- MODO 2: ELEGIR PERFIL + VALIDACIÓN ESTRICTA DE PIN       -->
      <!-- ======================================================== -->
      <div v-else-if="modoAcceso === 'perfil'" class="space-y-4">
        <!-- Paso A: Lista de Perfiles -->
        <div v-if="!usuarioSeleccionado" class="space-y-2.5 max-h-80 overflow-y-auto no-scrollbar">
          <div class="text-xs font-semibold text-slate-500 dark:text-slate-400 pb-1">
            Selecciona tu perfil de colaborador:
          </div>

          <div v-if="authStore.usuarios.length === 0" class="text-center py-6 text-slate-400 text-xs">
            No hay colaboradores registrados todavía.
          </div>

          <button
            v-for="u in authStore.usuarios"
            :key="u.id"
            @click="seleccionarPerfil(u)"
            class="w-full p-3.5 rounded-2xl border border-slate-200 dark:border-slate-800 hover:border-eden-600 dark:hover:border-eden-500 bg-slate-50 dark:bg-slate-800/60 hover:bg-eden-50/50 dark:hover:bg-eden-950/30 flex justify-between items-center transition active:scale-[0.98] text-left group"
          >
            <div class="flex items-center gap-3">
              <div class="w-10 h-10 rounded-xl bg-eden-100 dark:bg-eden-950/60 text-eden-800 dark:text-eden-300 font-black flex items-center justify-center text-sm shadow-xs border border-eden-200 dark:border-eden-800/50 group-hover:scale-105 transition-transform">
                {{ u.nombre.charAt(0) }}
              </div>
              <div>
                <div class="font-bold text-sm text-slate-800 dark:text-slate-100">{{ u.nombre }}</div>
                <div class="text-xs text-slate-400 capitalize">Rol: {{ u.rol }}</div>
              </div>
            </div>

            <!-- Candado de seguridad (Nunca el PIN) -->
            <span class="inline-flex items-center gap-1 text-2xs font-bold text-slate-500 dark:text-slate-400 bg-white dark:bg-slate-700/80 px-2.5 py-1 rounded-lg border border-slate-200 dark:border-slate-600">
              <span>🔒</span> Requiere PIN
            </span>
          </button>
        </div>

        <!-- Paso B: Validación de PIN para el Perfil Seleccionado -->
        <div v-else class="space-y-4">
          <!-- Banner del perfil seleccionado -->
          <div class="p-3 bg-eden-50 dark:bg-eden-950/40 rounded-2xl border border-eden-200 dark:border-eden-800/60 flex items-center justify-between">
            <div class="flex items-center gap-2.5">
              <div class="w-9 h-9 rounded-xl bg-eden-600 text-white font-black flex items-center justify-center text-sm shadow-xs">
                {{ usuarioSeleccionado.nombre.charAt(0) }}
              </div>
              <div>
                <div class="font-black text-sm text-slate-800 dark:text-slate-100">
                  {{ usuarioSeleccionado.nombre }}
                </div>
                <div class="text-3xs font-bold text-eden-700 dark:text-eden-400 capitalize">
                  {{ usuarioSeleccionado.rol }}
                </div>
              </div>
            </div>

            <button 
              @click="deseleccionarPerfil"
              class="text-xs font-bold text-slate-500 hover:text-slate-800 dark:text-slate-400 dark:hover:text-white px-2 py-1 rounded-lg hover:bg-slate-200/60 dark:hover:bg-slate-800 transition"
            >
              ← Cambiar
            </button>
          </div>

          <div class="text-center text-xs font-semibold text-slate-600 dark:text-slate-300">
            Ingresa tu PIN de 4 dígitos para autorizar el acceso:
          </div>

          <!-- Pantalla de Dígitos PIN -->
          <div class="flex justify-center items-center gap-3 py-1">
            <div 
              v-for="i in 4" 
              :key="i"
              :class="[
                'w-4 h-4 rounded-full border-2 transition-all',
                pin.length >= i 
                  ? 'bg-eden-600 border-eden-600 scale-110 shadow-xs' 
                  : 'border-slate-300 dark:border-slate-700'
              ]"
            ></div>
          </div>

          <div v-if="errorLogin" class="text-center text-xs font-bold text-rose-600 dark:text-rose-400">
            {{ errorLogin }}
          </div>

          <!-- Teclado Numérico Touch -->
          <div class="grid grid-cols-3 gap-2.5 max-w-xs mx-auto">
            <button 
              v-for="num in ['1', '2', '3', '4', '5', '6', '7', '8', '9']" 
              :key="num"
              @click="agregarDigitoPerfil(num)"
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
              @click="agregarDigitoPerfil('0')"
              class="h-14 rounded-2xl bg-slate-50 dark:bg-slate-800 hover:bg-slate-200 dark:hover:bg-slate-700 text-slate-800 dark:text-slate-100 font-black text-xl shadow-sm border border-slate-200 dark:border-slate-700/50 transition active:scale-95"
            >
              0
            </button>

            <button 
              @click="enviarPinPerfil"
              :disabled="pin.length < 4 || cargando"
              class="h-14 rounded-2xl bg-eden-600 hover:bg-eden-700 disabled:opacity-50 text-white font-black text-base shadow-sm transition active:scale-95 flex items-center justify-center"
            >
              <span v-if="cargando" class="animate-spin">⏳</span>
              <span v-else>✓</span>
            </button>
          </div>
        </div>
      </div>

      <!-- ======================================================== -->
      <!-- MODO 3: INGRESO POR CORREO Y CONTRASEÑA (ADMINISTRACIÓN) -->
      <!-- ======================================================== -->
      <div v-else class="space-y-4">
        <div class="text-center text-xs font-semibold text-slate-500 dark:text-slate-400">
          Ingreso administrativo con credenciales de cuenta:
        </div>

        <form @submit.prevent="enviarPassword" class="space-y-3">
          <div>
            <label class="text-xs font-bold text-slate-600 dark:text-slate-400">Correo Electrónico</label>
            <input 
              v-model="formPassword.email"
              type="email"
              required
              placeholder="admin@edencafe.com"
              class="w-full mt-1 p-3 bg-slate-50 dark:bg-slate-800 border border-slate-300 dark:border-slate-700 rounded-xl text-sm font-semibold text-slate-800 dark:text-slate-100 focus:outline-none focus:border-eden-600"
            />
          </div>

          <div>
            <label class="text-xs font-bold text-slate-600 dark:text-slate-400">Contraseña</label>
            <input 
              v-model="formPassword.password"
              type="password"
              required
              placeholder="••••••••"
              class="w-full mt-1 p-3 bg-slate-50 dark:bg-slate-800 border border-slate-300 dark:border-slate-700 rounded-xl text-sm font-semibold text-slate-800 dark:text-slate-100 focus:outline-none focus:border-eden-600"
            />
          </div>

          <div v-if="errorLogin" class="text-center text-xs font-bold text-rose-600 dark:text-rose-400">
            {{ errorLogin }}
          </div>

          <button 
            type="submit"
            :disabled="!formPassword.email || !formPassword.password || cargando"
            class="w-full py-3.5 bg-eden-600 hover:bg-eden-700 disabled:opacity-50 text-white rounded-xl font-bold text-sm shadow-md transition active:scale-95 flex items-center justify-center gap-2"
          >
            <span v-if="cargando">Verificando...</span>
            <span v-else>Iniciar Sesión</span>
          </button>
        </form>
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

const modoAcceso = ref('pin') // 'pin' | 'perfil' | 'password'
const pin = ref('')
const errorLogin = ref('')
const cargando = ref(false)
const usuarioSeleccionado = ref(null)

const formPassword = ref({
  email: '',
  password: ''
})

onMounted(async () => {
  await authStore.cargarUsuarios()
})

const cambiarModo = (nuevoModo) => {
  modoAcceso.value = nuevoModo
  pin.value = ''
  errorLogin.value = ''
  usuarioSeleccionado.value = null
}

const agregarDigito = (d) => {
  if (pin.value.length < 4) {
    pin.value += d
    errorLogin.value = ''
    if (pin.value.length === 4) {
      enviarPinDirecto()
    }
  }
}

const agregarDigitoPerfil = (d) => {
  if (pin.value.length < 4) {
    pin.value += d
    errorLogin.value = ''
    if (pin.value.length === 4) {
      enviarPinPerfil()
    }
  }
}

const borrarDigito = () => {
  pin.value = pin.value.slice(0, -1)
  errorLogin.value = ''
}

const enviarPinDirecto = async () => {
  if (pin.value.length !== 4) return
  cargando.value = true
  errorLogin.value = ''
  try {
    const usuario = await authStore.loginConPin(pin.value)
    redirigirSegunRol(usuario.rol)
  } catch (err) {
    errorLogin.value = err.response?.data?.detail || 'PIN no reconocido. Intenta de nuevo.'
    pin.value = ''
  } finally {
    cargando.value = false
  }
}

const seleccionarPerfil = (usuario) => {
  usuarioSeleccionado.value = usuario
  pin.value = ''
  errorLogin.value = ''
}

const deseleccionarPerfil = () => {
  usuarioSeleccionado.value = null
  pin.value = ''
  errorLogin.value = ''
}

const enviarPinPerfil = async () => {
  if (pin.value.length !== 4 || !usuarioSeleccionado.value) return
  cargando.value = true
  errorLogin.value = ''
  try {
    const usuario = await authStore.loginConPin(pin.value, usuarioSeleccionado.value.id)
    redirigirSegunRol(usuario.rol)
  } catch (err) {
    errorLogin.value = err.response?.data?.detail || `PIN incorrecto para ${usuarioSeleccionado.value.nombre}.`
    pin.value = ''
  } finally {
    cargando.value = false
  }
}

const enviarPassword = async () => {
  if (!formPassword.value.email || !formPassword.value.password) return
  cargando.value = true
  errorLogin.value = ''
  try {
    const usuario = await authStore.loginConPassword(
      formPassword.value.email,
      formPassword.value.password
    )
    redirigirSegunRol(usuario.rol)
  } catch (err) {
    errorLogin.value = err.response?.data?.detail || 'Credenciales incorrectas. Verifica tu correo y contraseña.'
  } finally {
    cargando.value = false
  }
}

const redirigirSegunRol = (rol) => {
  const rutaDestino = RUTA_INICIAL_POR_ROL[rol] || '/'
  router.push(rutaDestino)
}
</script>

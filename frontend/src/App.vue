<template>
  <div class="min-h-screen flex flex-col bg-slate-100 dark:bg-slate-950 text-slate-800 dark:text-slate-100 transition-colors">
    <!-- Navbar Superior del Personal (Se oculta en /login y en /carta) -->
    <header 
      v-if="mostrarNavbarPersonal"
      class="bg-white dark:bg-slate-900 border-b border-slate-200 dark:border-slate-800 sticky top-0 z-50 transition-colors"
    >
      <div class="max-w-7xl mx-auto px-4 h-16 flex items-center justify-between">
        <!-- Logo y Nombre del Restaurante -->
        <router-link to="/" class="flex items-center gap-3 group">
          <img 
            src="/logo.png" 
            alt="Edén Café Logo" 
            class="w-11 h-11 object-contain rounded-full shadow-sm group-hover:scale-105 transition-transform"
          />
          <div>
            <h1 class="font-black text-slate-800 dark:text-slate-100 text-base leading-tight tracking-tight">Edén Café</h1>
            <span class="text-xs text-eden-600 dark:text-eden-400 font-semibold flex items-center gap-1">
              <span class="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></span> Sistema en línea
            </span>
          </div>
        </router-link>

        <!-- Menú de Navegación Filtrado por Rol -->
        <nav class="hidden md:flex items-center gap-1 bg-slate-100 dark:bg-slate-800 p-1.5 rounded-xl border border-slate-200/80 dark:border-slate-700/80">
          <router-link
            v-for="item in navItemsPermitidos"
            :key="item.path"
            :to="item.path"
            class="px-3 py-1.5 rounded-lg text-xs font-bold transition-all flex items-center gap-1.5"
            :class="$route.path === item.path ? 'bg-white dark:bg-slate-700 text-slate-900 dark:text-white shadow-sm' : 'text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-white'"
          >
            <span>{{ item.icono }}</span>
            <span>{{ item.nombre }}</span>
          </router-link>

          <!-- Enlace rápido a la Carta Digital de Clientes -->
          <router-link
            to="/carta"
            target="_blank"
            class="px-2.5 py-1.5 rounded-lg text-xs font-bold text-eden-700 dark:text-eden-400 hover:bg-eden-50 dark:hover:bg-eden-950/40 transition flex items-center gap-1"
            title="Abrir Carta Digital para Clientes en nueva pestaña"
          >
            <span>📖</span>
            <span class="hidden lg:inline">Carta Clientes ↗</span>
          </router-link>
        </nav>

        <!-- Controles de Usuario, Tema y Cierre de Sesión -->
        <div class="flex items-center gap-2 sm:gap-3">
          <!-- Selector Rápido de Tema (Claro / Oscuro / Sistema) -->
          <div class="flex bg-slate-100 dark:bg-slate-800 p-1 rounded-xl border border-slate-200 dark:border-slate-700">
            <button
              @click="themeStore.establecerTema('claro')"
              :class="[
                'w-7 h-7 rounded-lg text-xs flex items-center justify-center transition-all',
                themeStore.tema === 'claro' ? 'bg-white dark:bg-slate-700 text-amber-500 shadow-sm' : 'text-slate-400 hover:text-slate-700'
              ]"
              title="Modo Claro"
            >
              ☀️
            </button>
            <button
              @click="themeStore.establecerTema('oscuro')"
              :class="[
                'w-7 h-7 rounded-lg text-xs flex items-center justify-center transition-all',
                themeStore.tema === 'oscuro' ? 'bg-white dark:bg-slate-700 text-sky-400 shadow-sm' : 'text-slate-400 hover:text-slate-700'
              ]"
              title="Modo Oscuro"
            >
              🌙
            </button>
            <button
              @click="themeStore.establecerTema('sistema')"
              :class="[
                'w-7 h-7 rounded-lg text-xs flex items-center justify-center transition-all',
                themeStore.tema === 'sistema' ? 'bg-white dark:bg-slate-700 text-emerald-500 shadow-sm' : 'text-slate-400 hover:text-slate-700'
              ]"
              title="Modo Sistema (Automático)"
            >
              💻
            </button>
          </div>

          <!-- Info Usuario en Turno -->
          <div v-if="authStore.usuarioActual" class="flex items-center gap-2 pl-1 sm:pl-2">
            <div class="text-right hidden sm:block">
              <div class="text-xs font-bold text-slate-800 dark:text-slate-100">{{ authStore.usuarioActual.nombre }}</div>
              <div class="text-2xs font-semibold text-eden-600 dark:text-eden-400 uppercase tracking-wider">{{ authStore.usuarioActual.rol }}</div>
            </div>
            
            <div class="w-8 h-8 rounded-full bg-eden-100 dark:bg-eden-900/60 text-eden-800 dark:text-eden-200 flex items-center justify-center font-black text-xs border border-eden-300 dark:border-eden-700">
              {{ authStore.usuarioActual.nombre.charAt(0) }}
            </div>

            <!-- Botón Cerrar Sesión -->
            <button
              @click="cerrarSesion"
              title="Cerrar Sesión"
              class="w-8 h-8 rounded-xl bg-slate-100 dark:bg-slate-800 hover:bg-rose-50 dark:hover:bg-rose-950/40 text-slate-500 hover:text-rose-600 dark:hover:text-rose-400 flex items-center justify-center text-sm transition active:scale-95 border border-slate-200 dark:border-slate-700"
            >
              🚪
            </button>
          </div>
        </div>
      </div>
    </header>

    <!-- Contenido Principal -->
    <main 
      class="flex-1 w-full"
      :class="{ 
        'max-w-7xl mx-auto p-4 md:p-6 pb-20 md:pb-6': mostrarNavbarPersonal,
        '': !mostrarNavbarPersonal 
      }"
    >
      <router-view />
    </main>

    <!-- Barra de Navegación Inferior Móvil (Filtrada por Rol, solo para el personal) -->
    <nav 
      v-if="mostrarNavbarPersonal && navItemsPermitidos.length > 1"
      class="md:hidden fixed bottom-0 left-0 right-0 bg-white dark:bg-slate-900 border-t border-slate-200 dark:border-slate-800 flex justify-around p-1.5 z-50 shadow-lg"
    >
      <router-link
        v-for="item in navItemsPermitidos"
        :key="item.path"
        :to="item.path"
        class="flex flex-col items-center py-1 px-2 rounded-lg text-2xs font-bold"
        :class="$route.path === item.path ? 'text-eden-600 dark:text-eden-400' : 'text-slate-500 dark:text-slate-400'"
      >
        <span class="text-base">{{ item.icono }}</span>
        <span>{{ item.nombre }}</span>
      </router-link>
    </nav>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAuthStore } from './stores/auth'
import { useThemeStore } from './stores/theme'

const route = useRoute()
const router = useRouter()
const authStore = useAuthStore()
const themeStore = useThemeStore()

const mostrarNavbarPersonal = computed(() => {
  return route.path !== '/login' && route.path !== '/carta'
})

const todosLosNavItems = [
  { nombre: 'Mesas', nombreRuta: 'mesas', path: '/', icono: '🪑' },
  { nombre: 'Comandero', nombreRuta: 'pos', path: '/pos', icono: '📝' },
  { nombre: 'Cocina KDS', nombreRuta: 'cocina', path: '/cocina', icono: '👨‍🍳' },
  { nombre: 'Caja', nombreRuta: 'caja', path: '/caja', icono: '💵' },
  { nombre: 'Inventario', nombreRuta: 'inventario', path: '/inventario', icono: '📦' },
  { nombre: 'Personal', nombreRuta: 'usuarios', path: '/usuarios', icono: '👥' },
]

const navItemsPermitidos = computed(() => {
  return todosLosNavItems.filter(item => authStore.tienePermiso(item.nombreRuta))
})

const cerrarSesion = () => {
  if (confirm('¿Deseas cerrar la sesión del turno actual?')) {
    authStore.logout()
    router.push('/login')
  }
}
</script>

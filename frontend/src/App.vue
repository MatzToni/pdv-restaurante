<template>
  <div class="min-h-screen flex flex-col bg-slate-100">
    <!-- Navbar Superior -->
    <header class="bg-white border-b border-slate-200 sticky top-0 z-50">
      <div class="max-w-7xl mx-auto px-4 h-16 flex items-center justify-between">
        <!-- Logo y Nombre del Restaurante -->
        <router-link to="/" class="flex items-center gap-3 group">
          <img 
            src="/logo.png" 
            alt="Edén Café Logo" 
            class="w-11 h-11 object-contain rounded-full shadow-sm group-hover:scale-105 transition-transform"
          />
          <div>
            <h1 class="font-black text-slate-800 text-base leading-tight tracking-tight">Edén Café</h1>
            <span class="text-xs text-eden-600 font-semibold flex items-center gap-1">
              <span class="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></span> Sistema en línea
            </span>
          </div>
        </router-link>

        <!-- Menú de Navegación Escritorio / Tablet -->
        <nav class="hidden md:flex items-center gap-1 bg-slate-100 p-1.5 rounded-xl border border-slate-200/80">
          <router-link
            v-for="item in navItems"
            :key="item.path"
            :to="item.path"
            class="px-3.5 py-1.5 rounded-lg text-xs font-bold transition-all flex items-center gap-1.5"
            :class="$route.path === item.path ? 'bg-white text-slate-900 shadow-sm' : 'text-slate-600 hover:text-slate-900'"
          >
            <span>{{ item.icono }}</span>
            <span>{{ item.nombre }}</span>
          </router-link>
        </nav>

        <!-- Info Usuario en Turno -->
        <router-link to="/usuarios" class="flex items-center gap-2 hover:bg-slate-50 p-1.5 rounded-xl transition">
          <div class="text-right hidden sm:block">
            <div class="text-xs font-bold text-slate-800">{{ authStore.usuarioActual.nombre }}</div>
            <div class="text-2xs font-semibold text-eden-600 capitalize">{{ authStore.usuarioActual.rol }}</div>
          </div>
          <div class="w-9 h-9 rounded-full bg-eden-100 text-eden-800 flex items-center justify-center font-black text-xs border border-eden-300">
            {{ authStore.usuarioActual.nombre.charAt(0) }}
          </div>
        </router-link>
      </div>
    </header>

    <!-- Contenido Principal -->
    <main class="flex-1 max-w-7xl w-full mx-auto p-4 md:p-6 pb-20 md:pb-6">
      <router-view />
    </main>

    <!-- Barra de Navegación Inferior Móvil (Para meseros en celular) -->
    <nav class="md:hidden fixed bottom-0 left-0 right-0 bg-white border-t border-slate-200 flex justify-around p-1.5 z-50 shadow-lg">
      <router-link
        v-for="item in navItems"
        :key="item.path"
        :to="item.path"
        class="flex flex-col items-center py-1 px-2 rounded-lg text-2xs font-bold"
        :class="$route.path === item.path ? 'text-eden-600' : 'text-slate-500'"
      >
        <span class="text-base">{{ item.icono }}</span>
        <span>{{ item.nombre }}</span>
      </router-link>
    </nav>
  </div>
</template>

<script setup>
import { useAuthStore } from './stores/auth'

const authStore = useAuthStore()

const navItems = [
  { nombre: 'Mesas', path: '/', icono: '🪑' },
  { nombre: 'Comandero', path: '/pos', icono: '📝' },
  { nombre: 'Cocina KDS', path: '/cocina', icono: '👨‍🍳' },
  { nombre: 'Caja', path: '/caja', icono: '💵' },
  { nombre: 'Inventario', path: '/inventario', icono: '📦' },
  { nombre: 'Personal', path: '/usuarios', icono: '👥' },
]
</script>

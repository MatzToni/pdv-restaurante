<template>
  <div class="min-h-screen flex flex-col bg-slate-100">
    <!-- Navbar Superior -->
    <header class="bg-white border-b border-slate-200 sticky top-0 z-50">
      <div class="max-w-7xl mx-auto px-4 h-16 flex items-center justify-between">
        <!-- Logo y Nombre del Restaurante -->
        <div class="flex items-center gap-3">
          <img 
            src="/logo.png" 
            alt="Edén Café Logo" 
            class="w-11 h-11 object-contain rounded-full shadow-sm hover:scale-105 transition-transform"
          />
          <div>
            <h1 class="font-black text-slate-800 text-base leading-tight tracking-tight">Edén Café</h1>
            <span class="text-xs text-eden-600 font-semibold flex items-center gap-1">
              <span class="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></span> Sistema en línea
            </span>
          </div>
        </div>

        <!-- Menú de Navegación Escritorio / Tablet -->
        <nav class="hidden md:flex items-center gap-1 bg-slate-100 p-1.5 rounded-xl border border-slate-200/80">
          <router-link
            v-for="item in navItems"
            :key="item.path"
            :to="item.path"
            class="px-4 py-2 rounded-lg text-sm font-bold transition-all"
            :class="$route.path === item.path ? 'bg-white text-slate-900 shadow-sm' : 'text-slate-600 hover:text-slate-900'"
          >
            <span class="mr-1.5">{{ item.icono }}</span> {{ item.nombre }}
          </router-link>
        </nav>

        <!-- Info Usuario / Turno -->
        <div class="flex items-center gap-3">
          <div class="text-right hidden sm:block">
            <div class="text-xs font-bold text-slate-700">Turno Activo</div>
            <div class="text-xs text-slate-400">Caja Principal</div>
          </div>
        </div>
      </div>
    </header>

    <!-- Contenido Principal -->
    <main class="flex-1 max-w-7xl w-full mx-auto p-4 md:p-6 pb-20 md:pb-6">
      <router-view />
    </main>

    <!-- Barra de Navegación Inferior Móvil (Para meseros en celular) -->
    <nav class="md:hidden fixed bottom-0 left-0 right-0 bg-white border-t border-slate-200 flex justify-around p-2 z-50 shadow-lg">
      <router-link
        v-for="item in navItems"
        :key="item.path"
        :to="item.path"
        class="flex flex-col items-center py-1 px-3 rounded-lg text-xs font-semibold"
        :class="$route.path === item.path ? 'text-eden-600 font-bold' : 'text-slate-500'"
      >
        <span class="text-lg">{{ item.icono }}</span>
        <span>{{ item.nombre }}</span>
      </router-link>
    </nav>
  </div>
</template>

<script setup>
const navItems = [
  { nombre: 'Mesas', path: '/', icono: '🪑' },
  { nombre: 'Comandero', path: '/pos', icono: '📝' },
  { nombre: 'Cocina (KDS)', path: '/cocina', icono: '👨‍🍳' },
  { nombre: 'Caja', path: '/caja', icono: '💵' },
]
</script>

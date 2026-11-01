<template>
  <div class="min-h-screen flex flex-col md:flex-row bg-slate-100 dark:bg-slate-950 text-slate-800 dark:text-slate-100 transition-colors selection:bg-eden-500 selection:text-white">

    <!-- ======================================================== -->
    <!-- 1. BARRA LATERAL DESKTOP (MD+) ESTILO iOS CRISTALINO     -->
    <!-- ======================================================== -->
    <aside
      v-if="mostrarNavbarPersonal"
      :class="[
        'hidden md:flex flex-col justify-between sticky top-0 h-screen z-40 transition-all duration-300 ease-[cubic-bezier(0.16,1,0.3,1)] shrink-0',
        'bg-white/70 dark:bg-slate-900/75 backdrop-blur-2xl backdrop-saturate-150',
        'border-r border-white/40 dark:border-white/10 shadow-[0_4px_30px_rgba(0,0,0,0.04)]',
        sidebarExpandida ? 'w-64 p-3.5' : 'w-20 p-2.5 items-center'
      ]"
    >
      <!-- Cabecera de Barra Lateral: Logo Redondo y Botón Retraer/Expandir -->
      <div class="w-full">
        <!-- Modo Expandido -->
        <div v-if="sidebarExpandida" class="pb-3 mb-2 border-b border-white/50 dark:border-white/10">
          <!-- Barra superior de control: Botón de contraer a la derecha -->
          <div class="flex items-center justify-between mb-1">
            <span class="text-3xs font-semibold uppercase tracking-wider text-slate-400 dark:text-slate-500 pl-1">
              Edén Café PDV
            </span>
            <button
              @click="alternarSidebar"
              title="Contraer barra lateral"
              class="rounded-xl p-1.5 bg-white/60 dark:bg-slate-800/60 hover:bg-white dark:hover:bg-slate-700 text-slate-500 hover:text-slate-900 dark:hover:text-white border border-white/50 dark:border-white/10 shadow-xs transition-all active:scale-95 flex items-center justify-center shrink-0"
            >
              <svg 
                xmlns="http://www.w3.org/2000/svg" 
                class="w-4 h-4" 
                viewBox="0 0 24 24" 
                fill="none" 
                stroke="currentColor" 
                stroke-width="2.5" 
                stroke-linecap="round" 
                stroke-linejoin="round"
              >
                <polyline points="15 18 9 12 15 6"></polyline>
              </svg>
            </button>
          </div>

          <!-- Logo redondo centrado y letras abajo del logo -->
          <router-link to="/" class="flex flex-col items-center text-center group py-1">
            <div class="relative mb-2">
              <div class="w-20 h-20 rounded-full overflow-hidden p-1 bg-white/95 dark:bg-slate-800/90 border-2 border-white/80 dark:border-white/20 shadow-md flex items-center justify-center group-hover:scale-105 transition-transform">
                <img 
                  src="/logo.png" 
                  alt="Edén Café Logo" 
                  class="w-full h-full object-cover rounded-full"
                />
              </div>
              <span class="absolute bottom-0 right-0 w-3.5 h-3.5 rounded-full bg-emerald-500 ring-2 ring-white dark:ring-slate-900 animate-pulse"></span>
            </div>

            <!-- Letras abajo del logo -->
            <h1 class="font-bold text-slate-800 dark:text-slate-100 text-sm leading-tight tracking-tight">
              Edén Café
            </h1>
            <span class="text-3xs text-eden-700 dark:text-eden-400 font-semibold tracking-tight mt-0.5">
              Comida Tradicional y Café
            </span>
            <span class="inline-flex items-center gap-1 text-3xs text-emerald-600 dark:text-emerald-400 font-semibold uppercase tracking-wider mt-1 px-2 py-0.5 rounded-full bg-emerald-50 dark:bg-emerald-950/60 border border-emerald-200 dark:border-emerald-800/40">
              <span class="w-1.5 h-1.5 rounded-full bg-emerald-500 animate-pulse"></span> En línea
            </span>
          </router-link>
        </div>

        <!-- Modo Contraído -->
        <div v-else class="flex flex-col items-center gap-2 pb-3 mb-2 border-b border-white/50 dark:border-white/10">
          <router-link to="/" class="group">
            <div class="relative">
              <div class="w-12 h-12 rounded-full overflow-hidden p-0.5 bg-white/95 dark:bg-slate-800/90 border border-white/80 dark:border-white/20 shadow-sm flex items-center justify-center group-hover:scale-105 transition-transform">
                <img 
                  src="/logo.png" 
                  alt="Edén Café Logo" 
                  class="w-full h-full object-cover rounded-full"
                />
              </div>
              <span class="absolute -bottom-0.5 -right-0.5 w-3 h-3 rounded-full bg-emerald-500 ring-2 ring-white dark:ring-slate-900 animate-pulse"></span>
            </div>
          </router-link>

          <button
            @click="alternarSidebar"
            title="Expandir barra lateral"
            class="rounded-xl p-2 bg-white/60 dark:bg-slate-800/60 hover:bg-white dark:hover:bg-slate-700 text-slate-500 hover:text-slate-900 dark:hover:text-white border border-white/50 dark:border-white/10 shadow-xs transition-all active:scale-95 flex items-center justify-center shrink-0"
          >
            <svg 
              xmlns="http://www.w3.org/2000/svg" 
              class="w-4 h-4" 
              viewBox="0 0 24 24" 
              fill="none" 
              stroke="currentColor" 
              stroke-width="2.5" 
              stroke-linecap="round" 
              stroke-linejoin="round"
            >
              <polyline points="9 18 15 12 9 6"></polyline>
            </svg>
          </button>
        </div>

        <!-- Etiqueta de Sección (Expandida) -->
        <div v-if="sidebarExpandida" class="px-2 mb-1.5 flex items-center justify-between text-2xs font-bold tracking-wider uppercase text-slate-400 dark:text-slate-500">
          <span>Módulos</span>
          <span class="text-3xs font-semibold text-emerald-600 dark:text-emerald-400 lowercase">en línea</span>
        </div>
      </div>

      <!-- Menú de Vistas (Scrollable si pantalla pequeña) -->
      <nav class="flex-1 w-full py-2 space-y-1.5 overflow-y-auto no-scrollbar">
        <!-- Vistas Permitidas por Rol -->
        <router-link
          v-for="item in navItemsPermitidos"
          :key="item.path"
          :to="item.path"
          class="group relative flex items-center rounded-2xl transition-all select-none"
          :class="[
            sidebarExpandida ? 'px-3.5 py-2.5 gap-3' : 'w-12 h-12 mx-auto justify-center',
            $route.path === item.path
              ? 'bg-eden-600/15 dark:bg-eden-500/20 text-eden-800 dark:text-eden-200 font-bold border border-eden-500/30 shadow-[0_2px_12px_rgba(72,104,72,0.12)] backdrop-blur-md'
              : 'text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-white hover:bg-white/50 dark:hover:bg-white/5 active:scale-[0.98]'
          ]"
        >
          <!-- Indicador lateral activo (Modo Expandido) -->
          <span 
            v-if="sidebarExpandida && $route.path === item.path"
            class="w-1 h-5 rounded-full bg-eden-600 dark:bg-eden-400 absolute left-1 shadow-sm"
          ></span>

          <!-- Icono del Módulo -->
          <span class="text-xl shrink-0 group-hover:scale-110 transition-transform">
            {{ item.icono }}
          </span>

          <!-- Nombre del Módulo (Modo Expandido) -->
          <span v-if="sidebarExpandida" class="text-xs font-semibold truncate">
            {{ item.nombre }}
          </span>

          <!-- Indicador puntual activo (Modo Contraído) -->
          <span 
            v-if="!sidebarExpandida && $route.path === item.path"
            class="w-1.5 h-1.5 rounded-full bg-eden-600 dark:bg-eden-400 absolute bottom-1.5 shadow-sm"
          ></span>

          <!-- Tooltip Flotante Estilo iOS (Modo Contraído al hacer Hover) -->
          <div
            v-if="!sidebarExpandida"
            class="pointer-events-none opacity-0 group-hover:opacity-100 group-hover:translate-x-0 -translate-x-2 transition-all duration-200 absolute left-full ml-3 px-3 py-1.5 bg-slate-900/90 dark:bg-white/95 text-white dark:text-slate-900 text-xs font-bold rounded-xl shadow-xl z-50 whitespace-nowrap backdrop-blur-md border border-white/10 dark:border-slate-800/20"
          >
            {{ item.nombre }}
          </div>
        </router-link>

        <!-- Divisor sutil de cristal -->
        <div class="my-2 border-t border-white/40 dark:border-white/10"></div>

        <!-- Enlace especial: Carta Digital Clientes (Abre en nueva pestaña) -->
        <router-link
          to="/carta"
          target="_blank"
          class="group relative flex items-center rounded-2xl transition-all select-none text-eden-700 dark:text-eden-400 bg-eden-50/70 dark:bg-eden-950/40 hover:bg-eden-100/80 dark:hover:bg-eden-900/60 border border-eden-200/60 dark:border-eden-800/40 active:scale-[0.98]"
          :class="sidebarExpandida ? 'px-3.5 py-2.5 gap-3' : 'w-12 h-12 mx-auto justify-center'"
          title="Abrir Carta Digital de Clientes en nueva pestaña"
        >
          <span class="text-xl shrink-0 group-hover:scale-110 transition-transform">📖</span>
          <span v-if="sidebarExpandida" class="text-xs font-semibold truncate flex items-center justify-between flex-1">
            <span>Carta Clientes</span>
            <span class="text-2xs opacity-75">↗</span>
          </span>

          <!-- Tooltip flotante (Contraído) -->
          <div
            v-if="!sidebarExpandida"
            class="pointer-events-none opacity-0 group-hover:opacity-100 group-hover:translate-x-0 -translate-x-2 transition-all duration-200 absolute left-full ml-3 px-3 py-1.5 bg-slate-900/90 dark:bg-white/95 text-white dark:text-slate-900 text-xs font-bold rounded-xl shadow-xl z-50 whitespace-nowrap backdrop-blur-md border border-white/10 dark:border-slate-800/20"
          >
            Carta Clientes ↗
          </div>
        </router-link>
      </nav>

      <!-- Pie de Barra Lateral: Usuario, Selector de Tema y Cierre de Sesión -->
      <div 
        class="w-full pt-3 mt-2 border-t border-white/50 dark:border-white/10 flex flex-col gap-2.5"
      >
        <!-- Info Usuario -->
        <div 
          v-if="authStore.usuarioActual"
          :class="[
            'rounded-2xl transition-all',
            sidebarExpandida 
              ? 'p-2.5 bg-white/70 dark:bg-slate-800/70 border border-white/60 dark:border-white/10 shadow-xs flex items-center gap-2.5 backdrop-blur-md'
              : 'relative group flex justify-center'
          ]"
        >
          <!-- Avatar con Inicial -->
          <div 
            class="w-9 h-9 rounded-xl bg-gradient-to-br from-eden-500 to-eden-700 text-white flex items-center justify-center font-bold text-xs shadow-sm ring-1 ring-white/60 dark:ring-white/10 shrink-0"
          >
            {{ authStore.usuarioActual.nombre ? authStore.usuarioActual.nombre.charAt(0) : 'U' }}
          </div>

          <!-- Nombre y Rol (Modo Expandido) -->
          <div v-if="sidebarExpandida" class="min-w-0 flex-1">
            <div 
              class="text-xs font-bold text-slate-800 dark:text-slate-100 leading-snug break-words"
              :title="authStore.usuarioActual.nombre"
            >
              {{ authStore.usuarioActual.nombre }}
            </div>
            <div class="mt-1 flex items-center gap-1.5 flex-wrap">
              <span class="text-3xs font-bold uppercase px-2 py-0.5 rounded-md bg-eden-100 dark:bg-eden-950/80 text-eden-700 dark:text-eden-400 tracking-wider">
                {{ authStore.usuarioActual.rol }}
              </span>
              <span class="w-1.5 h-1.5 rounded-full bg-emerald-500 animate-pulse"></span>
            </div>
          </div>

          <!-- Tooltip en modo contraído -->
          <div
            v-if="!sidebarExpandida"
            class="pointer-events-none opacity-0 group-hover:opacity-100 group-hover:translate-x-0 -translate-x-2 transition-all duration-200 absolute left-full ml-3 px-3 py-1.5 bg-slate-900/90 dark:bg-white/95 text-white dark:text-slate-900 text-xs font-bold rounded-xl shadow-xl z-50 whitespace-nowrap backdrop-blur-md border border-white/10 dark:border-slate-800/20"
          >
            {{ authStore.usuarioActual.nombre }} ({{ authStore.usuarioActual.rol }})
          </div>
        </div>

        <!-- Selector de Tema Estilo Segmented Control de iOS (Expandido) -->
        <div 
          v-if="sidebarExpandida"
          class="grid grid-cols-3 p-1 rounded-xl bg-slate-200/60 dark:bg-slate-800/80 border border-white/60 dark:border-white/10 backdrop-blur-md gap-1"
        >
          <button
            @click="themeStore.establecerTema('claro')"
            :class="[
              'py-1 rounded-lg text-xs flex items-center justify-center transition-all font-bold',
              themeStore.tema === 'claro' 
                ? 'bg-white dark:bg-slate-700 text-amber-500 shadow-xs' 
                : 'text-slate-500 hover:text-slate-800 dark:text-slate-400 dark:hover:text-white'
            ]"
            title="Modo Claro"
          >
            ☀️
          </button>
          <button
            @click="themeStore.establecerTema('oscuro')"
            :class="[
              'py-1 rounded-lg text-xs flex items-center justify-center transition-all font-bold',
              themeStore.tema === 'oscuro' 
                ? 'bg-white dark:bg-slate-700 text-sky-400 shadow-xs' 
                : 'text-slate-500 hover:text-slate-800 dark:text-slate-400 dark:hover:text-white'
            ]"
            title="Modo Oscuro"
          >
            🌙
          </button>
          <button
            @click="themeStore.establecerTema('sistema')"
            :class="[
              'py-1 rounded-lg text-xs flex items-center justify-center transition-all font-bold',
              themeStore.tema === 'sistema' 
                ? 'bg-white dark:bg-slate-700 text-emerald-500 shadow-xs' 
                : 'text-slate-500 hover:text-slate-800 dark:text-slate-400 dark:hover:text-white'
            ]"
            title="Modo Sistema (Automático)"
          >
            💻
          </button>
        </div>

        <!-- Alternador Rápido de Tema (Contraído) -->
        <div v-else class="relative group flex justify-center">
          <button
            @click="ciclarTema"
            class="w-10 h-10 rounded-xl bg-white/60 dark:bg-slate-800/60 hover:bg-white dark:hover:bg-slate-700 border border-white/50 dark:border-white/10 flex items-center justify-center text-sm shadow-xs transition active:scale-95"
            :title="`Tema actual: ${themeStore.tema}. Clic para alternar.`"
          >
            <span v-if="themeStore.tema === 'claro'">☀️</span>
            <span v-else-if="themeStore.tema === 'oscuro'">🌙</span>
            <span v-else>💻</span>
          </button>
          <div
            class="pointer-events-none opacity-0 group-hover:opacity-100 group-hover:translate-x-0 -translate-x-2 transition-all duration-200 absolute left-full ml-3 px-3 py-1.5 bg-slate-900/90 dark:bg-white/95 text-white dark:text-slate-900 text-xs font-bold rounded-xl shadow-xl z-50 whitespace-nowrap backdrop-blur-md border border-white/10 dark:border-slate-800/20"
          >
            Tema: {{ themeStore.tema }} (Alternar)
          </div>
        </div>

        <!-- Botón Cerrar Turno / Sesión -->
        <div :class="sidebarExpandida ? 'w-full' : 'relative group flex justify-center'">
          <button
            @click="cerrarSesion"
            :class="[
              'rounded-xl text-xs font-bold text-rose-600 dark:text-rose-400 hover:bg-rose-50 dark:hover:bg-rose-950/40 border border-rose-200/60 dark:border-rose-900/40 flex items-center justify-center transition active:scale-95 shadow-xs',
              sidebarExpandida ? 'w-full py-2 px-3 gap-2' : 'w-10 h-10'
            ]"
            title="Cerrar Turno"
          >
            <span class="text-sm">🚪</span>
            <span v-if="sidebarExpandida">Cerrar Turno</span>
          </button>

          <div
            v-if="!sidebarExpandida"
            class="pointer-events-none opacity-0 group-hover:opacity-100 group-hover:translate-x-0 -translate-x-2 transition-all duration-200 absolute left-full ml-3 px-3 py-1.5 bg-slate-900/90 dark:bg-white/95 text-white dark:text-slate-900 text-xs font-bold rounded-xl shadow-xl z-50 whitespace-nowrap backdrop-blur-md border border-white/10 dark:border-slate-800/20"
          >
            Cerrar Turno
          </div>
        </div>
      </div>
    </aside>

    <!-- ======================================================== -->
    <!-- 2. BARRA SUPERIOR MÓVIL (< MD) ESTILO FROSTED GLASS iOS  -->
    <!-- ======================================================== -->
    <header
      v-if="mostrarNavbarPersonal"
      class="md:hidden sticky top-0 z-30 h-14 bg-white/75 dark:bg-slate-900/80 backdrop-blur-2xl border-b border-white/40 dark:border-white/10 px-4 flex items-center justify-between shadow-xs transition-colors"
    >
      <!-- Botón Menú Hamburguesa + Título Actual -->
      <div class="flex items-center gap-3">
        <button
          @click="drawerMovilAbierto = true"
          class="w-10 h-10 rounded-xl bg-white/70 dark:bg-slate-800/70 border border-white/50 dark:border-white/10 flex items-center justify-center text-slate-700 dark:text-slate-200 shadow-xs active:scale-95 transition"
          aria-label="Abrir Menú de Navegación"
        >
          <svg xmlns="http://www.w3.org/2000/svg" class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M4 6h16M4 12h16M4 18h16" />
          </svg>
        </button>

        <div class="flex items-center gap-2">
          <img 
            src="/logo.png" 
            alt="Edén Café Logo" 
            class="w-8 h-8 object-contain rounded-xl shadow-xs ring-1 ring-white/60 dark:ring-white/10"
          />
          <div>
            <h1 class="font-bold text-slate-800 dark:text-slate-100 text-sm leading-tight tracking-tight">
              {{ tituloVistaActual }}
            </h1>
            <span class="text-3xs text-eden-600 dark:text-eden-400 font-semibold block leading-none">
              Edén Café
            </span>
          </div>
        </div>
      </div>

      <!-- Controles Rápidos Móviles: Tema y Perfil -->
      <div class="flex items-center gap-2">
        <button
          @click="ciclarTema"
          class="w-9 h-9 rounded-xl bg-white/60 dark:bg-slate-800/60 border border-white/50 dark:border-white/10 flex items-center justify-center text-xs shadow-xs active:scale-95 transition"
          title="Alternar Tema"
        >
          <span v-if="themeStore.tema === 'claro'">☀️</span>
          <span v-else-if="themeStore.tema === 'oscuro'">🌙</span>
          <span v-else>💻</span>
        </button>

        <div 
          v-if="authStore.usuarioActual"
          class="w-9 h-9 rounded-xl bg-gradient-to-br from-eden-500 to-eden-700 text-white flex items-center justify-center font-bold text-xs shadow-sm ring-1 ring-white/60 dark:ring-white/10"
          :title="`${authStore.usuarioActual.nombre} (${authStore.usuarioActual.rol})`"
        >
          {{ authStore.usuarioActual.nombre ? authStore.usuarioActual.nombre.charAt(0) : 'U' }}
        </div>
      </div>
    </header>

    <!-- ======================================================== -->
    <!-- 3. DRAWER MÓVIL DESLIZABLE ESTILO iOS FROSTED GLASS      -->
    <!-- ======================================================== -->
    <Teleport to="body">
      <div 
        v-if="mostrarNavbarPersonal && drawerMovilAbierto" 
        class="fixed inset-0 z-50 md:hidden flex"
      >
        <!-- Fondo translúcido oscuro con desenfoque (Backdrop) -->
        <div 
          @click="drawerMovilAbierto = false" 
          class="fixed inset-0 bg-slate-950/40 backdrop-blur-sm transition-opacity animate-in fade-in duration-200"
        ></div>

        <!-- Contenedor Lateral Deslizable -->
        <aside 
          class="relative w-72 max-w-[85vw] h-full bg-white/85 dark:bg-slate-900/90 backdrop-blur-2xl border-r border-white/40 dark:border-white/10 p-5 flex flex-col justify-between shadow-2xl z-50 animate-in slide-in-from-left duration-250"
        >
          <!-- Cabecera del Drawer -->
          <div>
            <div class="flex items-center justify-between pb-2 mb-2 border-b border-white/50 dark:border-white/10">
              <span class="text-3xs font-semibold uppercase tracking-wider text-slate-400 dark:text-slate-500">
                Edén Café PDV
              </span>
              <!-- Botón Cerrar Drawer -->
              <button
                @click="drawerMovilAbierto = false"
                class="w-8 h-8 rounded-xl bg-slate-100 dark:bg-slate-800 text-slate-500 hover:text-slate-900 dark:hover:text-white flex items-center justify-center text-sm active:scale-95 transition"
                aria-label="Cerrar Menú"
              >
                ✕
              </button>
            </div>

            <!-- Logo Redondo y Letras Abajo en Móvil -->
            <div class="flex flex-col items-center text-center pb-3 mb-3 border-b border-white/50 dark:border-white/10">
              <div class="relative mb-2">
                <div class="w-20 h-20 rounded-full overflow-hidden p-1 bg-white/95 dark:bg-slate-800/90 border-2 border-white/80 dark:border-white/20 shadow-md flex items-center justify-center">
                  <img 
                    src="/logo.png" 
                    alt="Edén Café Logo" 
                    class="w-full h-full object-cover rounded-full"
                  />
                </div>
                <span class="absolute bottom-0 right-0 w-3.5 h-3.5 rounded-full bg-emerald-500 ring-2 ring-white dark:ring-slate-900 animate-pulse"></span>
              </div>
              <h2 class="font-bold text-slate-800 dark:text-slate-100 text-sm leading-tight">Edén Café</h2>
              <span class="text-3xs text-eden-600 dark:text-eden-400 font-semibold">Comida Tradicional y Café</span>
            </div>

            <div class="px-2 mb-2 text-2xs font-bold tracking-wider uppercase text-slate-400 dark:text-slate-500">
              Módulos del Sistema
            </div>

            <!-- Lista de Vistas Móvil -->
            <nav class="space-y-1.5 overflow-y-auto max-h-[50vh] no-scrollbar">
              <router-link
                v-for="item in navItemsPermitidos"
                :key="item.path"
                :to="item.path"
                @click="drawerMovilAbierto = false"
                class="flex items-center gap-3 px-3.5 py-3 rounded-2xl text-xs font-semibold transition active:scale-[0.98]"
                :class="[
                  $route.path === item.path
                    ? 'bg-eden-600/15 dark:bg-eden-500/20 text-eden-800 dark:text-eden-200 font-bold border border-eden-500/30 shadow-xs'
                    : 'text-slate-600 dark:text-slate-400 hover:bg-white/50 dark:hover:bg-white/5'
                ]"
              >
                <span class="text-xl">{{ item.icono }}</span>
                <span>{{ item.nombre }}</span>
              </router-link>

              <!-- Carta Digital Clientes -->
              <router-link
                to="/carta"
                target="_blank"
                @click="drawerMovilAbierto = false"
                class="flex items-center justify-between px-3.5 py-3 rounded-2xl text-xs font-semibold text-eden-700 dark:text-eden-400 bg-eden-50/70 dark:bg-eden-950/40 border border-eden-200/60 dark:border-eden-800/40 mt-3"
              >
                <div class="flex items-center gap-3">
                  <span class="text-xl">📖</span>
                  <span>Carta Clientes</span>
                </div>
                <span class="text-2xs font-bold">↗</span>
              </router-link>
            </nav>
          </div>

          <!-- Pie del Drawer: Usuario, Tema y Logout -->
          <div class="pt-4 border-t border-white/50 dark:border-white/10 space-y-3">
            <!-- Usuario Móvil -->
            <div 
              v-if="authStore.usuarioActual" 
              class="p-3 rounded-2xl bg-white/70 dark:bg-slate-800/70 border border-white/60 dark:border-white/10 shadow-xs flex items-center gap-3"
            >
              <div class="w-10 h-10 rounded-2xl bg-gradient-to-br from-eden-500 to-eden-700 text-white flex items-center justify-center font-bold text-sm shadow-sm ring-1 ring-white/60 dark:ring-white/10 shrink-0">
                {{ authStore.usuarioActual.nombre ? authStore.usuarioActual.nombre.charAt(0) : 'U' }}
              </div>
              <div class="min-w-0 flex-1">
                <div class="text-xs font-bold text-slate-800 dark:text-slate-100 leading-snug break-words">
                  {{ authStore.usuarioActual.nombre }}
                </div>
                <div class="mt-1">
                  <span class="text-3xs font-bold uppercase px-2 py-0.5 rounded-md bg-eden-100 dark:bg-eden-950/80 text-eden-700 dark:text-eden-400 inline-block">
                    {{ authStore.usuarioActual.rol }}
                  </span>
                </div>
              </div>
            </div>

            <!-- Selector de Tema Segmented Móvil -->
            <div class="grid grid-cols-3 p-1 rounded-xl bg-slate-200/60 dark:bg-slate-800/80 border border-white/60 dark:border-white/10 gap-1">
              <button
                @click="themeStore.establecerTema('claro')"
                :class="[
                  'py-1.5 rounded-lg text-xs flex items-center justify-center font-bold transition-all',
                  themeStore.tema === 'claro' ? 'bg-white dark:bg-slate-700 text-amber-500 shadow-xs' : 'text-slate-500'
                ]"
              >
                ☀️ Claro
              </button>
              <button
                @click="themeStore.establecerTema('oscuro')"
                :class="[
                  'py-1.5 rounded-lg text-xs flex items-center justify-center font-bold transition-all',
                  themeStore.tema === 'oscuro' ? 'bg-white dark:bg-slate-700 text-sky-400 shadow-xs' : 'text-slate-500'
                ]"
              >
                🌙 Oscuro
              </button>
              <button
                @click="themeStore.establecerTema('sistema')"
                :class="[
                  'py-1.5 rounded-lg text-xs flex items-center justify-center font-bold transition-all',
                  themeStore.tema === 'sistema' ? 'bg-white dark:bg-slate-700 text-emerald-500 shadow-xs' : 'text-slate-500'
                ]"
              >
                💻 Auto
              </button>
            </div>

            <!-- Botón Cerrar Turno Móvil -->
            <button
              @click="cerrarSesion"
              class="w-full py-2.5 px-4 rounded-xl text-xs font-bold text-rose-600 dark:text-rose-400 hover:bg-rose-50 dark:hover:bg-rose-950/40 border border-rose-200/60 dark:border-rose-900/40 flex items-center justify-center gap-2 active:scale-95 transition"
            >
              <span>🚪</span>
              <span>Cerrar Turno</span>
            </button>
          </div>
        </aside>
      </div>
    </Teleport>

    <!-- ======================================================== -->
    <!-- 4. CONTENIDO PRINCIPAL DE LA APLICACIÓN                  -->
    <!-- ======================================================== -->
    <div class="flex-1 flex flex-col min-w-0 min-h-screen">
      <main 
        class="flex-1 w-full"
        :class="{ 
          'w-full max-w-[1920px] mx-auto p-3 sm:p-5 md:p-6 lg:p-7': mostrarNavbarPersonal,
          '': !mostrarNavbarPersonal 
        }"
      >
        <router-view />
      </main>
    </div>

  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAuthStore } from './stores/auth'
import { useThemeStore } from './stores/theme'

const route = useRoute()
const router = useRouter()
const authStore = useAuthStore()
const themeStore = useThemeStore()

// Estado de la barra lateral en Desktop: expandida o compacta
const sidebarExpandida = ref(true)

// Estado del drawer lateral en dispositivos móviles
const drawerMovilAbierto = ref(false)

// Recuperar preferencia de expansión de localStorage al montar
onMounted(() => {
  const guardado = localStorage.getItem('eden_sidebar_expandida')
  if (guardado !== null) {
    sidebarExpandida.value = guardado === 'true'
  }
})

// Alternar entre expandido y contraído y persistir preferencia
const alternarSidebar = () => {
  sidebarExpandida.value = !sidebarExpandida.value
  localStorage.setItem('eden_sidebar_expandida', String(sidebarExpandida.value))
}

// Alternar cíclicamente el tema (Claro -> Oscuro -> Sistema -> Claro)
const ciclarTema = () => {
  if (themeStore.tema === 'claro') {
    themeStore.establecerTema('oscuro')
  } else if (themeStore.tema === 'oscuro') {
    themeStore.establecerTema('sistema')
  } else {
    themeStore.establecerTema('claro')
  }
}

// Cerrar drawer móvil al cambiar de ruta
watch(() => route.path, () => {
  drawerMovilAbierto.value = false
})

// Ocultar barra de navegación del personal en Login y en la Carta Digital
const mostrarNavbarPersonal = computed(() => {
  return route.path !== '/login' && route.path !== '/carta'
})

// Módulos del sistema con sus permisos asociados
const todosLosNavItems = [
  { nombre: 'Mesas', nombreRuta: 'mesas', path: '/', icono: '🪑' },
  { nombre: 'Comandero', nombreRuta: 'pos', path: '/pos', icono: '📝' },
  { nombre: 'Cocina KDS', nombreRuta: 'cocina', path: '/cocina', icono: '👨‍🍳' },
  { nombre: 'Caja', nombreRuta: 'caja', path: '/caja', icono: '💵' },
  { nombre: 'Menú / Platillos', nombreRuta: 'platillos', path: '/platillos', icono: '🍽️' },
  { nombre: 'Inventario', nombreRuta: 'inventario', path: '/inventario', icono: '📦' },
  { nombre: 'Personal', nombreRuta: 'usuarios', path: '/usuarios', icono: '👥' },
]

// Filtrar ítems de navegación según el rol del usuario conectado
const navItemsPermitidos = computed(() => {
  return todosLosNavItems.filter(item => authStore.tienePermiso(item.nombreRuta))
})

// Título de la vista actual para el encabezado móvil
const tituloVistaActual = computed(() => {
  const item = todosLosNavItems.find(i => i.path === route.path)
  return item ? item.nombre : 'Edén Café'
})

// Diálogo de confirmación para cerrar sesión del turno
const cerrarSesion = () => {
  if (confirm('¿Deseas cerrar la sesión del turno actual?')) {
    authStore.logout()
    router.push('/login')
  }
}
</script>

<style scoped>
/* Ocultar barra de desplazamiento manteniendo funcionalidad táctil */
.no-scrollbar::-webkit-scrollbar {
  display: none;
}
.no-scrollbar {
  -ms-overflow-style: none;
  scrollbar-width: none;
}
</style>
<template>
  <div class="space-y-6">
    <!-- Header Principal -->
    <div class="flex flex-col lg:flex-row justify-between items-start lg:items-center gap-4 bg-white dark:bg-slate-900 p-6 rounded-3xl border border-slate-200 dark:border-slate-800 shadow-sm transition-colors">
      <div>
        <div class="flex items-center gap-2.5">
          <span class="text-2xl">🍽️</span>
          <h1 class="text-2xl font-black text-slate-800 dark:text-slate-100 tracking-tight">Gestión de Menú y Platillos</h1>
        </div>
        <p class="text-slate-500 dark:text-slate-400 text-xs sm:text-sm mt-0.5">
          Selecciona qué platillos están en la carta activa de hoy, configura el Menú del Día y administra el catálogo general
        </p>
      </div>

      <div class="flex flex-wrap items-center gap-2 w-full lg:w-auto">
        <!-- Botón Configurar Menú del Día -->
        <button 
          @click="abrirModalMenuDelDia"
          class="px-4 py-2.5 bg-amber-500 hover:bg-amber-600 text-white rounded-2xl text-xs font-black shadow-sm transition active:scale-95 flex items-center gap-2 shrink-0"
        >
          <span>🍱</span> Configurar Menú del Día
        </button>

        <!-- Botón Categorías (Géneros) -->
        <button 
          @click="abrirModalCategoria"
          class="px-3.5 py-2.5 bg-slate-100 dark:bg-slate-800 hover:bg-slate-200 dark:hover:bg-slate-700 text-slate-700 dark:text-slate-200 rounded-2xl text-xs font-bold transition active:scale-95 flex items-center gap-1.5 border border-slate-200 dark:border-slate-700 shrink-0"
        >
          <span>🏷️</span> Géneros ({{ menuStore.categorias.length }})
        </button>

        <!-- Botón Alta de Platillo -->
        <button 
          @click="abrirModalNuevoProducto"
          class="px-4 py-2.5 bg-eden-600 hover:bg-eden-700 text-white rounded-2xl text-xs font-bold shadow-sm transition active:scale-95 flex items-center gap-1.5 shrink-0"
        >
          <span>+</span> Dar de Alta Platillo
        </button>
      </div>
    </div>

    <!-- BANNER RESUMEN: Menú del Día (Comida Corrida) -->
    <div 
      v-if="menuStore.menuDelDia"
      class="bg-gradient-to-r from-amber-500/10 via-eden-500/10 to-emerald-500/10 dark:from-amber-950/40 dark:via-eden-950/40 dark:to-emerald-950/40 rounded-3xl border border-amber-300/60 dark:border-amber-800/60 p-5 shadow-sm space-y-3.5 transition-colors"
    >
      <div class="flex flex-col lg:flex-row justify-between items-start lg:items-center gap-3">
        <div class="flex items-center gap-3">
          <div class="w-12 h-12 rounded-2xl bg-amber-500 text-white flex items-center justify-center text-2xl shadow-sm shrink-0">
            🍱
          </div>
          <div>
            <div class="flex items-center gap-2 flex-wrap">
              <h2 class="text-base font-black text-slate-800 dark:text-slate-100">
                Menú del Día
              </h2>
              <span 
                :class="[
                  'text-3xs font-black uppercase px-2.5 py-0.5 rounded-full tracking-wider',
                  menuStore.menuDelDia.activo 
                    ? 'bg-emerald-500 text-white' 
                    : 'bg-slate-200 dark:bg-slate-700 text-slate-700 dark:text-slate-300'
                ]"
              >
                {{ menuStore.menuDelDia.activo ? '● Activo Hoy' : '○ Pausado' }}
              </span>
            </div>
            <p class="text-xs text-slate-500 dark:text-slate-400 mt-0.5">
              Horario de servicio: <span class="font-bold text-slate-700 dark:text-slate-200">{{ menuStore.menuDelDia.hora_inicio || '12:00' }} a {{ menuStore.menuDelDia.hora_fin || '18:00' }}</span>
              · {{ menuStore.menuDelDia.comidas_corridas?.length || 0 }} opciones registradas
            </p>
          </div>
        </div>

        <div class="flex flex-wrap items-center gap-2 w-full lg:w-auto">
          <button 
            @click="alternarEstadoMenuDelDia"
            :class="[
              'px-3.5 py-2 rounded-xl text-xs font-bold border transition active:scale-95 shrink-0',
              menuStore.menuDelDia.activo 
                ? 'border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-800 text-slate-700 dark:text-slate-200 hover:bg-slate-100' 
                : 'border-emerald-400 bg-emerald-600 text-white hover:bg-emerald-700'
            ]"
          >
            {{ menuStore.menuDelDia.activo ? '⏸️ Pausar Servicio' : '▶️ Activar Servicio' }}
          </button>
          <button 
            @click="abrirModalMenuDelDia"
            class="px-4 py-2 bg-slate-900 dark:bg-white text-white dark:text-slate-900 hover:bg-slate-800 rounded-xl text-xs font-bold shadow-xs transition active:scale-95 flex items-center justify-center gap-1.5 shrink-0"
          >
            <span>✏️</span> Configurar Menú del Día
          </button>
        </div>
      </div>

      <!-- Tarjetas de las Comidas Corridas activas de hoy -->
      <div v-if="menuStore.menuDelDia.comidas_corridas?.length" class="grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-3 gap-3 pt-1">
        <div 
          v-for="(cc, i) in menuStore.menuDelDia.comidas_corridas" 
          :key="cc.id || i"
          class="p-3.5 bg-white/90 dark:bg-slate-900/90 rounded-2xl border border-slate-200/80 dark:border-slate-800/80 shadow-2xs space-y-2 flex flex-col justify-between"
          :class="cc.activo === false ? 'opacity-70 border-rose-200 dark:border-rose-900/50' : ''"
        >
          <div>
            <div class="pb-2 border-b border-slate-100 dark:border-slate-800 space-y-1.5">
              <div class="flex items-center justify-between gap-2">
                <span class="font-black text-xs text-slate-800 dark:text-slate-100 flex items-center gap-1 truncate">
                  <span>🍱</span> {{ cc.nombre || `Comida Corrida #${i + 1}` }}
                </span>
                <span class="text-xs font-black text-eden-600 dark:text-eden-400 font-mono shrink-0">
                  ${{ Number(cc.precio || menuStore.menuDelDia.precio || 95).toFixed(2) }}
                </span>
              </div>

              <div class="flex items-center justify-between gap-2">
                <span 
                  :class="[
                    'text-3xs font-black uppercase px-2 py-0.5 rounded-full shrink-0',
                    cc.activo !== false ? 'bg-emerald-100 text-emerald-800 dark:bg-emerald-950 dark:text-emerald-300' : 'bg-rose-100 text-rose-800 dark:bg-rose-950 dark:text-rose-300'
                  ]"
                >
                  {{ cc.activo !== false ? '● Disponible' : '○ Agotada' }}
                </span>
                <button
                  @click="alternarDisponibilidadCC(cc, i)"
                  class="px-2.5 py-1 text-3xs font-extrabold rounded-lg border transition active:scale-95 shrink-0"
                  :class="cc.activo !== false ? 'border-rose-200 dark:border-rose-900/60 bg-rose-50 dark:bg-rose-950/60 text-rose-700 dark:text-rose-300 hover:bg-rose-100' : 'border-emerald-300 dark:border-emerald-800 bg-emerald-50 dark:bg-emerald-950/60 text-emerald-700 dark:text-emerald-300 hover:bg-emerald-100'"
                  :title="cc.activo !== false ? 'Marcar como agotada para que meseros y comensales no puedan pedirla' : 'Reactivar comida corrida'"
                >
                  {{ cc.activo !== false ? '✕ Marcar Agotada' : '✓ Reactivar' }}
                </button>
              </div>
            </div>
            <div class="flex items-start gap-2.5 mt-2">
              <!-- Miniatura de foto si existe -->
              <div 
                v-if="cc.imagen_url" 
                class="w-14 h-14 rounded-xl overflow-hidden bg-slate-100 dark:bg-slate-800 border border-slate-200 dark:border-slate-700 shrink-0"
              >
                <img 
                  :src="menuStore.obtenerUrlImagen(cc.imagen_url)" 
                  :alt="cc.nombre"
                  class="w-full h-full object-cover"
                  @error="$event.target.style.display = 'none'"
                />
              </div>

              <div class="text-3xs text-slate-600 dark:text-slate-300 space-y-1 flex-1 min-w-0">
                <div class="flex items-start gap-1">
                  <span class="font-bold text-amber-700 dark:text-amber-400 shrink-0">🥣 Entrada:</span>
                  <span class="truncate">{{ cc.entradas?.join(', ') || 'Sin definir' }}</span>
                </div>
                <div class="flex items-start gap-1">
                  <span class="font-bold text-amber-700 dark:text-amber-400 shrink-0">🍖 Fuerte:</span>
                  <span class="truncate">{{ cc.platos_fuertes?.join(', ') || 'Sin definir' }}</span>
                </div>
                <div class="flex items-start gap-1">
                  <span class="font-bold text-amber-700 dark:text-amber-400 shrink-0">🥤 Bebida:</span>
                  <span class="truncate">{{ cc.bebidas?.join(', ') || 'Sin definir' }}</span>
                </div>
                <div v-if="cc.postres?.length" class="flex items-start gap-1">
                  <span class="font-bold text-amber-700 dark:text-amber-400 shrink-0">🍮 Postre:</span>
                  <span class="truncate">{{ cc.postres.join(', ') }}</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
      <div v-else class="text-xs text-slate-400 italic py-2 text-center">
        No hay opciones de Menú del Día configuradas. Presiona "Configurar Menú del Día" para dar de alta las de hoy.
      </div>
    </div>

    <!-- VISTA PARALELA: COLUMNA IZQUIERDA (CARTA DE HOY) Y COLUMNA DERECHA (CATÁLOGO GENERAL) -->
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-6 items-start">
      
      <!-- ================= COLUMNA IZQUIERDA: CARTA / MENÚ ACTIVO DE HOY ================= -->
      <div class="bg-white dark:bg-slate-900 rounded-3xl border border-slate-200 dark:border-slate-800 p-5 shadow-sm space-y-4 transition-colors">
        
        <!-- Header de la Columna Izquierda -->
        <div class="flex items-center justify-between pb-3 border-b border-slate-100 dark:border-slate-800">
          <div>
            <div class="flex items-center gap-2">
              <span class="text-xl">📜</span>
              <h2 class="text-lg font-black text-slate-800 dark:text-slate-100 tracking-tight">Carta / Menú de Hoy</h2>
              <span class="px-2.5 py-0.5 rounded-full text-xs font-black bg-emerald-100 text-emerald-800 dark:bg-emerald-950/70 dark:text-emerald-300 border border-emerald-300 dark:border-emerald-800/50">
                {{ productosEnCarta.length }} activos
              </span>
            </div>
            <p class="text-2xs text-slate-400 dark:text-slate-500 mt-0.5">
              Platillos y bebidas listos para ordenar en Comandero y visibles en Carta Digital
            </p>
          </div>
        </div>

        <!-- Filtros y Búsqueda para Carta Activa -->
        <div class="space-y-2.5">
          <div class="relative">
            <input 
              v-model="busquedaCarta"
              type="text"
              maxlength="80"
              placeholder="Buscar en la carta de hoy..."
              class="w-full pl-9 pr-3.5 py-2 bg-slate-50 dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded-xl text-xs text-slate-800 dark:text-slate-100 font-semibold focus:outline-none focus:border-eden-600"
            />
            <span class="absolute left-3 top-2.5 text-xs text-slate-400">🔍</span>
          </div>

          <!-- Selector de Categorías de la Carta -->
          <div class="flex gap-1.5 overflow-x-auto no-scrollbar pt-0.5">
            <button
              @click="catFiltroCarta = null"
              :class="[
                'px-3 py-1.5 rounded-xl text-2xs font-extrabold transition-all shrink-0',
                catFiltroCarta === null 
                  ? 'bg-slate-900 dark:bg-white text-white dark:text-slate-900 shadow-xs' 
                  : 'bg-slate-100 dark:bg-slate-800 text-slate-600 dark:text-slate-400 hover:bg-slate-200'
              ]"
            >
              Todos ({{ totalEnCarta }})
            </button>
            <button
              v-for="cat in menuStore.categorias"
              :key="'carta-' + cat.id"
              @click="catFiltroCarta = cat.id"
              :class="[
                'px-3 py-1.5 rounded-xl text-2xs font-extrabold transition-all shrink-0',
                catFiltroCarta === cat.id 
                  ? 'bg-emerald-600 text-white shadow-xs' 
                  : 'bg-slate-100 dark:bg-slate-800 text-slate-600 dark:text-slate-400 hover:bg-slate-200'
              ]"
            >
              {{ cat.nombre }} ({{ conteoEnCartaPorCat(cat.id) }})
            </button>
          </div>
        </div>

        <!-- Lista de Platillos en Carta -->
        <div v-if="productosEnCarta.length === 0" class="text-center py-14 bg-slate-50 dark:bg-slate-800/40 rounded-2xl border border-dashed border-slate-200 dark:border-slate-800 text-slate-400 space-y-2">
          <span class="text-4xl block">🥣</span>
          <h3 class="text-sm font-bold text-slate-700 dark:text-slate-300">No hay platillos activos en esta sección</h3>
          <p class="text-xs text-slate-400 max-w-xs mx-auto">
            Selecciona platillos del catálogo a la derecha presionando <strong>"+ Poner en Carta"</strong> para agregarlos al menú de hoy.
          </p>
        </div>

        <div v-else class="space-y-2.5 max-h-[620px] overflow-y-auto pr-1">
          <div 
            v-for="item in productosEnCarta" 
            :key="'carta-item-' + item.id"
            class="p-3 bg-white dark:bg-slate-800/70 rounded-2xl border border-slate-200/90 dark:border-slate-700/80 shadow-2xs hover:border-emerald-500 transition-all flex items-center justify-between gap-3 group"
          >
            <!-- Imagen e Información -->
            <div class="flex items-center gap-3 min-w-0 flex-1">
              <div class="w-14 h-14 rounded-xl overflow-hidden bg-slate-100 dark:bg-slate-700/60 border border-slate-200 dark:border-slate-700 shrink-0 relative flex items-center justify-center">
                <img 
                  v-if="item.imagen_url"
                  :src="menuStore.obtenerUrlImagen(item.imagen_url)" 
                  :alt="item.nombre"
                  class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300"
                  @error="$event.target.style.display = 'none'"
                />
                <span v-else class="text-2xl">{{ iconoTipoItem(item.tipo_item) }}</span>
              </div>

              <div class="min-w-0 flex-1">
                <div class="flex items-center gap-1.5 flex-wrap">
                  <h4 class="font-extrabold text-slate-800 dark:text-slate-100 text-xs sm:text-sm leading-snug truncate">
                    {{ item.nombre }}
                  </h4>
                  <span class="text-3xs font-black px-1.5 py-0.5 rounded uppercase" :class="badgeTipoItem(item.tipo_item)">
                    {{ item.tipo_item || 'platillo' }}
                  </span>
                </div>
                <div class="flex items-center gap-2 mt-0.5 text-3xs text-slate-400 dark:text-slate-500">
                  <span class="font-bold text-slate-600 dark:text-slate-400">{{ item.categoria_nombre || 'General' }}</span>
                  <span v-if="item.requiere_cocina" class="text-amber-600 dark:text-amber-400">· 👨‍🍳 Cocina</span>
                </div>
                <div class="font-black text-emerald-600 dark:text-emerald-400 font-mono text-sm mt-0.5">
                  ${{ Number(item.precio).toFixed(2) }}
                </div>
              </div>
            </div>

            <!-- Botón Quitar de Carta -->
            <div class="flex items-center gap-1.5 shrink-0">
              <button 
                @click="alternarDisponibilidad(item)"
                class="px-3 py-2 text-2xs font-black bg-rose-50 dark:bg-rose-950/50 hover:bg-rose-100 text-rose-700 dark:text-rose-300 border border-rose-200 dark:border-rose-900/60 rounded-xl transition active:scale-95 flex items-center gap-1"
                title="Quitar este platillo de la carta activa de hoy"
              >
                <span>✕</span> Quitar de Carta
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- ================= COLUMNA DERECHA: CATÁLOGO GENERAL DE PLATILLOS ================= -->
      <div class="bg-white dark:bg-slate-900 rounded-3xl border border-slate-200 dark:border-slate-800 p-5 shadow-sm space-y-4 transition-colors">
        
        <!-- Header de la Columna Derecha -->
        <div class="flex items-center justify-between pb-3 border-b border-slate-100 dark:border-slate-800">
          <div>
            <div class="flex items-center gap-2">
              <span class="text-xl">🗃️</span>
              <h2 class="text-lg font-black text-slate-800 dark:text-slate-100 tracking-tight">Catálogo General</h2>
              <span class="px-2.5 py-0.5 rounded-full text-xs font-black bg-slate-100 text-slate-700 dark:bg-slate-800 dark:text-slate-300 border border-slate-200 dark:border-slate-700">
                {{ productosCatalogo.length }} registrados
              </span>
            </div>
            <p class="text-2xs text-slate-400 dark:text-slate-500 mt-0.5">
              Todos los platillos, bebidas y servicios dados de alta en Edén Café
            </p>
          </div>
        </div>

        <!-- Filtros y Búsqueda para Catálogo -->
        <div class="space-y-2.5">
          <div class="flex gap-2">
            <div class="relative flex-1">
              <input 
                v-model="busquedaCatalogo"
                type="text"
                maxlength="80"
                placeholder="Buscar en el catálogo general..."
                class="w-full pl-9 pr-3.5 py-2 bg-slate-50 dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded-xl text-xs text-slate-800 dark:text-slate-100 font-semibold focus:outline-none focus:border-eden-600"
              />
              <span class="absolute left-3 top-2.5 text-xs text-slate-400">🔍</span>
            </div>

            <!-- Filtro de estado rápido -->
            <select 
              v-model="filtroEstadoCatalogo"
              class="px-2.5 py-2 bg-slate-50 dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded-xl text-xs font-bold text-slate-700 dark:text-slate-200 focus:outline-none focus:border-eden-600"
            >
              <option value="todos">Todos los Estados</option>
              <option value="fuera_de_carta">Solo Pausados (Fuera de Carta)</option>
              <option value="en_carta">Solo en Carta de Hoy</option>
            </select>
          </div>

          <!-- Selector de Categorías del Catálogo -->
          <div class="flex gap-1.5 overflow-x-auto no-scrollbar pt-0.5">
            <button
              @click="catFiltroCatalogo = null"
              :class="[
                'px-3 py-1.5 rounded-xl text-2xs font-extrabold transition-all shrink-0',
                catFiltroCatalogo === null 
                  ? 'bg-slate-900 dark:bg-white text-white dark:text-slate-900 shadow-xs' 
                  : 'bg-slate-100 dark:bg-slate-800 text-slate-600 dark:text-slate-400 hover:bg-slate-200'
              ]"
            >
              Todos ({{ menuStore.productos.length }})
            </button>
            <button
              v-for="cat in menuStore.categorias"
              :key="'cat-' + cat.id"
              @click="catFiltroCatalogo = cat.id"
              :class="[
                'px-3 py-1.5 rounded-xl text-2xs font-extrabold transition-all shrink-0',
                catFiltroCatalogo === cat.id 
                  ? 'bg-eden-600 text-white shadow-xs' 
                  : 'bg-slate-100 dark:bg-slate-800 text-slate-600 dark:text-slate-400 hover:bg-slate-200'
              ]"
            >
              {{ cat.nombre }} ({{ conteoTotalPorCat(cat.id) }})
            </button>
          </div>
        </div>

        <!-- Lista de Platillos en Catálogo -->
        <div v-if="productosCatalogo.length === 0" class="text-center py-14 bg-slate-50 dark:bg-slate-800/40 rounded-2xl border border-dashed border-slate-200 dark:border-slate-800 text-slate-400 space-y-2">
          <span class="text-4xl block">🔍</span>
          <h3 class="text-sm font-bold text-slate-700 dark:text-slate-300">No se encontraron productos</h3>
          <p class="text-xs text-slate-400 max-w-xs mx-auto">
            Ajusta los filtros de búsqueda o da de alta un nuevo platillo o servicio con el botón superior.
          </p>
        </div>

        <div v-else class="space-y-2.5 max-h-[620px] overflow-y-auto pr-1">
          <div 
            v-for="item in productosCatalogo" 
            :key="'cat-item-' + item.id"
            class="p-3 bg-white dark:bg-slate-800/70 rounded-2xl border border-slate-200/90 dark:border-slate-700/80 shadow-2xs hover:border-eden-500 transition-all flex items-center justify-between gap-3 group"
          >
            <!-- Imagen e Información -->
            <div class="flex items-center gap-3 min-w-0 flex-1">
              <div class="w-14 h-14 rounded-xl overflow-hidden bg-slate-100 dark:bg-slate-700/60 border border-slate-200 dark:border-slate-700 shrink-0 relative flex items-center justify-center">
                <img 
                  v-if="item.imagen_url"
                  :src="menuStore.obtenerUrlImagen(item.imagen_url)" 
                  :alt="item.nombre"
                  class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300"
                  @error="$event.target.style.display = 'none'"
                />
                <span v-else class="text-2xl">{{ iconoTipoItem(item.tipo_item) }}</span>
              </div>

              <div class="min-w-0 flex-1">
                <div class="flex items-center gap-1.5 flex-wrap">
                  <h4 class="font-extrabold text-slate-800 dark:text-slate-100 text-xs sm:text-sm leading-snug truncate">
                    {{ item.nombre }}
                  </h4>
                  <span class="text-3xs font-black px-1.5 py-0.5 rounded uppercase" :class="badgeTipoItem(item.tipo_item)">
                    {{ item.tipo_item || 'platillo' }}
                  </span>
                  <span 
                    :class="[
                      'text-3xs font-extrabold px-1.5 py-0.2 rounded-full',
                      item.disponible ? 'bg-emerald-100 text-emerald-800 dark:bg-emerald-950/60 dark:text-emerald-300' : 'bg-slate-200 text-slate-600 dark:bg-slate-700 dark:text-slate-300'
                    ]"
                  >
                    {{ item.disponible ? 'En Carta' : 'Pausado' }}
                  </span>
                </div>
                <div class="flex items-center gap-2 mt-0.5 text-3xs text-slate-400 dark:text-slate-500">
                  <span class="font-bold text-slate-600 dark:text-slate-400">{{ item.categoria_nombre || 'General' }}</span>
                  <span v-if="item.requiere_cocina" class="text-amber-600 dark:text-amber-400">· 👨‍🍳 Cocina</span>
                </div>
                <div class="font-black text-eden-600 dark:text-eden-400 font-mono text-sm mt-0.5">
                  ${{ Number(item.precio).toFixed(2) }}
                </div>
              </div>
            </div>

            <!-- Botones de Acción -->
            <div class="flex items-center gap-1.5 shrink-0 flex-wrap justify-end">
              <!-- Botón Agregar a Comida Corrida -->
              <button 
                @click="abrirAsignarAComidaCorrida(item)"
                class="px-2.5 py-2 text-2xs font-black bg-amber-50 dark:bg-amber-950/50 hover:bg-amber-100 text-amber-700 dark:text-amber-300 border border-amber-300/80 dark:border-amber-700/60 rounded-xl transition active:scale-95 flex items-center gap-1"
                title="Agregar este producto al Menú del Día (Comida Corrida)"
              >
                <span>🍱</span>
                <span class="hidden xl:inline">+ A Menú del Día</span>
                <span class="xl:hidden">+ MDD</span>
              </button>

              <button 
                @click="abrirModalEditar(item)"
                class="px-2.5 py-2 text-2xs font-bold bg-slate-100 dark:bg-slate-700/70 hover:bg-slate-200 text-slate-700 dark:text-slate-200 rounded-xl transition active:scale-95"
                title="Editar platillo"
              >
                ✏️
              </button>

              <!-- Botón Eliminar Platillo o Servicio -->
              <button 
                @click="confirmarEliminarProducto(item)"
                class="px-2.5 py-2 text-2xs font-bold bg-rose-50 dark:bg-rose-950/40 hover:bg-rose-100 dark:hover:bg-rose-900/60 text-rose-600 dark:text-rose-400 border border-rose-200 dark:border-rose-800/60 rounded-xl transition active:scale-95"
                title="Eliminar platillo o servicio del catálogo general"
              >
                🗑️
              </button>

              <!-- Botón Poner en Carta / Quitar de Carta -->
              <button 
                v-if="!item.disponible"
                @click="alternarDisponibilidad(item)"
                class="px-3 py-2 text-2xs font-black bg-emerald-600 hover:bg-emerald-700 text-white rounded-xl shadow-xs transition active:scale-95 flex items-center gap-1"
                title="Poner este platillo en la carta activa de hoy"
              >
                <span>+</span> Poner en Carta
              </button>

              <button 
                v-else
                @click="alternarDisponibilidad(item)"
                class="px-2.5 py-2 text-2xs font-bold bg-slate-100 dark:bg-slate-800 hover:bg-rose-50 hover:text-rose-700 text-slate-500 rounded-xl transition active:scale-95 border border-slate-200 dark:border-slate-700"
                title="Quitar de carta de hoy"
              >
                ✕ Quitar
              </button>
            </div>
          </div>
        </div>
      </div>

    </div>

    <!-- ================= MODAL CONFIGURACIÓN MENÚ DEL DÍA (COMIDA CORRIDA) ================= -->
    <div v-if="modalMenuDelDia" class="fixed inset-0 bg-slate-900/60 backdrop-blur-sm flex items-center justify-center p-3 sm:p-4 z-50">
      <div class="bg-white dark:bg-slate-900 rounded-3xl p-5 sm:p-6 max-w-4xl w-full shadow-2xl border border-slate-200 dark:border-slate-800 space-y-4 max-h-[92vh] flex flex-col">
        <!-- Header Modal -->
        <div class="flex justify-between items-center border-b border-slate-100 dark:border-slate-800 pb-3">
          <div class="flex items-center gap-2.5">
            <span class="text-2xl">🍱</span>
            <div>
              <h3 class="text-lg font-black text-slate-800 dark:text-slate-100">Configuración del Menú del Día</h3>
              <p class="text-xs text-slate-400">Configura las opciones completas de Menú del Día con sus tiempos y platillos</p>
            </div>
          </div>
          <button @click="modalMenuDelDia = false" class="text-slate-400 hover:text-slate-600 font-bold text-lg">✕</button>
        </div>

        <div class="flex-1 overflow-y-auto space-y-4 pr-1">
          <!-- Switch de Activación y Horario General -->
          <div class="p-4 bg-slate-50 dark:bg-slate-800/60 rounded-2xl border border-slate-200 dark:border-slate-700 space-y-3">
            <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-3">
              <label class="flex items-center gap-2.5 cursor-pointer">
                <input 
                  v-model="formMenuDelDia.activo" 
                  type="checkbox" 
                  class="rounded text-amber-500 focus:ring-amber-400 w-5 h-5 cursor-pointer"
                />
                <div>
                  <span class="text-xs font-black text-slate-800 dark:text-slate-100 block">Servicio de Menú del Día Activo Hoy</span>
                  <span class="text-3xs text-slate-400">Si está activo, los meseros podrán ordenarlo en comandero y los comensales lo verán en la carta</span>
                </div>
              </label>

              <!-- Horario de Servicio -->
              <div class="flex items-center gap-2 text-xs">
                <div class="flex items-center gap-1">
                  <span class="text-3xs font-extrabold text-slate-400 uppercase">Inicio:</span>
                  <input 
                    v-model="formMenuDelDia.hora_inicio" 
                    type="time" 
                    class="p-1.5 bg-white dark:bg-slate-800 border border-slate-300 dark:border-slate-700 rounded-xl text-xs font-bold text-slate-800 dark:text-slate-100 focus:outline-none focus:border-amber-500"
                  />
                </div>
                <div class="flex items-center gap-1">
                  <span class="text-3xs font-extrabold text-slate-400 uppercase">Fin:</span>
                  <input 
                    v-model="formMenuDelDia.hora_fin" 
                    type="time" 
                    class="p-1.5 bg-white dark:bg-slate-800 border border-slate-300 dark:border-slate-700 rounded-xl text-xs font-bold text-slate-800 dark:text-slate-100 focus:outline-none focus:border-amber-500"
                  />
                </div>
              </div>
            </div>
          </div>

          <!-- Barra de Título y Botón Agregar Comida Corrida -->
          <div class="flex items-center justify-between pt-1">
            <div class="flex items-center gap-2">
              <span class="text-xs font-black uppercase text-slate-700 dark:text-slate-300 tracking-wider">
                Opciones del Menú del Día para Hoy ({{ formMenuDelDia.comidas_corridas?.length || 0 }})
              </span>
            </div>
            <button 
              type="button" 
              @click="agregarNuevaComidaCorrida"
              class="px-3.5 py-1.5 bg-amber-500 hover:bg-amber-600 text-white rounded-xl text-xs font-black shadow-xs transition active:scale-95 flex items-center gap-1.5"
            >
              <span>+</span> Agregar Otra Opción
            </button>
          </div>

          <!-- LISTA DE COMIDAS CORRIDAS -->
          <div class="space-y-4">
            <div 
              v-for="(cc, idx) in formMenuDelDia.comidas_corridas" 
              :key="cc.id || idx"
              class="p-4 bg-slate-50 dark:bg-slate-800/60 rounded-2xl border border-slate-200 dark:border-slate-700 space-y-3.5 shadow-2xs"
            >
              <!-- Cabecera de la Comida Corrida: Título e Input de Imagen -->
              <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-2.5 pb-2.5 border-b border-slate-200/60 dark:border-slate-700/60">
                <div class="flex items-center gap-2.5 flex-1 w-full sm:w-auto flex-wrap">
                  <!-- Identificador de la Comida Corrida -->
                  <span class="px-3 py-1.5 rounded-xl bg-amber-500 text-white text-xs font-black uppercase tracking-wider shrink-0 flex items-center gap-1.5 shadow-2xs">
                    <span>🍱</span> Comida Corrida #{{ idx + 1 }}
                  </span>

                  <!-- Input de Imagen de la Comida Corrida -->
                  <div class="flex items-center gap-2 bg-white dark:bg-slate-800 p-1.5 rounded-xl border border-slate-200 dark:border-slate-700 shadow-2xs">
                    <!-- Vista previa de la miniatura -->
                    <div class="w-10 h-10 rounded-lg overflow-hidden bg-slate-100 dark:bg-slate-700 border border-slate-200 dark:border-slate-600 shrink-0 flex items-center justify-center relative">
                      <img 
                        v-if="cc.imagen_url" 
                        :src="menuStore.obtenerUrlImagen(cc.imagen_url)" 
                        :alt="cc.nombre" 
                        class="w-full h-full object-cover"
                        @error="$event.target.style.display = 'none'"
                      />
                      <span v-else class="text-base text-slate-400">📷</span>
                      <div v-if="subiendoImagenCCIndex === idx" class="absolute inset-0 bg-black/60 flex items-center justify-center text-white text-2xs font-bold">
                        ⏳
                      </div>
                    </div>

                    <!-- Botón para subir archivo desde el dispositivo -->
                    <input 
                      type="file" 
                      :id="'file-upload-cc-' + idx"
                      accept="image/*" 
                      class="hidden" 
                      @change="subirImagenParaCC($event, cc, idx)"
                    />
                    <label 
                      :for="'file-upload-cc-' + idx"
                      class="cursor-pointer px-2.5 py-1.5 rounded-lg bg-slate-100 dark:bg-slate-700/80 hover:bg-slate-200 dark:hover:bg-slate-700 text-slate-700 dark:text-slate-200 text-3xs font-black flex items-center gap-1 transition active:scale-95"
                    >
                      <span>📁</span>
                      <span>{{ subiendoImagenCCIndex === idx ? 'Subiendo...' : (cc.imagen_url ? 'Cambiar Foto' : 'Subir Foto') }}</span>
                    </label>

                    <!-- Input para URL directa (opcional) -->
                    <input 
                      v-model="cc.imagen_url"
                      type="text" 
                      placeholder="O URL de imagen..."
                      class="w-28 sm:w-36 px-2 py-1 text-3xs bg-slate-50 dark:bg-slate-900 border border-slate-200 dark:border-slate-700 rounded-lg text-slate-600 dark:text-slate-300 font-mono focus:outline-none focus:border-amber-500"
                    />

                    <!-- Botón para quitar imagen si existe -->
                    <button 
                      v-if="cc.imagen_url"
                      type="button" 
                      @click="quitarImagenCC(cc)"
                      class="p-1 text-rose-500 hover:text-rose-700 text-xs font-bold transition"
                      title="Quitar imagen"
                    >
                      ✕
                    </button>
                  </div>
                </div>

                <div class="flex items-center gap-2 w-full sm:w-auto justify-end flex-wrap">
                  <!-- Switch de disponibilidad individual de esta comida corrida -->
                  <label class="flex items-center gap-1.5 cursor-pointer bg-white dark:bg-slate-800 px-2 py-1 rounded-xl border border-slate-300 dark:border-slate-700 shadow-2xs">
                    <input 
                      type="checkbox" 
                      v-model="cc.activo" 
                      class="rounded text-amber-500 focus:ring-amber-400 w-4 h-4 cursor-pointer"
                    />
                    <span class="text-3xs font-black uppercase" :class="cc.activo !== false ? 'text-emerald-600 dark:text-emerald-400' : 'text-rose-600 dark:text-rose-400'">
                      {{ cc.activo !== false ? '● Disponible' : '✕ Agotada' }}
                    </span>
                  </label>

                  <div class="flex items-center gap-1">
                    <span class="text-3xs font-extrabold text-slate-400">Precio $</span>
                    <input 
                      v-model.number="cc.precio"
                      type="number"
                      min="0"
                      step="0.50"
                      class="w-20 p-1.5 text-xs font-black text-eden-600 dark:text-eden-400 bg-white dark:bg-slate-800 border border-slate-300 dark:border-slate-700 rounded-xl font-mono focus:outline-none focus:border-amber-500 text-right"
                      placeholder="95.00"
                    />
                  </div>

                  <button 
                    v-if="formMenuDelDia.comidas_corridas.length > 1"
                    type="button" 
                    @click="eliminarComidaCorrida(idx)"
                    class="p-1.5 text-rose-500 hover:bg-rose-100 dark:hover:bg-rose-950/60 rounded-xl transition"
                    title="Eliminar esta comida corrida"
                  >
                    🗑️
                  </button>
                </div>
              </div>

              <!-- Los 4 Apartados (Entrada, Fuerte con Guarnición, Bebida, Postre) -->
              <div class="grid grid-cols-1 md:grid-cols-2 gap-3 text-xs">
                
                <!-- 1. Apartado Entrada -->
                <div class="p-3 bg-white dark:bg-slate-900 rounded-xl border border-slate-200 dark:border-slate-700/80 space-y-2">
                  <div class="flex items-center justify-between">
                    <span class="text-3xs font-black uppercase text-amber-700 dark:text-amber-400">
                      🥣 Entrada (Sopa, Puchero, Consomé...)
                    </span>
                    <span class="text-3xs text-slate-400 font-bold">{{ cc.entradas?.length || 0 }}</span>
                  </div>

                  <!-- Selector rápido desde Catálogo General -->
                  <select 
                    @change="agregarDesdeSelectCatalogo(cc, 'entradas', $event)"
                    class="w-full p-2 text-xs font-semibold bg-slate-50 dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded-xl text-slate-700 dark:text-slate-200 focus:outline-none focus:border-amber-500"
                  >
                    <option value="">📋 Elegir del Catálogo General...</option>
                    <optgroup v-for="grupo in catalogoPorCategoria" :key="grupo.id" :label="grupo.nombre">
                      <option v-for="p in grupo.productos" :key="p.id" :value="p.nombre">
                        {{ p.nombre }}
                      </option>
                    </optgroup>
                  </select>

                  <!-- O escribir platillo especial del día -->
                  <div class="flex gap-1.5">
                    <input 
                      v-model="cc.nuevaEntrada"
                      @keydown.enter.prevent="agregarOpcionCC(cc, 'entradas', 'nuevaEntrada')"
                      type="text" 
                      maxlength="60"
                      placeholder="O escribe especial del día..."
                      class="flex-1 p-1.5 text-xs font-semibold bg-slate-50 dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded-lg text-slate-800 dark:text-slate-100 focus:outline-none focus:border-amber-500"
                    />
                    <button 
                      type="button" 
                      @click="agregarOpcionCC(cc, 'entradas', 'nuevaEntrada')"
                      class="px-2.5 py-1 bg-amber-500 hover:bg-amber-600 text-white rounded-lg text-2xs font-bold transition shrink-0"
                    >
                      + Agregar
                    </button>
                  </div>
                  <!-- Chips -->
                  <div class="flex flex-wrap gap-1 min-h-[1.5rem]">
                    <span 
                      v-for="(opc, oi) in cc.entradas" 
                      :key="oi"
                      class="inline-flex items-center gap-1 px-2 py-0.5 rounded-lg bg-slate-100 dark:bg-slate-800 text-slate-700 dark:text-slate-200 text-3xs font-bold border border-slate-200 dark:border-slate-700"
                    >
                      {{ opc }}
                      <button type="button" @click="quitarOpcionCC(cc, 'entradas', oi)" class="text-rose-500 font-black">✕</button>
                    </span>
                    <span v-if="!cc.entradas?.length" class="text-3xs text-slate-400 italic">Sin entrada agregada</span>
                  </div>
                </div>

                <!-- 2. Apartado Plato Fuerte con Guarnición -->
                <div class="p-3 bg-white dark:bg-slate-900 rounded-xl border border-slate-200 dark:border-slate-700/80 space-y-2">
                  <div class="flex items-center justify-between">
                    <span class="text-3xs font-black uppercase text-amber-700 dark:text-amber-400">
                      🍖 Plato Fuerte con Guarnición
                    </span>
                    <span class="text-3xs text-slate-400 font-bold">{{ cc.platos_fuertes?.length || 0 }}</span>
                  </div>

                  <!-- Selector rápido desde Catálogo General -->
                  <select 
                    @change="agregarDesdeSelectCatalogo(cc, 'platos_fuertes', $event)"
                    class="w-full p-2 text-xs font-semibold bg-slate-50 dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded-xl text-slate-700 dark:text-slate-200 focus:outline-none focus:border-amber-500"
                  >
                    <option value="">📋 Elegir del Catálogo General...</option>
                    <optgroup v-for="grupo in catalogoPorCategoria" :key="grupo.id" :label="grupo.nombre">
                      <option v-for="p in grupo.productos" :key="p.id" :value="p.nombre">
                        {{ p.nombre }}
                      </option>
                    </optgroup>
                  </select>

                  <!-- O escribir platillo especial del día -->
                  <div class="flex gap-1.5">
                    <input 
                      v-model="cc.nuevoFuerte"
                      @keydown.enter.prevent="agregarOpcionCC(cc, 'platos_fuertes', 'nuevoFuerte')"
                      type="text" 
                      maxlength="80"
                      placeholder="O escribe especial del día..."
                      class="flex-1 p-1.5 text-xs font-semibold bg-slate-50 dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded-lg text-slate-800 dark:text-slate-100 focus:outline-none focus:border-amber-500"
                    />
                    <button 
                      type="button" 
                      @click="agregarOpcionCC(cc, 'platos_fuertes', 'nuevoFuerte')"
                      class="px-2.5 py-1 bg-amber-500 hover:bg-amber-600 text-white rounded-lg text-2xs font-bold transition shrink-0"
                    >
                      + Agregar
                    </button>
                  </div>
                  <!-- Chips -->
                  <div class="flex flex-wrap gap-1 min-h-[1.5rem]">
                    <span 
                      v-for="(opc, oi) in cc.platos_fuertes" 
                      :key="oi"
                      class="inline-flex items-center gap-1 px-2 py-0.5 rounded-lg bg-slate-100 dark:bg-slate-800 text-slate-700 dark:text-slate-200 text-3xs font-bold border border-slate-200 dark:border-slate-700"
                    >
                      {{ opc }}
                      <button type="button" @click="quitarOpcionCC(cc, 'platos_fuertes', oi)" class="text-rose-500 font-black">✕</button>
                    </span>
                    <span v-if="!cc.platos_fuertes?.length" class="text-3xs text-slate-400 italic">Sin plato fuerte agregado</span>
                  </div>
                </div>

                <!-- 3. Apartado Bebida -->
                <div class="p-3 bg-white dark:bg-slate-900 rounded-xl border border-slate-200 dark:border-slate-700/80 space-y-2">
                  <div class="flex items-center justify-between">
                    <span class="text-3xs font-black uppercase text-amber-700 dark:text-amber-400">
                      🥤 Bebida del Día
                    </span>
                    <span class="text-3xs text-slate-400 font-bold">{{ cc.bebidas?.length || 0 }}</span>
                  </div>

                  <!-- Selector rápido desde Catálogo General -->
                  <select 
                    @change="agregarDesdeSelectCatalogo(cc, 'bebidas', $event)"
                    class="w-full p-2 text-xs font-semibold bg-slate-50 dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded-xl text-slate-700 dark:text-slate-200 focus:outline-none focus:border-amber-500"
                  >
                    <option value="">📋 Elegir del Catálogo General...</option>
                    <optgroup v-for="grupo in catalogoPorCategoria" :key="grupo.id" :label="grupo.nombre">
                      <option v-for="p in grupo.productos" :key="p.id" :value="p.nombre">
                        {{ p.nombre }}
                      </option>
                    </optgroup>
                  </select>

                  <!-- O escribir bebida especial del día -->
                  <div class="flex gap-1.5">
                    <input 
                      v-model="cc.nuevaBebida"
                      @keydown.enter.prevent="agregarOpcionCC(cc, 'bebidas', 'nuevaBebida')"
                      type="text" 
                      maxlength="60"
                      placeholder="O escribe agua fresca del día..."
                      class="flex-1 p-1.5 text-xs font-semibold bg-slate-50 dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded-lg text-slate-800 dark:text-slate-100 focus:outline-none focus:border-amber-500"
                    />
                    <button 
                      type="button" 
                      @click="agregarOpcionCC(cc, 'bebidas', 'nuevaBebida')"
                      class="px-2.5 py-1 bg-amber-500 hover:bg-amber-600 text-white rounded-lg text-2xs font-bold transition shrink-0"
                    >
                      + Agregar
                    </button>
                  </div>
                  <!-- Chips -->
                  <div class="flex flex-wrap gap-1 min-h-[1.5rem]">
                    <span 
                      v-for="(opc, oi) in cc.bebidas" 
                      :key="oi"
                      class="inline-flex items-center gap-1 px-2 py-0.5 rounded-lg bg-slate-100 dark:bg-slate-800 text-slate-700 dark:text-slate-200 text-3xs font-bold border border-slate-200 dark:border-slate-700"
                    >
                      {{ opc }}
                      <button type="button" @click="quitarOpcionCC(cc, 'bebidas', oi)" class="text-rose-500 font-black">✕</button>
                    </span>
                    <span v-if="!cc.bebidas?.length" class="text-3xs text-slate-400 italic">Sin bebida agregada</span>
                  </div>
                </div>

                <!-- 4. Apartado Postre -->
                <div class="p-3 bg-white dark:bg-slate-900 rounded-xl border border-slate-200 dark:border-slate-700/80 space-y-2">
                  <div class="flex items-center justify-between">
                    <span class="text-3xs font-black uppercase text-amber-700 dark:text-amber-400">
                      🍮 Postre (Opcional)
                    </span>
                    <span class="text-3xs text-slate-400 font-bold">{{ cc.postres?.length || 0 }}</span>
                  </div>

                  <!-- Selector rápido desde Catálogo General -->
                  <select 
                    @change="agregarDesdeSelectCatalogo(cc, 'postres', $event)"
                    class="w-full p-2 text-xs font-semibold bg-slate-50 dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded-xl text-slate-700 dark:text-slate-200 focus:outline-none focus:border-amber-500"
                  >
                    <option value="">📋 Elegir del Catálogo General...</option>
                    <optgroup v-for="grupo in catalogoPorCategoria" :key="grupo.id" :label="grupo.nombre">
                      <option v-for="p in grupo.productos" :key="p.id" :value="p.nombre">
                        {{ p.nombre }}
                      </option>
                    </optgroup>
                  </select>

                  <!-- O escribir postre del día -->
                  <div class="flex gap-1.5">
                    <input 
                      v-model="cc.nuevoPostre"
                      @keydown.enter.prevent="agregarOpcionCC(cc, 'postres', 'nuevoPostre')"
                      type="text" 
                      maxlength="60"
                      placeholder="O escribe postre del día..."
                      class="flex-1 p-1.5 text-xs font-semibold bg-slate-50 dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded-lg text-slate-800 dark:text-slate-100 focus:outline-none focus:border-amber-500"
                    />
                    <button 
                      type="button" 
                      @click="agregarOpcionCC(cc, 'postres', 'nuevoPostre')"
                      class="px-2.5 py-1 bg-amber-500 hover:bg-amber-600 text-white rounded-lg text-2xs font-bold transition shrink-0"
                    >
                      + Agregar
                    </button>
                  </div>
                  <!-- Chips -->
                  <div class="flex flex-wrap gap-1 min-h-[1.5rem]">
                    <span 
                      v-for="(opc, oi) in cc.postres" 
                      :key="oi"
                      class="inline-flex items-center gap-1 px-2 py-0.5 rounded-lg bg-slate-100 dark:bg-slate-800 text-slate-700 dark:text-slate-200 text-3xs font-bold border border-slate-200 dark:border-slate-700"
                    >
                      {{ opc }}
                      <button type="button" @click="quitarOpcionCC(cc, 'postres', oi)" class="text-rose-500 font-black">✕</button>
                    </span>
                    <span v-if="!cc.postres?.length" class="text-3xs text-slate-400 italic">Opcional / Sin postre</span>
                  </div>
                </div>

              </div>
            </div>
          </div>
        </div>

        <!-- Footer Modal -->
        <div class="pt-3 border-t border-slate-100 dark:border-slate-800 flex justify-end gap-2">
          <button 
            @click="modalMenuDelDia = false" 
            class="px-4 py-2 text-xs font-bold text-slate-600 dark:text-slate-300 hover:bg-slate-100 dark:hover:bg-slate-800 rounded-xl"
          >
            Cancelar
          </button>
          <button 
            @click="guardarConfigMenuDelDia(true)"
            :disabled="guardandoMenuDelDia"
            class="px-5 py-2 text-xs font-bold bg-amber-500 hover:bg-amber-600 disabled:opacity-50 text-white rounded-xl shadow-sm transition active:scale-95"
          >
            <span>{{ guardandoMenuDelDia ? 'Guardando...' : 'Guardar Menú del Día' }}</span>
          </button>
        </div>
      </div>
    </div>

    <!-- ================= MODAL ASIGNAR PRODUCTO DEL CATÁLOGO AL MENÚ DEL DÍA ================= -->
    <div v-if="modalAsignarCC && prodParaAsignar" class="fixed inset-0 bg-slate-900/60 backdrop-blur-sm flex items-center justify-center p-4 z-50">
      <div class="bg-white dark:bg-slate-900 rounded-3xl p-6 max-w-md w-full shadow-2xl border border-slate-200 dark:border-slate-800 space-y-4">
        <!-- Header -->
        <div class="flex justify-between items-center border-b border-slate-100 dark:border-slate-800 pb-3">
          <div class="flex items-center gap-2">
            <span class="text-2xl">🍱</span>
            <div>
              <h3 class="text-base font-black text-slate-800 dark:text-slate-100">Agregar al Menú del Día</h3>
              <p class="text-2xs text-slate-400">Integrar producto del catálogo como opción de Comida Corrida</p>
            </div>
          </div>
          <button @click="modalAsignarCC = false" class="text-slate-400 hover:text-slate-600 font-bold">✕</button>
        </div>

        <!-- Platillo Seleccionado Info Card -->
        <div class="p-3 bg-amber-50/70 dark:bg-amber-950/30 rounded-2xl border border-amber-200/80 dark:border-amber-900/50 flex items-center gap-3">
          <div class="w-12 h-12 rounded-xl overflow-hidden bg-white dark:bg-slate-800 border border-amber-200 dark:border-amber-800/60 shrink-0 flex items-center justify-center">
            <img 
              v-if="prodParaAsignar.imagen_url"
              :src="menuStore.obtenerUrlImagen(prodParaAsignar.imagen_url)" 
              class="w-full h-full object-cover"
            />
            <span v-else class="text-xl">{{ iconoTipoItem(prodParaAsignar.tipo_item) }}</span>
          </div>
          <div class="min-w-0 flex-1">
            <h4 class="font-black text-xs text-slate-800 dark:text-slate-100 truncate">{{ prodParaAsignar.nombre }}</h4>
            <div class="text-3xs text-slate-500 dark:text-slate-400 mt-0.5">
              Categoría: <span class="font-bold text-slate-700 dark:text-slate-300">{{ prodParaAsignar.categoria_nombre || 'General' }}</span>
              · Precio carta: ${{ Number(prodParaAsignar.precio).toFixed(2) }}
            </div>
            <div class="text-3xs text-amber-700 dark:text-amber-400 font-semibold mt-0.5">
              💡 En comida corrida el cliente pagará el precio fijo del paquete.
            </div>
          </div>
        </div>

        <!-- Selección de Comida Corrida Destino -->
        <div>
          <label class="text-xs font-bold text-slate-700 dark:text-slate-300 block mb-1.5">
            1. Selecciona la Comida Corrida destino:
          </label>
          <div v-if="formMenuDelDia.comidas_corridas?.length" class="space-y-1.5 max-h-36 overflow-y-auto pr-1">
            <label 
              v-for="(cc, idx) in formMenuDelDia.comidas_corridas" 
              :key="cc.id || idx"
              class="flex items-center justify-between p-2.5 rounded-xl border cursor-pointer transition text-xs"
              :class="asignarCCIndex === idx 
                ? 'border-amber-500 bg-amber-50 dark:bg-amber-950/40 text-slate-900 dark:text-slate-100 font-extrabold shadow-2xs' 
                : 'border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-800 text-slate-700 dark:text-slate-300 hover:bg-slate-50'"
            >
              <div class="flex items-center gap-2 min-w-0 flex-1">
                <input 
                  type="radio" 
                  name="asignarCC" 
                  :value="idx" 
                  v-model="asignarCCIndex" 
                  class="text-amber-600 focus:ring-amber-500"
                />
                <span class="truncate">{{ cc.nombre || `Comida Corrida #${idx + 1}` }}</span>
                <span v-if="cc.activo === false" class="text-3xs bg-rose-100 text-rose-700 dark:bg-rose-950 dark:text-rose-300 px-1.5 py-0.2 rounded font-black shrink-0">Agotada</span>
              </div>
              <span class="text-xs font-mono font-bold text-eden-600 dark:text-eden-400 shrink-0">
                ${{ Number(cc.precio || 95).toFixed(2) }}
              </span>
            </label>
          </div>
          <div v-else class="text-xs text-slate-400 italic">
            No hay comidas corridas registradas. Se creará una automáticamente.
          </div>
        </div>

        <!-- Selección de Apartado / Tiempo del Menú -->
        <div>
          <label class="text-xs font-bold text-slate-700 dark:text-slate-300 block mb-1.5">
            2. ¿En qué tiempo o apartado se servirá?
          </label>
          <div class="grid grid-cols-2 gap-2">
            <button 
              type="button"
              @click="asignarApartado = 'entradas'"
              class="p-2.5 rounded-xl border text-left transition flex items-center gap-2"
              :class="asignarApartado === 'entradas' 
                ? 'border-amber-500 bg-amber-500 text-white font-black shadow-xs' 
                : 'border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-800 text-slate-700 dark:text-slate-200 font-bold hover:bg-slate-100'"
            >
              <span class="text-base">🥣</span>
              <div>
                <div class="text-xs">Entrada</div>
                <div class="text-3xs opacity-80 font-normal">Sopa, consomé...</div>
              </div>
            </button>

            <button 
              type="button"
              @click="asignarApartado = 'platos_fuertes'"
              class="p-2.5 rounded-xl border text-left transition flex items-center gap-2"
              :class="asignarApartado === 'platos_fuertes' 
                ? 'border-amber-500 bg-amber-500 text-white font-black shadow-xs' 
                : 'border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-800 text-slate-700 dark:text-slate-200 font-bold hover:bg-slate-100'"
            >
              <span class="text-base">🍖</span>
              <div>
                <div class="text-xs">Plato Fuerte</div>
                <div class="text-3xs opacity-80 font-normal">Con guarnición</div>
              </div>
            </button>

            <button 
              type="button"
              @click="asignarApartado = 'bebidas'"
              class="p-2.5 rounded-xl border text-left transition flex items-center gap-2"
              :class="asignarApartado === 'bebidas' 
                ? 'border-amber-500 bg-amber-500 text-white font-black shadow-xs' 
                : 'border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-800 text-slate-700 dark:text-slate-200 font-bold hover:bg-slate-100'"
            >
              <span class="text-base">🥤</span>
              <div>
                <div class="text-xs">Bebida</div>
                <div class="text-3xs opacity-80 font-normal">Agua fresca, té...</div>
              </div>
            </button>

            <button 
              type="button"
              @click="asignarApartado = 'postres'"
              class="p-2.5 rounded-xl border text-left transition flex items-center gap-2"
              :class="asignarApartado === 'postres' 
                ? 'border-amber-500 bg-amber-500 text-white font-black shadow-xs' 
                : 'border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-800 text-slate-700 dark:text-slate-200 font-bold hover:bg-slate-100'"
            >
              <span class="text-base">🍮</span>
              <div>
                <div class="text-xs">Postre</div>
                <div class="text-3xs opacity-80 font-normal">Flan, gelatina...</div>
              </div>
            </button>
          </div>
        </div>

        <!-- Botones de Acción -->
        <div class="pt-3 border-t border-slate-100 dark:border-slate-800 flex justify-end gap-2">
          <button 
            type="button"
            @click="modalAsignarCC = false"
            class="px-4 py-2 text-xs font-bold text-slate-600 dark:text-slate-300 hover:bg-slate-100 dark:hover:bg-slate-800 rounded-xl"
          >
            Cancelar
          </button>
          <button 
            type="button"
            @click="confirmarAsignarAComidaCorrida"
            :disabled="guardandoAsignacion"
            class="px-5 py-2 text-xs font-black bg-amber-500 hover:bg-amber-600 text-white rounded-xl shadow-xs transition active:scale-95 disabled:opacity-50 flex items-center gap-1.5"
          >
            <span>{{ guardandoAsignacion ? 'Guardando...' : '✓ Asignar al Menú del Día' }}</span>
          </button>
        </div>
      </div>
    </div>

    <!-- Toast de Notificación Rápida -->
    <transition enter-active-class="transform ease-out duration-300 transition" enter-from-class="translate-y-2 opacity-0 sm:translate-y-0 sm:translate-x-2" enter-to-class="translate-y-0 opacity-100 sm:translate-x-0" leave-active-class="transition ease-in duration-200" leave-from-class="opacity-100" leave-to-class="opacity-0">
      <div 
        v-if="toastNotif.visible" 
        class="fixed bottom-5 right-5 z-50 p-4 rounded-2xl shadow-xl flex items-center gap-3 border"
        :class="toastNotif.tipo === 'success' 
          ? 'bg-slate-900 text-white border-slate-700 dark:bg-emerald-950 dark:border-emerald-800' 
          : 'bg-rose-900 text-white border-rose-700'"
      >
        <span class="text-xl">{{ toastNotif.icono || '🍱' }}</span>
        <div class="text-xs font-bold">{{ toastNotif.mensaje }}</div>
      </div>
    </transition>

    <!-- ================= MODAL ALTA / EDICIÓN DE PLATILLO O SERVICIO ================= -->
    <div v-if="modalProducto" class="fixed inset-0 bg-slate-900/60 backdrop-blur-sm flex items-center justify-center p-4 z-50">
      <div class="bg-white dark:bg-slate-900 rounded-3xl p-6 max-w-lg w-full shadow-2xl border border-slate-200 dark:border-slate-800 space-y-4 max-h-[90vh] flex flex-col">
        <div class="flex justify-between items-center border-b border-slate-100 dark:border-slate-800 pb-3">
          <h3 class="text-lg font-black text-slate-800 dark:text-slate-100">
            {{ editandoId ? 'Editar Platillo o Servicio' : 'Dar de Alta Platillo, Producto o Servicio' }}
          </h3>
          <button @click="modalProducto = false" class="text-slate-400 hover:text-slate-600 font-bold">✕</button>
        </div>

        <div class="flex-1 overflow-y-auto space-y-3.5 pr-1">
          <!-- Nombre -->
          <div>
            <label class="text-xs font-bold text-slate-700 dark:text-slate-300">Nombre del Platillo / Producto / Servicio *</label>
            <input 
              v-model="formProducto.nombre"
              type="text"
              maxlength="100"
              placeholder="Ej. Café Moka Tradicional, Hamburguesa BBQ, Descorche..."
              class="w-full mt-1 p-2.5 text-xs font-semibold bg-white dark:bg-slate-800 border border-slate-300 dark:border-slate-700 rounded-xl text-slate-800 dark:text-slate-100 focus:outline-none focus:border-eden-600"
            />
          </div>

          <!-- Género / Categoría y Tipo de Ítem -->
          <div class="grid grid-cols-1 sm:grid-cols-2 gap-3">
            <div>
              <div class="flex justify-between items-center">
                <label class="text-xs font-bold text-slate-700 dark:text-slate-300">Tipo o Género (Categoría) *</label>
                <button 
                  type="button" 
                  @click="abrirModalCategoria" 
                  class="text-3xs font-extrabold text-eden-600 hover:underline"
                >
                  + Nueva
                </button>
              </div>
              <select 
                v-model.number="formProducto.categoria_id"
                class="w-full mt-1 p-2.5 text-xs font-semibold bg-white dark:bg-slate-800 border border-slate-300 dark:border-slate-700 rounded-xl text-slate-800 dark:text-slate-100 focus:outline-none focus:border-eden-600"
              >
                <option v-for="cat in menuStore.categorias" :key="cat.id" :value="cat.id">
                  {{ cat.nombre }}
                </option>
              </select>
            </div>

            <div>
              <label class="text-xs font-bold text-slate-700 dark:text-slate-300">Naturaleza del Ítem *</label>
              <select 
                v-model="formProducto.tipo_item"
                class="w-full mt-1 p-2.5 text-xs font-semibold bg-white dark:bg-slate-800 border border-slate-300 dark:border-slate-700 rounded-xl text-slate-800 dark:text-slate-100 focus:outline-none focus:border-eden-600"
              >
                <option value="platillo">🍽️ Platillo (Comida Cocina)</option>
                <option value="bebida">☕ Bebida (Barra / Cafetería)</option>
                <option value="producto">📦 Producto (Sin preparación)</option>
                <option value="servicio">🛎️ Servicio (Cobrable)</option>
              </select>
            </div>
          </div>

          <!-- Precio y Requerimiento de Cocina -->
          <div class="grid grid-cols-1 sm:grid-cols-2 gap-3">
            <div>
              <label class="text-xs font-bold text-slate-700 dark:text-slate-300">Precio de Venta ($ MXN) *</label>
              <input 
                v-model.number="formProducto.precio"
                type="number"
                min="0"
                max="99999.99"
                step="0.50"
                inputmode="decimal"
                placeholder="0.00"
                class="w-full mt-1 p-2.5 text-xs font-black bg-white dark:bg-slate-800 border border-slate-300 dark:border-slate-700 rounded-xl text-slate-800 dark:text-slate-100 focus:outline-none focus:border-eden-600 font-mono"
              />
            </div>

            <div class="flex items-center pt-5">
              <label class="flex items-center gap-2 cursor-pointer text-xs font-bold text-slate-700 dark:text-slate-300">
                <input 
                  v-model="formProducto.requiere_cocina"
                  type="checkbox"
                  class="rounded text-eden-600 focus:ring-eden-500 w-4 h-4"
                />
                <span>¿Enviar a pantalla Cocina/KDS?</span>
              </label>
            </div>
          </div>

          <!-- Descripción -->
          <div>
            <label class="text-xs font-bold text-slate-700 dark:text-slate-300">Descripción / Ingredientes para la carta:</label>
            <textarea 
              v-model="formProducto.descripcion"
              rows="2.5"
              placeholder="Ej. Exquisito café espresso con leche vaporizada..."
              class="w-full mt-1 p-2.5 text-xs font-semibold bg-white dark:bg-slate-800 border border-slate-300 dark:border-slate-700 rounded-xl text-slate-800 dark:text-slate-100 focus:outline-none focus:border-eden-600 resize-none"
            ></textarea>
          </div>

          <!-- Fotografía o Imagen -->
          <div class="p-3 bg-slate-50 dark:bg-slate-800/60 rounded-2xl border border-slate-200 dark:border-slate-700 space-y-2.5">
            <div class="flex justify-between items-center">
              <label class="text-xs font-bold text-slate-700 dark:text-slate-300">
                Fotografía o Imagen del Platillo
              </label>
              <button 
                v-if="formProducto.imagen_url" 
                type="button" 
                @click="quitarImagen"
                class="text-3xs font-bold text-rose-600 hover:text-rose-700 dark:text-rose-400"
              >
                ✕ Quitar Imagen
              </button>
            </div>

            <div class="flex items-center gap-3">
              <div class="w-16 h-16 rounded-2xl overflow-hidden bg-white dark:bg-slate-800 border-2 border-dashed border-slate-300 dark:border-slate-600 shrink-0 flex items-center justify-center relative shadow-xs">
                <img 
                  v-if="formProducto.imagen_url" 
                  :src="menuStore.obtenerUrlImagen(formProducto.imagen_url)" 
                  alt="Preview" 
                  class="w-full h-full object-cover"
                />
                <div v-else class="text-center p-1 text-slate-300 dark:text-slate-600">
                  <span class="text-xl block">📷</span>
                </div>
                <div v-if="subiendoImagen" class="absolute inset-0 bg-black/60 flex items-center justify-center text-white text-xs font-bold">
                  ⏳
                </div>
              </div>

              <div class="flex-1 space-y-2">
                <input 
                  ref="inputArchivo"
                  type="file" 
                  accept="image/*" 
                  @change="manejarSubidaImagen" 
                  class="hidden" 
                  id="file-upload-dish"
                />
                <label 
                  for="file-upload-dish"
                  class="cursor-pointer inline-flex items-center gap-1.5 px-3 py-1.5 rounded-xl bg-white dark:bg-slate-800 hover:bg-slate-100 dark:hover:bg-slate-700 border border-slate-300 dark:border-slate-600 text-slate-700 dark:text-slate-200 text-xs font-bold shadow-2xs active:scale-95 transition"
                >
                  <span>📁</span>
                  <span>{{ subiendoImagen ? 'Subiendo imagen...' : 'Cargar foto del dispositivo' }}</span>
                </label>

                <input 
                  v-model="formProducto.imagen_url" 
                  type="text" 
                  maxlength="255"
                  placeholder="O escribe URL: https://... o /uploads/..."
                  class="w-full px-2.5 py-1.5 text-xs bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded-xl text-slate-700 dark:text-slate-200 focus:outline-none focus:border-eden-600 font-mono text-3xs"
                />
              </div>
            </div>
          </div>

          <!-- Disponibilidad -->
          <label class="flex items-center gap-2 p-2.5 rounded-xl bg-slate-50 dark:bg-slate-800 border border-slate-200 dark:border-slate-700 cursor-pointer">
            <input 
              v-model="formProducto.disponible"
              type="checkbox"
              class="rounded text-emerald-600 focus:ring-emerald-500 w-4 h-4"
            />
            <span class="text-xs font-bold text-slate-700 dark:text-slate-300">
              Disponible de inmediato en la Carta de Hoy (Comandero y Carta Digital)
            </span>
          </label>
        </div>

        <div class="pt-3 border-t border-slate-100 dark:border-slate-800 flex justify-between items-center gap-2">
          <div>
            <button 
              v-if="editandoId"
              type="button"
              @click="eliminarDesdeModal"
              class="px-3.5 py-2 text-xs font-bold text-rose-600 dark:text-rose-400 hover:bg-rose-50 dark:hover:bg-rose-950/40 rounded-xl transition flex items-center gap-1.5"
            >
              <span>🗑️</span>
              <span>Eliminar Platillo</span>
            </button>
          </div>
          <div class="flex items-center gap-2">
            <button 
              @click="modalProducto = false"
              class="px-4 py-2 text-xs font-bold text-slate-600 dark:text-slate-300 hover:bg-slate-100 dark:hover:bg-slate-800 rounded-xl"
            >
              Cancelar
            </button>
            <button 
              @click="guardarProducto"
              :disabled="!formProducto.nombre || !formProducto.categoria_id || formProducto.precio <= 0 || guardando"
              class="px-5 py-2 text-xs font-bold bg-eden-600 hover:bg-eden-700 disabled:opacity-50 text-white rounded-xl shadow-sm transition active:scale-95"
            >
              <span v-if="guardando">Guardando...</span>
              <span v-else>{{ editandoId ? 'Actualizar Cambios' : 'Guardar y Publicar' }}</span>
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- ================= MODAL GESTIÓN DE CATEGORÍAS (GÉNEROS) ================= -->
    <div v-if="modalCategorias" class="fixed inset-0 bg-slate-900/60 backdrop-blur-sm flex items-center justify-center p-4 z-50">
      <div class="bg-white dark:bg-slate-900 rounded-3xl p-6 max-w-md w-full shadow-2xl border border-slate-200 dark:border-slate-800 space-y-4">
        <div class="flex justify-between items-center border-b border-slate-100 dark:border-slate-800 pb-3">
          <div class="flex items-center gap-2">
            <span class="text-xl">🏷️</span>
            <h3 class="text-lg font-black text-slate-800 dark:text-slate-100">Géneros y Categorías</h3>
          </div>
          <button @click="modalCategorias = false" class="text-slate-400 hover:text-slate-600 font-bold">✕</button>
        </div>

        <!-- Formulario para agregar nueva categoría -->
        <div class="p-3 bg-slate-50 dark:bg-slate-800/60 rounded-2xl border border-slate-200 dark:border-slate-700 space-y-2">
          <span class="text-2xs font-extrabold uppercase text-slate-400">Crear Nueva Categoría</span>
          <div class="flex gap-2">
            <input 
              v-model="nuevaCatNombre"
              type="text"
              maxlength="50"
              placeholder="Ej. Desayunos, Entradas, Postres..."
              class="flex-1 p-2 text-xs font-semibold bg-white dark:bg-slate-800 border border-slate-300 dark:border-slate-700 rounded-xl text-slate-800 dark:text-slate-100 focus:outline-none focus:border-eden-600"
            />
            <button 
              @click="guardarNuevaCategoria"
              :disabled="!nuevaCatNombre.trim()"
              class="px-3.5 py-2 text-xs font-bold bg-eden-600 hover:bg-eden-700 disabled:opacity-50 text-white rounded-xl shadow-xs transition"
            >
              + Agregar
            </button>
          </div>
        </div>

        <!-- Lista de categorías existentes -->
        <div class="space-y-1.5 max-h-56 overflow-y-auto pr-1">
          <div 
            v-for="cat in menuStore.categorias" 
            :key="cat.id"
            class="flex justify-between items-center p-2.5 rounded-xl bg-slate-50 dark:bg-slate-800 border border-slate-200 dark:border-slate-700 text-xs"
          >
            <div>
              <span class="font-bold text-slate-800 dark:text-slate-100">{{ cat.nombre }}</span>
              <span class="text-3xs text-slate-400 block">{{ cat.descripcion || 'Sin descripción' }}</span>
            </div>
            <button 
              @click="eliminarCategoria(cat.id)"
              title="Desactivar categoría"
              class="text-xs text-rose-500 hover:bg-rose-100 dark:hover:bg-rose-950/60 p-1.5 rounded-lg transition"
            >
              🗑️
            </button>
          </div>
        </div>

        <div class="pt-3 border-t border-slate-100 dark:border-slate-800 flex justify-end">
          <button 
            @click="modalCategorias = false"
            class="px-4 py-2 bg-slate-100 dark:bg-slate-800 hover:bg-slate-200 text-slate-700 dark:text-slate-300 rounded-xl text-xs font-bold"
          >
            Listo
          </button>
        </div>
      </div>
    </div>

  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useMenuStore } from '../stores/menu'

const menuStore = useMenuStore()

// Búsqueda y Filtros Columna Izquierda (Carta de Hoy)
const busquedaCarta = ref('')
const catFiltroCarta = ref(null)

// Búsqueda y Filtros Columna Derecha (Catálogo General)
const busquedaCatalogo = ref('')
const catFiltroCatalogo = ref(null)
const filtroEstadoCatalogo = ref('todos') // 'todos', 'fuera_de_carta', 'en_carta'

// Modales y Formularios
const modalProducto = ref(false)
const editandoId = ref(null)
const guardando = ref(false)
const subiendoImagen = ref(false)
const inputArchivo = ref(null)

const formProducto = ref({
  nombre: '',
  categoria_id: null,
  tipo_item: 'platillo',
  precio: 0,
  descripcion: '',
  imagen_url: '',
  requiere_cocina: true,
  disponible: true
})

// Modal Menú del Día (Comidas Corridas)
const modalMenuDelDia = ref(false)
const guardandoMenuDelDia = ref(false)
const formMenuDelDia = ref({
  activo: true,
  nombre: 'Menú del Día (Comida Corrida)',
  descripcion: 'Comida corrida completa con Entrada, Plato Fuerte, Bebida y Postre',
  precio: 95.0,
  hora_inicio: '12:00',
  hora_fin: '18:00',
  comidas_corridas: []
})

// Modal Asignar a Comida Corrida desde Catálogo General o Carta
const modalAsignarCC = ref(false)
const prodParaAsignar = ref(null)
const asignarCCIndex = ref(0)
const asignarApartado = ref('platos_fuertes')
const guardandoAsignacion = ref(false)

// Notificación Toast en pantalla
const toastNotif = ref({
  visible: false,
  mensaje: '',
  tipo: 'success',
  icono: '🍱'
})
let toastTimeout = null
const mostrarToast = (mensaje, tipo = 'success', icono = '🍱') => {
  if (toastTimeout) clearTimeout(toastTimeout)
  toastNotif.value = { visible: true, mensaje, tipo, icono }
  toastTimeout = setTimeout(() => {
    toastNotif.value.visible = false
  }, 3500)
}

// Modal Categorías
const modalCategorias = ref(false)
const nuevaCatNombre = ref('')

onMounted(async () => {
  await menuStore.cargarCatalogo(true)
  if (menuStore.categorias.length > 0 && !formProducto.value.categoria_id) {
    formProducto.value.categoria_id = menuStore.categorias[0].id
  }
  sincronizarFormMenuDelDia()
})

const sincronizarFormMenuDelDia = () => {
  if (menuStore.menuDelDia) {
    let rawCC = menuStore.menuDelDia.comidas_corridas || []
    if (rawCC.length === 0) {
      rawCC = [{
        id: '1',
        nombre: 'Comida Corrida #1',
        precio: Number(menuStore.menuDelDia.precio || 95.0),
        activo: true,
        imagen_url: '',
        entradas: [...(menuStore.menuDelDia.entradas || [])],
        platos_fuertes: [...(menuStore.menuDelDia.platos_fuertes || [])],
        bebidas: [...(menuStore.menuDelDia.bebidas || [])],
        postres: [...(menuStore.menuDelDia.postres || [])]
      }]
    }
    formMenuDelDia.value = {
      activo: menuStore.menuDelDia.activo ?? true,
      nombre: menuStore.menuDelDia.nombre || 'Menú del Día (Comida Corrida)',
      descripcion: menuStore.menuDelDia.descripcion || '',
      precio: Number(menuStore.menuDelDia.precio || 95.0),
      hora_inicio: menuStore.menuDelDia.hora_inicio || '12:00',
      hora_fin: menuStore.menuDelDia.hora_fin || '18:00',
      comidas_corridas: rawCC.map((c, i) => ({
        id: c.id || String(i + 1),
        nombre: c.nombre || `Comida Corrida #${i + 1}`,
        precio: Number(c.precio || menuStore.menuDelDia.precio || 95.0),
        activo: c.activo ?? true,
        imagen_url: c.imagen_url || '',
        entradas: [...(c.entradas || [])],
        platos_fuertes: [...(c.platos_fuertes || [])],
        bebidas: [...(c.bebidas || [])],
        postres: [...(c.postres || [])],
        nuevaEntrada: '',
        nuevoFuerte: '',
        nuevaBebida: '',
        nuevoPostre: ''
      }))
    }
  }
}

const agregarNuevaComidaCorrida = () => {
  const num = formMenuDelDia.value.comidas_corridas.length + 1
  formMenuDelDia.value.comidas_corridas.push({
    id: String(Date.now()),
    nombre: `Comida Corrida #${num}`,
    precio: Number(formMenuDelDia.value.precio || 95.0),
    activo: true,
    imagen_url: '',
    entradas: [],
    platos_fuertes: [],
    bebidas: [],
    postres: [],
    nuevaEntrada: '',
    nuevoFuerte: '',
    nuevaBebida: '',
    nuevoPostre: ''
  })
}

const eliminarComidaCorrida = (idx) => {
  formMenuDelDia.value.comidas_corridas.splice(idx, 1)
}

// Métodos de carga de foto para Comida Corrida
const subiendoImagenCCIndex = ref(null)

const subirImagenParaCC = async (e, cc, idx) => {
  const file = e.target.files?.[0]
  if (!file) return
  subiendoImagenCCIndex.value = idx
  try {
    const res = await menuStore.subirImagen(file)
    cc.imagen_url = res.url
  } catch (err) {
    alert(err.response?.data?.detail || 'Error al subir la imagen')
  } finally {
    subiendoImagenCCIndex.value = null
  }
}

const quitarImagenCC = (cc) => {
  cc.imagen_url = ''
}

const agregarOpcionCC = (cc, campo, inputKey) => {
  const val = cc[inputKey]?.trim()
  if (!val) return
  if (!cc[campo]) cc[campo] = []
  if (!cc[campo].includes(val)) {
    cc[campo].push(val)
  }
  cc[inputKey] = ''
}

const agregarDesdeSelectCatalogo = (cc, campo, event) => {
  const nombre = event.target.value
  if (!nombre) return
  if (!cc[campo]) cc[campo] = []
  if (!cc[campo].includes(nombre)) {
    cc[campo].push(nombre)
  }
  event.target.value = ''
}

const quitarOpcionCC = (cc, campo, idx) => {
  if (cc[campo]) {
    cc[campo].splice(idx, 1)
  }
}

const abrirModalMenuDelDia = () => {
  sincronizarFormMenuDelDia()
  modalMenuDelDia.value = true
}

const alternarEstadoMenuDelDia = async () => {
  if (!menuStore.menuDelDia) return
  const nuevoEstado = !menuStore.menuDelDia.activo
  try {
    await menuStore.guardarMenuDelDia({
      ...menuStore.menuDelDia,
      activo: nuevoEstado
    })
    mostrarToast(nuevoEstado ? 'Servicio de Menú del Día activado hoy.' : 'Servicio de Menú del Día pausado.')
  } catch (err) {
    alert('Error al cambiar estado del Menú del Día.')
  }
}

const alternarDisponibilidadCC = async (cc, index) => {
  if (!menuStore.menuDelDia) return
  const nuevoActivo = cc.activo === false ? true : false
  const corridasActualizadas = (menuStore.menuDelDia.comidas_corridas || []).map((item, idx) => {
    if (idx === index) {
      return { ...item, activo: nuevoActivo }
    }
    return item
  })
  try {
    await menuStore.guardarMenuDelDia({
      ...menuStore.menuDelDia,
      comidas_corridas: corridasActualizadas
    })
    sincronizarFormMenuDelDia()
    mostrarToast(nuevoActivo ? `"${cc.nombre}" reactivada como disponible.` : `"${cc.nombre}" marcada como agotada hoy.`, nuevoActivo ? 'success' : 'error')
  } catch (err) {
    alert('Error al cambiar disponibilidad de la comida corrida.')
  }
}

const guardarConfigMenuDelDia = async (mostrarAlerta = true) => {
  guardandoMenuDelDia.value = true
  try {
    const payload = {
      activo: formMenuDelDia.value.activo,
      nombre: formMenuDelDia.value.nombre,
      descripcion: formMenuDelDia.value.descripcion,
      precio: Number(formMenuDelDia.value.precio || 95.0),
      hora_inicio: formMenuDelDia.value.hora_inicio,
      hora_fin: formMenuDelDia.value.hora_fin,
      comidas_corridas: formMenuDelDia.value.comidas_corridas.map((c, i) => ({
        id: c.id || String(i + 1),
        nombre: c.nombre || `Comida Corrida #${i + 1}`,
        precio: Number(c.precio || 95.0),
        activo: Boolean(c.activo !== false),
        imagen_url: c.imagen_url || '',
        entradas: [...(c.entradas || [])],
        platos_fuertes: [...(c.platos_fuertes || [])],
        bebidas: [...(c.bebidas || [])],
        postres: [...(c.postres || [])]
      }))
    }
    await menuStore.guardarMenuDelDia(payload)
    if (mostrarAlerta) {
      modalMenuDelDia.value = false
      mostrarToast('Comidas corridas guardadas y sincronizadas exitosamente.', 'success', '🍱')
    }
  } catch (err) {
    alert(err.response?.data?.detail || 'Error al guardar la configuración de comidas corridas.')
    throw err
  } finally {
    guardandoMenuDelDia.value = false
  }
}

// Catálogo por categoría para selectores en modal
const catalogoPorCategoria = computed(() => {
  return menuStore.categorias.map(cat => ({
    id: cat.id,
    nombre: cat.nombre,
    productos: menuStore.productos.filter(p => p.categoria_id === cat.id)
  })).filter(g => g.productos.length > 0)
})

// Acciones para asignación rápida desde tarjeta de Catálogo General
const abrirAsignarAComidaCorrida = (item) => {
  sincronizarFormMenuDelDia()
  if (!formMenuDelDia.value.comidas_corridas || formMenuDelDia.value.comidas_corridas.length === 0) {
    agregarNuevaComidaCorrida()
  }
  prodParaAsignar.value = item
  asignarCCIndex.value = 0

  const nombre = (item.nombre || '').toLowerCase()
  const cat = (item.categoria_nombre || '').toLowerCase()
  const tipo = item.tipo_item || ''

  if (tipo === 'bebida' || cat.includes('bebida') || cat.includes('café') || cat.includes('cafe') || cat.includes('jugo') || cat.includes('agua')) {
    asignarApartado.value = 'bebidas'
  } else if (cat.includes('postre') || cat.includes('dulce') || cat.includes('reposter') || cat.includes('helado')) {
    asignarApartado.value = 'postres'
  } else if (cat.includes('sopa') || cat.includes('entrada') || cat.includes('caldo') || cat.includes('crema') || nombre.includes('sopa') || nombre.includes('puchero') || nombre.includes('consom')) {
    asignarApartado.value = 'entradas'
  } else {
    asignarApartado.value = 'platos_fuertes'
  }

  modalAsignarCC.value = true
}

const confirmarAsignarAComidaCorrida = async () => {
  if (!prodParaAsignar.value) return
  guardandoAsignacion.value = true
  try {
    const cc = formMenuDelDia.value.comidas_corridas[asignarCCIndex.value]
    if (!cc) {
      alert('Selecciona una comida corrida válida.')
      return
    }

    if (!cc[asignarApartado.value]) {
      cc[asignarApartado.value] = []
    }

    const itemNombre = prodParaAsignar.value.nombre
    if (!cc[asignarApartado.value].includes(itemNombre)) {
      cc[asignarApartado.value].push(itemNombre)
    }

    await guardarConfigMenuDelDia(false)
    modalAsignarCC.value = false

    const nombresApartados = {
      entradas: 'Entrada 🥣',
      platos_fuertes: 'Plato Fuerte 🍖',
      bebidas: 'Bebida 🥤',
      postres: 'Postre 🍮'
    }
    mostrarToast(`"${itemNombre}" se agregó a ${cc.nombre} (${nombresApartados[asignarApartado.value] || ''})`, 'success', '🍱')
  } catch (err) {
    alert('Error al agregar el platillo al Menú del Día.')
  } finally {
    guardandoAsignacion.value = false
  }
}

// Computeds Columna Izquierda: Carta de Hoy (disponible = true)
const totalEnCarta = computed(() => {
  return menuStore.productos.filter(p => p.disponible).length
})

const conteoEnCartaPorCat = (catId) => {
  return menuStore.productos.filter(p => p.disponible && p.categoria_id === catId).length
}

const productosEnCarta = computed(() => {
  return menuStore.productos.filter(p => {
    if (!p.disponible) return false
    const matchCat = catFiltroCarta.value ? p.categoria_id === catFiltroCarta.value : true
    const matchBusq = busquedaCarta.value 
      ? p.nombre.toLowerCase().includes(busquedaCarta.value.toLowerCase()) || 
        (p.descripcion && p.descripcion.toLowerCase().includes(busquedaCarta.value.toLowerCase()))
      : true
    return matchCat && matchBusq
  })
})

// Computeds Columna Derecha: Catálogo General
const conteoTotalPorCat = (catId) => {
  return menuStore.productos.filter(p => p.categoria_id === catId).length
}

const productosCatalogo = computed(() => {
  return menuStore.productos.filter(p => {
    // Filtro por estado
    if (filtroEstadoCatalogo.value === 'fuera_de_carta' && p.disponible) return false
    if (filtroEstadoCatalogo.value === 'en_carta' && !p.disponible) return false

    // Filtro por categoría
    const matchCat = catFiltroCatalogo.value ? p.categoria_id === catFiltroCatalogo.value : true

    // Filtro por búsqueda
    const matchBusq = busquedaCatalogo.value 
      ? p.nombre.toLowerCase().includes(busquedaCatalogo.value.toLowerCase()) || 
        (p.descripcion && p.descripcion.toLowerCase().includes(busquedaCatalogo.value.toLowerCase()))
      : true

    return matchCat && matchBusq
  })
})

// Acciones Menú del Día
// Acciones Platillos
const abrirModalNuevoProducto = () => {
  editandoId.value = null
  formProducto.value = {
    nombre: '',
    categoria_id: menuStore.categorias[0]?.id || 1,
    tipo_item: 'platillo',
    precio: 0,
    descripcion: '',
    imagen_url: '',
    requiere_cocina: true,
    disponible: true
  }
  if (inputArchivo.value) inputArchivo.value.value = ''
  modalProducto.value = true
}

const abrirModalEditar = (item) => {
  editandoId.value = item.id
  formProducto.value = {
    nombre: item.nombre,
    categoria_id: item.categoria_id,
    tipo_item: item.tipo_item || 'platillo',
    precio: Number(item.precio),
    descripcion: item.descripcion || '',
    imagen_url: item.imagen_url || '',
    requiere_cocina: item.requiere_cocina ?? true,
    disponible: item.disponible ?? true
  }
  if (inputArchivo.value) inputArchivo.value.value = ''
  modalProducto.value = true
}

const manejarSubidaImagen = async (e) => {
  const file = e.target.files?.[0]
  if (!file) return
  subiendoImagen.value = true
  try {
    const res = await menuStore.subirImagen(file)
    formProducto.value.imagen_url = res.url
  } catch (err) {
    alert(err.response?.data?.detail || 'Error al subir la imagen')
  } finally {
    subiendoImagen.value = false
  }
}

const quitarImagen = () => {
  formProducto.value.imagen_url = ''
  if (inputArchivo.value) inputArchivo.value.value = ''
}

const guardarProducto = async () => {
  guardando.value = true
  try {
    if (editandoId.value) {
      await menuStore.actualizarProducto(editandoId.value, formProducto.value)
      alert('Platillo actualizado exitosamente.')
    } else {
      await menuStore.crearProducto(formProducto.value)
      alert('Platillo / producto dado de alta exitosamente en el menú.')
    }
    modalProducto.value = false
  } catch (err) {
    alert(err.response?.data?.detail || 'Error al guardar el producto.')
  } finally {
    guardando.value = false
  }
}

const alternarDisponibilidad = async (item) => {
  try {
    await menuStore.alternarDisponibilidad(item.id)
  } catch (err) {
    alert('Error al cambiar disponibilidad.')
  }
}

const confirmarEliminarProducto = async (item) => {
  if (!confirm(`¿Estás seguro de que deseas eliminar "${item.nombre}" del catálogo general?`)) return
  try {
    await menuStore.eliminarProducto(item.id)
    mostrarToast(`"${item.nombre}" eliminado del catálogo general.`, 'success', '🗑️')
  } catch (err) {
    alert(err.response?.data?.detail || 'Error al eliminar el platillo o servicio.')
  }
}

const eliminarDesdeModal = async () => {
  if (!editandoId.value) return
  const item = menuStore.productos.find(p => p.id === editandoId.value)
  const nombre = item ? item.nombre : 'este platillo'
  if (!confirm(`¿Estás seguro de que deseas eliminar permanentemente "${nombre}" del catálogo general?`)) return
  try {
    await menuStore.eliminarProducto(editandoId.value)
    modalProducto.value = false
    editandoId.value = null
    mostrarToast(`"${nombre}" eliminado del catálogo general.`, 'success', '🗑️')
  } catch (err) {
    alert(err.response?.data?.detail || 'Error al eliminar el platillo o servicio.')
  }
}

// Categorías
const abrirModalCategoria = () => {
  nuevaCatNombre.value = ''
  modalCategorias.value = true
}

const guardarNuevaCategoria = async () => {
  if (!nuevaCatNombre.value.trim()) return
  try {
    await menuStore.crearCategoria({
      nombre: nuevaCatNombre.value.trim(),
      descripcion: `Categoría ${nuevaCatNombre.value.trim()}`,
      orden: menuStore.categorias.length + 1
    })
    nuevaCatNombre.value = ''
    alert('Categoría creada exitosamente.')
  } catch (err) {
    alert(err.response?.data?.detail || 'Error al crear categoría.')
  }
}

const eliminarCategoria = async (id) => {
  if (!confirm('¿Deseas desactivar esta categoría del menú?')) return
  try {
    await menuStore.eliminarCategoria(id)
    alert('Categoría desactivada.')
  } catch (err) {
    alert('Error al desactivar categoría.')
  }
}

const badgeTipoItem = (tipo) => {
  switch (tipo) {
    case 'bebida': return 'bg-sky-100 text-sky-800 dark:bg-sky-950/60 dark:text-sky-300'
    case 'producto': return 'bg-amber-100 text-amber-800 dark:bg-amber-950/60 dark:text-amber-300'
    case 'servicio': return 'bg-purple-100 text-purple-800 dark:bg-purple-950/60 dark:text-purple-300'
    default: return 'bg-slate-100 text-slate-800 dark:bg-slate-800 dark:text-slate-300'
  }
}

const iconoTipoItem = (tipo) => {
  switch (tipo) {
    case 'bebida': return '☕'
    case 'producto': return '📦'
    case 'servicio': return '🛎️'
    case 'menu_del_dia': return '🍱'
    default: return '🍽️'
  }
}
</script>

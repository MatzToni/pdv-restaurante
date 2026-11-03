<template>
  <div class="min-h-screen bg-slate-50 dark:bg-slate-950 text-slate-800 dark:text-slate-100 transition-colors">
    <!-- Navbar Exclusiva para Clientes -->
    <header class="bg-white/90 dark:bg-slate-900/90 backdrop-blur-md sticky top-0 z-40 border-b border-slate-200/80 dark:border-slate-800/80">
      <div class="max-w-5xl mx-auto px-4 h-16 flex items-center justify-between">
        <!-- Logo y Nombre -->
        <div class="flex items-center gap-3">
          <img 
            :src="configStore.logoUrl || '/logo.png'" 
            :alt="configStore.nombreRestaurante" 
            class="w-10 h-10 object-contain rounded-full shadow-sm"
          />
          <div>
            <h1 class="font-black text-slate-800 dark:text-slate-100 text-base leading-tight tracking-tight">{{ configStore.nombreRestaurante }}</h1>
            <span class="text-2xs text-eden-600 dark:text-eden-400 font-bold uppercase tracking-wider">Menú Digital & Carta</span>
          </div>
        </div>

        <!-- Acciones: Tema y Código QR -->
        <div class="flex items-center gap-2">
          <!-- Botón Ver QR de la Mesa -->
          <button 
            @click="modalQR = true"
            class="px-3 py-1.5 bg-slate-100 dark:bg-slate-800 hover:bg-slate-200 dark:hover:bg-slate-700 text-slate-700 dark:text-slate-300 rounded-xl text-xs font-bold transition flex items-center gap-1.5 border border-slate-200 dark:border-slate-700"
          >
            <span>📱</span> Código QR
          </button>

          <!-- Selector de Tema (Claro / Oscuro) -->
          <button
            @click="alternarTema"
            class="w-9 h-9 rounded-xl bg-slate-100 dark:bg-slate-800 text-slate-600 dark:text-slate-300 flex items-center justify-center text-sm transition border border-slate-200 dark:border-slate-700"
            :title="themeStore.tema === 'oscuro' ? 'Cambiar a Modo Claro' : 'Cambiar a Modo Oscuro'"
          >
            {{ themeStore.tema === 'oscuro' ? '☀️' : '🌙' }}
          </button>
        </div>
      </div>
    </header>

    <!-- Hero / Bienvenida -->
    <section class="max-w-5xl mx-auto px-4 pt-8 pb-4 text-center space-y-3">
      <div v-if="configStore.slogan" class="flex items-center justify-center">
        <span class="inline-block px-3 py-1 rounded-full bg-eden-100 dark:bg-eden-950/60 text-eden-800 dark:text-eden-300 text-2xs font-black uppercase tracking-widest border border-eden-200 dark:border-eden-800/40">
          {{ configStore.slogan }}
        </span>
      </div>

      <h2 class="text-3xl sm:text-4xl font-black text-slate-900 dark:text-slate-100 tracking-tight">
        {{ configStore.tituloCarta || 'Nuestra Carta' }}
      </h2>
      <p class="text-xs sm:text-sm text-slate-500 dark:text-slate-400 max-w-md mx-auto whitespace-pre-line leading-relaxed">
        {{ configStore.subtituloCarta || 'Platillos preparados al momento con ingredientes frescos, recetas mexicanas tradicionales y café tostado artesanal.' }}
      </p>

      <!-- Barra de Búsqueda Interactiva -->
      <div class="max-w-md mx-auto pt-3">
        <div class="relative">
          <span class="absolute inset-y-0 left-0 pl-3.5 flex items-center pointer-events-none text-slate-400">
            🔍
          </span>
          <input 
            v-model="busqueda"
            type="text"
            maxlength="80"
            placeholder="Buscar por platillo, café, postre..."
            class="w-full pl-10 pr-4 py-3 rounded-2xl bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 text-slate-800 dark:text-slate-100 text-sm font-medium shadow-sm focus:outline-none focus:border-eden-600 dark:focus:border-eden-500 transition"
          />
        </div>
      </div>
    </section>

    <!-- Filtro de Categorías Sticky -->
    <div class="sticky top-16 z-30 bg-slate-50/95 dark:bg-slate-950/95 backdrop-blur-md py-3 border-y border-slate-200/60 dark:border-slate-800/60">
      <div class="max-w-5xl mx-auto px-4 flex gap-2 overflow-x-auto no-scrollbar">
        <button
          @click="categoriaActiva = null"
          :class="[
            'px-4 py-2 rounded-xl text-xs font-extrabold transition-all shrink-0',
            categoriaActiva === null
              ? 'bg-eden-600 text-white shadow-md shadow-eden-600/20'
              : 'bg-white dark:bg-slate-900 text-slate-600 dark:text-slate-300 hover:bg-slate-100 dark:hover:bg-slate-800 border border-slate-200 dark:border-slate-800'
          ]"
        >
          Todo el Menú
        </button>
        <button
          v-for="cat in menuStore.categorias"
          :key="cat.id"
          @click="categoriaActiva = cat.id"
          :class="[
            'px-4 py-2 rounded-xl text-xs font-extrabold transition-all shrink-0',
            categoriaActiva === cat.id
              ? 'bg-eden-600 text-white shadow-md shadow-eden-600/20'
              : 'bg-white dark:bg-slate-900 text-slate-600 dark:text-slate-300 hover:bg-slate-100 dark:hover:bg-slate-800 border border-slate-200 dark:border-slate-800'
          ]"
        >
          {{ cat.nombre }}
        </button>
      </div>
    </div>

    <!-- Contenido de Platillos -->
    <main class="max-w-5xl mx-auto px-4 py-6 space-y-8">
      <!-- Banner Especial Menú del Día de Hoy para Clientes -->
      <div 
        v-if="menuStore.menuDelDia?.activo && !busqueda"
        class="bg-gradient-to-r from-amber-500/10 via-eden-500/10 to-emerald-500/10 dark:from-amber-950/40 dark:via-eden-950/40 dark:to-emerald-950/40 rounded-3xl border border-amber-300 dark:border-amber-700/60 p-6 shadow-sm space-y-4"
      >
        <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-3">
          <div class="flex items-center gap-3">
            <div class="w-12 h-12 rounded-2xl bg-amber-500 text-white flex items-center justify-center text-2xl shadow-sm shrink-0">
              🍱
            </div>
            <div>
              <div class="flex items-center gap-2 flex-wrap">
                <h3 class="text-lg font-black text-slate-800 dark:text-slate-100">
                  Menú del Día
                </h3>
                <span class="text-3xs font-black uppercase px-2.5 py-0.5 rounded-full bg-emerald-600 text-white shadow-2xs">
                  {{ menuStore.menuDelDia.hora_inicio }} - {{ menuStore.menuDelDia.hora_fin }}
                </span>
              </div>
              <p class="text-xs text-slate-500 dark:text-slate-400 mt-0.5">
                Menú completo tradicional: Entrada, Plato Fuerte, Bebida del día y Postre
              </p>
            </div>
          </div>
        </div>

        <!-- Tarjetas de cada comida corrida -->
        <div v-if="menuStore.menuDelDia.comidas_corridas?.length" class="grid grid-cols-1 md:grid-cols-2 gap-3.5 pt-1">
          <div 
            v-for="(cc, i) in menuStore.menuDelDia.comidas_corridas" 
            :key="cc.id || i"
            class="p-4 bg-white/90 dark:bg-slate-900/90 rounded-2xl border border-slate-200/80 dark:border-slate-800/80 shadow-2xs space-y-2 flex flex-col justify-between transition-all"
            :class="cc.activo === false ? 'opacity-65 grayscale-[25%] border-rose-200 dark:border-rose-900/50 bg-rose-50/10' : ''"
          >
            <div>
              <div class="flex justify-between items-start gap-2 pb-2 border-b border-slate-100 dark:border-slate-800">
                <div class="flex items-center gap-2 flex-wrap">
                  <h4 class="font-black text-sm text-slate-800 dark:text-slate-100">
                    🍱 {{ cc.nombre || `Comida Corrida #${i + 1}` }}
                  </h4>
                  <span 
                    v-if="cc.activo === false"
                    class="text-3xs font-black uppercase px-2 py-0.5 rounded-full bg-rose-600 text-white"
                  >
                    Agotada hoy
                  </span>
                </div>
                <span class="text-base font-black text-eden-600 dark:text-eden-400 font-mono shrink-0">
                  ${{ Number(cc.precio || menuStore.menuDelDia.precio || 95).toFixed(2) }}
                </span>
              </div>

              <div class="flex items-start gap-3 mt-2.5">
                <!-- Foto si existe -->
                <div 
                  v-if="cc.imagen_url" 
                  class="w-20 h-20 rounded-xl overflow-hidden bg-slate-100 dark:bg-slate-800 border border-slate-200 dark:border-slate-700 shrink-0 shadow-2xs"
                >
                  <img 
                    :src="menuStore.obtenerUrlImagen(cc.imagen_url)" 
                    :alt="cc.nombre" 
                    class="w-full h-full object-cover" 
                    @error="$event.target.style.display = 'none'"
                  />
                </div>

                <div class="text-xs text-slate-600 dark:text-slate-300 space-y-1.5 flex-1 min-w-0">
                  <div class="flex items-start gap-1">
                    <span class="font-bold text-amber-700 dark:text-amber-400 shrink-0">🥣 Entrada:</span>
                    <span>{{ cc.entradas?.join(', ') || 'N/A' }}</span>
                  </div>
                  <div class="flex items-start gap-1">
                    <span class="font-bold text-amber-700 dark:text-amber-400 shrink-0">🍖 Plato Fuerte:</span>
                    <span>{{ cc.platos_fuertes?.join(', ') || 'N/A' }}</span>
                  </div>
                  <div class="flex items-start gap-1">
                    <span class="font-bold text-amber-700 dark:text-amber-400 shrink-0">🥤 Bebida:</span>
                    <span>{{ cc.bebidas?.join(', ') || 'N/A' }}</span>
                  </div>
                  <div v-if="cc.postres?.length" class="flex items-start gap-1">
                    <span class="font-bold text-amber-700 dark:text-amber-400 shrink-0">🍮 Postre:</span>
                    <span>{{ cc.postres.join(', ') }}</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Spinner de Carga -->
      <div v-if="menuStore.cargando" class="text-center py-20 text-slate-400">
        <div class="inline-block animate-spin rounded-full h-8 w-8 border-4 border-slate-200 dark:border-slate-800 border-t-eden-600 mb-2"></div>
        <p class="text-sm">Preparando la carta digital...</p>
      </div>

      <!-- Si no hay resultados de búsqueda -->
      <div v-else-if="platillosFiltrados.length === 0" class="text-center py-16 text-slate-400">
        <span class="text-4xl block mb-2">🍽️</span>
        <h4 class="font-bold text-slate-700 dark:text-slate-300">No encontramos platillos</h4>
        <p class="text-xs text-slate-400 mt-1">Intenta con otro término de búsqueda o selecciona otra categoría.</p>
      </div>

      <!-- Agrupación por Categoría -->
      <div 
        v-else 
        v-for="grupo in categoriasConProductos" 
        :key="grupo.id"
        class="space-y-4"
      >
        <div class="border-b border-slate-200 dark:border-slate-800 pb-2 flex justify-between items-end">
          <div>
            <h3 class="text-xl font-black text-slate-900 dark:text-slate-100 tracking-tight">{{ grupo.nombre }}</h3>
            <p v-if="grupo.descripcion" class="text-xs text-slate-500 dark:text-slate-400 mt-0.5">{{ grupo.descripcion }}</p>
          </div>
          <span class="text-xs font-bold text-slate-400">{{ grupo.productos.length }} opciones</span>
        </div>

        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
          <div
            v-for="prod in grupo.productos"
            :key="prod.id"
            class="bg-white dark:bg-slate-900 rounded-3xl p-5 border border-slate-200 dark:border-slate-800 shadow-sm hover:shadow-md transition-all flex flex-col justify-between space-y-3 group"
          >
            <div>
              <!-- Imagen del Platillo si existe -->
              <div 
                v-if="prod.imagen_url" 
                class="h-44 w-full rounded-2xl overflow-hidden bg-slate-100 dark:bg-slate-800 border border-slate-100 dark:border-slate-800 mb-3"
              >
                <img 
                  :src="menuStore.obtenerUrlImagen(prod.imagen_url)" 
                  :alt="prod.nombre" 
                  class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300" 
                  @error="$event.target.style.display = 'none'"
                />
              </div>

              <div class="flex justify-between items-start gap-2">
                <h4 class="font-extrabold text-base text-slate-900 dark:text-slate-100 group-hover:text-eden-600 dark:group-hover:text-eden-400 transition-colors">
                  {{ prod.nombre }}
                </h4>
                <span class="text-xs font-bold px-2 py-0.5 rounded-full bg-eden-50 dark:bg-eden-950/40 text-eden-700 dark:text-eden-300 shrink-0 border border-eden-200/60 dark:border-eden-800/40">
                  Tradicional
                </span>
              </div>
              <p class="text-xs text-slate-500 dark:text-slate-400 mt-1.5 leading-relaxed">
                {{ prod.descripcion || 'Elaborado artesanalmente con la receta de la casa.' }}
              </p>
            </div>

            <div class="flex justify-between items-center pt-2 border-t border-slate-100 dark:border-slate-800/80">
              <span class="text-xl font-black text-slate-900 dark:text-slate-100">
                ${{ Number(prod.precio).toFixed(2) }} <span class="text-xs font-normal text-slate-400">MXN</span>
              </span>
              <span class="text-2xs text-slate-400 flex items-center gap-1 font-medium">
                <span>☕</span> Hecho al momento
              </span>
            </div>
          </div>
        </div>
      </div>
    </main>

    <!-- Footer Información Restaurante -->
    <footer class="bg-white dark:bg-slate-900 border-t border-slate-200 dark:border-slate-800 mt-12 py-10 transition-colors">
      <div class="max-w-4xl mx-auto px-4 text-center space-y-6">
        <!-- Logo e Identidad del Negocio -->
        <div class="flex flex-col items-center justify-center space-y-2">
          <div class="w-14 h-14 rounded-full p-1 bg-white dark:bg-slate-800 border-2 border-slate-200 dark:border-slate-700 shadow-sm ring-2 ring-eden-500/20 flex items-center justify-center overflow-hidden">
            <img 
              :src="configStore.logoUrl || '/logo.png'" 
              :alt="configStore.nombreRestaurante" 
              class="w-full h-full object-contain rounded-full" 
            />
          </div>
          <div>
            <h3 class="font-black text-slate-800 dark:text-slate-100 text-base sm:text-lg tracking-tight">
              {{ configStore.nombreRestaurante }}
            </h3>
            <p v-if="configStore.slogan" class="text-xs text-eden-600 dark:text-eden-400 font-bold">
              {{ configStore.slogan }}
            </p>
          </div>
        </div>

        <!-- Tarjetas de Información: Horario, Ubicación y Contacto -->
        <div class="grid grid-cols-1 sm:grid-cols-3 gap-3 max-w-2xl mx-auto text-xs">
          <!-- Horario de Atención -->
          <div class="p-3.5 rounded-2xl bg-slate-50 dark:bg-slate-800/60 border border-slate-200/80 dark:border-slate-700/60 space-y-1">
            <span class="text-base block">🕒</span>
            <span class="font-bold text-slate-700 dark:text-slate-200 block text-3xs uppercase tracking-wider">Horario de Servicio</span>
            <p class="text-slate-600 dark:text-slate-400 text-2xs leading-tight">
              {{ configStore.diasServicio }}<br />
              <strong class="text-slate-800 dark:text-slate-100">{{ configStore.horarioApertura }} - {{ configStore.horarioCierre }}</strong>
            </p>
          </div>

          <!-- Ubicación / Dirección -->
          <div class="p-3.5 rounded-2xl bg-slate-50 dark:bg-slate-800/60 border border-slate-200/80 dark:border-slate-700/60 space-y-1">
            <span class="text-base block">📍</span>
            <span class="font-bold text-slate-700 dark:text-slate-200 block text-3xs uppercase tracking-wider">Ubicación</span>
            <p class="text-slate-600 dark:text-slate-400 text-2xs leading-tight">
              {{ configStore.direccion || 'Consulte dirección en sucursal' }}
            </p>
          </div>

          <!-- Contacto / Teléfono -->
          <div class="p-3.5 rounded-2xl bg-slate-50 dark:bg-slate-800/60 border border-slate-200/80 dark:border-slate-700/60 space-y-1">
            <span class="text-base block">📞</span>
            <span class="font-bold text-slate-700 dark:text-slate-200 block text-3xs uppercase tracking-wider">Contacto</span>
            <p class="text-slate-600 dark:text-slate-400 text-2xs leading-tight">
              {{ configStore.telefono ? `Tel: ${configStore.telefono}` : 'Atención al comensal' }}
            </p>
          </div>
        </div>

        <!-- Leyenda de Impuestos y Precios -->
        <div class="max-w-md mx-auto pt-2 border-t border-slate-100 dark:border-slate-800/80">
          <p class="text-2xs sm:text-xs text-slate-500 dark:text-slate-400 leading-relaxed whitespace-pre-line">
            {{ configStore.notaPieCarta || 'Precios incluyen IVA. Para dudas sobre ingredientes o alérgenos, consulta a tu mesero.' }}
          </p>
        </div>

        <!-- Copyright / Cierre -->
        <p class="text-3xs text-slate-400 dark:text-slate-500">
          © {{ new Date().getFullYear() }} {{ configStore.nombreRestaurante }}. Sistema de Punto de Venta & Menú Digital.
        </p>
      </div>
    </footer>

    <!-- Modal de Código QR para Imprimir o Compartir -->
    <div v-if="modalQR" class="fixed inset-0 bg-slate-900/60 backdrop-blur-sm flex items-center justify-center p-4 z-50">
      <div class="bg-white dark:bg-slate-900 rounded-3xl p-6 sm:p-7 max-w-sm w-full shadow-2xl border border-slate-200 dark:border-slate-800 text-center space-y-4">
        <div class="flex justify-between items-center">
          <h3 class="text-base font-black text-slate-800 dark:text-slate-100">Código QR del Menú</h3>
          <button @click="modalQR = false" class="text-slate-400 hover:text-slate-700 text-sm font-bold">✕</button>
        </div>

        <p class="text-xs text-slate-500 dark:text-slate-400">
          Tus clientes pueden escanear este código con su teléfono celular para ver la carta digital en su mesa.
        </p>

        <!-- Código QR Dinámico -->
        <div class="p-4 bg-white rounded-2xl border-2 border-slate-200 inline-block shadow-inner">
          <img 
            :src="qrUrl" 
            alt="Código QR de la Carta" 
            class="w-48 h-48 mx-auto object-contain"
          />
        </div>

        <div class="text-2xs font-mono text-slate-400 break-all bg-slate-50 dark:bg-slate-800 p-2 rounded-xl">
          {{ urlCartaActual }}
        </div>

        <button 
          @click="imprimirQR"
          class="w-full py-2.5 bg-eden-600 hover:bg-eden-700 text-white rounded-xl text-xs font-bold transition shadow-sm"
        >
          🖨️ Imprimir QR para Mesas
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useMenuStore } from '../stores/menu'
import { useThemeStore } from '../stores/theme'
import { useConfiguracionStore } from '../stores/configuracion'

const menuStore = useMenuStore()
const themeStore = useThemeStore()
const configStore = useConfiguracionStore()

const categoriaActiva = ref(null)
const busqueda = ref('')
const modalQR = ref(false)

onMounted(async () => {
  await Promise.all([
    menuStore.cargarCatalogo(),
    configStore.cargarConfiguracion()
  ])
})

const urlCartaActual = computed(() => {
  if (typeof window !== 'undefined') {
    return `${window.location.origin}/carta`
  }
  return 'http://localhost:5173/carta'
})

const qrUrl = computed(() => {
  return `https://api.qrserver.com/v1/create-qr-code/?size=250x250&data=${encodeURIComponent(urlCartaActual.value)}&margin=10`
})

const platillosFiltrados = computed(() => {
  let lista = menuStore.productos.filter(p => p.disponible)

  if (categoriaActiva.value) {
    lista = lista.filter(p => p.categoria_id === categoriaActiva.value)
  }

  if (busqueda.value.trim()) {
    const q = busqueda.value.toLowerCase().trim()
    lista = lista.filter(p => 
      p.nombre.toLowerCase().includes(q) || 
      (p.descripcion && p.descripcion.toLowerCase().includes(q))
    )
  }

  return lista
})

const categoriasConProductos = computed(() => {
  const grupos = []
  const cats = categoriaActiva.value 
    ? menuStore.categorias.filter(c => c.id === categoriaActiva.value)
    : menuStore.categorias

  for (const cat of cats) {
    const prods = platillosFiltrados.value.filter(p => p.categoria_id === cat.id)
    if (prods.length > 0) {
      grupos.push({
        id: cat.id,
        nombre: cat.nombre,
        descripcion: cat.descripcion,
        productos: prods
      })
    }
  }
  return grupos
})

const alternarTema = () => {
  const nuevo = themeStore.tema === 'oscuro' ? 'claro' : 'oscuro'
  themeStore.establecerTema(nuevo)
}

const imprimirQR = () => {
  window.print()
}
</script>

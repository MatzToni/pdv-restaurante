<template>
  <div class="min-h-screen bg-slate-50 dark:bg-slate-950 text-slate-800 dark:text-slate-100 transition-colors">
    <!-- Navbar Exclusiva para Clientes -->
    <header class="bg-white/90 dark:bg-slate-900/90 backdrop-blur-md sticky top-0 z-40 border-b border-slate-200/80 dark:border-slate-800/80">
      <div class="max-w-5xl mx-auto px-4 h-16 flex items-center justify-between">
        <!-- Logo y Nombre -->
        <div class="flex items-center gap-3">
          <img 
            src="/logo.png" 
            alt="Edén Café Logo" 
            class="w-10 h-10 object-contain rounded-full shadow-sm"
          />
          <div>
            <h1 class="font-black text-slate-800 dark:text-slate-100 text-base leading-tight tracking-tight">Edén Café</h1>
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

          <!-- Enlace Acceso Personal -->
          <router-link
            to="/login"
            class="hidden sm:inline-flex px-3 py-1.5 bg-eden-600 hover:bg-eden-700 text-white rounded-xl text-xs font-bold transition shadow-sm"
          >
            Acceso Personal
          </router-link>
        </div>
      </div>
    </header>

    <!-- Hero / Bienvenida -->
    <section class="max-w-5xl mx-auto px-4 pt-8 pb-4 text-center space-y-2">
      <span class="inline-block px-3 py-1 rounded-full bg-eden-100 dark:bg-eden-950/60 text-eden-800 dark:text-eden-300 text-2xs font-black uppercase tracking-widest border border-eden-200 dark:border-eden-800/40">
        Comida Tradicional y Café de Especialidad
      </span>
      <h2 class="text-3xl sm:text-4xl font-black text-slate-900 dark:text-slate-100 tracking-tight">
        Nuestra Carta
      </h2>
      <p class="text-xs sm:text-sm text-slate-500 dark:text-slate-400 max-w-md mx-auto">
        Platillos preparados al momento con ingredientes frescos, recetas mexicanas tradicionales y café tostado artesanal.
      </p>

      <!-- Barra de Búsqueda Interactiva -->
      <div class="max-w-md mx-auto pt-4">
        <div class="relative">
          <span class="absolute inset-y-0 left-0 pl-3.5 flex items-center pointer-events-none text-slate-400">
            🔍
          </span>
          <input 
            v-model="busqueda"
            type="text"
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
    <footer class="bg-white dark:bg-slate-900 border-t border-slate-200 dark:border-slate-800 mt-12 py-8 transition-colors">
      <div class="max-w-5xl mx-auto px-4 text-center space-y-4">
        <div class="flex justify-center items-center gap-2">
          <img src="/logo.png" alt="Edén Café" class="w-8 h-8 rounded-full" />
          <span class="font-black text-slate-800 dark:text-slate-100 text-sm">Edén Café</span>
        </div>
        <p class="text-xs text-slate-500 dark:text-slate-400 max-w-sm mx-auto leading-relaxed">
          Horario de Servicio: Lunes a Domingo de 8:00 AM a 10:00 PM.<br />
          Precios incluyen IVA. Para dudas sobre ingredientes o alérgenos, consulta a tu mesero.
        </p>
        <div class="pt-2">
          <router-link to="/login" class="text-xs text-eden-600 dark:text-eden-400 font-bold hover:underline">
            Acceso exclusivo para el personal del restaurante →
          </router-link>
        </div>
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

const menuStore = useMenuStore()
const themeStore = useThemeStore()

const categoriaActiva = ref(null)
const busqueda = ref('')
const modalQR = ref(false)

onMounted(() => {
  menuStore.cargarCatalogo()
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

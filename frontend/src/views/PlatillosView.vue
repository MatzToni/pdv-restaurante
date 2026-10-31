<template>
  <div class="space-y-6">
    <!-- Header -->
    <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 bg-white dark:bg-slate-900 p-6 rounded-2xl border border-slate-200 dark:border-slate-800 shadow-sm transition-colors">
      <div>
        <h1 class="text-2xl font-black text-slate-800 dark:text-slate-100 tracking-tight">Catálogo de Platillos y Menú</h1>
        <p class="text-slate-500 dark:text-slate-400 text-sm">Alta de platillos, bebidas, productos, servicios y categorías (géneros)</p>
      </div>

      <div class="flex flex-wrap items-center gap-2">
        <button 
          @click="abrirModalCategoria"
          class="px-3.5 py-2 bg-slate-100 dark:bg-slate-800 hover:bg-slate-200 dark:hover:bg-slate-700 text-slate-700 dark:text-slate-200 rounded-xl text-xs font-bold transition active:scale-95 flex items-center gap-1.5 border border-slate-200 dark:border-slate-700"
        >
          <span>🏷️</span> Géneros / Categorías ({{ menuStore.categorias.length }})
        </button>

        <button 
          @click="abrirModalNuevoProducto"
          class="px-4 py-2 bg-eden-600 hover:bg-eden-700 text-white rounded-xl text-xs font-bold shadow-sm transition active:scale-95 flex items-center gap-1.5"
        >
          <span>+</span> Dar de Alta Platillo o Servicio
        </button>
      </div>
    </div>

    <!-- Barra de Búsqueda y Filtros de Categoría / Tipo -->
    <div class="bg-white dark:bg-slate-900 p-4 rounded-2xl border border-slate-200 dark:border-slate-800 shadow-sm space-y-3 transition-colors">
      <div class="flex flex-col sm:flex-row gap-3">
        <!-- Buscador -->
        <div class="flex-1 relative">
          <input 
            v-model="busqueda"
            type="text"
            placeholder="Buscar por nombre o ingrediente..."
            class="w-full pl-9 pr-4 py-2 bg-slate-50 dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded-xl text-xs text-slate-800 dark:text-slate-100 font-semibold focus:outline-none focus:border-eden-600"
          />
          <span class="absolute left-3 top-2.5 text-xs text-slate-400">🔍</span>
        </div>

        <!-- Filtro por Tipo de Ítem -->
        <select 
          v-model="filtroTipoItem"
          class="px-3 py-2 bg-slate-50 dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded-xl text-xs text-slate-700 dark:text-slate-200 font-bold focus:outline-none focus:border-eden-600"
        >
          <option value="">Todos los Tipos</option>
          <option value="platillo">🍽️ Platillos (Cocina)</option>
          <option value="bebida">☕ Bebidas (Barra)</option>
          <option value="producto">📦 Productos Empaquetados</option>
          <option value="servicio">🛎️ Servicios</option>
        </select>
      </div>

      <!-- Selector horizontal de Categorías (Géneros) -->
      <div class="flex gap-1.5 overflow-x-auto no-scrollbar pt-1">
        <button
          @click="categoriaFiltro = null"
          :class="[
            'px-3.5 py-1.5 rounded-xl text-2xs font-extrabold transition-all shrink-0',
            categoriaFiltro === null 
              ? 'bg-slate-900 dark:bg-white text-white dark:text-slate-900 shadow-sm' 
              : 'bg-slate-100 dark:bg-slate-800 text-slate-600 dark:text-slate-400 hover:bg-slate-200'
          ]"
        >
          Todos ({{ menuStore.productos.length }})
        </button>
        <button
          v-for="cat in menuStore.categorias"
          :key="cat.id"
          @click="categoriaFiltro = cat.id"
          :class="[
            'px-3.5 py-1.5 rounded-xl text-2xs font-extrabold transition-all shrink-0',
            categoriaFiltro === cat.id 
              ? 'bg-eden-600 text-white shadow-sm' 
              : 'bg-slate-100 dark:bg-slate-800 text-slate-600 dark:text-slate-400 hover:bg-slate-200'
          ]"
        >
          {{ cat.nombre }}
        </button>
      </div>
    </div>

    <!-- Grid de Platillos y Servicios -->
    <div v-if="productosFiltrados.length === 0" class="text-center py-16 bg-white dark:bg-slate-900 rounded-3xl border border-slate-200 dark:border-slate-800 text-slate-400">
      <span class="text-4xl block mb-2">🍽️</span>
      <h3 class="text-base font-bold text-slate-700 dark:text-slate-300">No se encontraron productos</h3>
      <p class="text-xs text-slate-400 mt-1">Intenta con otro término de búsqueda o agrega un nuevo platillo al menú</p>
    </div>

    <div v-else class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
      <div 
        v-for="item in productosFiltrados" 
        :key="item.id"
        class="bg-white dark:bg-slate-900 rounded-2xl border border-slate-200 dark:border-slate-800 p-4 shadow-sm flex flex-col justify-between hover:border-eden-500 transition-all space-y-3"
      >
        <div>
          <!-- Cabecera de la tarjeta con Género y Tipo -->
          <div class="flex justify-between items-start gap-1">
            <span class="text-3xs font-extrabold px-2 py-0.5 rounded-md bg-eden-50 dark:bg-eden-950/60 text-eden-800 dark:text-eden-300 border border-eden-200 dark:border-eden-800/40 truncate">
              {{ item.categoria_nombre || 'General' }}
            </span>
            <span class="text-3xs font-bold px-1.5 py-0.5 rounded uppercase" :class="badgeTipoItem(item.tipo_item)">
              {{ iconoTipoItem(item.tipo_item) }} {{ item.tipo_item || 'platillo' }}
            </span>
          </div>

          <!-- Nombre y Descripción -->
          <h3 class="font-black text-slate-800 dark:text-slate-100 text-sm mt-2 leading-snug">
            {{ item.nombre }}
          </h3>
          <p class="text-xs text-slate-400 dark:text-slate-500 mt-1 line-clamp-2 leading-relaxed">
            {{ item.descripcion || 'Sin descripción adicional' }}
          </p>
        </div>

        <div class="space-y-2 pt-2 border-t border-slate-100 dark:border-slate-800">
          <div class="flex justify-between items-center">
            <span class="text-lg font-black text-eden-600 dark:text-eden-400 font-mono">
              ${{ Number(item.precio).toFixed(2) }}
            </span>
            <span 
              :class="[
                'text-3xs font-extrabold px-2 py-0.5 rounded-full',
                item.disponible ? 'bg-emerald-100 text-emerald-800 dark:bg-emerald-950/60 dark:text-emerald-300' : 'bg-rose-100 text-rose-800 dark:bg-rose-950/60 dark:text-rose-300'
              ]"
            >
              {{ item.disponible ? 'Disponible' : 'Agotado' }}
            </span>
          </div>

          <!-- Botones de Acción -->
          <div class="flex items-center gap-1.5 pt-1">
            <button 
              @click="alternarDisponibilidad(item)"
              :class="[
                'flex-1 py-1 text-2xs font-bold rounded-lg border transition',
                item.disponible 
                  ? 'border-slate-200 dark:border-slate-700 hover:bg-slate-100 text-slate-700 dark:text-slate-300' 
                  : 'border-emerald-300 bg-emerald-50 text-emerald-700 hover:bg-emerald-100'
              ]"
            >
              {{ item.disponible ? 'Pausar' : 'Activar' }}
            </button>
            <button 
              @click="abrirModalEditar(item)"
              class="px-2.5 py-1 text-2xs font-bold bg-slate-100 dark:bg-slate-800 hover:bg-slate-200 text-slate-700 dark:text-slate-200 rounded-lg transition"
            >
              ✏️ Editar
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- MODAL ALTA / EDICIÓN DE PLATILLO O SERVICIO -->
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
                step="0.50"
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
                <span>¿Enviar orden a pantalla Cocina/KDS?</span>
              </label>
            </div>
          </div>

          <!-- Descripción -->
          <div>
            <label class="text-xs font-bold text-slate-700 dark:text-slate-300">Descripción / Ingredientes para la carta del cliente:</label>
            <textarea 
              v-model="formProducto.descripcion"
              rows="2.5"
              placeholder="Ej. Exquisito café espresso con chocolate amargo, leche vaporizada y canela..."
              class="w-full mt-1 p-2.5 text-xs font-semibold bg-white dark:bg-slate-800 border border-slate-300 dark:border-slate-700 rounded-xl text-slate-800 dark:text-slate-100 focus:outline-none focus:border-eden-600 resize-none"
            ></textarea>
          </div>

          <!-- Disponibilidad -->
          <label class="flex items-center gap-2 p-2.5 rounded-xl bg-slate-50 dark:bg-slate-800 border border-slate-200 dark:border-slate-700 cursor-pointer">
            <input 
              v-model="formProducto.disponible"
              type="checkbox"
              class="rounded text-emerald-600 focus:ring-emerald-500 w-4 h-4"
            />
            <span class="text-xs font-bold text-slate-700 dark:text-slate-300">
              Disponible para venta en comandero y carta pública
            </span>
          </label>
        </div>

        <div class="pt-3 border-t border-slate-100 dark:border-slate-800 flex justify-end gap-2">
          <button 
            @click="modalProducto = false"
            class="px-4 py-2 text-xs font-bold text-slate-600 dark:text-slate-300 hover:bg-slate-100 rounded-xl"
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

    <!-- MODAL GESTIÓN DE CATEGORÍAS (GÉNEROS) -->
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
              placeholder="Ej. Bebidas Frías, Coctelería..."
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
              class="text-xs text-rose-500 hover:bg-rose-100 dark:hover:bg-rose-950/60 p-1 rounded-lg transition"
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

const busqueda = ref('')
const categoriaFiltro = ref(null)
const filtroTipoItem = ref('')

const modalProducto = ref(false)
const editandoId = ref(null)
const guardando = ref(false)

const formProducto = ref({
  nombre: '',
  categoria_id: null,
  tipo_item: 'platillo',
  precio: 0,
  descripcion: '',
  requiere_cocina: true,
  disponible: true
})

// Modal Categorías
const modalCategorias = ref(false)
const nuevaCatNombre = ref('')

onMounted(async () => {
  await menuStore.cargarCatalogo(true)
  if (menuStore.categorias.length > 0 && !formProducto.value.categoria_id) {
    formProducto.value.categoria_id = menuStore.categorias[0].id
  }
})

const productosFiltrados = computed(() => {
  return menuStore.productos.filter(p => {
    const matchCat = categoriaFiltro.value ? p.categoria_id === categoriaFiltro.value : true
    const matchTipo = filtroTipoItem.value ? p.tipo_item === filtroTipoItem.value : true
    const matchBusq = busqueda.value 
      ? p.nombre.toLowerCase().includes(busqueda.value.toLowerCase()) || (p.descripcion && p.descripcion.toLowerCase().includes(busqueda.value.toLowerCase()))
      : true
    return matchCat && matchTipo && matchBusq
  })
})

const abrirModalNuevoProducto = () => {
  editandoId.value = null
  formProducto.value = {
    nombre: '',
    categoria_id: menuStore.categorias[0]?.id || 1,
    tipo_item: 'platillo',
    precio: 0,
    descripcion: '',
    requiere_cocina: true,
    disponible: true
  }
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
    requiere_cocina: item.requiere_cocina ?? true,
    disponible: item.disponible ?? true
  }
  modalProducto.value = true
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
    default: return '🍽️'
  }
}
</script>

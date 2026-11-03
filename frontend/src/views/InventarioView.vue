<template>
  <div class="space-y-6">
    <!-- Header -->
    <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 bg-white dark:bg-slate-900 p-6 rounded-2xl shadow-sm border border-slate-200 dark:border-slate-800 transition-colors">
      <div>
        <h1 class="text-2xl font-black text-slate-800 dark:text-slate-100 tracking-tight">Control de Inventario y Almacén</h1>
        <p class="text-slate-500 dark:text-slate-400 text-sm">Materia prima, desechables, vajilla y suministros de limpieza</p>
      </div>

      <div class="flex flex-wrap items-center gap-2">
        <button 
          @click="modalMovimiento = true"
          class="px-3.5 py-2 bg-slate-900 dark:bg-slate-800 hover:bg-slate-800 dark:hover:bg-slate-700 text-white rounded-xl text-xs font-bold shadow-sm transition active:scale-95 flex items-center gap-1.5 border border-transparent dark:border-slate-700"
        >
          <span>📦</span> Movimiento (Entrada/Merma)
        </button>
        <button 
          @click="modalNuevoArticulo = true"
          class="px-3.5 py-2 bg-eden-600 hover:bg-eden-700 text-white rounded-xl text-xs font-bold shadow-sm transition active:scale-95 flex items-center gap-1.5"
        >
          <span>+</span> Registrar Artículo
        </button>
      </div>
    </div>

    <!-- Pestañas de Clasificación de Inventario -->
    <div class="flex gap-2 overflow-x-auto no-scrollbar pb-1">
      <button
        v-for="tab in tabs"
        :key="tab.id"
        @click="cambiarTab(tab.id)"
        :class="[
          'px-4 py-2 rounded-xl text-xs font-bold transition-all shrink-0 flex items-center gap-1.5',
          inventarioStore.tipoActivo === tab.id
            ? 'bg-eden-600 text-white shadow-sm'
            : 'bg-white dark:bg-slate-900 text-slate-600 dark:text-slate-300 hover:bg-slate-100 dark:hover:bg-slate-800 border border-slate-200 dark:border-slate-800'
        ]"
      >
        <span>{{ tab.icono }}</span>
        <span>{{ tab.nombre }}</span>
      </button>
    </div>

    <!-- Tabla de Artículos -->
    <div class="bg-white dark:bg-slate-900 rounded-2xl border border-slate-200 dark:border-slate-800 shadow-sm overflow-hidden transition-colors">
      <div class="overflow-x-auto">
        <table class="w-full text-left text-sm">
          <thead class="bg-slate-50 dark:bg-slate-800/60 text-slate-500 dark:text-slate-400 uppercase text-2xs font-extrabold tracking-wider border-b border-slate-200 dark:border-slate-800">
            <tr>
              <th class="p-4">Artículo</th>
              <th class="p-4">Clasificación</th>
              <th class="p-4">Stock Actual</th>
              <th class="p-4">Stock Mínimo</th>
              <th class="p-4">Costo Unitario</th>
              <th class="p-4">Estado</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-slate-100 dark:divide-slate-800/80 text-slate-700 dark:text-slate-200 font-medium">
            <tr v-if="inventarioStore.cargando">
              <td colspan="6" class="p-8 text-center text-slate-400">Cargando inventario...</td>
            </tr>
            <tr v-else-if="inventarioStore.articulosFiltrados.length === 0">
              <td colspan="6" class="p-8 text-center text-slate-400">No hay artículos en esta categoría.</td>
            </tr>
            <tr 
              v-for="art in inventarioStore.articulosFiltrados" 
              :key="art.id"
              class="hover:bg-slate-50/80 dark:hover:bg-slate-800/40 transition"
            >
              <td class="p-4 font-bold text-slate-800 dark:text-slate-100">
                {{ art.nombre }}
                <span v-if="art.codigo" class="block text-2xs font-normal text-slate-400">{{ art.codigo }}</span>
              </td>
              <td class="p-4">
                <span :class="[
                  'px-2.5 py-1 rounded-full text-2xs font-bold capitalize',
                  art.tipo === 'ingrediente' ? 'bg-amber-100 dark:bg-amber-950/60 text-amber-800 dark:text-amber-300' :
                  art.tipo === 'desechable' ? 'bg-sky-100 dark:bg-sky-950/60 text-sky-800 dark:text-sky-300' :
                  art.tipo === 'utensilio' ? 'bg-purple-100 dark:bg-purple-950/60 text-purple-800 dark:text-purple-300' :
                  'bg-emerald-100 dark:bg-emerald-950/60 text-emerald-800 dark:text-emerald-300'
                ]">
                  {{ art.tipo }}
                </span>
              </td>
              <td class="p-4 font-extrabold text-slate-900 dark:text-slate-100 text-base">
                {{ Number(art.stock_actual).toFixed(2) }} <span class="text-xs font-normal text-slate-500 dark:text-slate-400">{{ art.unidad_medida }}</span>
              </td>
              <td class="p-4 text-slate-500 dark:text-slate-400">
                {{ Number(art.stock_minimo).toFixed(2) }} {{ art.unidad_medida }}
              </td>
              <td class="p-4 font-semibold text-slate-700 dark:text-slate-300">
                ${{ Number(art.costo_unitario).toFixed(2) }}
              </td>
              <td class="p-4">
                <span 
                  v-if="Number(art.stock_actual) <= Number(art.stock_minimo)"
                  class="inline-flex items-center gap-1 text-2xs font-bold bg-rose-100 dark:bg-rose-950/60 text-rose-800 dark:text-rose-300 px-2 py-0.5 rounded-full"
                >
                  ⚠️ Reabastecer
                </span>
                <span 
                  v-else
                  class="inline-flex items-center gap-1 text-2xs font-bold bg-emerald-100 dark:bg-emerald-950/60 text-emerald-800 dark:text-emerald-300 px-2 py-0.5 rounded-full"
                >
                  ✓ Óptimo
                </span>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Modal Nuevo Artículo -->
    <div v-if="modalNuevoArticulo" class="fixed inset-0 bg-slate-900/60 backdrop-blur-sm flex items-center justify-center p-4 z-50">
      <div class="bg-white dark:bg-slate-900 rounded-3xl p-6 max-w-md w-full shadow-2xl border border-slate-200 dark:border-slate-800 space-y-4">
        <h3 class="text-lg font-black text-slate-800 dark:text-slate-100">Registrar en Inventario</h3>
        
        <div class="space-y-3">
          <div>
            <label class="text-xs font-bold text-slate-700 dark:text-slate-300">Nombre del Insumo / Artículo</label>
            <input 
              v-model="formArticulo.nombre" 
              type="text" 
              maxlength="100"
              placeholder="Ej. Pechuga de pollo, Vaso 12oz, Escoba, Plato" 
              class="w-full mt-1 p-2.5 text-xs font-semibold border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-800 text-slate-800 dark:text-slate-100 rounded-xl focus:outline-none focus:border-eden-600"
            />
          </div>

          <div class="grid grid-cols-2 gap-2">
            <div>
              <label class="text-xs font-bold text-slate-700 dark:text-slate-300">Tipo de Insumo</label>
              <select 
                v-model="formArticulo.tipo" 
                class="w-full mt-1 p-2.5 text-xs font-semibold border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-800 text-slate-800 dark:text-slate-100 rounded-xl focus:outline-none focus:border-eden-600"
              >
                <option value="ingrediente">Ingrediente (Recetas)</option>
                <option value="desechable">Desechable</option>
                <option value="utensilio">Utensilio / Vajilla</option>
                <option value="limpieza">Limpieza / Sanitizante</option>
              </select>
            </div>

            <div>
              <label class="text-xs font-bold text-slate-700 dark:text-slate-300">Unidad de Medida</label>
              <select 
                v-model="formArticulo.unidad_medida" 
                class="w-full mt-1 p-2.5 text-xs font-semibold border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-800 text-slate-800 dark:text-slate-100 rounded-xl focus:outline-none focus:border-eden-600"
              >
                <option value="kg">Kilogramos (kg)</option>
                <option value="g">Gramos (g)</option>
                <option value="lt">Litros (lt)</option>
                <option value="ml">Mililitros (ml)</option>
                <option value="pza">Piezas (pza)</option>
              </select>
            </div>
          </div>

          <div class="grid grid-cols-3 gap-2">
            <div>
              <label class="text-xs font-bold text-slate-700 dark:text-slate-300">Stock Inicial</label>
              <input 
                v-model.number="formArticulo.stock_actual" 
                type="number" 
                min="0"
                max="999999"
                step="0.01" 
                inputmode="decimal"
                class="w-full mt-1 p-2.5 text-xs font-semibold border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-800 text-slate-800 dark:text-slate-100 rounded-xl focus:outline-none focus:border-eden-600"
              />
            </div>
            <div>
              <label class="text-xs font-bold text-slate-700 dark:text-slate-300">Stock Mínimo</label>
              <input 
                v-model.number="formArticulo.stock_minimo" 
                type="number" 
                min="0"
                max="999999"
                step="0.01" 
                inputmode="decimal"
                class="w-full mt-1 p-2.5 text-xs font-semibold border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-800 text-slate-800 dark:text-slate-100 rounded-xl focus:outline-none focus:border-eden-600"
              />
            </div>
            <div>
              <label class="text-xs font-bold text-slate-700 dark:text-slate-300">Costo Unitario ($)</label>
              <input 
                v-model.number="formArticulo.costo_unitario" 
                type="number" 
                min="0"
                max="999999"
                step="0.50" 
                inputmode="decimal"
                class="w-full mt-1 p-2.5 text-xs font-semibold border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-800 text-slate-800 dark:text-slate-100 rounded-xl focus:outline-none focus:border-eden-600"
              />
            </div>
          </div>
        </div>

        <div class="flex gap-2 pt-2">
          <button 
            @click="modalNuevoArticulo = false" 
            class="flex-1 py-2.5 bg-slate-100 dark:bg-slate-800 hover:bg-slate-200 dark:hover:bg-slate-700 text-slate-700 dark:text-slate-300 rounded-xl font-bold text-xs transition"
          >
            Cancelar
          </button>
          <button 
            @click="guardarArticulo" 
            :disabled="!formArticulo.nombre"
            class="flex-1 py-2.5 bg-eden-600 hover:bg-eden-700 disabled:opacity-50 text-white rounded-xl font-bold text-xs transition shadow-sm"
          >
            Guardar Artículo
          </button>
        </div>
      </div>
    </div>

    <!-- Modal Registrar Movimiento (Entrada, Ajuste, Merma) -->
    <div v-if="modalMovimiento" class="fixed inset-0 bg-slate-900/60 backdrop-blur-sm flex items-center justify-center p-4 z-50">
      <div class="bg-white dark:bg-slate-900 rounded-3xl p-6 max-w-sm w-full shadow-2xl border border-slate-200 dark:border-slate-800 space-y-4">
        <h3 class="text-lg font-black text-slate-800 dark:text-slate-100">Registrar Movimiento de Almacén</h3>
        
        <div class="space-y-3">
          <div>
            <label class="text-xs font-bold text-slate-700 dark:text-slate-300">Artículo</label>
            <select 
              v-model.number="formMovimiento.articulo_id" 
              class="w-full mt-1 p-2.5 text-xs font-semibold border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-800 text-slate-800 dark:text-slate-100 rounded-xl focus:outline-none focus:border-eden-600"
            >
              <option v-for="art in inventarioStore.articulos" :key="art.id" :value="art.id">
                {{ art.nombre }} ({{ art.unidad_medida }})
              </option>
            </select>
          </div>

          <div>
            <label class="text-xs font-bold text-slate-700 dark:text-slate-300">Tipo de Movimiento</label>
            <select 
              v-model="formMovimiento.tipo" 
              class="w-full mt-1 p-2.5 text-xs font-semibold border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-800 text-slate-800 dark:text-slate-100 rounded-xl focus:outline-none focus:border-eden-600"
            >
              <option value="entrada">📥 Entrada / Compra</option>
              <option value="merma_desperdicio">🗑️ Merma / Desperdicio / Caducado</option>
              <option value="ajuste">⚙️ Ajuste de Inventario Físico</option>
            </select>
          </div>

          <div>
            <label class="text-xs font-bold text-slate-700 dark:text-slate-300">Cantidad</label>
            <input 
              v-model.number="formMovimiento.cantidad" 
              type="number" 
              min="0.01"
              max="999999"
              step="0.01" 
              inputmode="decimal"
              placeholder="0.00"
              class="w-full mt-1 p-2.5 text-xs font-semibold border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-800 text-slate-800 dark:text-slate-100 rounded-xl focus:outline-none focus:border-eden-600"
            />
          </div>

          <div>
            <label class="text-xs font-bold text-slate-700 dark:text-slate-300">Motivo / Proveedor</label>
            <input 
              v-model="formMovimiento.motivo" 
              type="text" 
              maxlength="150"
              placeholder="Ej. Factura #402, Merma por caducidad" 
              class="w-full mt-1 p-2.5 text-xs font-semibold border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-800 text-slate-800 dark:text-slate-100 rounded-xl focus:outline-none focus:border-eden-600"
            />
          </div>
        </div>

        <div class="flex gap-2 pt-2">
          <button 
            @click="modalMovimiento = false" 
            class="flex-1 py-2.5 bg-slate-100 dark:bg-slate-800 hover:bg-slate-200 dark:hover:bg-slate-700 text-slate-700 dark:text-slate-300 rounded-xl font-bold text-xs transition"
          >
            Cancelar
          </button>
          <button 
            @click="guardarMovimiento" 
            :disabled="!formMovimiento.articulo_id || !formMovimiento.cantidad"
            class="flex-1 py-2.5 bg-slate-900 dark:bg-slate-700 hover:bg-slate-800 dark:hover:bg-slate-600 disabled:opacity-50 text-white rounded-xl font-bold text-xs transition shadow-sm"
          >
            Registrar
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useInventarioStore } from '../stores/inventario'

const inventarioStore = useInventarioStore()

const tabs = [
  { id: 'todos', nombre: 'Todos los Artículos', icono: '📦' },
  { id: 'ingrediente', nombre: 'Ingredientes (Recetas)', icono: '🥑' },
  { id: 'desechable', nombre: 'Desechables', icono: '🥤' },
  { id: 'utensilio', nombre: 'Utensilios y Vajilla', icono: '🍽️' },
  { id: 'limpieza', nombre: 'Limpieza', icono: '🧹' },
]

const modalNuevoArticulo = ref(false)
const formArticulo = ref({
  nombre: '',
  tipo: 'ingrediente',
  unidad_medida: 'kg',
  stock_actual: 0,
  stock_minimo: 0,
  costo_unitario: 0
})

const modalMovimiento = ref(false)
const formMovimiento = ref({
  articulo_id: null,
  tipo: 'entrada',
  cantidad: 0,
  motivo: ''
})

onMounted(() => {
  inventarioStore.cargarArticulos()
})

const cambiarTab = (tipo) => {
  inventarioStore.tipoActivo = tipo
}

const guardarArticulo = async () => {
  try {
    await inventarioStore.registrarArticulo(formArticulo.value)
    modalNuevoArticulo.value = false
    formArticulo.value = { nombre: '', tipo: 'ingrediente', unidad_medida: 'kg', stock_actual: 0, stock_minimo: 0, costo_unitario: 0 }
    alert('Artículo registrado con éxito en el inventario.')
  } catch (err) {
    alert('Error al registrar el artículo.')
  }
}

const guardarMovimiento = async () => {
  try {
    await inventarioStore.registrarMovimiento(formMovimiento.value)
    modalMovimiento.value = false
    formMovimiento.value = { articulo_id: null, tipo: 'entrada', cantidad: 0, motivo: '' }
    alert('Movimiento de inventario aplicado.')
  } catch (err) {
    alert('Error al registrar movimiento.')
  }
}
</script>

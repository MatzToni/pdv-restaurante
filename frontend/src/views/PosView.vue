<template>
  <div class="h-[calc(100vh-5.5rem)] flex flex-col lg:flex-row gap-4">
    <!-- Menú y Selección de Platillos (Izquierda) -->
    <div class="flex-1 flex flex-col bg-white rounded-2xl border border-slate-200 overflow-hidden shadow-sm">
      <!-- Selector de Categorías -->
      <div class="p-3 border-b border-slate-100 flex gap-2 overflow-x-auto no-scrollbar bg-slate-50/50">
        <button
          @click="categoriaSeleccionada = null"
          :class="[
            'px-4 py-2 rounded-xl text-xs font-bold transition-all shrink-0',
            categoriaSeleccionada === null 
              ? 'bg-slate-900 text-white shadow-sm' 
              : 'bg-white text-slate-600 hover:bg-slate-200 border border-slate-200'
          ]"
        >
          Todos los Platillos
        </button>
        <button
          v-for="cat in menuStore.categorias"
          :key="cat.id"
          @click="categoriaSeleccionada = cat.id"
          :class="[
            'px-4 py-2 rounded-xl text-xs font-bold transition-all shrink-0',
            categoriaSeleccionada === cat.id 
              ? 'bg-eden-600 text-white shadow-sm' 
              : 'bg-white text-slate-600 hover:bg-slate-200 border border-slate-200'
          ]"
        >
          {{ cat.nombre }}
        </button>
      </div>

      <!-- Cuadrícula de Platillos Touch -->
      <div class="flex-1 p-4 overflow-y-auto">
        <div v-if="menuStore.cargando" class="text-center py-12 text-slate-400">
          <p class="text-sm">Cargando menú de Edén Café...</p>
        </div>

        <div v-else class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 gap-3">
          <button
            v-for="item in platillosFiltrados"
            :key="item.id"
            @click="agregarAlPedido(item)"
            class="flex flex-col justify-between p-3.5 bg-slate-50 hover:bg-eden-50/50 border border-slate-200 hover:border-eden-600 rounded-2xl text-left transition-all active:scale-95 group shadow-sm h-36"
          >
            <div>
              <div class="font-extrabold text-slate-800 text-sm group-hover:text-eden-700 leading-snug">{{ item.nombre }}</div>
              <div class="text-xs text-slate-400 mt-1 line-clamp-2 leading-relaxed">{{ item.descripcion }}</div>
            </div>
            <div class="mt-2 flex justify-between items-center w-full">
              <span class="font-black text-eden-600 text-base">
                ${{ Number(item.precio).toFixed(2) }}
              </span>
              <span class="text-xs font-bold bg-white px-2 py-0.5 rounded-lg border border-slate-200 group-hover:bg-eden-600 group-hover:text-white transition">
                + Agregar
              </span>
            </div>
          </button>
        </div>
      </div>
    </div>

    <!-- Comanda / Ticket Actual (Derecha) -->
    <div class="w-full lg:w-96 flex flex-col bg-white rounded-2xl border border-slate-200 overflow-hidden shadow-sm">
      <div class="p-4 border-b border-slate-100 flex justify-between items-center bg-slate-50">
        <div>
          <h2 class="font-extrabold text-slate-800 text-base">Comanda: {{ mesaNumero }}</h2>
          <span class="text-xs text-slate-500 font-medium">Mesero: {{ authStore.usuarioActual.nombre }}</span>
        </div>
        <button 
          v-if="itemsComanda.length > 0"
          @click="itemsComanda = []" 
          class="text-xs font-bold text-rose-500 hover:underline"
        >
          Limpiar
        </button>
      </div>

      <!-- Lista de Items en la Comanda -->
      <div class="flex-1 p-3 overflow-y-auto space-y-2.5">
        <div v-if="itemsComanda.length === 0" class="h-full flex flex-col items-center justify-center text-slate-400 text-sm">
          <span class="text-3xl mb-2">🍽️</span>
          <p class="font-bold">No hay platillos seleccionados</p>
          <span class="text-xs text-slate-400 mt-1 text-center">Toca los platillos de la izquierda para agregarlos a la orden</span>
        </div>

        <div 
          v-for="(item, index) in itemsComanda" 
          :key="index"
          class="p-2.5 rounded-xl bg-slate-50 border border-slate-200/80 space-y-1.5"
        >
          <div class="flex items-center justify-between">
            <div class="flex-1 min-w-0 pr-2">
              <h4 class="font-bold text-sm text-slate-800 truncate">{{ item.nombre }}</h4>
              <div class="text-xs text-slate-500 font-semibold">${{ Number(item.precio).toFixed(2) }} c/u</div>
            </div>
            <div class="flex items-center gap-1.5">
              <button @click="decrementar(index)" class="w-7 h-7 rounded-lg bg-white border border-slate-300 text-slate-700 flex items-center justify-center font-bold text-sm hover:bg-slate-100">-</button>
              <span class="font-black text-sm w-5 text-center">{{ item.cantidad }}</span>
              <button @click="incrementar(index)" class="w-7 h-7 rounded-lg bg-white border border-slate-300 text-slate-700 flex items-center justify-center font-bold text-sm hover:bg-slate-100">+</button>
              <span class="font-black text-sm text-slate-800 ml-2 w-16 text-right">${{ (item.precio * item.cantidad).toFixed(2) }}</span>
            </div>
          </div>

          <!-- Nota específica para cocina -->
          <input 
            v-model="item.notas"
            type="text"
            placeholder="Nota para cocina (ej. sin cebolla, salsa aparte)"
            class="w-full text-xs p-1.5 bg-white border border-slate-200 rounded-lg focus:outline-none focus:border-eden-600 text-slate-600"
          />
        </div>
      </div>

      <!-- Resumen y Envío a Cocina -->
      <div class="p-4 border-t border-slate-100 bg-slate-50 space-y-3">
        <!-- Notas generales de la mesa -->
        <input 
          v-model="notasGenerales"
          type="text"
          placeholder="Notas de la comanda general..."
          class="w-full text-xs p-2 bg-white border border-slate-200 rounded-xl focus:outline-none focus:border-eden-600"
        />

        <div class="flex justify-between items-center text-lg font-black text-slate-900 border-t border-slate-200 pt-2">
          <span>Total Estimado</span>
          <span class="text-eden-600">${{ total.toFixed(2) }}</span>
        </div>

        <button 
          @click="enviarComandaCocina"
          :disabled="itemsComanda.length === 0 || enviando"
          class="w-full py-3.5 bg-eden-600 hover:bg-eden-700 disabled:opacity-50 text-white rounded-xl font-bold text-sm shadow-md transition active:scale-95 flex items-center justify-center gap-2"
        >
          <span v-if="enviando">Enviando comanda...</span>
          <span v-else>👨‍🍳 Enviar Comanda a Cocina ({{ itemsComanda.reduce((acc, i) => acc + i.cantidad, 0) }} platillos)</span>
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useMenuStore } from '../stores/menu'
import { useOrdenesStore } from '../stores/ordenes'
import { useAuthStore } from '../stores/auth'

const route = useRoute()
const router = useRouter()
const menuStore = useMenuStore()
const ordenesStore = useOrdenesStore()
const authStore = useAuthStore()

const mesaId = computed(() => Number(route.query.mesaId) || 1)
const mesaNumero = computed(() => route.query.mesaNumero || 'Mesa 1')

const categoriaSeleccionada = ref(null)
const itemsComanda = ref([])
const notasGenerales = ref('')
const enviando = ref(false)

onMounted(() => {
  menuStore.cargarCatalogo()
})

const platillosFiltrados = computed(() => {
  if (!categoriaSeleccionada.value) return menuStore.productos
  return menuStore.productos.filter(p => p.categoria_id === categoriaSeleccionada.value)
})

const total = computed(() => {
  return itemsComanda.value.reduce((acc, item) => acc + (Number(item.precio) * item.cantidad), 0)
})

const agregarAlPedido = (producto) => {
  const existente = itemsComanda.value.find(i => i.id === producto.id)
  if (existente) {
    existente.cantidad++
  } else {
    itemsComanda.value.push({
      id: producto.id,
      nombre: producto.nombre,
      precio: Number(producto.precio),
      cantidad: 1,
      notas: ''
    })
  }
}

const incrementar = (idx) => { itemsComanda.value[idx].cantidad++ }
const decrementar = (idx) => {
  if (itemsComanda.value[idx].cantidad > 1) {
    itemsComanda.value[idx].cantidad--
  } else {
    itemsComanda.value.splice(idx, 1)
  }
}

const enviarComandaCocina = async () => {
  if (itemsComanda.value.length === 0) return
  enviando.value = true
  try {
    const ordenPayload = {
      mesa_id: mesaId.value,
      mesero_id: authStore.usuarioActual.id,
      notas: notasGenerales.value || null,
      items: itemsComanda.value.map(i => ({
        producto_id: i.id,
        cantidad: i.cantidad,
        notas: i.notas || null
      }))
    }
    await ordenesStore.enviarComanda(ordenPayload)
    alert(`¡Comanda enviada a Cocina/Barra para ${mesaNumero.value}! Se descontaron automáticamente los insumos de inventario.`)
    itemsComanda.value = []
    notasGenerales.value = ''
    router.push('/')
  } catch (err) {
    alert('Error al enviar la comanda a cocina.')
  } finally {
    enviando.value = false
  }
}
</script>

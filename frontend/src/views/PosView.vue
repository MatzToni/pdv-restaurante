<template>
  <div class="h-[calc(100vh-5rem)] flex flex-col lg:flex-row gap-4">
    <!-- Menú y Selección de Platillos (Izquierda) -->
    <div class="flex-1 flex flex-col bg-white rounded-2xl border border-slate-200 overflow-hidden shadow-sm">
      <!-- Categorías -->
      <div class="p-4 border-b border-slate-100 flex gap-2 overflow-x-auto no-scrollbar">
        <button
          v-for="cat in categorias"
          :key="cat"
          @click="categoriaActiva = cat"
          :class="[
            'px-4 py-2 rounded-xl text-sm font-semibold transition-colors shrink-0',
            categoriaActiva === cat 
              ? 'bg-slate-900 text-white shadow-sm' 
              : 'bg-slate-100 text-slate-600 hover:bg-slate-200'
          ]"
        >
          {{ cat }}
        </button>
      </div>

      <!-- Cuadrícula de Platillos Touch -->
      <div class="flex-1 p-4 overflow-y-auto grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 gap-3">
        <button
          v-for="item in platillosFiltrados"
          :key="item.id"
          @click="agregarAlPedido(item)"
          class="flex flex-col justify-between p-3.5 bg-slate-50 hover:bg-emerald-50/50 border border-slate-200/80 hover:border-emerald-500 rounded-xl text-left transition-all active:scale-95 group shadow-sm"
        >
          <div>
            <div class="font-bold text-slate-800 text-sm group-hover:text-emerald-700 leading-snug">{{ item.nombre }}</div>
            <div class="text-xs text-slate-400 mt-0.5 line-clamp-1">{{ item.descripcion }}</div>
          </div>
          <div class="mt-3 font-extrabold text-emerald-600 text-base">
            ${{ item.precio.toFixed(2) }}
          </div>
        </button>
      </div>
    </div>

    <!-- Comanda / Ticket Actual (Derecha) -->
    <div class="w-full lg:w-96 flex flex-col bg-white rounded-2xl border border-slate-200 overflow-hidden shadow-sm">
      <div class="p-4 border-b border-slate-100 flex justify-between items-center bg-slate-50">
        <div>
          <h2 class="font-bold text-slate-800">Comanda: {{ mesaActual }}</h2>
          <span class="text-xs text-slate-500">Mesero: Juan Pérez</span>
        </div>
        <button @click="limpiarTicket" class="text-xs text-rose-500 hover:underline">Limpiar</button>
      </div>

      <!-- Lista de Items en Comanda -->
      <div class="flex-1 p-4 overflow-y-auto space-y-3">
        <div v-if="itemsComanda.length === 0" class="h-full flex flex-col items-center justify-center text-slate-400 text-sm">
          <p>No hay platillos agregados</p>
          <span class="text-xs mt-1">Selecciona productos a la izquierda</span>
        </div>

        <div 
          v-for="(item, index) in itemsComanda" 
          :key="index"
          class="flex items-center justify-between p-2.5 rounded-xl bg-slate-50 border border-slate-100"
        >
          <div class="flex-1 min-w-0 pr-2">
            <h4 class="font-semibold text-sm text-slate-800 truncate">{{ item.nombre }}</h4>
            <div class="text-xs text-slate-500">${{ item.precio.toFixed(2) }} c/u</div>
          </div>
          <div class="flex items-center gap-2">
            <button @click="decrementar(index)" class="w-7 h-7 rounded-lg bg-slate-200 text-slate-700 flex items-center justify-center font-bold text-sm hover:bg-slate-300">-</button>
            <span class="font-bold text-sm w-5 text-center">{{ item.cantidad }}</span>
            <button @click="incrementar(index)" class="w-7 h-7 rounded-lg bg-slate-200 text-slate-700 flex items-center justify-center font-bold text-sm hover:bg-slate-300">+</button>
            <span class="font-bold text-sm text-slate-800 ml-2 w-16 text-right">${{ (item.precio * item.cantidad).toFixed(2) }}</span>
          </div>
        </div>
      </div>

      <!-- Resumen y Acciones Rápidas -->
      <div class="p-4 border-t border-slate-100 bg-slate-50 space-y-3">
        <div class="flex justify-between items-center text-sm text-slate-600">
          <span>Subtotal</span>
          <span>${{ subtotal.toFixed(2) }}</span>
        </div>
        <div class="flex justify-between items-center text-lg font-black text-slate-900 border-t border-slate-200 pt-2">
          <span>Total</span>
          <span class="text-emerald-600">${{ total.toFixed(2) }}</span>
        </div>

        <div class="grid grid-cols-2 gap-2 pt-2">
          <button 
            @click="enviarACocina"
            :disabled="itemsComanda.length === 0"
            class="w-full py-3 bg-amber-500 hover:bg-amber-600 disabled:opacity-50 text-white rounded-xl font-bold text-sm shadow-sm transition active:scale-95"
          >
            👨‍🍳 A Cocina
          </button>
          <button 
            @click="cobrarCuenta"
            :disabled="itemsComanda.length === 0"
            class="w-full py-3 bg-emerald-600 hover:bg-emerald-700 disabled:opacity-50 text-white rounded-xl font-bold text-sm shadow-sm transition active:scale-95"
          >
            💳 Cobrar
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'

const route = useRoute()
const router = useRouter()
const mesaActual = computed(() => route.query.mesaNombre || 'Mesa 1')

const categorias = ['Todos', 'Entradas', 'Platos Fuertes', 'Bebidas', 'Postres']
const categoriaActiva = ref('Todos')

const menuDemo = [
  { id: 101, categoria: 'Entradas', nombre: 'Guacamole con Totopos', descripcion: 'Aguacate fresco, pico de gallo', precio: 110.00 },
  { id: 102, categoria: 'Entradas', nombre: 'Papas Bravas', descripcion: 'Salsa chipotle y alioli', precio: 95.00 },
  { id: 103, categoria: 'Platos Fuertes', nombre: 'Hamburguesa Artesanal', descripcion: 'Carne de res 200g, queso cheddar, tocino', precio: 195.00 },
  { id: 104, categoria: 'Platos Fuertes', nombre: 'Tacos de Rib Eye (3 pzs)', descripcion: 'Cebolla caramelizada y salsa tatemada', precio: 240.00 },
  { id: 105, categoria: 'Platos Fuertes', nombre: 'Pizza Margarita', descripcion: 'Masa madre, albahaca y mozzarella', precio: 180.00 },
  { id: 106, categoria: 'Bebidas', nombre: 'Limonada Mineral', descripcion: 'Limón fresco y menta 500ml', precio: 55.00 },
  { id: 107, categoria: 'Bebidas', nombre: 'Cerveza Artesanal', descripcion: 'Estilo IPA 355ml', precio: 85.00 },
  { id: 108, categoria: 'Postres', nombre: 'Pastel de Chocolate', descripcion: 'Bizcocho húmedo con ganache', precio: 90.00 },
]

const platillosFiltrados = computed(() => {
  if (categoriaActiva.value === 'Todos') return menuDemo
  return menuDemo.filter(item => item.categoria === categoriaActiva.value)
})

const itemsComanda = ref([
  { id: 103, nombre: 'Hamburguesa Artesanal', precio: 195.00, cantidad: 1 },
  { id: 106, nombre: 'Limonada Mineral', precio: 55.00, cantidad: 2 }
])

const subtotal = computed(() => itemsComanda.value.reduce((acc, item) => acc + (item.precio * item.cantidad), 0))
const total = computed(() => subtotal.value)

const agregarAlPedido = (item) => {
  const existente = itemsComanda.value.find(i => i.id === item.id)
  if (existente) {
    existente.cantidad++
  } else {
    itemsComanda.value.push({ ...item, cantidad: 1 })
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
const limpiarTicket = () => { itemsComanda.value = [] }

const enviarACocina = () => {
  alert('¡Comanda enviada a Cocina/Barra en tiempo real!')
}

const cobrarCuenta = () => {
  router.push('/caja')
}
</script>

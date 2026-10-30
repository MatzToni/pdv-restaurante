<template>
  <div class="space-y-6">
    <!-- Header -->
    <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 bg-white p-6 rounded-2xl shadow-sm border border-slate-200">
      <div>
        <h1 class="text-2xl font-bold text-slate-800">Mapa de Mesas</h1>
        <p class="text-slate-500 text-sm">Gestiona el estado de las mesas y órdenes activas</p>
      </div>
      <div class="flex items-center gap-2">
        <span class="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-medium bg-emerald-100 text-emerald-800">
          <span class="w-2 h-2 rounded-full bg-emerald-500"></span> 8 Libres
        </span>
        <span class="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-medium bg-amber-100 text-amber-800">
          <span class="w-2 h-2 rounded-full bg-amber-500"></span> 4 Ocupadas
        </span>
        <span class="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-medium bg-rose-100 text-rose-800">
          <span class="w-2 h-2 rounded-full bg-rose-500"></span> 2 Por Cobrar
        </span>
      </div>
    </div>

    <!-- Grid de mesas demo -->
    <div class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-6 gap-4">
      <div 
        v-for="mesa in mesasDemo" 
        :key="mesa.id"
        @click="seleccionarMesa(mesa)"
        :class="[
          'p-5 rounded-2xl border-2 transition-all cursor-pointer flex flex-col justify-between h-36 active:scale-95 shadow-sm',
          mesa.estado === 'libre' ? 'border-slate-200 bg-white hover:border-emerald-500 hover:shadow-md' :
          mesa.estado === 'ocupada' ? 'border-amber-400 bg-amber-50/60' :
          'border-rose-400 bg-rose-50/60'
        ]"
      >
        <div class="flex justify-between items-start">
          <span class="font-bold text-lg text-slate-800">{{ mesa.nombre }}</span>
          <span 
            :class="[
              'w-3 h-3 rounded-full',
              mesa.estado === 'libre' ? 'bg-emerald-500' :
              mesa.estado === 'ocupada' ? 'bg-amber-500' : 'bg-rose-500'
            ]"
          ></span>
        </div>
        
        <div class="text-xs text-slate-500">
          <div v-if="mesa.estado === 'libre'">Capacidad: {{ mesa.capacidad }} pers.</div>
          <div v-else>
            <div class="font-semibold text-slate-700">${{ mesa.total?.toFixed(2) }}</div>
            <div>{{ mesa.tiempo }}</div>
          </div>
        </div>

        <div class="text-xs font-semibold capitalize" :class="{
          'text-emerald-600': mesa.estado === 'libre',
          'text-amber-600': mesa.estado === 'ocupada',
          'text-rose-600': mesa.estado === 'cuenta'
        }">
          {{ mesa.estado === 'cuenta' ? 'Por cobrar' : mesa.estado }}
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

const mesasDemo = ref([
  { id: 1, nombre: 'Mesa 1', capacidad: 4, estado: 'libre' },
  { id: 2, nombre: 'Mesa 2', capacidad: 2, estado: 'ocupada', total: 420.50, tiempo: '35 min' },
  { id: 3, nombre: 'Mesa 3', capacidad: 4, estado: 'libre' },
  { id: 4, nombre: 'Mesa 4', capacidad: 6, estado: 'ocupada', total: 980.00, tiempo: '15 min' },
  { id: 5, nombre: 'Mesa 5', capacidad: 2, estado: 'cuenta', total: 615.00, tiempo: '50 min' },
  { id: 6, nombre: 'Mesa 6', capacidad: 8, estado: 'libre' },
  { id: 7, nombre: 'Mesa 7', capacidad: 4, estado: 'libre' },
  { id: 8, nombre: 'Mesa 8', capacidad: 4, estado: 'libre' },
  { id: 9, nombre: 'Barra 1', capacidad: 1, estado: 'ocupada', total: 180.00, tiempo: '10 min' },
  { id: 10, nombre: 'Barra 2', capacidad: 1, estado: 'libre' },
])

const seleccionarMesa = (mesa) => {
  router.push({ path: '/pos', query: { mesaId: mesa.id, mesaNombre: mesa.nombre } })
}
</script>

<template>
  <div class="space-y-4">
    <div class="flex justify-between items-center bg-white p-4 rounded-2xl border border-slate-200 shadow-sm">
      <div>
        <h1 class="text-2xl font-bold text-slate-800">Pantalla de Cocina (KDS)</h1>
        <p class="text-slate-500 text-sm">Órdenes pendientes de preparación en tiempo real</p>
      </div>
      <div class="flex items-center gap-3">
        <span class="inline-flex items-center gap-2 px-3 py-1.5 rounded-xl bg-amber-50 text-amber-700 text-sm font-semibold border border-amber-200">
          🕒 3 Órdenes en preparación
        </span>
      </div>
    </div>

    <!-- Grid de Comandas KDS -->
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
      <div 
        v-for="orden in ordenesDemo" 
        :key="orden.id"
        class="bg-white rounded-2xl border-2 border-slate-200 overflow-hidden shadow-sm flex flex-col justify-between"
      >
        <div>
          <!-- Cabecera de la comanda -->
          <div :class="[
            'p-3.5 flex justify-between items-center text-white font-bold',
            orden.tiempoMinutos > 20 ? 'bg-rose-600' :
            orden.tiempoMinutos > 10 ? 'bg-amber-500' : 'bg-slate-800'
          ]">
            <div>
              <span class="text-lg">{{ orden.mesa }}</span>
              <span class="text-xs opacity-80 block">Orden #{{ orden.id }}</span>
            </div>
            <div class="text-right">
              <span class="text-base">⏱️ {{ orden.tiempoMinutos }} min</span>
              <span class="text-xs opacity-80 block">{{ orden.mesero }}</span>
            </div>
          </div>

          <!-- Items de la comanda -->
          <div class="p-4 space-y-3">
            <div 
              v-for="(item, i) in orden.items" 
              :key="i"
              class="flex justify-between items-start border-b border-slate-100 pb-2 last:border-0"
            >
              <div class="flex items-start gap-2">
                <span class="font-extrabold text-slate-900 bg-slate-100 px-2 py-0.5 rounded text-sm">{{ item.cantidad }}x</span>
                <div>
                  <span class="font-bold text-slate-800 text-sm block">{{ item.nombre }}</span>
                  <span v-if="item.notas" class="text-xs text-rose-600 font-semibold italic">{{ item.notas }}</span>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Botón para completar -->
        <div class="p-3 bg-slate-50 border-t border-slate-100">
          <button 
            @click="completarOrden(orden.id)"
            class="w-full py-2.5 bg-emerald-600 hover:bg-emerald-700 text-white rounded-xl font-bold text-sm shadow-sm transition active:scale-95"
          >
            ✓ Marcar como Listo
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const ordenesDemo = ref([
  {
    id: 1042,
    mesa: 'Mesa 4',
    mesero: 'Carlos L.',
    tiempoMinutos: 8,
    items: [
      { cantidad: 2, nombre: 'Hamburguesa Artesanal', notas: 'Término 3/4, sin cebolla' },
      { cantidad: 1, nombre: 'Papas Bravas', notas: 'Salsa aparte' }
    ]
  },
  {
    id: 1043,
    mesa: 'Mesa 2',
    mesero: 'Ana G.',
    tiempoMinutos: 16,
    items: [
      { cantidad: 1, nombre: 'Pizza Margarita', notas: 'Bien dorada' },
      { cantidad: 2, nombre: 'Tacos de Rib Eye', notas: 'Con todo' }
    ]
  },
  {
    id: 1044,
    mesa: 'Barra 1',
    mesero: 'Juan P.',
    tiempoMinutos: 4,
    items: [
      { cantidad: 1, nombre: 'Guacamole con Totopos', notas: '' }
    ]
  }
])

const completarOrden = (id) => {
  ordenesDemo.value = ordenesDemo.value.filter(o => o.id !== id)
}
</script>

<template>
  <div class="space-y-6">
    <!-- Header -->
    <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 bg-white p-6 rounded-2xl shadow-sm border border-slate-200">
      <div>
        <h1 class="text-2xl font-black text-slate-800 tracking-tight">Mapa de Mesas</h1>
        <p class="text-slate-500 text-sm">Gestiona el estado de las mesas y salones en tiempo real</p>
      </div>

      <div class="flex flex-wrap items-center gap-3">
        <!-- Indicadores -->
        <span class="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-bold bg-emerald-100 text-emerald-800">
          <span class="w-2 h-2 rounded-full bg-emerald-500"></span> {{ mesasStore.mesasLibres.length }} Libres
        </span>
        <span class="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-bold bg-amber-100 text-amber-800">
          <span class="w-2 h-2 rounded-full bg-amber-500"></span> {{ mesasStore.mesasOcupadas.length }} Ocupadas
        </span>
        <span class="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-bold bg-rose-100 text-rose-800">
          <span class="w-2 h-2 rounded-full bg-rose-500"></span> {{ mesasStore.mesasCuenta.length }} Por Cobrar
        </span>

        <!-- Botón crear mesa -->
        <button 
          @click="modalNuevaMesa = true"
          class="px-3.5 py-1.5 bg-eden-600 hover:bg-eden-700 text-white rounded-xl text-xs font-bold shadow-sm transition active:scale-95"
        >
          + Nueva Mesa
        </button>
      </div>
    </div>

    <!-- Spinner de carga -->
    <div v-if="mesasStore.cargando" class="text-center py-16 text-slate-400">
      <div class="inline-block animate-spin rounded-full h-8 w-8 border-4 border-slate-200 border-t-eden-600 mb-2"></div>
      <p class="text-sm">Cargando mesas desde el servidor...</p>
    </div>

    <!-- Grid de Mesas por Área -->
    <div v-else class="space-y-8">
      <div v-for="area in mesasPorArea" :key="area.id" class="space-y-3">
        <h2 class="text-sm font-extrabold uppercase tracking-wider text-slate-500 flex items-center gap-2">
          <span>📍</span> {{ area.nombre }}
          <span class="text-xs bg-slate-200 text-slate-700 font-bold px-2 py-0.5 rounded-full">{{ area.mesas.length }}</span>
        </h2>

        <div class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 xl:grid-cols-6 gap-3.5">
          <div 
            v-for="mesa in area.mesas" 
            :key="mesa.id"
            @click="abrirComandero(mesa)"
            :class="[
              'p-4 rounded-2xl border-2 transition-all cursor-pointer flex flex-col justify-between h-32 active:scale-95 shadow-sm',
              mesa.estado === 'libre' ? 'border-slate-200 bg-white hover:border-emerald-500 hover:shadow-md' :
              mesa.estado === 'ocupada' ? 'border-amber-400 bg-amber-50/70 hover:border-amber-500' :
              'border-rose-400 bg-rose-50/70 hover:border-rose-500'
            ]"
          >
            <div class="flex justify-between items-start">
              <span class="font-bold text-base text-slate-800">{{ mesa.numero }}</span>
              <span 
                :class="[
                  'w-3 h-3 rounded-full',
                  mesa.estado === 'libre' ? 'bg-emerald-500' :
                  mesa.estado === 'ocupada' ? 'bg-amber-500' : 'bg-rose-500'
                ]"
              ></span>
            </div>

            <div class="text-xs text-slate-500 font-medium">
              <span>Capacidad: {{ mesa.capacidad }} pers.</span>
            </div>

            <div class="text-xs font-bold capitalize flex justify-between items-center" :class="{
              'text-emerald-600': mesa.estado === 'libre',
              'text-amber-600': mesa.estado === 'ocupada',
              'text-rose-600': mesa.estado === 'cuenta'
            }">
              <span>{{ mesa.estado === 'cuenta' ? 'Por cobrar' : mesa.estado }}</span>
              <span class="text-slate-400 font-normal">→</span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Modal para Crear Nueva Mesa -->
    <div v-if="modalNuevaMesa" class="fixed inset-0 bg-slate-900/50 backdrop-blur-sm flex items-center justify-center p-4 z-50">
      <div class="bg-white rounded-3xl p-6 max-w-sm w-full shadow-2xl border border-slate-200 space-y-4">
        <h3 class="text-lg font-black text-slate-800">Agregar Nueva Mesa</h3>
        
        <div class="space-y-3">
          <div>
            <label class="text-xs font-bold text-slate-600">Nombre / Denominación</label>
            <input 
              v-model="formMesa.numero" 
              type="text" 
              placeholder="Ej. Mesa 7, Terraza 5" 
              class="w-full mt-1 p-2.5 border border-slate-300 rounded-xl text-sm font-semibold focus:outline-none focus:border-eden-600"
            />
          </div>

          <div>
            <label class="text-xs font-bold text-slate-600">Área / Salón</label>
            <select 
              v-model.number="formMesa.area_id" 
              class="w-full mt-1 p-2.5 border border-slate-300 rounded-xl text-sm font-semibold focus:outline-none focus:border-eden-600"
            >
              <option v-for="area in mesasStore.areas" :key="area.id" :value="area.id">
                {{ area.nombre }}
              </option>
            </select>
          </div>

          <div>
            <label class="text-xs font-bold text-slate-600">Capacidad (Personas)</label>
            <input 
              v-model.number="formMesa.capacidad" 
              type="number" 
              min="1" 
              class="w-full mt-1 p-2.5 border border-slate-300 rounded-xl text-sm font-semibold focus:outline-none focus:border-eden-600"
            />
          </div>
        </div>

        <div class="flex gap-2 pt-2">
          <button 
            @click="modalNuevaMesa = false" 
            class="flex-1 py-2.5 bg-slate-100 hover:bg-slate-200 text-slate-700 rounded-xl font-bold text-sm transition"
          >
            Cancelar
          </button>
          <button 
            @click="guardarMesa" 
            :disabled="!formMesa.numero || !formMesa.area_id"
            class="flex-1 py-2.5 bg-eden-600 hover:bg-eden-700 disabled:opacity-50 text-white rounded-xl font-bold text-sm transition shadow-sm"
          >
            Crear Mesa
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useMesasStore } from '../stores/mesas'

const router = useRouter()
const mesasStore = useMesasStore()

const modalNuevaMesa = ref(false)
const formMesa = ref({
  numero: '',
  area_id: 1,
  capacidad: 4,
  estado: 'libre'
})

onMounted(() => {
  mesasStore.cargarMesas()
})

const mesasPorArea = computed(() => {
  return mesasStore.areas.map(area => ({
    ...area,
    mesas: mesasStore.mesas.filter(m => m.area_id === area.id)
  }))
})

const abrirComandero = (mesa) => {
  router.push({
    path: '/pos',
    query: { mesaId: mesa.id, mesaNumero: mesa.numero }
  })
}

const guardarMesa = async () => {
  try {
    await mesasStore.crearMesa(formMesa.value)
    modalNuevaMesa.value = false
    formMesa.value = { numero: '', area_id: mesasStore.areas[0]?.id || 1, capacidad: 4, estado: 'libre' }
  } catch (err) {
    alert('Error al crear la mesa.')
  }
}
</script>

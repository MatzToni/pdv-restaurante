<template>
  <div class="space-y-6">
    <!-- Header -->
    <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 bg-white dark:bg-slate-900 p-6 rounded-2xl shadow-sm border border-slate-200 dark:border-slate-800 transition-colors">
      <div>
        <h1 class="text-2xl font-black text-slate-800 dark:text-slate-100 tracking-tight">Mapa de Mesas</h1>
        <p class="text-slate-500 dark:text-slate-400 text-sm">Gestiona el estado de las mesas y salones en tiempo real</p>
      </div>

      <div class="flex flex-wrap items-center gap-3">
        <!-- Indicadores -->
        <span class="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-bold bg-emerald-100 dark:bg-emerald-950/60 text-emerald-800 dark:text-emerald-300 border border-emerald-200 dark:border-emerald-800/40">
          <span class="w-2 h-2 rounded-full bg-emerald-500"></span> {{ mesasStore.mesasLibres.length }} Libres
        </span>
        <span class="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-bold bg-amber-100 dark:bg-amber-950/60 text-amber-800 dark:text-amber-300 border border-amber-200 dark:border-amber-800/40">
          <span class="w-2 h-2 rounded-full bg-amber-500"></span> {{ mesasStore.mesasOcupadas.length }} Ocupadas
        </span>
        <span class="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-bold bg-rose-100 dark:bg-rose-950/60 text-rose-800 dark:text-rose-300 border border-rose-200 dark:border-rose-800/40">
          <span class="w-2 h-2 rounded-full bg-rose-500"></span> {{ mesasStore.mesasCuenta.length }} Por Cobrar
        </span>

        <!-- Botón crear mesa (solo visible para admin/gerente/jefe) -->
        <button 
          v-if="['administrador', 'gerente', 'jefe'].includes(authStore.rolActual)"
          @click="modalNuevaMesa = true"
          class="px-3.5 py-1.5 bg-eden-600 hover:bg-eden-700 text-white rounded-xl text-xs font-bold shadow-sm transition active:scale-95"
        >
          + Nueva Mesa
        </button>
      </div>
    </div>

    <!-- Spinner de carga -->
    <div v-if="mesasStore.cargando" class="text-center py-16 text-slate-400">
      <div class="inline-block animate-spin rounded-full h-8 w-8 border-4 border-slate-200 dark:border-slate-800 border-t-eden-600 mb-2"></div>
      <p class="text-sm">Cargando mesas desde el servidor...</p>
    </div>

    <!-- Grid de Mesas por Área -->
    <div v-else class="space-y-8">
      <div v-for="area in mesasPorArea" :key="area.id" class="space-y-3">
        <h2 class="text-sm font-extrabold uppercase tracking-wider text-slate-500 dark:text-slate-400 flex items-center gap-2">
          <span>📍</span> {{ area.nombre }}
          <span class="text-xs bg-slate-200 dark:bg-slate-800 text-slate-700 dark:text-slate-300 font-bold px-2 py-0.5 rounded-full">{{ area.mesas.length }}</span>
        </h2>

        <div class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 xl:grid-cols-6 gap-3.5">
          <div 
            v-for="mesa in area.mesas" 
            :key="mesa.id"
            @click="abrirOpcionesMesa(mesa)"
            :class="[
              'p-4 rounded-2xl border-2 transition-all cursor-pointer flex flex-col justify-between min-h-[8.5rem] h-auto active:scale-95 shadow-sm',
              mesa.estado === 'libre' ? 'border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 hover:border-emerald-500 hover:shadow-md' :
              mesa.estado === 'ocupada' ? 'border-amber-400 dark:border-amber-600 bg-amber-50/70 dark:bg-amber-950/30 hover:border-amber-500' :
              'border-rose-400 dark:border-rose-600 bg-rose-50/70 dark:bg-rose-950/30 hover:border-rose-500'
            ]"
          >
            <div class="flex justify-between items-start">
              <span class="font-bold text-base text-slate-800 dark:text-slate-100">{{ mesa.numero }}</span>
              <div class="flex items-center gap-1.5">
                <span v-if="getAlertaMesa(mesa.id)" 
                  :class="[
                    'text-3xs font-black px-1.5 py-0.5 rounded-full uppercase',
                    getAlertaMesa(mesa.id).tipo === 'observacion' ? 'bg-amber-500 text-white animate-pulse' : 'bg-emerald-500 text-white'
                  ]">
                  {{ getAlertaMesa(mesa.id).texto }}
                </span>
                <span 
                  :class="[
                    'w-3 h-3 rounded-full',
                    mesa.estado === 'libre' ? 'bg-emerald-500' :
                    mesa.estado === 'ocupada' ? 'bg-amber-500' : 'bg-rose-500'
                  ]"
                ></span>
              </div>
            </div>

            <div class="text-xs text-slate-500 dark:text-slate-400 font-medium">
              <span>Capacidad: {{ mesa.capacidad }} pers.</span>
            </div>

            <div class="text-xs font-bold capitalize flex justify-between items-center" :class="{
              'text-emerald-600 dark:text-emerald-400': mesa.estado === 'libre',
              'text-amber-600 dark:text-amber-400': mesa.estado === 'ocupada',
              'text-rose-600 dark:text-rose-400': mesa.estado === 'cuenta'
            }">
              <span>{{ mesa.estado === 'cuenta' ? 'Por cobrar' : mesa.estado }}</span>
              <span class="text-slate-400 font-normal">→</span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Modal para Crear Nueva Mesa -->
    <div v-if="modalNuevaMesa" class="fixed inset-0 bg-slate-900/60 backdrop-blur-sm flex items-center justify-center p-4 z-50">
      <div class="bg-white dark:bg-slate-900 rounded-3xl p-6 max-w-sm w-full shadow-2xl border border-slate-200 dark:border-slate-800 space-y-4">
        <h3 class="text-lg font-black text-slate-800 dark:text-slate-100">Agregar Nueva Mesa</h3>
        
        <div class="space-y-3">
          <div>
            <label class="text-xs font-bold text-slate-600 dark:text-slate-400">Nombre / Denominación</label>
            <input 
              v-model="formMesa.numero" 
              type="text" 
              placeholder="Ej. Mesa 7, Terraza 5" 
              class="w-full mt-1 p-2.5 border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-800 text-slate-800 dark:text-slate-100 rounded-xl text-sm font-semibold focus:outline-none focus:border-eden-600"
            />
          </div>

          <div>
            <label class="text-xs font-bold text-slate-600 dark:text-slate-400">Área / Salón</label>
            <select 
              v-model.number="formMesa.area_id" 
              class="w-full mt-1 p-2.5 border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-800 text-slate-800 dark:text-slate-100 rounded-xl text-sm font-semibold focus:outline-none focus:border-eden-600"
            >
              <option v-for="area in mesasStore.areas" :key="area.id" :value="area.id">
                {{ area.nombre }}
              </option>
            </select>
          </div>

          <div>
            <label class="text-xs font-bold text-slate-600 dark:text-slate-400">Capacidad (Personas)</label>
            <input 
              v-model.number="formMesa.capacidad" 
              type="number" 
              min="1" 
              class="w-full mt-1 p-2.5 border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-800 text-slate-800 dark:text-slate-100 rounded-xl text-sm font-semibold focus:outline-none focus:border-eden-600"
            />
          </div>
        </div>

        <div class="flex gap-2 pt-2">
          <button 
            @click="modalNuevaMesa = false" 
            class="flex-1 py-2.5 bg-slate-100 dark:bg-slate-800 hover:bg-slate-200 dark:hover:bg-slate-700 text-slate-700 dark:text-slate-300 rounded-xl font-bold text-sm transition"
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

    <!-- Modal Opciones de Mesa (Ciclo de Vida: Libre -> Ocupada -> Por Cobrar -> Libre) -->
    <div v-if="modalOpcionesMesa && mesaSeleccionada" class="fixed inset-0 bg-slate-900/60 backdrop-blur-sm flex items-center justify-center p-4 z-50">
      <div class="bg-white dark:bg-slate-900 rounded-3xl p-6 max-w-sm w-full shadow-2xl border border-slate-200 dark:border-slate-800 space-y-4">
        <div class="flex justify-between items-start border-b border-slate-100 dark:border-slate-800 pb-3">
          <div>
            <h3 class="text-xl font-black text-slate-800 dark:text-slate-100">{{ mesaSeleccionada.numero }}</h3>
            <span class="text-xs text-slate-400">Capacidad: {{ mesaSeleccionada.capacidad }} personas</span>
          </div>
          <span 
            :class="[
              'text-xs font-black px-2.5 py-1 rounded-full uppercase',
              mesaSeleccionada.estado === 'libre' ? 'bg-emerald-100 text-emerald-800 dark:bg-emerald-950/60 dark:text-emerald-300' :
              mesaSeleccionada.estado === 'ocupada' ? 'bg-amber-100 text-amber-800 dark:bg-amber-950/60 dark:text-amber-300' :
              'bg-rose-100 text-rose-800 dark:bg-rose-950/60 dark:text-rose-300'
            ]"
          >
            {{ mesaSeleccionada.estado === 'cuenta' ? 'Por cobrar' : mesaSeleccionada.estado }}
          </span>
        </div>

        <!-- Capacidad / Comensales (Editable al instante) -->
        <div class="p-3 bg-slate-50 dark:bg-slate-800/60 rounded-2xl border border-slate-200/80 dark:border-slate-700/60 flex items-center justify-between">
          <div class="flex items-center gap-2">
            <span class="text-lg">👥</span>
            <div>
              <div class="text-xs font-bold text-slate-700 dark:text-slate-200">Personas / Capacidad</div>
              <div class="text-3xs text-slate-400">Comensales sugeridos</div>
            </div>
          </div>
          
          <div class="flex items-center gap-1.5">
            <button 
              @click="ajustarCapacidad(mesaSeleccionada, -1)"
              :disabled="mesaSeleccionada.capacidad <= 1"
              class="w-9 h-9 rounded-xl bg-white dark:bg-slate-700 border border-slate-200 dark:border-slate-600 font-bold text-base text-slate-700 dark:text-slate-200 hover:bg-slate-100 dark:hover:bg-slate-600 disabled:opacity-40 active:scale-95 shadow-xs flex items-center justify-center transition"
              title="Restar comensal"
            >
              −
            </button>
            <input 
              type="number" 
              min="1" 
              max="99"
              v-model.number="mesaSeleccionada.capacidad"
              @change="guardarCapacidadDirecta(mesaSeleccionada)"
              class="w-12 text-center text-sm font-black bg-white dark:bg-slate-700 border border-slate-200 dark:border-slate-600 rounded-xl py-1.5 text-slate-800 dark:text-slate-100 focus:outline-none focus:border-eden-600"
            />
            <button 
              @click="ajustarCapacidad(mesaSeleccionada, 1)"
              class="w-9 h-9 rounded-xl bg-white dark:bg-slate-700 border border-slate-200 dark:border-slate-600 font-bold text-base text-slate-700 dark:text-slate-200 hover:bg-slate-100 dark:hover:bg-slate-600 active:scale-95 shadow-xs flex items-center justify-center transition"
              title="Sumar comensal"
            >
              +
            </button>
          </div>
        </div>

        <!-- Acciones Principales -->
        <div class="space-y-2">
          <!-- Abrir Comandero -->
          <button 
            @click="abrirComandero(mesaSeleccionada)"
            class="w-full py-3 bg-eden-600 hover:bg-eden-700 text-white rounded-xl font-black text-xs shadow-sm transition active:scale-95 flex items-center justify-center gap-2"
          >
            <span>📝</span>
            <span>{{ mesaSeleccionada.estado === 'libre' ? 'Tomar Orden (Comandero)' : 'Ver / Agregar Rondas' }}</span>
          </button>

          <!-- Si está libre: opción de ocupar mesa directamente -->
          <button 
            v-if="mesaSeleccionada.estado === 'libre'"
            @click="cambiarEstadoMesa(mesaSeleccionada, 'ocupada')"
            class="w-full py-2.5 bg-amber-50 dark:bg-amber-950/40 hover:bg-amber-100 border border-amber-300 dark:border-amber-800 text-amber-800 dark:text-amber-300 rounded-xl font-bold text-xs transition active:scale-95 flex items-center justify-center gap-1.5"
          >
            <span>👤</span> Ocupar Mesa (Comensales Sentados)
          </button>

          <!-- Si está ocupada: opción de pedir cuenta o liberar -->
          <button 
            v-if="mesaSeleccionada.estado === 'ocupada'"
            @click="solicitarCuentaMesa(mesaSeleccionada)"
            class="w-full py-2.5 bg-rose-50 dark:bg-rose-950/40 hover:bg-rose-100 border border-rose-300 dark:border-rose-800 text-rose-700 dark:text-rose-300 rounded-xl font-bold text-xs transition active:scale-95 flex items-center justify-center gap-1.5"
          >
            <span>🧾</span> Solicitar Cuenta (Pasar a Por Cobrar)
          </button>

          <!-- Si está en cuenta: ir a caja -->
          <button 
            v-if="mesaSeleccionada.estado === 'cuenta'"
            @click="router.push('/caja')"
            class="w-full py-2.5 bg-purple-600 hover:bg-purple-700 text-white rounded-xl font-bold text-xs shadow-sm transition active:scale-95 flex items-center justify-center gap-1.5"
          >
            <span>💵</span> Ir a Caja para Cobrar
          </button>

          <!-- Liberar mesa si ya no está libre -->
          <button 
            v-if="mesaSeleccionada.estado !== 'libre'"
            @click="cambiarEstadoMesa(mesaSeleccionada, 'libre')"
            class="w-full py-2.5 bg-slate-100 dark:bg-slate-800 hover:bg-slate-200 text-slate-700 dark:text-slate-300 rounded-xl font-bold text-xs transition active:scale-95 flex items-center justify-center gap-1.5"
          >
            <span>🟢</span> Marcar como Libre / Limpia
          </button>

          <!-- Opción de editar mesa completa para administración -->
          <button 
            v-if="['administrador', 'gerente', 'jefe'].includes(authStore.rolActual)"
            @click="abrirEditarMesa(mesaSeleccionada)"
            class="w-full py-2 bg-slate-100 dark:bg-slate-800 hover:bg-slate-200 dark:hover:bg-slate-700 text-slate-700 dark:text-slate-300 rounded-xl font-bold text-xs transition active:scale-95 flex items-center justify-center gap-1.5 border border-slate-200 dark:border-slate-700"
          >
            <span>⚙️</span> Editar Datos de la Mesa
          </button>
        </div>

        <div class="pt-2 border-t border-slate-100 dark:border-slate-800 flex justify-end">
          <button 
            @click="modalOpcionesMesa = false" 
            class="px-4 py-2 text-xs font-bold text-slate-500 hover:text-slate-700"
          >
            Cerrar
          </button>
        </div>
      </div>
    </div>

    <!-- Modal para Editar Mesa Completa (Nombre, Área, Capacidad) -->
    <div v-if="modalEditarMesa" class="fixed inset-0 bg-slate-900/60 backdrop-blur-sm flex items-center justify-center p-4 z-50">
      <div class="bg-white dark:bg-slate-900 rounded-3xl p-6 max-w-sm w-full shadow-2xl border border-slate-200 dark:border-slate-800 space-y-4">
        <h3 class="text-lg font-black text-slate-800 dark:text-slate-100">Editar Mesa</h3>
        
        <div class="space-y-3">
          <div>
            <label class="text-xs font-bold text-slate-600 dark:text-slate-400">Nombre / Denominación</label>
            <input 
              v-model="formEditarMesa.numero" 
              type="text" 
              placeholder="Ej. Mesa 1, Terraza 2" 
              class="w-full mt-1 p-2.5 border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-800 text-slate-800 dark:text-slate-100 rounded-xl text-sm font-semibold focus:outline-none focus:border-eden-600"
            />
          </div>

          <div>
            <label class="text-xs font-bold text-slate-600 dark:text-slate-400">Área / Salón</label>
            <select 
              v-model.number="formEditarMesa.area_id" 
              class="w-full mt-1 p-2.5 border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-800 text-slate-800 dark:text-slate-100 rounded-xl text-sm font-semibold focus:outline-none focus:border-eden-600"
            >
              <option v-for="area in mesasStore.areas" :key="area.id" :value="area.id">
                {{ area.nombre }}
              </option>
            </select>
          </div>

          <div>
            <label class="text-xs font-bold text-slate-600 dark:text-slate-400">Capacidad (Personas)</label>
            <div class="flex items-center gap-2 mt-1">
              <button 
                type="button"
                @click="formEditarMesa.capacidad = Math.max(1, (formEditarMesa.capacidad || 1) - 1)"
                class="w-10 h-10 rounded-xl bg-slate-100 dark:bg-slate-800 font-bold text-base active:scale-95 flex items-center justify-center border border-slate-300 dark:border-slate-700 text-slate-700 dark:text-slate-200"
              >
                −
              </button>
              <input 
                v-model.number="formEditarMesa.capacidad" 
                type="number" 
                min="1" 
                class="flex-1 text-center p-2.5 border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-800 text-slate-800 dark:text-slate-100 rounded-xl text-sm font-bold focus:outline-none focus:border-eden-600"
              />
              <button 
                type="button"
                @click="formEditarMesa.capacidad = (formEditarMesa.capacidad || 1) + 1"
                class="w-10 h-10 rounded-xl bg-slate-100 dark:bg-slate-800 font-bold text-base active:scale-95 flex items-center justify-center border border-slate-300 dark:border-slate-700 text-slate-700 dark:text-slate-200"
              >
                +
              </button>
            </div>
          </div>
        </div>

        <div class="flex gap-2 pt-2">
          <button 
            @click="modalEditarMesa = false" 
            class="flex-1 py-2.5 bg-slate-100 dark:bg-slate-800 hover:bg-slate-200 dark:hover:bg-slate-700 text-slate-700 dark:text-slate-300 rounded-xl font-bold text-sm transition"
          >
            Cancelar
          </button>
          <button 
            @click="guardarEdicionMesa" 
            :disabled="!formEditarMesa.numero || !formEditarMesa.area_id || formEditarMesa.capacidad < 1"
            class="flex-1 py-2.5 bg-eden-600 hover:bg-eden-700 disabled:opacity-50 text-white rounded-xl font-bold text-sm transition shadow-sm"
          >
            Guardar Cambios
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
import { useOrdenesStore } from '../stores/ordenes'
import { useAuthStore } from '../stores/auth'

const router = useRouter()
const mesasStore = useMesasStore()
const ordenesStore = useOrdenesStore()
const authStore = useAuthStore()

const modalNuevaMesa = ref(false)
const modalOpcionesMesa = ref(false)
const modalEditarMesa = ref(false)
const mesaSeleccionada = ref(null)

const formMesa = ref({
  numero: '',
  area_id: 1,
  capacidad: 4,
  estado: 'libre'
})

const formEditarMesa = ref({
  id: null,
  numero: '',
  area_id: 1,
  capacidad: 4
})

onMounted(() => {
  mesasStore.cargarMesas()
  ordenesStore.cargarOrdenesActivas()
})

const abrirOpcionesMesa = (mesa) => {
  mesaSeleccionada.value = mesa
  modalOpcionesMesa.value = true
}

const abrirEditarMesa = (mesa) => {
  formEditarMesa.value = {
    id: mesa.id,
    numero: mesa.numero,
    area_id: mesa.area_id,
    capacidad: mesa.capacidad
  }
  modalOpcionesMesa.value = false
  modalEditarMesa.value = true
}

const guardarEdicionMesa = async () => {
  try {
    const data = await mesasStore.actualizarMesa(formEditarMesa.value.id, {
      numero: formEditarMesa.value.numero,
      area_id: formEditarMesa.value.area_id,
      capacidad: formEditarMesa.value.capacidad
    })
    modalEditarMesa.value = false
    if (mesaSeleccionada.value && mesaSeleccionada.value.id === data.id) {
      mesaSeleccionada.value.numero = data.numero
      mesaSeleccionada.value.area_id = data.area_id
      mesaSeleccionada.value.capacidad = data.capacidad
    }
  } catch (err) {
    console.error('Error al actualizar mesa:', err)
    alert(err.response?.data?.detail || 'Error al actualizar la mesa.')
  }
}

const ajustarCapacidad = async (mesa, delta) => {
  const nuevaCapacidad = (mesa.capacidad || 4) + delta
  if (nuevaCapacidad < 1) return
  const anterior = mesa.capacidad
  mesa.capacidad = nuevaCapacidad
  try {
    await mesasStore.actualizarCapacidad(mesa.id, nuevaCapacidad)
  } catch (err) {
    mesa.capacidad = anterior
    console.error('Error al actualizar capacidad:', err)
    alert(err.response?.data?.detail || 'Error al actualizar la capacidad de la mesa.')
  }
}

const guardarCapacidadDirecta = async (mesa) => {
  if (!mesa.capacidad || mesa.capacidad < 1) {
    mesa.capacidad = 1
  }
  try {
    await mesasStore.actualizarCapacidad(mesa.id, mesa.capacidad)
  } catch (err) {
    console.error('Error al actualizar capacidad:', err)
    alert(err.response?.data?.detail || 'Error al actualizar la capacidad de la mesa.')
  }
}

const cambiarEstadoMesa = async (mesa, nuevoEstado) => {
  try {
    await mesasStore.cambiarEstadoMesa(mesa.id, nuevoEstado)
    mesa.estado = nuevoEstado
    modalOpcionesMesa.value = false
  } catch (err) {
    console.error('Error al actualizar estado:', err)
    alert(err.response?.data?.detail || 'Error al actualizar estado de la mesa.')
  }
}

const solicitarCuentaMesa = async (mesa) => {
  try {
    const ord = ordenesStore.ordenesActivas.find(o => o.mesa_id === mesa.id && o.estado !== 'pagado')
    if (ord) {
      await ordenesStore.pedirCuenta(ord.id)
    } else {
      await mesasStore.cambiarEstadoMesa(mesa.id, 'cuenta')
    }
    mesa.estado = 'cuenta'
    modalOpcionesMesa.value = false
    alert(`Mesa ${mesa.numero} marcada como 'Por Cobrar'. Ahora visible en Caja.`)
  } catch (err) {
    console.error('Error al solicitar la cuenta:', err)
    alert(err.response?.data?.detail || 'Error al solicitar la cuenta.')
  }
}

const getAlertaMesa = (mesaId) => {
  const ord = ordenesStore.ordenesActivas.find(o => o.mesa_id === mesaId && o.estado !== 'pagado' && o.estado !== 'cancelada')
  if (!ord) return null
  const tieneObservacion = ord.items?.some(i => i.estado === 'en_observacion')
  if (tieneObservacion) return { tipo: 'observacion', texto: '⚠️ Cocina' }
  const tieneListo = ord.items?.some(i => i.estado === 'listo')
  if (tieneListo) return { tipo: 'listo', texto: '✓ Listo' }
  return null
}

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

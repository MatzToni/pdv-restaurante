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
        <span 
          class="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-bold bg-amber-100 dark:bg-amber-950/60 text-amber-800 dark:text-amber-300 border border-amber-200 dark:border-amber-800/40"
          :title="esRolAlto ? 'Total de mesas ocupadas' : `Mis mesas ocupadas (${conteoOcupadas} de ${mesasStore.mesasOcupadas.length} en total)`"
        >
          <span class="w-2 h-2 rounded-full bg-amber-500"></span> {{ conteoOcupadas }} {{ esRolAlto ? 'Ocupadas' : 'Mis Ocupadas' }}
        </span>
        <span 
          class="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-bold bg-rose-100 dark:bg-rose-950/60 text-rose-800 dark:text-rose-300 border border-rose-200 dark:border-rose-800/40"
          :title="esRolAlto ? 'Total de mesas por cobrar' : `Mis mesas por cobrar (${conteoCuenta} de ${mesasStore.mesasCuenta.length} en total)`"
        >
          <span class="w-2 h-2 rounded-full bg-rose-500"></span> {{ conteoCuenta }} {{ esRolAlto ? 'Por Cobrar' : 'Mis Por Cobrar' }}
        </span>

        <!-- Botón crear mesa (solo roles de jefe para arriba) -->
        <button 
          v-if="esRolAlto"
          @click="modalNuevaMesa = true"
          class="px-3.5 py-1.5 bg-eden-600 hover:bg-eden-700 text-white rounded-xl text-xs font-bold shadow-sm transition active:scale-95 flex items-center gap-1.5"
        >
          <span>+</span> Nueva Mesa
        </button>
      </div>
    </div>

    <!-- Spinner de carga -->
    <div v-if="mesasStore.cargando" class="text-center py-16 text-slate-400">
      <div class="inline-block animate-spin rounded-full h-8 w-8 border-4 border-slate-200 dark:border-slate-800 border-t-eden-600 mb-2"></div>
      <p class="text-sm">Cargando mesas desde el servidor...</p>
    </div>

    <!-- Grid de Mesas -->
    <div v-else class="space-y-4">
      <!-- Selector / Filtro opcional si existen áreas -->
      <div v-if="mesasStore.areas && mesasStore.areas.length > 0" class="flex flex-wrap items-center gap-2">
        <button
          @click="filtroArea = 'todas'"
          :class="[
            'px-3 py-1.5 rounded-xl text-xs font-bold transition active:scale-95',
            filtroArea === 'todas'
              ? 'bg-eden-600 text-white shadow-xs'
              : 'bg-white dark:bg-slate-800 text-slate-600 dark:text-slate-300 border border-slate-200 dark:border-slate-700 hover:bg-slate-50'
          ]"
        >
          Todas ({{ mesasStore.mesas.length }})
        </button>
        <button
          v-for="area in mesasStore.areas"
          :key="area.id"
          @click="filtroArea = area.id"
          :class="[
            'px-3 py-1.5 rounded-xl text-xs font-bold transition active:scale-95',
            filtroArea === area.id
              ? 'bg-eden-600 text-white shadow-xs'
              : 'bg-white dark:bg-slate-800 text-slate-600 dark:text-slate-300 border border-slate-200 dark:border-slate-700 hover:bg-slate-50'
          ]"
        >
          {{ area.nombre }} ({{ mesasStore.mesas.filter(m => m.area_id === area.id).length }})
        </button>
      </div>

      <!-- Cuadrícula unificada de Mesas -->
      <div class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 xl:grid-cols-6 gap-3.5">
        <div 
          v-for="mesa in mesasFiltradas" 
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

          <div class="text-xs font-semibold my-1">
            <span 
              v-if="mesa.mesero_nombre" 
              class="inline-flex items-center gap-1 px-2 py-0.5 rounded-lg border truncate max-w-full"
              :class="mesa.mesero_id === authStore.usuarioActual?.id
                ? 'bg-eden-100 text-eden-800 dark:bg-eden-950/70 dark:text-eden-300 border-eden-300 dark:border-eden-800 font-bold'
                : 'text-slate-700 dark:text-slate-200 bg-slate-100 dark:bg-slate-800 border-slate-200/80 dark:border-slate-700/60'"
              :title="'Mesero: ' + mesa.mesero_nombre"
            >
              <span class="text-xs">🤵</span>
              <span class="truncate">{{ mesa.mesero_id === authStore.usuarioActual?.id ? 'Tú (' + mesa.mesero_nombre + ')' : mesa.mesero_nombre }}</span>
            </span>
            <span v-else class="text-slate-400 dark:text-slate-500 font-normal text-2xs italic">
              Sin mesero
            </span>
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
              placeholder="Ej. Mesa 1, Mesa 7, Barra 2" 
              class="w-full mt-1 p-2.5 border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-800 text-slate-800 dark:text-slate-100 rounded-xl text-sm font-semibold focus:outline-none focus:border-eden-600"
              @keyup.enter="guardarMesa"
              autofocus
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
            :disabled="!formMesa.numero?.trim()"
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
        <div class="flex justify-between items-center border-b border-slate-100 dark:border-slate-800 pb-3">
          <h3 class="text-xl font-black text-slate-800 dark:text-slate-100">{{ mesaSeleccionada.numero }}</h3>
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

        <!-- Información de Mesero Asignado / Tomar Mesa -->
        <div 
          class="p-3.5 rounded-2xl border transition-colors"
          :class="mesaSeleccionada.mesero_nombre
            ? 'bg-eden-50/70 dark:bg-eden-950/30 border-eden-200 dark:border-eden-800/60'
            : 'bg-slate-50 dark:bg-slate-800/60 border-slate-200/80 dark:border-slate-700/60'"
        >
          <div class="flex items-center justify-between">
            <div class="flex items-center gap-2.5">
              <div 
                class="w-9 h-9 rounded-xl flex items-center justify-center text-lg"
                :class="mesaSeleccionada.mesero_nombre ? 'bg-eden-100 dark:bg-eden-900/60' : 'bg-slate-200 dark:bg-slate-700'"
              >
                🤵
              </div>
              <div>
                <div 
                  class="text-3xs font-extrabold uppercase tracking-wider"
                  :class="mesaSeleccionada.mesero_nombre ? 'text-eden-800 dark:text-eden-300' : 'text-slate-400'"
                >
                  Mesero Asignado
                </div>
                <div class="text-sm font-bold text-slate-800 dark:text-slate-100">
                  {{ mesaSeleccionada.mesero_nombre || 'Sin mesero asignado' }}
                </div>
              </div>
            </div>

            <!-- Botón Tomar Mesa si no tiene o Desasignar si está libre o rol alto -->
            <button 
              v-if="!mesaSeleccionada.mesero_id"
              @click="tomarMesaAsignarAMi(mesaSeleccionada)"
              class="px-3.5 py-1.5 bg-eden-600 hover:bg-eden-700 text-white rounded-xl text-xs font-bold shadow-xs active:scale-95 transition flex items-center gap-1.5"
            >
              <span>👋</span> Tomar Mesa
            </button>
            <button 
              v-else-if="mesaSeleccionada.estado === 'libre' || esRolAlto"
              @click="desasignarMeseroMesa(mesaSeleccionada)"
              class="text-2xs font-bold text-rose-600 dark:text-rose-400 hover:underline px-2 py-1"
              title="Quitar mesero asignado"
            >
              Desasignar
            </button>
          </div>

          <!-- Selector de delegación: Exclusivo para Roles Altos (Admin, Gerente, Jefe) y solo meseros/auxiliares -->
          <div 
            v-if="esRolAlto && colaboradoresAtencion.length > 0" 
            class="mt-2.5 pt-2.5 border-t border-slate-200/60 dark:border-slate-700/60 flex items-center justify-between gap-2"
          >
            <span class="text-2xs text-slate-500 dark:text-slate-400 font-semibold shrink-0">Asignar a:</span>
            <select 
              :value="mesaSeleccionada.mesero_id || ''"
              @change="cambiarMeseroDirecto(mesaSeleccionada, $event.target.value)"
              class="text-xs font-bold bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 text-slate-700 dark:text-slate-200 rounded-lg px-2 py-1 focus:outline-none focus:border-eden-600"
            >
              <option value="">-- Sin asignar --</option>
              <option v-for="colab in colaboradoresAtencion" :key="colab.id" :value="colab.id">
                {{ colab.nombre }} ({{ colab.rol }})
              </option>
            </select>
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

          <!-- Si está ocupada: opción de pedir cuenta -->
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

          <!-- Botón explícito para Liberar Mesa si los comensales no pidieron nada o se retiraron -->
          <button 
            v-if="mesaSeleccionada.estado !== 'libre'"
            @click="liberarMesaSinConsumo(mesaSeleccionada)"
            class="w-full py-2.5 bg-slate-100 dark:bg-slate-800/80 hover:bg-rose-50 dark:hover:bg-rose-950/30 text-slate-700 dark:text-slate-200 hover:text-rose-700 dark:hover:text-rose-300 border border-slate-200 dark:border-slate-700 hover:border-rose-300 dark:hover:border-rose-800/60 rounded-xl font-bold text-xs transition active:scale-95 flex items-center justify-center gap-1.5 shadow-xs"
            title="Liberar mesa si los comensales se retiraron sin pedir nada"
          >
            <span>🪑</span> Liberar Mesa (Sin Consumo / Salieron)
          </button>

          <!-- Opción de editar mesa completa (solo roles de jefe para arriba) -->
          <button 
            v-if="esRolAlto"
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

    <!-- Modal para Editar Mesa Completa (sin requerir ubicación) -->
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
              @keyup.enter="guardarEdicionMesa"
            />
          </div>
        </div>

        <div class="flex gap-2 pt-2">
          <button 
            v-if="mesaSeleccionada?.estado === 'libre'"
            @click="confirmarEliminarMesa"
            class="px-3 py-2.5 bg-rose-50 dark:bg-rose-950/40 hover:bg-rose-100 text-rose-600 dark:text-rose-400 border border-rose-200 dark:border-rose-900 rounded-xl font-bold text-xs transition active:scale-95"
            title="Eliminar esta mesa definitivamente"
          >
            🗑️ Eliminar
          </button>
          <button 
            @click="modalEditarMesa = false" 
            class="flex-1 py-2.5 bg-slate-100 dark:bg-slate-800 hover:bg-slate-200 dark:hover:bg-slate-700 text-slate-700 dark:text-slate-300 rounded-xl font-bold text-sm transition"
          >
            Cancelar
          </button>
          <button 
            @click="guardarEdicionMesa" 
            :disabled="!formEditarMesa.numero?.trim()"
            class="flex-1 py-2.5 bg-eden-600 hover:bg-eden-700 disabled:opacity-50 text-white rounded-xl font-bold text-sm transition shadow-sm"
          >
            Guardar
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
const filtroArea = ref('todas')

const mesasFiltradas = computed(() => {
  if (filtroArea.value === 'todas') {
    return mesasStore.mesas
  }
  return mesasStore.mesas.filter(m => m.area_id === Number(filtroArea.value))
})

const esRolAlto = computed(() => {
  return ['administrador', 'gerente', 'jefe'].includes(authStore.rolActual)
})

const conteoOcupadas = computed(() => {
  if (esRolAlto.value) {
    return mesasStore.mesasOcupadas.length
  }
  return mesasStore.mesasOcupadas.filter(m => m.mesero_id === authStore.usuarioActual?.id).length
})

const conteoCuenta = computed(() => {
  if (esRolAlto.value) {
    return mesasStore.mesasCuenta.length
  }
  return mesasStore.mesasCuenta.filter(m => m.mesero_id === authStore.usuarioActual?.id).length
})

const colaboradoresAtencion = computed(() => {
  return authStore.usuarios.filter(u => 
    u.activo && 
    u.acceso_sistema && 
    ['mesero', 'auxiliar_general', 'administrador'].includes(u.rol)
  )
})

const formMesa = ref({
  numero: '',
  capacidad: 4,
  estado: 'libre'
})

const formEditarMesa = ref({
  id: null,
  numero: '',
  capacidad: 4
})

onMounted(() => {
  mesasStore.cargarMesas()
  ordenesStore.cargarOrdenesActivas()
  authStore.cargarUsuarios()
})

const abrirOpcionesMesa = (mesa) => {
  mesaSeleccionada.value = mesa
  modalOpcionesMesa.value = true
}

const abrirEditarMesa = (mesa) => {
  formEditarMesa.value = {
    id: mesa.id,
    numero: mesa.numero,
    capacidad: mesa.capacidad || 4
  }
  modalOpcionesMesa.value = false
  modalEditarMesa.value = true
}

const tomarMesaAsignarAMi = async (mesa) => {
  if (!authStore.usuarioActual?.id) {
    alert('Debes iniciar sesión para asignarte una mesa.')
    return
  }
  const rol = authStore.rolActual
  if (!['mesero', 'auxiliar_general', 'administrador'].includes(rol)) {
    alert('Solo los meseros y auxiliares generales pueden tener asignadas mesas para atender.')
    return
  }
  try {
    const data = await mesasStore.asignarMesero(mesa.id, authStore.usuarioActual.id)
    mesa.mesero_id = data.mesero_id
    mesa.mesero_nombre = data.mesero_nombre
    mesa.estado = data.estado
  } catch (err) {
    console.error('Error al asignarse la mesa:', err)
    alert(err.response?.data?.detail || 'Error al asignarse la mesa.')
  }
}

const liberarMesaSinConsumo = async (mesa) => {
  const ord = ordenesStore.ordenesActivas.find(
    o => o.mesa_id === mesa.id && o.estado !== 'pagado' && o.estado !== 'cancelada'
  )

  if (ord && ord.items && ord.items.length > 0) {
    const confirmar = confirm(`La ${mesa.numero} tiene productos registrados (#${ord.id}). ¿Deseas liberar la mesa porque los clientes se retiraron sin consumir?`)
    if (!confirmar) return
    try {
      await ordenesStore.cancelarOrden(ord.id, 'Clientes se retiraron sin consumir', false)
    } catch (err) {
      console.warn('Error cancelando orden activa:', err)
    }
  } else if (ord) {
    try {
      await ordenesStore.cancelarOrden(ord.id, 'Liberada sin consumo', false)
    } catch (err) {
      console.warn('Error cancelando orden vacía:', err)
    }
  }

  try {
    await mesasStore.cambiarEstadoMesa(mesa.id, 'libre')
    await mesasStore.asignarMesero(mesa.id, null)
    mesa.estado = 'libre'
    mesa.mesero_id = null
    mesa.mesero_nombre = null
    modalOpcionesMesa.value = false
    alert(`Mesa ${mesa.numero} liberada exitosamente.`)
  } catch (err) {
    console.error('Error al liberar la mesa:', err)
    alert(err.response?.data?.detail || 'Error al liberar la mesa.')
  }
}

const desasignarMeseroMesa = async (mesa) => {
  try {
    const data = await mesasStore.asignarMesero(mesa.id, null)
    mesa.mesero_id = null
    mesa.mesero_nombre = null
  } catch (err) {
    console.error('Error al desasignar mesero:', err)
    alert(err.response?.data?.detail || 'Error al desasignar mesero.')
  }
}

const cambiarMeseroDirecto = async (mesa, nuevoId) => {
  const meseroId = nuevoId ? Number(nuevoId) : null
  try {
    const data = await mesasStore.asignarMesero(mesa.id, meseroId)
    mesa.mesero_id = data.mesero_id
    mesa.mesero_nombre = data.mesero_nombre
    mesa.estado = data.estado
  } catch (err) {
    console.error('Error al cambiar mesero:', err)
    alert(err.response?.data?.detail || 'Error al cambiar mesero.')
  }
}

const guardarMesa = async () => {
  if (!formMesa.value.numero?.trim()) return
  try {
    await mesasStore.crearMesa({
      numero: formMesa.value.numero.trim(),
      capacidad: 4,
      estado: 'libre'
    })
    modalNuevaMesa.value = false
    formMesa.value = { numero: '', capacidad: 4, estado: 'libre' }
  } catch (err) {
    console.error('Error al crear mesa:', err)
    alert(err.response?.data?.detail || 'Error al crear la mesa.')
  }
}

const guardarEdicionMesa = async () => {
  if (!formEditarMesa.value.numero?.trim()) return
  try {
    const data = await mesasStore.actualizarMesa(formEditarMesa.value.id, {
      numero: formEditarMesa.value.numero.trim()
    })
    modalEditarMesa.value = false
    if (mesaSeleccionada.value && mesaSeleccionada.value.id === data.id) {
      mesaSeleccionada.value.numero = data.numero
    }
  } catch (err) {
    console.error('Error al actualizar mesa:', err)
    alert(err.response?.data?.detail || 'Error al actualizar la mesa.')
  }
}

const confirmarEliminarMesa = async () => {
  if (!confirm(`¿Deseas eliminar la mesa "${formEditarMesa.value.numero}"?`)) return
  try {
    await mesasStore.eliminarMesa(formEditarMesa.value.id)
    modalEditarMesa.value = false
    modalOpcionesMesa.value = false
    mesaSeleccionada.value = null
  } catch (err) {
    console.error('Error al eliminar mesa:', err)
    alert(err.response?.data?.detail || 'Error al eliminar la mesa.')
  }
}

const cambiarEstadoMesa = async (mesa, nuevoEstado) => {
  try {
    if (nuevoEstado === 'ocupada' && !mesa.mesero_id && authStore.usuarioActual?.id) {
      await mesasStore.asignarMesero(mesa.id, authStore.usuarioActual.id)
      mesa.mesero_id = authStore.usuarioActual.id
      mesa.mesero_nombre = authStore.usuarioActual.nombre
    } else {
      await mesasStore.cambiarEstadoMesa(mesa.id, nuevoEstado)
    }
    mesa.estado = nuevoEstado
    if (nuevoEstado === 'libre') {
      mesa.mesero_id = null
      mesa.mesero_nombre = null
    }
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

const abrirComandero = async (mesa) => {
  const rol = authStore.rolActual
  if (!mesa.mesero_id && authStore.usuarioActual?.id && ['mesero', 'auxiliar_general', 'administrador'].includes(rol)) {
    try {
      const data = await mesasStore.asignarMesero(mesa.id, authStore.usuarioActual.id)
      mesa.mesero_id = data.mesero_id
      mesa.mesero_nombre = data.mesero_nombre
    } catch (err) {
      console.warn('No se pudo pre-asignar mesero:', err)
    }
  }
  router.push({
    path: '/pos',
    query: { mesaId: mesa.id, mesaNumero: mesa.numero }
  })
}
</script>

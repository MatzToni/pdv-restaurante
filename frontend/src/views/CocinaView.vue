<template>
  <div class="space-y-4">
    <!-- Header KDS -->
    <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 bg-white dark:bg-slate-900 p-5 rounded-2xl border border-slate-200 dark:border-slate-800 shadow-sm transition-colors">
      <div>
        <h1 class="text-2xl font-black text-slate-800 dark:text-slate-100 tracking-tight">Pantalla de Cocina y Barra (KDS)</h1>
        <p class="text-slate-500 dark:text-slate-400 text-sm">Comandas activas, control de preparación y reporte de incidencias</p>
      </div>

      <div class="flex items-center gap-3">
        <button 
          @click="ordenesStore.cargarOrdenesActivas()"
          class="px-3.5 py-1.5 bg-slate-100 dark:bg-slate-800 hover:bg-slate-200 dark:hover:bg-slate-700 text-slate-700 dark:text-slate-200 rounded-xl text-xs font-bold transition active:scale-95 flex items-center gap-1.5 border border-slate-200 dark:border-slate-700"
        >
          <span>🔄</span> Actualizar
        </button>

        <span class="inline-flex items-center gap-2 px-3 py-1.5 rounded-xl bg-amber-50 dark:bg-amber-950/60 text-amber-800 dark:text-amber-300 text-xs font-bold border border-amber-200 dark:border-amber-800/40">
          <span class="w-2 h-2 rounded-full bg-amber-500 animate-pulse"></span>
          {{ comandasActivas.length }} Comandas Activas
        </span>
      </div>
    </div>

    <!-- Si no hay órdenes -->
    <div v-if="comandasActivas.length === 0" class="text-center py-20 bg-white dark:bg-slate-900 rounded-3xl border border-slate-200 dark:border-slate-800 text-slate-400 dark:text-slate-500">
      <span class="text-5xl block mb-3">👨‍🍳</span>
      <h3 class="text-lg font-bold text-slate-700 dark:text-slate-300">Cocina al día</h3>
      <p class="text-sm text-slate-400 dark:text-slate-500 mt-1">No hay órdenes pendientes en este momento</p>
    </div>

    <!-- Grid de Comandas KDS -->
    <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
      <div 
        v-for="orden in comandasActivas" 
        :key="orden.id"
        class="bg-white dark:bg-slate-900 rounded-2xl border-2 border-slate-200 dark:border-slate-800 overflow-hidden shadow-sm flex flex-col justify-between transition-colors"
      >
        <div>
          <!-- Cabecera de la comanda -->
          <div class="p-3.5 bg-slate-900 dark:bg-slate-800 text-white font-bold flex justify-between items-center border-b border-slate-800 dark:border-slate-700">
            <div>
              <span class="text-lg font-black">{{ orden.mesa_numero || `Mesa #${orden.mesa_id}` }}</span>
              <span class="text-xs text-slate-400 block font-normal">Orden #{{ orden.id }} · {{ orden.mesero_nombre || 'Mesero' }}</span>
            </div>
            <div class="text-right">
              <span class="text-xs bg-slate-800 dark:bg-slate-700 text-slate-300 px-2 py-0.5 rounded-md font-mono">
                {{ formatHora(orden.fecha_apertura) }}
              </span>
              <span class="block text-3xs font-extrabold uppercase mt-1" :class="semaforoTiempoColor(orden.fecha_apertura)">
                ⏱️ {{ minutosTranscurridos(orden.fecha_apertura) }} min
              </span>
            </div>
          </div>

          <!-- Notas generales de la comanda -->
          <div v-if="orden.notas" class="bg-amber-50 dark:bg-amber-950/40 px-3.5 py-1.5 text-xs text-amber-800 dark:text-amber-300 font-semibold border-b border-amber-100 dark:border-amber-900/40 flex items-center gap-1.5">
            <span>📝</span> {{ orden.notas }}
          </div>

          <!-- Items de la comanda -->
          <div class="p-3 space-y-2.5">
            <div 
              v-for="item in orden.items" 
              :key="item.id"
              :class="[
                'p-2.5 rounded-xl border transition-all flex flex-col gap-1',
                item.estado === 'cancelado' ? 'bg-rose-50 dark:bg-rose-950/30 border-rose-200 dark:border-rose-900/50 opacity-60' :
                item.estado === 'en_observacion' ? 'bg-amber-500/15 border-amber-500 dark:border-amber-400 animate-pulse' :
                item.estado === 'listo' ? 'bg-emerald-50 dark:bg-emerald-950/30 border-emerald-300 dark:border-emerald-800/60' :
                item.estado === 'entregado' ? 'bg-purple-50 dark:bg-purple-950/30 border-purple-200 dark:border-purple-800/60' :
                item.estado === 'preparando' ? 'bg-amber-50 dark:bg-amber-950/30 border-amber-300 dark:border-amber-800/60' :
                'bg-slate-50 dark:bg-slate-800/60 border-slate-200 dark:border-slate-700/60'
              ]"
            >
              <div class="flex justify-between items-start">
                <div class="flex items-start gap-2 flex-1">
                  <span class="font-black text-slate-900 dark:text-slate-100 bg-white dark:bg-slate-700 border border-slate-200 dark:border-slate-600 px-2 py-0.5 rounded text-xs shadow-2xs">
                    {{ item.cantidad }}x
                  </span>
                  <div class="flex-1">
                    <span class="font-bold text-slate-800 dark:text-slate-100 text-sm block leading-snug">
                      {{ item.producto_nombre }}
                    </span>

                    <!-- Desglose de extras resaltados para cocina -->
                    <div v-if="item.extras && item.extras.length > 0" class="flex flex-wrap gap-1 mt-1">
                      <span 
                        v-for="(ex, ei) in item.extras" 
                        :key="ei"
                        class="text-3xs font-extrabold bg-eden-100 dark:bg-eden-950 text-eden-800 dark:text-eden-300 px-1.5 py-0.5 rounded border border-eden-300 dark:border-eden-800"
                      >
                        + {{ ex.nombre }}
                      </span>
                    </div>

                    <!-- Nota del mesero -->
                    <span v-if="item.notas" class="text-xs text-amber-700 dark:text-amber-400 font-semibold italic block mt-0.5">
                      📝 {{ item.notas }}
                    </span>

                    <!-- Alerta de observación activa -->
                    <div v-if="item.estado === 'en_observacion'" class="mt-1 p-1.5 rounded-lg bg-amber-500/20 text-amber-900 dark:text-amber-200 text-xs font-bold border border-amber-400/50">
                      ⚠️ En espera del mesero: "{{ item.observacion_cocina }}"
                    </div>

                    <!-- Si son múltiples platillos iguales: opción para preparar 1 y descartar otro o separarlos -->
                    <div v-if="item.cantidad > 1 && item.estado !== 'cancelado'" class="flex items-center gap-1.5 py-1 px-2 mt-1 bg-slate-100 dark:bg-slate-800 rounded-lg text-3xs font-bold text-slate-600 dark:text-slate-300">
                      <span>Múltiples ({{ item.cantidad }}x):</span>
                      <button 
                        @click="separarPorcion(item)"
                        title="Separar en porciones individuales para controlar cada una"
                        class="px-2 py-0.5 bg-white dark:bg-slate-700 hover:bg-slate-200 border border-slate-300 dark:border-slate-600 rounded text-slate-800 dark:text-slate-100 transition active:scale-95"
                      >
                        ✂️ Separar
                      </button>
                      <button 
                        @click="abrirModalDescartarUnidad(item)"
                        title="Descartar 1 porción y preparar la(s) restante(s)"
                        class="px-2 py-0.5 bg-rose-50 dark:bg-rose-950/60 hover:bg-rose-100 text-rose-700 dark:text-rose-300 border border-rose-300 dark:border-rose-800 rounded transition active:scale-95"
                      >
                        ✕ Descartar 1
                      </button>
                    </div>

                    <span v-if="item.estado === 'cancelado'" class="text-xs text-rose-600 dark:text-rose-400 font-bold block mt-0.5">
                      Cancelado: {{ item.motivo_cancelacion }}
                    </span>
                  </div>
                </div>

                <!-- Botón Cancelar Platillo con PIN -->
                <button 
                  v-if="item.estado !== 'cancelado'"
                  @click="abrirModalCancelar(item)"
                  title="Cancelar platillo con PIN"
                  class="text-xs text-slate-400 hover:text-rose-600 font-bold px-1.5 py-0.5 hover:bg-rose-100 dark:hover:bg-rose-900/40 rounded transition"
                >
                  ✕
                </button>
              </div>

              <!-- Acciones de Estado del Platillo -->
              <div v-if="item.estado !== 'cancelado'" class="flex gap-1.5 pt-1.5 mt-1 border-t border-slate-200/50 dark:border-slate-700/50">
                <button 
                  v-if="item.estado === 'pendiente'"
                  @click="cambiarEstadoItem(item.id, 'preparando')"
                  class="flex-1 py-1.5 text-xs font-bold rounded-lg bg-amber-500 hover:bg-amber-600 text-white transition active:scale-95 shadow-2xs"
                >
                  👨‍🍳 Preparar
                </button>

                <button 
                  v-if="item.estado === 'preparando'"
                  @click="cambiarEstadoItem(item.id, 'listo')"
                  class="flex-1 py-1.5 text-xs font-bold rounded-lg bg-emerald-600 hover:bg-emerald-700 text-white transition active:scale-95 shadow-2xs"
                >
                  ✓ Listo
                </button>

                <!-- Botón Reportar Incidencia / Falta Ingrediente -->
                <button 
                  v-if="['pendiente', 'preparando'].includes(item.estado)"
                  @click="abrirModalIncidencia(item)"
                  title="Reportar falta de ingrediente o aclaración al mesero"
                  class="px-2 py-1.5 text-xs font-bold rounded-lg bg-amber-100 dark:bg-amber-950/60 hover:bg-amber-200 text-amber-800 dark:text-amber-300 border border-amber-300 dark:border-amber-800 transition active:scale-95 flex items-center gap-1"
                >
                  <span>⚠️</span> Aclarar
                </button>

                <span 
                  v-if="item.estado === 'en_observacion'"
                  class="text-xs font-black text-amber-600 dark:text-amber-400 flex items-center gap-1 mx-auto py-1"
                >
                  ⏳ Esperando al mesero...
                </span>

                <button 
                  v-if="item.estado === 'listo'"
                  @click="cambiarEstadoItem(item.id, 'entregado')"
                  class="flex-1 py-1.5 text-xs font-bold rounded-lg bg-purple-600 hover:bg-purple-700 text-white transition active:scale-95 shadow-2xs flex items-center justify-center gap-1"
                >
                  <span>🍽️</span> Servido / Entregado
                </button>

                <span 
                  v-if="item.estado === 'entregado'"
                  class="text-xs font-black text-purple-700 dark:text-purple-300 flex items-center gap-1 mx-auto py-1"
                >
                  ✓ Servido en Mesa
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- MODAL REPORTAR INCIDENCIA / FALTA DE INGREDIENTE -->
    <div v-if="modalIncidencia && itemIncidencia" class="fixed inset-0 bg-slate-900/60 backdrop-blur-sm flex items-center justify-center p-4 z-50">
      <div class="bg-white dark:bg-slate-900 rounded-3xl p-6 max-w-sm w-full shadow-2xl border border-slate-200 dark:border-slate-800 space-y-4">
        <div class="flex items-center gap-2 text-amber-600 dark:text-amber-400">
          <span class="text-2xl">⚠️</span>
          <h3 class="text-lg font-black text-slate-800 dark:text-slate-100">Reportar Incidencia</h3>
        </div>

        <p class="text-xs text-slate-500 dark:text-slate-400">
          Esta notificación pausará el platillo y alertará inmediatamente al mesero de la mesa para consultar con el cliente.
        </p>

        <div class="p-2.5 rounded-xl bg-slate-50 dark:bg-slate-800 border border-slate-200 dark:border-slate-700 text-xs font-bold text-slate-800 dark:text-slate-100">
          Platillo: {{ itemIncidencia.producto_nombre }}
        </div>

        <!-- Motivos predefinidos rápidos -->
        <div class="space-y-1.5">
          <label class="text-2xs font-extrabold uppercase text-slate-400">Motivos rápidos</label>
          <div class="flex flex-wrap gap-1.5">
            <button 
              v-for="motivo in motivosPredefinidos" 
              :key="motivo"
              type="button"
              @click="textoIncidencia = motivo"
              class="px-2.5 py-1 text-2xs font-bold rounded-lg border border-slate-200 dark:border-slate-700 hover:bg-slate-100 dark:hover:bg-slate-800 text-slate-700 dark:text-slate-300 transition"
            >
              {{ motivo }}
            </button>
          </div>
        </div>

        <div>
          <label class="text-xs font-bold text-slate-700 dark:text-slate-300">Detalle / Pregunta al mesero:</label>
          <textarea 
            v-model="textoIncidencia"
            rows="3"
            placeholder="Ej. Se agotó el aguacate, ¿cambiar por pollo o cancelar?"
            class="w-full mt-1 p-2.5 text-xs font-semibold border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-800 text-slate-800 dark:text-slate-100 rounded-xl focus:outline-none focus:border-amber-500 resize-none"
          ></textarea>
        </div>

        <div class="flex justify-end gap-2 pt-2">
          <button 
            @click="modalIncidencia = false"
            class="px-4 py-2 text-xs font-bold text-slate-600 dark:text-slate-300 hover:bg-slate-100 rounded-xl"
          >
            Cancelar
          </button>
          <button 
            @click="confirmarIncidencia"
            :disabled="!textoIncidencia.trim()"
            class="px-5 py-2 text-xs font-bold bg-amber-500 hover:bg-amber-600 disabled:opacity-50 text-white rounded-xl shadow-sm transition active:scale-95"
          >
            ⚠️ Enviar Alerta al Mesero
          </button>
        </div>
      </div>
    </div>

    <!-- MODAL DESCARTAR 1 PORCIÓN DE PLATILLOS MÚLTIPLES -->
    <div v-if="modalDescartarUnidad && itemDescartar" class="fixed inset-0 bg-slate-900/60 backdrop-blur-sm flex items-center justify-center p-4 z-50">
      <div class="bg-white dark:bg-slate-900 rounded-3xl p-6 max-w-sm w-full shadow-2xl border border-slate-200 dark:border-slate-800 space-y-4">
        <div class="flex items-center gap-2 text-rose-600 dark:text-rose-400">
          <span class="text-2xl">🍽️</span>
          <h3 class="text-lg font-black text-slate-800 dark:text-slate-100">Descartar 1 Porción</h3>
        </div>

        <p class="text-xs text-slate-500 dark:text-slate-400">
          Esta acción descartará 1 porción de <strong>{{ itemDescartar.producto_nombre }}</strong> (quedarán {{ itemDescartar.cantidad - 1 }} por preparar). El importe de 1 porción se descontará automáticamente de la cuenta de la mesa.
        </p>

        <div class="space-y-3">
          <div>
            <label class="text-xs font-bold text-slate-700 dark:text-slate-300">Motivo de descarte</label>
            <input 
              v-model="formDescartar.motivo" 
              type="text" 
              placeholder="Ej. Insumo suficiente solo para 1 platillo" 
              class="w-full mt-1 p-2.5 text-xs font-semibold border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-800 text-slate-800 dark:text-slate-100 rounded-xl focus:outline-none focus:border-rose-500"
            />
          </div>

          <label class="flex items-center gap-2 p-2.5 rounded-xl bg-slate-50 dark:bg-slate-800 border border-slate-200 dark:border-slate-700 cursor-pointer">
            <input 
              v-model="formDescartar.genera_merma" 
              type="checkbox" 
              class="rounded text-rose-600 focus:ring-rose-500 w-4 h-4"
            />
            <span class="text-xs font-bold text-slate-700 dark:text-slate-300">
              ¿Genera Merma? (El insumo se desperdició)
            </span>
          </label>
        </div>

        <div class="flex justify-end gap-2 pt-2">
          <button 
            @click="modalDescartarUnidad = false"
            class="px-4 py-2 text-xs font-bold text-slate-600 dark:text-slate-300 hover:bg-slate-100 dark:hover:bg-slate-800 rounded-xl"
          >
            Volver
          </button>
          <button 
            @click="confirmarDescartarUnidad"
            class="px-5 py-2 text-xs font-bold bg-rose-600 hover:bg-rose-700 text-white rounded-xl shadow-sm transition active:scale-95"
          >
            Confirmar Descarte
          </button>
        </div>
      </div>
    </div>

    <!-- Modal Cancelar Platillo con PIN y Merma -->
    <div v-if="modalCancelar" class="fixed inset-0 bg-slate-900/60 backdrop-blur-sm flex items-center justify-center p-4 z-50">
      <div class="bg-white dark:bg-slate-900 rounded-3xl p-6 max-w-sm w-full shadow-2xl border border-slate-200 dark:border-slate-800 space-y-4">
        <div class="flex items-center gap-2 text-rose-600 dark:text-rose-400">
          <span class="text-2xl">⚠️</span>
          <h3 class="text-lg font-black text-slate-800 dark:text-slate-100">Cancelar Platillo</h3>
        </div>

        <p class="text-xs text-slate-500 dark:text-slate-400">
          Se requiere autorización de Gerente o Jefe de turno para cancelar este platillo.
        </p>

        <div class="space-y-3">
          <div>
            <label class="text-xs font-bold text-slate-700 dark:text-slate-300">PIN de Autorización (4 dígitos)</label>
            <input 
              v-model="formCancelar.pin" 
              type="password" 
              maxlength="10"
              placeholder="••••" 
              class="w-full mt-1 p-2.5 text-center text-lg tracking-widest font-mono border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-800 text-slate-800 dark:text-slate-100 rounded-xl focus:outline-none focus:border-rose-500"
            />
          </div>

          <div>
            <label class="text-xs font-bold text-slate-700 dark:text-slate-300">Motivo de Cancelación</label>
            <input 
              v-model="formCancelar.motivo" 
              type="text" 
              placeholder="Ej. Platillo frío, cliente cambió de opinión" 
              class="w-full mt-1 p-2.5 text-xs font-semibold border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-800 text-slate-800 dark:text-slate-100 rounded-xl focus:outline-none focus:border-rose-500"
            />
          </div>

          <label class="flex items-center gap-2 p-2.5 rounded-xl bg-slate-50 dark:bg-slate-800 border border-slate-200 dark:border-slate-700 cursor-pointer">
            <input 
              v-model="formCancelar.genera_merma" 
              type="checkbox" 
              class="rounded text-rose-600 focus:ring-rose-500 w-4 h-4"
            />
            <span class="text-xs font-bold text-slate-700 dark:text-slate-300">
              ¿Genera Merma? (El platillo ya se preparó)
            </span>
          </label>
        </div>

        <div class="flex justify-end gap-2 pt-2">
          <button 
            @click="modalCancelar = false"
            class="px-4 py-2 text-xs font-bold text-slate-600 dark:text-slate-300 hover:bg-slate-100 dark:hover:bg-slate-800 rounded-xl"
          >
            Volver
          </button>
          <button 
            @click="confirmarCancelacion"
            :disabled="!formCancelar.pin || !formCancelar.motivo"
            class="px-5 py-2 text-xs font-bold bg-rose-600 hover:bg-rose-700 disabled:opacity-50 text-white rounded-xl shadow-sm transition active:scale-95"
          >
            Confirmar Cancelación
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useOrdenesStore } from '../stores/ordenes'

const ordenesStore = useOrdenesStore()
let timer = null

// Modal Incidencia / Falta de ingrediente
const modalIncidencia = ref(false)
const itemIncidencia = ref(null)
const textoIncidencia = ref('')

const motivosPredefinidos = [
  'Se agotó un ingrediente',
  'Aclaración de término',
  'Duda de salsas / aderezos',
  'Platillo demorado'
]

// Modal Cancelación
const modalCancelar = ref(false)
const itemSeleccionado = ref(null)
const formCancelar = ref({
  pin: '',
  motivo: '',
  genera_merma: false
})

// Modal Descartar 1 Porción
const modalDescartarUnidad = ref(false)
const itemDescartar = ref(null)
const formDescartar = ref({
  motivo: 'Insumo suficiente solo para 1 platillo',
  genera_merma: false
})

onMounted(() => {
  ordenesStore.cargarOrdenesActivas()
  timer = setInterval(() => {
    ordenesStore.cargarOrdenesActivas()
  }, 10000)
})

onUnmounted(() => {
  if (timer) clearInterval(timer)
})

const comandasActivas = computed(() => {
  return ordenesStore.ordenesActivas.filter(o => o.estado !== 'pagado' && o.estado !== 'cancelada')
})

const cambiarEstadoItem = async (itemId, nuevoEstado) => {
  try {
    await ordenesStore.cambiarEstadoItem(itemId, nuevoEstado)
  } catch (err) {
    alert('Error al actualizar el estado del platillo.')
  }
}

const abrirModalIncidencia = (item) => {
  itemIncidencia.value = item
  textoIncidencia.value = ''
  modalIncidencia.value = true
}

const confirmarIncidencia = async () => {
  if (!itemIncidencia.value || !textoIncidencia.value.trim()) return
  try {
    await ordenesStore.reportarObservacionItem(itemIncidencia.value.id, textoIncidencia.value.trim())
    modalIncidencia.value = false
    alert('Alerta enviada al mesero.')
  } catch (err) {
    alert('Error al enviar la incidencia.')
  }
}

const abrirModalCancelar = (item) => {
  itemSeleccionado.value = item
  formCancelar.value = { pin: '', motivo: '', genera_merma: item.estado === 'listo' }
  modalCancelar.value = true
}

const confirmarCancelacion = async () => {
  try {
    await ordenesStore.cancelarItem(itemSeleccionado.value.id, {
      pin_autorizacion: formCancelar.value.pin,
      motivo: formCancelar.value.motivo,
      genera_merma: formCancelar.value.genera_merma
    })
    modalCancelar.value = false
    alert('Platillo cancelado correctamente.')
  } catch (err) {
    alert(err.response?.data?.detail || 'Error al autorizar cancelación.')
  }
}

const separarPorcion = async (item) => {
  try {
    await ordenesStore.separarItem(item.id)
    alert(`Porciones de ${item.producto_nombre} separadas exitosamente en cocina.`)
  } catch (err) {
    alert('Error al separar porciones.')
  }
}

const abrirModalDescartarUnidad = (item) => {
  itemDescartar.value = item
  formDescartar.value = { motivo: 'Insumo suficiente solo para 1 platillo', genera_merma: false }
  modalDescartarUnidad.value = true
}

const confirmarDescartarUnidad = async () => {
  if (!itemDescartar.value) return
  try {
    await ordenesStore.descartarUnidadItem(itemDescartar.value.id, {
      motivo: formDescartar.value.motivo,
      genera_merma: formDescartar.value.genera_merma
    })
    modalDescartarUnidad.value = false
    alert(`Se descartó 1 porción de "${itemDescartar.value.producto_nombre}". La comanda y la cuenta fueron ajustadas.`)
  } catch (err) {
    alert('Error al descartar la porción.')
  }
}

const formatHora = (fechaIso) => {
  if (!fechaIso) return ''
  const d = new Date(fechaIso)
  return d.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
}

const minutosTranscurridos = (fechaIso) => {
  if (!fechaIso) return 0
  const difMs = Date.now() - new Date(fechaIso).getTime()
  return Math.max(0, Math.floor(difMs / 60000))
}

const semaforoTiempoColor = (fechaIso) => {
  const min = minutosTranscurridos(fechaIso)
  if (min >= 20) return 'text-rose-400'
  if (min >= 10) return 'text-amber-400'
  return 'text-emerald-400'
}
</script>

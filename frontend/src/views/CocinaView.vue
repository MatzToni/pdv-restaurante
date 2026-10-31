<template>
  <div class="space-y-4">
    <!-- Header KDS -->
    <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 bg-white dark:bg-slate-900 p-5 rounded-2xl border border-slate-200 dark:border-slate-800 shadow-sm transition-colors">
      <div>
        <h1 class="text-2xl font-black text-slate-800 dark:text-slate-100 tracking-tight">Pantalla de Cocina (KDS)</h1>
        <p class="text-slate-500 dark:text-slate-400 text-sm">Comandas activas en preparación y control de platillos</p>
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
          {{ ordenesStore.ordenesActivas.length }} Comandas Activas
        </span>
      </div>
    </div>

    <!-- Si no hay órdenes -->
    <div v-if="ordenesStore.ordenesActivas.length === 0" class="text-center py-20 bg-white dark:bg-slate-900 rounded-3xl border border-slate-200 dark:border-slate-800 text-slate-400 dark:text-slate-500">
      <span class="text-5xl block mb-3">👨‍🍳</span>
      <h3 class="text-lg font-bold text-slate-700 dark:text-slate-300">Cocina al día</h3>
      <p class="text-sm text-slate-400 dark:text-slate-500 mt-1">No hay órdenes pendientes en este momento</p>
    </div>

    <!-- Grid de Comandas KDS -->
    <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
      <div 
        v-for="orden in ordenesStore.ordenesActivas" 
        :key="orden.id"
        class="bg-white dark:bg-slate-900 rounded-2xl border-2 border-slate-200 dark:border-slate-800 overflow-hidden shadow-sm flex flex-col justify-between transition-colors"
      >
        <div>
          <!-- Cabecera de la comanda -->
          <div class="p-3.5 bg-slate-900 dark:bg-slate-800 text-white font-bold flex justify-between items-center border-b border-slate-800 dark:border-slate-700">
            <div>
              <span class="text-lg font-black">Mesa #{{ orden.mesa_id }}</span>
              <span class="text-xs text-slate-400 block font-normal">Orden #{{ orden.id }}</span>
            </div>
            <div class="text-right">
              <span class="text-xs bg-slate-800 dark:bg-slate-700 text-slate-300 px-2 py-0.5 rounded-md font-mono">
                {{ formatHora(orden.fecha_apertura) }}
              </span>
            </div>
          </div>

          <!-- Notas generales de la comanda -->
          <div v-if="orden.notas" class="bg-amber-50 dark:bg-amber-950/40 px-3.5 py-1.5 text-xs text-amber-800 dark:text-amber-300 font-semibold border-b border-amber-100 dark:border-amber-900/40 flex items-center gap-1.5">
            <span>📝</span> {{ orden.notas }}
          </div>

          <!-- Items de la comanda -->
          <div class="p-4 space-y-3">
            <div 
              v-for="item in orden.items" 
              :key="item.id"
              :class="[
                'p-2.5 rounded-xl border transition-all flex flex-col gap-1',
                item.estado === 'cancelado' ? 'bg-rose-50 dark:bg-rose-950/30 border-rose-200 dark:border-rose-900/50 opacity-60' :
                item.estado === 'listo' ? 'bg-emerald-50 dark:bg-emerald-950/30 border-emerald-300 dark:border-emerald-800/60' :
                item.estado === 'preparando' ? 'bg-amber-50 dark:bg-amber-950/30 border-amber-300 dark:border-amber-800/60' :
                'bg-slate-50 dark:bg-slate-800/60 border-slate-200 dark:border-slate-700/60'
              ]"
            >
              <div class="flex justify-between items-start">
                <div class="flex items-start gap-2">
                  <span class="font-black text-slate-900 dark:text-slate-100 bg-white dark:bg-slate-700 border border-slate-200 dark:border-slate-600 px-2 py-0.5 rounded text-xs shadow-2xs">
                    {{ item.cantidad }}x
                  </span>
                  <div>
                    <span class="font-bold text-slate-800 dark:text-slate-100 text-sm block leading-snug">
                      Platillo #{{ item.producto_id }}
                    </span>
                    <span v-if="item.notas" class="text-xs text-amber-700 dark:text-amber-400 font-semibold italic">
                      {{ item.notas }}
                    </span>
                    <span v-if="item.estado === 'cancelado'" class="text-xs text-rose-600 dark:text-rose-400 font-bold block">
                      Cancelado: {{ item.motivo_cancelacion }}
                    </span>
                  </div>
                </div>

                <!-- Botón Cancelar Platillo (si no está cancelado) -->
                <button 
                  v-if="item.estado !== 'cancelado'"
                  @click="abrirModalCancelar(item)"
                  title="Cancelar o rechazar platillo"
                  class="text-xs text-rose-400 hover:text-rose-600 font-bold px-1.5 py-0.5 hover:bg-rose-100 dark:hover:bg-rose-900/40 rounded transition"
                >
                  ✕
                </button>
              </div>

              <!-- Acciones de Estado del Platillo -->
              <div v-if="item.estado !== 'cancelado'" class="flex gap-1.5 pt-1 mt-1 border-t border-slate-200/50 dark:border-slate-700/50">
                <button 
                  v-if="item.estado === 'pendiente'"
                  @click="cambiarEstadoItem(item.id, 'preparando')"
                  class="flex-1 py-1 text-xs font-bold rounded-lg bg-amber-500 hover:bg-amber-600 text-white transition active:scale-95"
                >
                  👨‍🍳 Preparar
                </button>
                <button 
                  v-if="item.estado === 'preparando'"
                  @click="cambiarEstadoItem(item.id, 'listo')"
                  class="flex-1 py-1 text-xs font-bold rounded-lg bg-emerald-600 hover:bg-emerald-700 text-white transition active:scale-95"
                >
                  ✓ Listo
                </button>
                <span 
                  v-if="item.estado === 'listo'"
                  class="text-xs font-black text-emerald-700 dark:text-emerald-400 flex items-center gap-1 mx-auto"
                >
                  ✓ Listo para entrega
                </span>
              </div>
            </div>
          </div>
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

          <!-- Genera Merma Checkbox -->
          <label class="flex items-start gap-2.5 p-3 rounded-xl bg-slate-50 dark:bg-slate-800/60 border border-slate-200 dark:border-slate-700 cursor-pointer">
            <input 
              v-model="formCancelar.genera_merma" 
              type="checkbox" 
              class="mt-0.5 rounded text-rose-600 focus:ring-rose-500"
            />
            <div class="text-xs">
              <span class="font-bold text-slate-800 dark:text-slate-200 block">¿Genera merma / desperdicio?</span>
              <span class="text-slate-500 dark:text-slate-400 block">Marca esta casilla si la comida ya había comenzado a cocinarse.</span>
            </div>
          </label>
        </div>

        <div class="flex gap-2 pt-2">
          <button 
            @click="modalCancelar = false" 
            class="flex-1 py-2.5 bg-slate-100 dark:bg-slate-800 hover:bg-slate-200 dark:hover:bg-slate-700 text-slate-700 dark:text-slate-300 rounded-xl font-bold text-xs transition"
          >
            Atrás
          </button>
          <button 
            @click="ejecutarCancelacion" 
            :disabled="!formCancelar.pin || !formCancelar.motivo"
            class="flex-1 py-2.5 bg-rose-600 hover:bg-rose-700 disabled:opacity-50 text-white rounded-xl font-bold text-xs transition shadow-sm"
          >
            Confirmar Cancelación
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useOrdenesStore } from '../stores/ordenes'

const ordenesStore = useOrdenesStore()

const modalCancelar = ref(false)
const itemSeleccionado = ref(null)
const formCancelar = ref({
  pin: '',
  motivo: '',
  genera_merma: false
})

onMounted(() => {
  ordenesStore.cargarOrdenesActivas()
})

const formatHora = (fechaIso) => {
  if (!fechaIso) return ''
  const d = new Date(fechaIso)
  return d.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
}

const cambiarEstadoItem = async (itemId, estado) => {
  try {
    await ordenesStore.cambiarEstadoItem(itemId, estado)
  } catch (err) {
    alert('Error al actualizar estado del platillo.')
  }
}

const abrirModalCancelar = (item) => {
  itemSeleccionado.value = item
  formCancelar.value = { pin: '', motivo: '', genera_merma: item.estado === 'preparando' }
  modalCancelar.value = true
}

const ejecutarCancelacion = async () => {
  if (!itemSeleccionado.value) return
  try {
    await ordenesStore.cancelarItem(itemSeleccionado.value.id, {
      pin_autorizacion: formCancelar.value.pin,
      motivo: formCancelar.value.motivo,
      genera_merma: formCancelar.value.genera_merma
    })
    modalCancelar.value = false
    alert('Platillo cancelado correctamente.')
  } catch (err) {
    alert(err.response?.data?.detail || 'PIN incorrecto o error al cancelar.')
  }
}
</script>

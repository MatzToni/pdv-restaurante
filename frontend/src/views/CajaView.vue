<template>
  <div class="space-y-6 max-w-5xl mx-auto">
    <!-- Header -->
    <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 bg-white dark:bg-slate-900 p-6 rounded-2xl border border-slate-200 dark:border-slate-800 shadow-sm transition-colors">
      <div>
        <h1 class="text-2xl font-black text-slate-800 dark:text-slate-100 tracking-tight">Caja y Cobro</h1>
        <p class="text-slate-500 dark:text-slate-400 text-sm">Cobro de cuentas de mesas, registro de pagos y arqueos</p>
      </div>
      <div class="flex gap-2">
        <button 
          @click="cajaStore.cargarCuentasPendientes()"
          class="px-3.5 py-2 bg-slate-100 dark:bg-slate-800 hover:bg-slate-200 dark:hover:bg-slate-700 text-slate-700 dark:text-slate-300 rounded-xl text-xs font-bold transition active:scale-95"
        >
          🔄 Actualizar
        </button>
        <button 
          @click="abrirCorteX"
          class="px-4 py-2 bg-slate-900 dark:bg-eden-600 hover:bg-slate-800 dark:hover:bg-eden-700 text-white rounded-xl text-xs font-bold shadow-sm transition active:scale-95 flex items-center gap-1.5"
        >
          <span>📊</span> Arqueo Parcial (Corte X)
        </button>
      </div>
    </div>

    <!-- Si no hay mesas con orden activa -->
    <div v-if="cajaStore.cuentasPendientes.length === 0" class="text-center py-20 bg-white dark:bg-slate-900 rounded-3xl border border-slate-200 dark:border-slate-800 text-slate-400 dark:text-slate-500">
      <span class="text-5xl block mb-3">🪙</span>
      <h3 class="text-lg font-bold text-slate-700 dark:text-slate-300">No hay cuentas pendientes de cobro</h3>
      <p class="text-sm text-slate-400 dark:text-slate-500 mt-1">Las mesas aparecerán aquí cuando los meseros pidan la cuenta o concluyan el servicio</p>
    </div>

    <div v-else class="space-y-4">
      <!-- Selector horizontal de mesas por cobrar -->
      <div class="flex items-center gap-2 overflow-x-auto pb-2 no-scrollbar">
        <button
          v-for="orden in cajaStore.cuentasPendientes"
          :key="orden.id"
          @click="ordenSeleccionada = orden"
          :class="[
            'px-4 py-3 rounded-2xl border text-left shrink-0 transition-all active:scale-95 shadow-sm min-w-44',
            ordenSeleccionada?.id === orden.id
              ? 'border-eden-600 bg-eden-50/80 dark:bg-eden-950/60 ring-2 ring-eden-500'
              : 'border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 hover:bg-slate-50'
          ]"
        >
          <div class="flex justify-between items-center">
            <span class="font-black text-sm text-slate-800 dark:text-slate-100">{{ orden.mesa_numero || `Mesa ${orden.mesa_id}` }}</span>
            <span class="w-2.5 h-2.5 rounded-full bg-amber-500 animate-pulse"></span>
          </div>
          <div class="text-xs text-slate-500 dark:text-slate-400 mt-0.5">Orden #{{ orden.id }}</div>
          <div class="text-base font-black text-eden-600 dark:text-eden-400 mt-1">
            ${{ Number(orden.total).toFixed(2) }}
          </div>
        </button>
      </div>

      <!-- Módulo de Cobro Activo -->
      <div v-if="ordenSeleccionada" class="grid grid-cols-1 md:grid-cols-2 gap-6">
        <!-- Detalle de la Cuenta -->
        <div class="bg-white dark:bg-slate-900 p-6 rounded-2xl border border-slate-200 dark:border-slate-800 shadow-sm space-y-4 transition-colors">
          <div class="flex justify-between items-center border-b border-slate-100 dark:border-slate-800 pb-3">
            <div>
              <h3 class="font-extrabold text-slate-800 dark:text-slate-100 text-base">
                Detalle de {{ ordenSeleccionada.mesa_numero || `Mesa ${ordenSeleccionada.mesa_id}` }}
              </h3>
              <span class="text-xs text-slate-400">Mesero: {{ ordenSeleccionada.mesero_nombre || 'N/A' }}</span>
            </div>
            <span class="text-xs bg-slate-100 dark:bg-slate-800 text-slate-600 dark:text-slate-300 font-mono px-2 py-1 rounded-lg">
              Ticket #{{ ordenSeleccionada.id }}
            </span>
          </div>
          
          <!-- Lista de platillos y extras de la orden -->
          <div class="space-y-3 max-h-64 overflow-y-auto pr-1 text-sm border-b border-slate-100 dark:border-slate-800 pb-4">
            <div 
              v-for="item in itemsCobrables" 
              :key="item.id" 
              class="flex justify-between items-start text-slate-700 dark:text-slate-300"
            >
              <div>
                <span class="font-bold">{{ item.cantidad }}x {{ item.producto_nombre }}</span>
                <div v-if="item.extras && item.extras.length > 0" class="flex flex-wrap gap-1 mt-0.5">
                  <span v-for="(ex, ei) in item.extras" :key="ei" class="text-3xs bg-slate-100 dark:bg-slate-800 text-slate-600 dark:text-slate-300 px-1 py-0.2 rounded">
                    + {{ ex.nombre }}
                  </span>
                </div>
              </div>
              <span class="font-bold font-mono text-slate-900 dark:text-slate-100">
                ${{ (Number(item.precio_unitario) * item.cantidad).toFixed(2) }}
              </span>
            </div>
          </div>

          <!-- Totales y Propina -->
          <div class="space-y-2.5">
            <div class="flex justify-between text-slate-600 dark:text-slate-400 text-sm">
              <span>Subtotal</span>
              <span class="font-mono font-bold">${{ Number(ordenSeleccionada.total).toFixed(2) }}</span>
            </div>

            <!-- Botones de propina -->
            <div class="flex items-center justify-between gap-2 pt-1">
              <span class="text-xs font-bold text-slate-600 dark:text-slate-400">Propina:</span>
              <div class="flex gap-1">
                <button 
                  v-for="pct in [0, 10, 15]" 
                  :key="pct"
                  type="button"
                  @click="porcentajePropina = pct"
                  :class="[
                    'px-2.5 py-1 text-2xs font-extrabold rounded-lg border transition',
                    porcentajePropina === pct 
                      ? 'bg-eden-600 text-white border-eden-600' 
                      : 'bg-slate-50 dark:bg-slate-800 text-slate-700 dark:text-slate-300 border-slate-200 dark:border-slate-700'
                  ]"
                >
                  {{ pct }}%
                </button>
              </div>
            </div>

            <div class="flex justify-between text-slate-600 dark:text-slate-400 text-sm">
              <span>Monto Propina</span>
              <span class="font-mono font-bold text-eden-600 dark:text-eden-400">+${{ montoPropina.toFixed(2) }}</span>
            </div>

            <div class="flex justify-between text-xl font-black text-slate-900 dark:text-slate-100 pt-2 border-t border-slate-200 dark:border-slate-800">
              <span>Gran Total</span>
              <span class="text-eden-600 dark:text-eden-400 font-mono">${{ totalConPropina.toFixed(2) }}</span>
            </div>
          </div>
        </div>

        <!-- Opciones de Pago -->
        <div class="bg-white dark:bg-slate-900 p-6 rounded-2xl border border-slate-200 dark:border-slate-800 shadow-sm flex flex-col justify-between space-y-4 transition-colors">
          <div>
            <h3 class="font-extrabold text-slate-800 dark:text-slate-100 text-base mb-3">Método de Liquidación</h3>
            <div class="grid grid-cols-3 gap-2">
              <button 
                v-for="metodo in [
                  { label: 'Efectivo', val: 'efectivo' },
                  { label: 'Tarjeta', val: 'tarjeta' },
                  { label: 'Transfer.', val: 'transferencia' }
                ]" 
                :key="metodo.val"
                @click="metodoPago = metodo.val"
                :class="[
                  'py-3 rounded-xl font-bold text-xs border-2 transition active:scale-95 text-center',
                  metodoPago === metodo.val 
                    ? 'border-eden-600 bg-eden-50 dark:bg-eden-950/40 text-eden-800 dark:text-eden-300 shadow-xs' 
                    : 'border-slate-200 dark:border-slate-800 text-slate-600 dark:text-slate-400 hover:bg-slate-50 dark:hover:bg-slate-800'
                ]"
              >
                {{ metodo.label }}
              </button>
            </div>

            <!-- Entrada de efectivo y cálculo de cambio -->
            <div v-if="metodoPago === 'efectivo'" class="mt-4 space-y-3">
              <label class="text-xs font-bold text-slate-600 dark:text-slate-400">Monto Entregado por Cliente ($)</label>
              <input 
                v-model.number="montoRecibido" 
                type="number" 
                step="0.50"
                placeholder="0.00"
                class="w-full text-2xl font-black p-3 border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-800 text-slate-900 dark:text-slate-100 rounded-xl focus:outline-none focus:border-eden-500 font-mono"
              />

              <!-- Billetes rápidos -->
              <div class="flex gap-2">
                <button 
                  v-for="billete in billetesRapidos" 
                  :key="billete"
                  type="button"
                  @click="montoRecibido = billete"
                  class="flex-1 py-1.5 bg-slate-100 dark:bg-slate-800 hover:bg-slate-200 text-slate-700 dark:text-slate-300 font-bold text-xs rounded-lg transition"
                >
                  ${{ billete }}
                </button>
                <button 
                  type="button"
                  @click="montoRecibido = totalConPropina"
                  class="flex-1 py-1.5 bg-eden-100 dark:bg-eden-950/60 text-eden-800 dark:text-eden-300 font-bold text-xs rounded-lg transition"
                >
                  Exacto
                </button>
              </div>

              <div class="flex justify-between items-center text-sm pt-2 font-bold bg-slate-50 dark:bg-slate-800/60 p-3 rounded-xl border border-slate-200 dark:border-slate-700">
                <span class="text-slate-600 dark:text-slate-400">Cambio al cliente:</span>
                <span :class="cambio >= 0 ? 'text-eden-600 dark:text-eden-400 font-black text-lg font-mono' : 'text-rose-500 font-bold text-xs'">
                  {{ cambio >= 0 ? `$${cambio.toFixed(2)}` : 'Monto insuficiente' }}
                </span>
              </div>
            </div>
          </div>

          <div class="space-y-2 pt-4">
            <button 
              @click="procesarPago"
              :disabled="cobrando || (metodoPago === 'efectivo' && cambio < 0)"
              class="w-full py-4 bg-eden-600 hover:bg-eden-700 disabled:opacity-50 text-white rounded-xl font-black text-sm shadow-md transition active:scale-95 flex items-center justify-center gap-2"
            >
              <span v-if="cobrando">Procesando pago...</span>
              <span v-else>✓ Finalizar Cobro y Liberar Mesa (${{ totalConPropina.toFixed(2) }})</span>
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- MODAL CORTE DE CAJA (CORTE X) -->
    <div v-if="modalCorteX && datosCorteX" class="fixed inset-0 bg-slate-900/60 backdrop-blur-sm flex items-center justify-center p-4 z-50">
      <div class="bg-white dark:bg-slate-900 rounded-3xl p-6 max-w-md w-full shadow-2xl border border-slate-200 dark:border-slate-800 space-y-4">
        <div class="flex justify-between items-center border-b border-slate-100 dark:border-slate-800 pb-3">
          <div class="flex items-center gap-2">
            <span class="text-2xl">📊</span>
            <h3 class="text-lg font-black text-slate-800 dark:text-slate-100">Arqueo de Turno (Corte X)</h3>
          </div>
          <span class="text-2xs bg-slate-100 dark:bg-slate-800 text-slate-600 dark:text-slate-300 px-2 py-0.5 rounded font-mono">
            Edén Café
          </span>
        </div>

        <div class="space-y-2.5 text-xs">
          <div class="flex justify-between py-1.5 border-b border-slate-100 dark:border-slate-800 text-slate-700 dark:text-slate-300">
            <span>Órdenes Liquidadas Hoy</span>
            <span class="font-bold">{{ datosCorteX.ordenes_cobradas }}</span>
          </div>
          <div class="flex justify-between py-1.5 border-b border-slate-100 dark:border-slate-800 text-slate-700 dark:text-slate-300">
            <span>Efectivo en Caja</span>
            <span class="font-mono font-bold text-slate-900 dark:text-slate-100">${{ Number(datosCorteX.total_efectivo).toFixed(2) }}</span>
          </div>
          <div class="flex justify-between py-1.5 border-b border-slate-100 dark:border-slate-800 text-slate-700 dark:text-slate-300">
            <span>Tarjetas de Crédito/Débito</span>
            <span class="font-mono font-bold text-slate-900 dark:text-slate-100">${{ Number(datosCorteX.total_tarjeta).toFixed(2) }}</span>
          </div>
          <div class="flex justify-between py-1.5 border-b border-slate-100 dark:border-slate-800 text-slate-700 dark:text-slate-300">
            <span>Transferencias</span>
            <span class="font-mono font-bold text-slate-900 dark:text-slate-100">${{ Number(datosCorteX.total_transferencia).toFixed(2) }}</span>
          </div>
          <div class="flex justify-between py-1.5 border-b border-slate-100 dark:border-slate-800 text-slate-700 dark:text-slate-300">
            <span>Propinas Acumuladas</span>
            <span class="font-mono font-bold text-eden-600 dark:text-eden-400">${{ Number(datosCorteX.total_propinas).toFixed(2) }}</span>
          </div>
          <div class="flex justify-between text-base font-black pt-2 text-slate-900 dark:text-slate-100">
            <span>Gran Total Vendido</span>
            <span class="font-mono text-eden-600 dark:text-eden-400">${{ Number(datosCorteX.gran_total).toFixed(2) }}</span>
          </div>
        </div>

        <div class="pt-3 border-t border-slate-100 dark:border-slate-800 flex justify-end">
          <button 
            @click="modalCorteX = false"
            class="px-5 py-2.5 bg-slate-900 dark:bg-slate-700 text-white rounded-xl text-xs font-bold transition hover:bg-slate-800"
          >
            Cerrar Resumen
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useCajaStore } from '../stores/caja'
import { useMesasStore } from '../stores/mesas'

const cajaStore = useCajaStore()
const mesasStore = useMesasStore()

const ordenSeleccionada = ref(null)
const metodoPago = ref('efectivo')
const porcentajePropina = ref(0)
const montoRecibido = ref(0)
const cobrando = ref(false)

const modalCorteX = ref(false)
const datosCorteX = ref(null)

onMounted(async () => {
  await cajaStore.cargarCuentasPendientes()
  if (cajaStore.cuentasPendientes.length > 0) {
    ordenSeleccionada.value = cajaStore.cuentasPendientes[0]
  }
})

watch(() => ordenSeleccionada.value, (nuevaOrden) => {
  if (nuevaOrden) {
    montoRecibido.value = Number(nuevaOrden.total)
  }
})

const itemsCobrables = computed(() => {
  if (!ordenSeleccionada.value?.items) return []
  return ordenSeleccionada.value.items.filter(i => i.estado !== 'cancelado')
})

const montoPropina = computed(() => {
  if (!ordenSeleccionada.value) return 0
  return (Number(ordenSeleccionada.value.total) * porcentajePropina.value) / 100
})

const totalConPropina = computed(() => {
  if (!ordenSeleccionada.value) return 0
  return Number(ordenSeleccionada.value.total) + montoPropina.value
})

const cambio = computed(() => {
  if (metodoPago.value !== 'efectivo') return 0
  return (montoRecibido.value || 0) - totalConPropina.value
})

const billetesRapidos = computed(() => {
  const tot = totalConPropina.value
  const billetes = [100, 200, 500, 1000]
  return billetes.filter(b => b >= tot).slice(0, 3)
})

const procesarPago = async () => {
  if (!ordenSeleccionada.value) return
  cobrando.value = true
  try {
    const payload = {
      orden_id: ordenSeleccionada.value.id,
      metodo: metodoPago.value,
      monto_recibido: metodoPago.value === 'efectivo' ? montoRecibido.value : totalConPropina.value,
      propina: montoPropina.value
    }
    await cajaStore.cobrarOrden(payload)
    await mesasStore.cargarMesas()
    alert(`¡Cobro de ${ordenSeleccionada.value.mesa_numero || 'Mesa'} procesado con éxito! Mesa liberada.`)
    ordenSeleccionada.value = cajaStore.cuentasPendientes.length > 0 ? cajaStore.cuentasPendientes[0] : null
  } catch (err) {
    alert(err.response?.data?.detail || 'Error al procesar el cobro.')
  } finally {
    cobrando.value = false
  }
}

const abrirCorteX = async () => {
  const res = await cajaStore.obtenerCorteX()
  if (res) {
    datosCorteX.value = res
    modalCorteX.value = true
  } else {
    alert('No fue posible generar el corte parcial.')
  }
}
</script>

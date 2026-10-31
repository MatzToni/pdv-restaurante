<template>
  <div class="space-y-6 max-w-4xl mx-auto">
    <div class="flex justify-between items-center bg-white dark:bg-slate-900 p-6 rounded-2xl border border-slate-200 dark:border-slate-800 shadow-sm transition-colors">
      <div>
        <h1 class="text-2xl font-black text-slate-800 dark:text-slate-100 tracking-tight">Caja y Cobro</h1>
        <p class="text-slate-500 dark:text-slate-400 text-sm">Cobro de cuentas, arqueos e impresión de cortes</p>
      </div>
      <button 
        @click="hacerCorteCaja"
        class="px-4 py-2 bg-slate-900 dark:bg-eden-600 hover:bg-slate-800 dark:hover:bg-eden-700 text-white rounded-xl text-xs font-bold shadow-sm transition active:scale-95"
      >
        📊 Corte de Caja (Corte X)
      </button>
    </div>

    <!-- Módulo de Cobro de Mesa -->
    <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
      <div class="bg-white dark:bg-slate-900 p-6 rounded-2xl border border-slate-200 dark:border-slate-800 shadow-sm space-y-4 transition-colors">
        <h3 class="font-extrabold text-slate-800 dark:text-slate-100 text-base">Detalle de la Cuenta (Mesa 5)</h3>
        
        <div class="space-y-2 border-b border-slate-100 dark:border-slate-800 pb-4 text-sm">
          <div class="flex justify-between text-slate-600 dark:text-slate-400">
            <span>2x Hamburguesa Edén Especial</span>
            <span class="font-semibold text-slate-800 dark:text-slate-200">$370.00</span>
          </div>
          <div class="flex justify-between text-slate-600 dark:text-slate-400">
            <span>1x Chilaquiles Verdes con Pollo</span>
            <span class="font-semibold text-slate-800 dark:text-slate-200">$135.00</span>
          </div>
          <div class="flex justify-between text-slate-600 dark:text-slate-400">
            <span>2x Café de Olla Tradicional</span>
            <span class="font-semibold text-slate-800 dark:text-slate-200">$90.00</span>
          </div>
        </div>

        <div class="space-y-2">
          <div class="flex justify-between text-slate-600 dark:text-slate-400 text-sm">
            <span>Subtotal</span>
            <span>$595.00</span>
          </div>
          <div class="flex justify-between text-slate-600 dark:text-slate-400 text-sm">
            <span>Propina sugerida (10%)</span>
            <span>$59.50</span>
          </div>
          <div class="flex justify-between text-xl font-black text-slate-900 dark:text-slate-100 pt-2 border-t border-slate-200 dark:border-slate-800">
            <span>Total a Pagar</span>
            <span class="text-eden-600 dark:text-eden-400">${{ totalCobro.toFixed(2) }}</span>
          </div>
        </div>
      </div>

      <div class="bg-white dark:bg-slate-900 p-6 rounded-2xl border border-slate-200 dark:border-slate-800 shadow-sm flex flex-col justify-between space-y-4 transition-colors">
        <div>
          <h3 class="font-extrabold text-slate-800 dark:text-slate-100 text-base mb-3">Método de Pago</h3>
          <div class="grid grid-cols-3 gap-2">
            <button 
              v-for="metodo in ['Efectivo', 'Tarjeta', 'Mixto']" 
              :key="metodo"
              @click="metodoPago = metodo"
              :class="[
                'py-3 rounded-xl font-bold text-xs border-2 transition active:scale-95',
                metodoPago === metodo 
                  ? 'border-eden-600 bg-eden-50 dark:bg-eden-950/40 text-eden-800 dark:text-eden-300' 
                  : 'border-slate-200 dark:border-slate-800 text-slate-600 dark:text-slate-400 hover:bg-slate-50 dark:hover:bg-slate-800'
              ]"
            >
              {{ metodo }}
            </button>
          </div>

          <div v-if="metodoPago === 'Efectivo'" class="mt-4 space-y-2">
            <label class="text-xs font-bold text-slate-600 dark:text-slate-400">Monto Recibido ($)</label>
            <input 
              v-model.number="montoRecibido" 
              type="number" 
              placeholder="0.00"
              class="w-full text-2xl font-bold p-3 border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-800 text-slate-900 dark:text-slate-100 rounded-xl focus:outline-none focus:border-eden-500"
            />
            <div class="flex justify-between text-sm pt-2 font-semibold">
              <span class="text-slate-600 dark:text-slate-400">Cambio:</span>
              <span :class="cambio >= 0 ? 'text-eden-600 dark:text-eden-400 font-black' : 'text-rose-600 font-bold'">
                ${{ cambio >= 0 ? cambio.toFixed(2) : '0.00' }}
              </span>
            </div>
          </div>
        </div>

        <div class="space-y-2 pt-4">
          <button 
            @click="imprimirTicket"
            class="w-full py-3 bg-slate-100 dark:bg-slate-800 hover:bg-slate-200 dark:hover:bg-slate-700 text-slate-700 dark:text-slate-300 rounded-xl font-bold text-xs transition active:scale-95"
          >
            🖨️ Imprimir Ticket de Cuenta
          </button>
          <button 
            @click="finalizarCobro"
            class="w-full py-3.5 bg-eden-600 hover:bg-eden-700 text-white rounded-xl font-bold text-sm shadow-sm transition active:scale-95"
          >
            ✓ Finalizar Cobro y Cerrar Mesa
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'

const totalCobro = ref(654.50)
const metodoPago = ref('Efectivo')
const montoRecibido = ref(700)

const cambio = computed(() => {
  return (montoRecibido.value || 0) - totalCobro.value
})

const imprimirTicket = () => {
  alert('Imprimiendo ticket en impresora térmica de Edén Café...')
}

const finalizarCobro = () => {
  alert('¡Cobro exitoso! Mesa 5 liberada y registrada en turno de caja.')
}

const hacerCorteCaja = () => {
  alert('Generando Corte X del turno actual...')
}
</script>

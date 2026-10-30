<template>
  <div class="space-y-6 max-w-4xl mx-auto">
    <div class="flex justify-between items-center bg-white p-6 rounded-2xl border border-slate-200 shadow-sm">
      <div>
        <h1 class="text-2xl font-bold text-slate-800">Caja y Cobro</h1>
        <p class="text-slate-500 text-sm">Cobro de cuentas, impresión de tickets y cortes</p>
      </div>
      <button 
        @click="hacerCorteCaja"
        class="px-4 py-2 bg-slate-900 text-white rounded-xl text-sm font-bold hover:bg-slate-800 shadow-sm transition active:scale-95"
      >
        📊 Corte de Caja (Corte X)
      </button>
    </div>

    <!-- Módulo de Cobro de Mesa -->
    <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
      <div class="bg-white p-6 rounded-2xl border border-slate-200 shadow-sm space-y-4">
        <h3 class="font-bold text-slate-800 text-lg">Detalle de la Cuenta (Mesa 5)</h3>
        
        <div class="space-y-2 border-b border-slate-100 pb-4 text-sm">
          <div class="flex justify-between text-slate-600">
            <span>2x Hamburguesa Artesanal</span>
            <span>$390.00</span>
          </div>
          <div class="flex justify-between text-slate-600">
            <span>1x Papas Bravas</span>
            <span>$95.00</span>
          </div>
          <div class="flex justify-between text-slate-600">
            <span>2x Cerveza Artesanal</span>
            <span>$170.00</span>
          </div>
        </div>

        <div class="space-y-2">
          <div class="flex justify-between text-slate-600 text-sm">
            <span>Subtotal</span>
            <span>$655.00</span>
          </div>
          <div class="flex justify-between text-slate-600 text-sm">
            <span>Propina sugerida (10%)</span>
            <span>$65.50</span>
          </div>
          <div class="flex justify-between text-xl font-black text-slate-900 pt-2 border-t border-slate-200">
            <span>Total a Pagar</span>
            <span class="text-emerald-600">${{ totalCobro.toFixed(2) }}</span>
          </div>
        </div>
      </div>

      <div class="bg-white p-6 rounded-2xl border border-slate-200 shadow-sm flex flex-col justify-between space-y-4">
        <div>
          <h3 class="font-bold text-slate-800 text-lg mb-3">Método de Pago</h3>
          <div class="grid grid-cols-3 gap-2">
            <button 
              v-for="metodo in ['Efectivo', 'Tarjeta', 'Mixto']" 
              :key="metodo"
              @click="metodoPago = metodo"
              :class="[
                'py-3 rounded-xl font-bold text-sm border-2 transition active:scale-95',
                metodoPago === metodo ? 'border-emerald-600 bg-emerald-50 text-emerald-800' : 'border-slate-200 text-slate-600 hover:bg-slate-50'
              ]"
            >
              {{ metodo }}
            </button>
          </div>

          <div v-if="metodoPago === 'Efectivo'" class="mt-4 space-y-2">
            <label class="text-xs font-semibold text-slate-500">Monto Recibido ($)</label>
            <input 
              v-model.number="montoRecibido" 
              type="number" 
              placeholder="0.00"
              class="w-full text-2xl font-bold p-3 border border-slate-300 rounded-xl focus:outline-none focus:border-emerald-500"
            />
            <div class="flex justify-between text-sm pt-2 font-semibold">
              <span class="text-slate-600">Cambio:</span>
              <span :class="cambio >= 0 ? 'text-emerald-600' : 'text-rose-600'">
                ${{ cambio >= 0 ? cambio.toFixed(2) : '0.00' }}
              </span>
            </div>
          </div>
        </div>

        <div class="space-y-2 pt-4">
          <button 
            @click="imprimirTicket"
            class="w-full py-3 bg-slate-100 hover:bg-slate-200 text-slate-700 rounded-xl font-bold text-sm transition active:scale-95"
          >
            🖨️ Imprimir Ticket de Cuenta
          </button>
          <button 
            @click="finalizarCobro"
            class="w-full py-3.5 bg-emerald-600 hover:bg-emerald-700 text-white rounded-xl font-bold text-base shadow-sm transition active:scale-95"
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

const totalCobro = ref(720.50)
const metodoPago = ref('Efectivo')
const montoRecibido = ref(800)

const cambio = computed(() => {
  return (montoRecibido.value || 0) - totalCobro.value
})

const imprimirTicket = () => {
  alert('Imprimiendo ticket en impresora térmica...')
}

const finalizarCobro = () => {
  alert('¡Cobro exitoso! Mesa liberada e inventario actualizado.')
}

const hacerCorteCaja = () => {
  alert('Generando Corte X del turno actual...')
}
</script>

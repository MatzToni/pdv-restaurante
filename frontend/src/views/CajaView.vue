<template>
  <div class="space-y-6 max-w-6xl mx-auto">
    <!-- Header Principal -->
    <div class="flex flex-col md:flex-row justify-between items-start md:items-center gap-4 bg-white dark:bg-slate-900 p-6 rounded-3xl border border-slate-200 dark:border-slate-800 shadow-sm transition-colors">
      <div>
        <div class="flex items-center gap-2.5">
          <h1 class="text-2xl font-black text-slate-800 dark:text-slate-100 tracking-tight">Caja y Cobro</h1>
          <!-- Indicador en vivo -->
          <span class="inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-full text-3xs font-extrabold bg-emerald-100 dark:bg-emerald-950/80 text-emerald-800 dark:text-emerald-300 border border-emerald-300 dark:border-emerald-800">
            <span class="w-1.5 h-1.5 rounded-full bg-emerald-500 animate-pulse"></span>
            En vivo
          </span>
        </div>
        <p class="text-slate-500 dark:text-slate-400 text-xs sm:text-sm mt-0.5">
          Liquidación de mesas, pedidos para llevar/envío, emisión de tickets y arqueos
        </p>
      </div>

      <div class="flex flex-wrap items-center gap-2 w-full md:w-auto">
        <!-- Botón Actualizar -->
        <button 
          @click="actualizarManual"
          :disabled="cargandoManual"
          class="px-3.5 py-2.5 bg-slate-100 dark:bg-slate-800 hover:bg-slate-200 dark:hover:bg-slate-700 text-slate-700 dark:text-slate-300 rounded-xl text-xs font-bold transition active:scale-95 flex items-center gap-1.5 border border-slate-200 dark:border-slate-700"
          title="Actualizar cuentas pendientes"
        >
          <span :class="cargandoManual ? 'animate-spin' : ''">🔄</span>
          <span>Actualizar</span>
        </button>

        <!-- Botón Corte X -->
        <button 
          @click="abrirCorteX"
          class="px-3.5 py-2.5 bg-slate-100 dark:bg-slate-800 hover:bg-slate-200 dark:hover:bg-slate-700 text-slate-700 dark:text-slate-300 rounded-xl text-xs font-bold transition active:scale-95 flex items-center gap-1.5 border border-slate-200 dark:border-slate-700"
        >
          <span>📊</span>
          <span>Corte X (Parcial)</span>
        </button>

        <!-- Botón Turno de Caja (Abrir / Corte Z) -->
        <button 
          v-if="!cajaStore.turnoActivo"
          @click="modalAbrirTurno = true"
          class="px-4 py-2.5 bg-eden-600 hover:bg-eden-700 text-white rounded-xl text-xs font-bold shadow-sm transition active:scale-95 flex items-center gap-1.5"
        >
          <span>🟢</span>
          <span>Abrir Turno</span>
        </button>
        <button 
          v-else
          @click="abrirModalCerrarTurno"
          class="px-4 py-2.5 bg-amber-600 hover:bg-amber-700 text-white rounded-xl text-xs font-bold shadow-sm transition active:scale-95 flex items-center gap-1.5"
        >
          <span>🔒</span>
          <span>Cierre de Turno (Corte Z)</span>
        </button>
      </div>
    </div>

    <!-- Barra informativa de Turno Abierto si existe -->
    <div 
      v-if="cajaStore.turnoActivo"
      class="bg-gradient-to-r from-eden-50 via-emerald-50 to-teal-50 dark:from-eden-950/40 dark:via-emerald-950/40 dark:to-teal-950/40 border border-eden-200 dark:border-eden-800/60 p-3.5 rounded-2xl flex flex-wrap items-center justify-between gap-3 text-xs"
    >
      <div class="flex items-center gap-2 text-slate-700 dark:text-slate-300">
        <span class="w-2.5 h-2.5 rounded-full bg-emerald-500 animate-pulse"></span>
        <span class="font-extrabold text-eden-800 dark:text-eden-300">Turno Activo:</span>
        <span class="font-medium">Cajero: {{ cajaStore.turnoActivo.usuario_nombre || 'Principal' }}</span>
        <span class="text-slate-400">|</span>
        <span>Fondo Inicial: <strong>${{ Number(cajaStore.turnoActivo.monto_apertura).toFixed(2) }}</strong></span>
      </div>
      <div class="flex items-center gap-3 text-slate-700 dark:text-slate-300">
        <span>Ventas Turno: <strong class="text-eden-700 dark:text-eden-400 font-mono">${{ Number(cajaStore.turnoActivo.gran_total).toFixed(2) }}</strong></span>
        <span class="text-slate-400">|</span>
        <span>Efectivo en Caja: <strong class="text-slate-900 dark:text-slate-100 font-mono">${{ Number(cajaStore.turnoActivo.total_efectivo_en_caja).toFixed(2) }}</strong></span>
      </div>
    </div>

    <!-- Pestañas de Filtro y Búsqueda -->
    <div class="flex flex-col sm:flex-row items-stretch sm:items-center justify-between gap-3">
      <!-- Pestañas -->
      <div class="flex items-center gap-1.5 overflow-x-auto pb-1 no-scrollbar">
        <button
          v-for="tab in tabsFiltro"
          :key="tab.id"
          @click="filtroActivo = tab.id"
          :class="[
            'px-3.5 py-2 rounded-xl text-xs font-extrabold transition-all shrink-0 flex items-center gap-1.5 min-h-[40px]',
            filtroActivo === tab.id
              ? tab.activeClass
              : 'bg-white dark:bg-slate-900 text-slate-600 dark:text-slate-400 hover:bg-slate-100 dark:hover:bg-slate-800 border border-slate-200 dark:border-slate-800'
          ]"
        >
          <span>{{ tab.emoji }}</span>
          <span>{{ tab.label }}</span>
          <span 
            :class="[
              'px-1.5 py-0.2 rounded-full text-3xs font-black',
              filtroActivo === tab.id ? 'bg-white/30 text-white' : 'bg-slate-100 dark:bg-slate-800 text-slate-600 dark:text-slate-400'
            ]"
          >
            {{ tab.count }}
          </span>
        </button>
      </div>

      <!-- Barra de búsqueda rápida -->
      <div class="relative w-full sm:w-64 shrink-0">
        <span class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none text-slate-400 text-xs">
          🔍
        </span>
        <input 
          v-model="busqueda"
          type="text"
          placeholder="Buscar mesa o cliente..."
          class="w-full pl-8 pr-3 py-2 bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-xl text-xs text-slate-800 dark:text-slate-100 placeholder-slate-400 focus:outline-none focus:border-eden-500 transition"
        />
        <button 
          v-if="busqueda" 
          @click="busqueda = ''"
          class="absolute inset-y-0 right-0 pr-2.5 flex items-center text-slate-400 hover:text-slate-600 text-xs"
        >
          ✕
        </button>
      </div>
    </div>

    <!-- Si no hay cuentas en la lista -->
    <div v-if="cuentasFiltradas.length === 0" class="text-center py-16 bg-white dark:bg-slate-900 rounded-3xl border border-slate-200 dark:border-slate-800 text-slate-400 dark:text-slate-500 shadow-sm">
      <span class="text-5xl block mb-3">🪙</span>
      <h3 class="text-lg font-bold text-slate-700 dark:text-slate-300">
        {{ busqueda ? 'No se encontraron resultados con ese criterio' : 'No hay cuentas pendientes de cobro' }}
      </h3>
      <p class="text-xs text-slate-400 dark:text-slate-500 mt-1 max-w-md mx-auto">
        {{ busqueda ? 'Intenta borrar la búsqueda para ver todas las comandas.' : 'Las mesas aparecerán aquí cuando los meseros pidan la cuenta o cuando se generen pedidos para llevar o entrega a domicilio.' }}
      </p>
    </div>

    <!-- Lista Horizontal de Tarjetas de Cuentas -->
    <div v-else class="space-y-4">
      <div class="flex items-center gap-2.5 overflow-x-auto pb-2 no-scrollbar">
        <button
          v-for="orden in cuentasFiltradas"
          :key="orden.id"
          @click="seleccionarOrden(orden)"
          :class="[
            'p-3.5 rounded-2xl border text-left shrink-0 transition-all active:scale-95 shadow-sm min-w-52 relative',
            ordenSeleccionada?.id === orden.id
              ? 'border-eden-600 bg-eden-50/90 dark:bg-eden-950/70 ring-2 ring-eden-500'
              : orden.mesa_estado === 'cuenta'
                ? 'border-amber-400 dark:border-amber-600 bg-amber-50/40 dark:bg-amber-950/30 hover:border-amber-500'
                : 'border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 hover:bg-slate-50 dark:hover:bg-slate-800/60'
          ]"
        >
          <!-- Badge de ALERTA si la mesa solicitó la cuenta -->
          <div v-if="orden.mesa_estado === 'cuenta'" class="mb-1.5">
            <span class="inline-flex items-center gap-1 px-2 py-0.5 rounded-full text-3xs font-black uppercase bg-amber-500 text-white shadow-xs">
              <span class="w-1.5 h-1.5 rounded-full bg-white animate-ping"></span>
              🔔 Piden Cuenta
            </span>
          </div>

          <div class="flex justify-between items-start gap-1">
            <div class="min-w-0">
              <span class="font-black text-sm text-slate-800 dark:text-slate-100 block truncate">
                {{ obtenerNombreCabecera(orden) }}
              </span>
              <span class="text-3xs text-slate-400 block mt-0.5 font-medium">
                Folio #{{ orden.id }} • {{ contarPlatillos(orden) }} platillos
              </span>
            </div>

            <!-- Badge tipo pedido -->
            <span 
              v-if="orden.tipo_pedido === 'domicilio'" 
              class="text-3xs font-extrabold px-1.5 py-0.5 rounded bg-blue-100 dark:bg-blue-950 text-blue-800 dark:text-blue-300 shrink-0"
            >
              🛵 Envío
            </span>
            <span 
              v-else-if="orden.tipo_pedido === 'para_llevar'" 
              class="text-3xs font-extrabold px-1.5 py-0.5 rounded bg-amber-100 dark:bg-amber-950 text-amber-800 dark:text-amber-300 shrink-0"
            >
              🛍️ Llevar
            </span>
            <span 
              v-else
              class="text-3xs font-extrabold px-1.5 py-0.5 rounded bg-slate-100 dark:bg-slate-800 text-slate-700 dark:text-slate-300 shrink-0"
            >
              🍽️ Mesa
            </span>
          </div>

          <div class="flex justify-between items-end mt-2 pt-1 border-t border-slate-100 dark:border-slate-800">
            <span class="text-3xs text-slate-400">
              {{ formatearHora(orden.fecha_apertura) }}
            </span>
            <span class="text-base font-black text-eden-600 dark:text-eden-400 font-mono">
              ${{ Number(orden.total).toFixed(2) }}
            </span>
          </div>
        </button>
      </div>

      <!-- ================= ÁREA DE COBRO Y DETALLE ================= -->
      <div v-if="ordenSeleccionada" class="grid grid-cols-1 lg:grid-cols-12 gap-6 items-start">
        
        <!-- COLUMNA IZQUIERDA: Detalle de la Cuenta & Ticket Proforma (7 cols) -->
        <div class="lg:col-span-7 bg-white dark:bg-slate-900 p-6 rounded-3xl border border-slate-200 dark:border-slate-800 shadow-sm space-y-4 transition-colors">
          
          <!-- Encabezado de la comanda -->
          <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-2 border-b border-slate-100 dark:border-slate-800 pb-3">
            <div>
              <div class="flex items-center gap-2 flex-wrap">
                <h3 class="font-black text-slate-800 dark:text-slate-100 text-lg">
                  {{ obtenerNombreCabecera(ordenSeleccionada) }}
                </h3>
                <span 
                  v-if="ordenSeleccionada.mesa_estado === 'cuenta'"
                  class="text-3xs font-black uppercase px-2 py-0.5 rounded-full bg-amber-500 text-white"
                >
                  🔔 Cuenta Solicitada
                </span>
                <span 
                  class="text-3xs font-extrabold px-2 py-0.5 rounded-full"
                  :class="badgeEstadoOrden(ordenSeleccionada.estado).clase"
                >
                  {{ badgeEstadoOrden(ordenSeleccionada.estado).texto }}
                </span>
              </div>
              <div class="text-xs text-slate-400 mt-0.5 flex items-center gap-2">
                <span>Atendido por: <strong class="text-slate-600 dark:text-slate-300">{{ ordenSeleccionada.mesero_nombre || 'Mesero General' }}</strong></span>
                <span>•</span>
                <span>Apertura: {{ formatearHora(ordenSeleccionada.fecha_apertura) }}</span>
              </div>
            </div>

            <!-- Acciones rápidas pre-cuenta -->
            <div class="flex items-center gap-2">
              <button 
                @click="abrirPreCuenta"
                class="px-3.5 py-2 bg-slate-100 dark:bg-slate-800 hover:bg-slate-200 dark:hover:bg-slate-700 text-slate-700 dark:text-slate-300 rounded-xl text-xs font-bold transition flex items-center gap-1.5 border border-slate-200 dark:border-slate-700 active:scale-95"
                title="Generar e imprimir pre-cuenta para comensal"
              >
                <span>🖨️</span>
                <span>Pre-Cuenta</span>
              </button>
            </div>
          </div>

          <!-- Si es envío a domicilio o para llevar, mostrar tarjeta con datos de cliente -->
          <div 
            v-if="ordenSeleccionada.datos_entrega" 
            class="p-3.5 rounded-2xl bg-blue-50/70 dark:bg-blue-950/40 border border-blue-200 dark:border-blue-900/60 text-xs space-y-1.5"
          >
            <div class="flex items-center justify-between text-blue-900 dark:text-blue-300 font-extrabold">
              <span class="flex items-center gap-1.5">
                <span>🛵</span> Datos de Entrega
              </span>
              <span v-if="Number(ordenSeleccionada.costo_envio || 0) > 0" class="font-mono text-2xs bg-blue-100 dark:bg-blue-900 px-2 py-0.5 rounded">
                Envío: +${{ Number(ordenSeleccionada.costo_envio).toFixed(2) }}
              </span>
            </div>
            <div class="grid grid-cols-1 sm:grid-cols-2 gap-2 text-slate-700 dark:text-slate-300">
              <div>
                <span class="text-slate-400 block text-3xs">Cliente</span>
                <span class="font-bold">{{ ordenSeleccionada.datos_entrega.cliente || 'No especificado' }}</span>
              </div>
              <div v-if="ordenSeleccionada.datos_entrega.telefono">
                <span class="text-slate-400 block text-3xs">Teléfono</span>
                <a :href="`tel:${ordenSeleccionada.datos_entrega.telefono}`" class="font-bold text-blue-600 dark:text-blue-400 hover:underline">
                  📞 {{ ordenSeleccionada.datos_entrega.telefono }}
                </a>
              </div>
            </div>
            <div v-if="ordenSeleccionada.datos_entrega.direccion" class="pt-1 text-slate-700 dark:text-slate-300">
              <span class="text-slate-400 block text-3xs">Dirección de Destino</span>
              <span class="font-medium">📍 {{ ordenSeleccionada.datos_entrega.direccion }}</span>
            </div>
          </div>

          <!-- Notas generales de la comanda -->
          <div 
            v-if="ordenSeleccionada.notas" 
            class="p-3 rounded-xl bg-amber-50/60 dark:bg-amber-950/30 border border-amber-200/80 dark:border-amber-900/40 text-xs text-amber-900 dark:text-amber-300"
          >
            <strong>📝 Notas:</strong> {{ ordenSeleccionada.notas }}
          </div>

          <!-- Lista de Platillos y Servicios -->
          <div class="space-y-2.5 max-h-[26rem] overflow-y-auto pr-1 text-sm border-b border-slate-100 dark:border-slate-800 pb-4">
            <div 
              v-for="item in itemsCobrables" 
              :key="item.id" 
              class="flex justify-between items-start p-2.5 rounded-xl hover:bg-slate-50 dark:hover:bg-slate-800/40 transition text-slate-700 dark:text-slate-300"
            >
              <div class="space-y-0.5 min-w-0 pr-3">
                <div class="flex items-center gap-2 flex-wrap">
                  <span class="font-black text-slate-900 dark:text-slate-100">{{ item.cantidad }}x</span>
                  <span class="font-bold">{{ item.producto_nombre }}</span>
                  <span 
                    v-if="item.para_llevar" 
                    class="text-3xs font-extrabold bg-amber-100 dark:bg-amber-950 text-amber-800 dark:text-amber-300 px-1.5 py-0.2 rounded border border-amber-300 dark:border-amber-800"
                  >
                    📦 Para Llevar (+${{ (Number(item.cargo_desechable || 0) * item.cantidad).toFixed(2) }})
                  </span>
                </div>

                <!-- Extras -->
                <div v-if="item.extras && item.extras.length > 0" class="flex flex-wrap gap-1 mt-0.5">
                  <span 
                    v-for="(ex, ei) in item.extras" 
                    :key="ei" 
                    class="text-3xs bg-slate-100 dark:bg-slate-800 text-slate-600 dark:text-slate-300 px-1.5 py-0.2 rounded"
                  >
                    + {{ ex.nombre }}
                  </span>
                </div>

                <!-- Clarificación / Notas de Cocina -->
                <div v-if="item.notas" class="text-3xs text-slate-400 italic">
                  {{ item.notas }}
                </div>
              </div>

              <div class="text-right shrink-0">
                <span class="font-black font-mono text-slate-900 dark:text-slate-100 text-sm">
                  ${{ (Number(item.precio_unitario) * item.cantidad).toFixed(2) }}
                </span>
                <span v-if="item.cantidad > 1" class="block text-3xs text-slate-400 font-mono">
                  ${{ Number(item.precio_unitario).toFixed(2) }} c/u
                </span>
              </div>
            </div>
          </div>

          <!-- Totales, Envío y Propinas -->
          <div class="space-y-2 pt-1">
            <div class="flex justify-between text-slate-600 dark:text-slate-400 text-xs sm:text-sm">
              <span>Subtotal Productos</span>
              <span class="font-mono font-bold">${{ subtotalSinEnvio.toFixed(2) }}</span>
            </div>

            <div v-if="Number(ordenSeleccionada.costo_envio || 0) > 0" class="flex justify-between text-blue-700 dark:text-blue-400 text-xs sm:text-sm font-semibold">
              <span class="flex items-center gap-1">🛵 Costo de Envío / Entrega</span>
              <span class="font-mono font-bold">+${{ Number(ordenSeleccionada.costo_envio).toFixed(2) }}</span>
            </div>

            <!-- Descuento si está aplicado -->
            <div v-if="Number(ordenSeleccionada.descuento || 0) > 0" class="flex justify-between items-center text-rose-700 dark:text-rose-400 text-xs sm:text-sm font-bold bg-rose-50 dark:bg-rose-950/40 p-2.5 rounded-xl border border-rose-200 dark:border-rose-900/60">
              <span class="flex items-center gap-1.5">
                <span>🏷️</span>
                <span>Descuento / Cupón:</span>
              </span>
              <div class="flex items-center gap-2">
                <span class="font-mono font-black">-${{ Number(ordenSeleccionada.descuento).toFixed(2) }}</span>
                <button 
                  type="button" 
                  @click="quitarDescuentoActivo"
                  :disabled="quitandoDescuento"
                  class="px-2 py-0.5 rounded text-3xs font-extrabold bg-rose-200 dark:bg-rose-900 hover:bg-rose-300 text-rose-900 dark:text-rose-200 transition"
                  title="Quitar descuento de la orden"
                >
                  ✕ Quitar
                </button>
              </div>
            </div>

            <!-- Botón Agregar Descuento si no tiene -->
            <div v-else class="flex justify-between items-center pt-0.5">
              <span class="text-xs text-slate-400">¿Aplica descuento o cupón?</span>
              <button 
                type="button" 
                @click="abrirModalDescuento"
                class="px-3 py-1.5 rounded-xl text-xs font-black text-amber-700 dark:text-amber-400 bg-amber-50 dark:bg-amber-950/40 hover:bg-amber-100 dark:hover:bg-amber-900/60 border border-amber-300 dark:border-amber-800 transition active:scale-95 flex items-center gap-1.5"
              >
                <span>🏷️</span>
                <span>+ Descuento / Cupón</span>
              </button>
            </div>

            <div class="flex justify-between text-slate-800 dark:text-slate-100 font-black text-sm border-t border-slate-100 dark:border-slate-800 pt-2">
              <span>Total Comanda</span>
              <span class="font-mono font-black">${{ Number(ordenSeleccionada.total).toFixed(2) }}</span>
            </div>

            <!-- Botones de Selección de Propina -->
            <div class="bg-slate-50 dark:bg-slate-800/50 p-3 rounded-2xl border border-slate-200/60 dark:border-slate-700/60 space-y-2">
              <div class="flex items-center justify-between">
                <span class="text-xs font-bold text-slate-700 dark:text-slate-300">Propina Sugerida:</span>
                <span class="font-mono font-bold text-eden-600 dark:text-eden-400 text-xs">
                  +${{ montoPropina.toFixed(2) }}
                </span>
              </div>

              <div class="grid grid-cols-5 gap-1.5">
                <button 
                  v-for="opc in [0, 10, 15, 20]" 
                  :key="opc"
                  type="button"
                  @click="seleccionarPorcentajePropina(opc)"
                  :class="[
                    'py-1.5 text-xs font-black rounded-xl border transition active:scale-95 text-center',
                    tipoPropina === 'pct' && porcentajePropina === opc 
                      ? 'bg-eden-600 text-white border-eden-600 shadow-xs' 
                      : 'bg-white dark:bg-slate-800 text-slate-700 dark:text-slate-300 border-slate-200 dark:border-slate-700 hover:bg-slate-100'
                  ]"
                >
                  {{ opc }}%
                </button>
                <button 
                  type="button"
                  @click="tipoPropina = 'monto'"
                  :class="[
                    'py-1.5 text-xs font-black rounded-xl border transition active:scale-95 text-center',
                    tipoPropina === 'monto' 
                      ? 'bg-eden-600 text-white border-eden-600 shadow-xs' 
                      : 'bg-white dark:bg-slate-800 text-slate-700 dark:text-slate-300 border-slate-200 dark:border-slate-700 hover:bg-slate-100'
                  ]"
                >
                  $ Libre
                </button>
              </div>

              <!-- Input de monto libre de propina -->
              <div v-if="tipoPropina === 'monto'" class="pt-1 flex items-center gap-2">
                <span class="text-xs text-slate-500 font-bold">$</span>
                <input 
                  v-model.number="propinaManual"
                  type="number"
                  min="0"
                  step="5"
                  placeholder="0.00"
                  class="flex-1 px-3 py-1.5 bg-white dark:bg-slate-900 border border-slate-300 dark:border-slate-700 rounded-xl text-xs font-bold font-mono text-slate-900 dark:text-slate-100 focus:outline-none focus:border-eden-500"
                />
              </div>
            </div>

            <!-- Gran Total Highlight -->
            <div class="flex justify-between items-center text-xl font-black text-slate-900 dark:text-slate-100 pt-2 border-t border-slate-200 dark:border-slate-800">
              <span>Gran Total</span>
              <span class="text-eden-600 dark:text-eden-400 font-mono text-2xl font-black">
                ${{ totalConPropina.toFixed(2) }}
              </span>
            </div>
          </div>
        </div>

        <!-- COLUMNA DERECHA: Módulo de Liquidación / Pago (5 cols) -->
        <div class="lg:col-span-5 bg-white dark:bg-slate-900 p-6 rounded-3xl border border-slate-200 dark:border-slate-800 shadow-sm flex flex-col justify-between space-y-5 transition-colors">
          <div class="space-y-4">
            <h3 class="font-black text-slate-800 dark:text-slate-100 text-base">
              Método de Liquidación
            </h3>

            <!-- Botones Touch de Método de Pago -->
            <div class="grid grid-cols-3 gap-2">
              <button 
                v-for="metodo in [
                  { label: 'Efectivo', val: 'efectivo', emoji: '💵' },
                  { label: 'Tarjeta', val: 'tarjeta', emoji: '💳' },
                  { label: 'Transfer.', val: 'transferencia', emoji: '📲' }
                ]" 
                :key="metodo.val"
                @click="metodoPago = metodo.val"
                :class="[
                  'py-3.5 px-2 rounded-2xl font-black text-xs border-2 transition active:scale-95 flex flex-col items-center justify-center gap-1 min-h-[54px]',
                  metodoPago === metodo.val 
                    ? 'border-eden-600 bg-eden-50 dark:bg-eden-950/50 text-eden-800 dark:text-eden-300 shadow-sm' 
                    : 'border-slate-200 dark:border-slate-800 text-slate-600 dark:text-slate-400 hover:bg-slate-50 dark:hover:bg-slate-800'
                ]"
              >
                <span class="text-base">{{ metodo.emoji }}</span>
                <span>{{ metodo.label }}</span>
              </button>
            </div>

            <!-- MÓDULO EFECTIVO -->
            <div v-if="metodoPago === 'efectivo'" class="space-y-3 pt-2">
              <label class="block text-xs font-black text-slate-700 dark:text-slate-300">
                Monto Entregado por Cliente ($)
              </label>

              <input 
                v-model.number="montoRecibido" 
                type="number" 
                min="0"
                max="999999"
                step="1"
                inputmode="decimal"
                placeholder="0.00"
                class="w-full text-2xl font-black p-3.5 border-2 border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-800 text-slate-900 dark:text-slate-100 rounded-2xl focus:outline-none focus:border-eden-500 font-mono shadow-inner"
              />

              <!-- Billetes Rápidos y Exacto -->
              <div class="space-y-2">
                <span class="text-3xs font-extrabold text-slate-400 uppercase tracking-wider block">Billetes sugeridos:</span>
                <div class="grid grid-cols-4 gap-1.5">
                  <button 
                    type="button"
                    @click="montoRecibido = totalConPropina"
                    class="py-2 bg-eden-100 dark:bg-eden-950/80 hover:bg-eden-200 text-eden-800 dark:text-eden-300 font-black text-xs rounded-xl transition border border-eden-300 dark:border-eden-800 active:scale-95"
                  >
                    Exacto
                  </button>
                  <button 
                    v-for="billete in [100, 200, 500]" 
                    :key="billete"
                    type="button"
                    @click="montoRecibido = billete"
                    class="py-2 bg-slate-100 dark:bg-slate-800 hover:bg-slate-200 text-slate-700 dark:text-slate-300 font-black text-xs rounded-xl transition border border-slate-200 dark:border-slate-700 active:scale-95"
                  >
                    ${{ billete }}
                  </button>
                </div>
                
                <div class="flex gap-1.5">
                  <button 
                    v-for="extra in [20, 50, 100]" 
                    :key="extra"
                    type="button"
                    @click="montoRecibido = (montoRecibido || 0) + extra"
                    class="flex-1 py-1.5 bg-slate-50 dark:bg-slate-800/60 hover:bg-slate-100 text-slate-600 dark:text-slate-400 font-bold text-2xs rounded-lg border border-slate-200 dark:border-slate-700"
                  >
                    +${{ extra }}
                  </button>
                  <button 
                    type="button"
                    @click="montoRecibido = 1000"
                    class="flex-1 py-1.5 bg-slate-100 dark:bg-slate-800 text-slate-700 dark:text-slate-300 font-bold text-2xs rounded-lg border border-slate-200 dark:border-slate-700"
                  >
                    $1000
                  </button>
                </div>
              </div>

              <!-- Tarjeta de Cálculo de Cambio -->
              <div 
                class="p-4 rounded-2xl border transition-all"
                :class="[
                  cambio >= 0 
                    ? 'bg-emerald-50 dark:bg-emerald-950/40 border-emerald-300 dark:border-emerald-800 text-emerald-900 dark:text-emerald-300'
                    : 'bg-rose-50 dark:bg-rose-950/40 border-rose-300 dark:border-rose-800 text-rose-900 dark:text-rose-300'
                ]"
              >
                <div class="flex justify-between items-center">
                  <span class="text-xs font-bold">
                    {{ cambio >= 0 ? 'Cambio al cliente:' : 'Falta dinero:' }}
                  </span>
                  <span 
                    class="font-black font-mono text-xl"
                    :class="cambio >= 0 ? 'text-emerald-600 dark:text-emerald-400' : 'text-rose-600 dark:text-rose-400'"
                  >
                    {{ cambio >= 0 ? `$${cambio.toFixed(2)}` : `-$${Math.abs(cambio).toFixed(2)}` }}
                  </span>
                </div>
                <p v-if="cambio < 0" class="text-3xs text-rose-600 dark:text-rose-400 mt-1 font-medium">
                  El monto entregado no cubre el total de ${{ totalConPropina.toFixed(2) }}.
                </p>
              </div>
            </div>

            <!-- MÓDULO TARJETA -->
            <div v-else-if="metodoPago === 'tarjeta'" class="p-4 rounded-2xl bg-slate-50 dark:bg-slate-800/60 border border-slate-200 dark:border-slate-700 space-y-2.5 text-xs">
              <div class="flex items-center gap-2 font-black text-slate-800 dark:text-slate-200">
                <span>💳</span>
                <span>Terminal Bancaria (TPV)</span>
              </div>
              <p class="text-slate-500 dark:text-slate-400">
                Cobrar el monto exacto de <strong class="text-slate-800 dark:text-slate-100 font-mono text-sm">${{ totalConPropina.toFixed(2) }}</strong> en la terminal bancaria e ingresar tarjeta.
              </p>
              <div class="pt-1">
                <label class="block text-3xs font-bold text-slate-500 mb-1">Referencia o autorización (Opcional):</label>
                <input 
                  v-model="referenciaPago"
                  type="text"
                  placeholder="Ej. Auth #84920"
                  class="w-full p-2 bg-white dark:bg-slate-900 border border-slate-300 dark:border-slate-700 rounded-xl text-xs text-slate-800 dark:text-slate-100 focus:outline-none focus:border-eden-500"
                />
              </div>
            </div>

            <!-- MÓDULO TRANSFERENCIA -->
            <div v-else-if="metodoPago === 'transferencia'" class="p-4 rounded-2xl bg-slate-50 dark:bg-slate-800/60 border border-slate-200 dark:border-slate-700 space-y-2.5 text-xs">
              <div class="flex items-center gap-2 font-black text-slate-800 dark:text-slate-200">
                <span>📲</span>
                <span>Transferencia SPEI</span>
              </div>
              <p class="text-slate-500 dark:text-slate-400">
                Verificar que el cliente haya transferido <strong class="text-slate-800 dark:text-slate-100 font-mono text-sm">${{ totalConPropina.toFixed(2) }}</strong> antes de liberar la comanda.
              </p>
              <div class="pt-1">
                <label class="block text-3xs font-bold text-slate-500 mb-1">Clave de rastreo o folio SPEI (Opcional):</label>
                <input 
                  v-model="referenciaPago"
                  type="text"
                  placeholder="Ej. SPEI #12345"
                  class="w-full p-2 bg-white dark:bg-slate-900 border border-slate-300 dark:border-slate-700 rounded-xl text-xs text-slate-800 dark:text-slate-100 focus:outline-none focus:border-eden-500"
                />
              </div>
            </div>
          </div>

          <!-- Mensaje en Ticket (Seleccionable o Manual) -->
          <div class="border border-slate-200 dark:border-slate-800 rounded-2xl p-3 bg-slate-50/70 dark:bg-slate-800/40 space-y-2">
            <div class="flex items-center justify-between">
              <span class="text-xs font-black text-slate-700 dark:text-slate-300 flex items-center gap-1.5">
                <span>💬</span> Mensaje en Ticket (Opcional)
              </span>
              <button 
                type="button" 
                @click="mostrarEditorMensaje = !mostrarEditorMensaje"
                class="text-3xs text-eden-600 dark:text-eden-400 font-bold hover:underline"
              >
                {{ mostrarEditorMensaje ? 'Ocultar' : 'Editar / Elegir' }}
              </button>
            </div>

            <!-- Vista previa corta del mensaje activo -->
            <p v-if="!mostrarEditorMensaje" class="text-2xs text-slate-500 dark:text-slate-400 italic truncate">
              "{{ mensajeTicket || 'Sin mensaje adicional' }}"
            </p>

            <div v-if="mostrarEditorMensaje" class="space-y-2 pt-1">
              <!-- Chips de mensajes predeterminados -->
              <div class="flex flex-wrap gap-1">
                <button 
                  v-for="preset in plantillasMensaje" 
                  :key="preset.id"
                  type="button"
                  @click="seleccionarPlantilla(preset)"
                  :class="[
                    'px-2 py-1 rounded-lg text-3xs font-extrabold border transition active:scale-95 text-left',
                    mensajeTicket === preset.texto
                      ? 'bg-eden-600 text-white border-eden-600 shadow-2xs'
                      : 'bg-white dark:bg-slate-800 text-slate-600 dark:text-slate-300 border-slate-200 dark:border-slate-700 hover:bg-slate-100 dark:hover:bg-slate-700'
                  ]"
                >
                  {{ preset.etiqueta }}
                </button>
              </div>

              <!-- Textarea para edición manual -->
              <textarea
                v-model="mensajeTicket"
                rows="2"
                maxlength="200"
                placeholder="Escribe un mensaje personalizado para el ticket..."
                class="w-full p-2 bg-white dark:bg-slate-900 border border-slate-300 dark:border-slate-700 rounded-xl text-xs text-slate-800 dark:text-slate-100 focus:outline-none focus:border-eden-500 font-mono"
              ></textarea>
              <div class="flex items-center justify-between text-3xs text-slate-400">
                <span>{{ mensajeTicket.length }}/200 caracteres</span>
                <button 
                  type="button" 
                  @click="guardarMensajeComoPredeterminado" 
                  class="text-eden-600 dark:text-eden-400 font-bold hover:underline"
                >
                  💾 Recordar como predeterminado
                </button>
              </div>
            </div>
          </div>

          <!-- Botón Principal Finalizar Cobro -->
          <div class="pt-4 border-t border-slate-100 dark:border-slate-800 space-y-2">
            <button 
              @click="procesarPago"
              :disabled="cobrando || (metodoPago === 'efectivo' && cambio < 0)"
              class="w-full py-4 px-4 bg-eden-600 hover:bg-eden-700 disabled:opacity-40 disabled:cursor-not-allowed text-white rounded-2xl font-black text-sm sm:text-base shadow-lg shadow-eden-600/20 transition-all active:scale-95 flex items-center justify-center gap-2 min-h-[56px]"
            >
              <span v-if="cobrando" class="animate-spin">🔄</span>
              <span v-if="cobrando">Procesando pago y liberando mesa...</span>
              <span v-else class="flex items-center gap-2">
                <span>✓ Finalizar Cobro (${{ totalConPropina.toFixed(2) }})</span>
              </span>
            </button>
            <p class="text-center text-3xs text-slate-400">
              Al finalizar, la orden se marcará como pagada y la mesa quedará liberada inmediatamente.
            </p>
          </div>

        </div>
      </div>
    </div>

    <!-- ================= MODAL: PRE-CUENTA TICKET COMENSAL ================= -->
    <div v-if="modalPreCuenta && ordenSeleccionada" class="fixed inset-0 bg-slate-900/60 backdrop-blur-sm flex items-center justify-center p-4 z-50">
      <div class="bg-white dark:bg-slate-900 rounded-3xl p-6 max-w-sm w-full shadow-2xl border border-slate-200 dark:border-slate-800 space-y-4">
        <div class="flex justify-between items-center border-b border-slate-100 dark:border-slate-800 pb-3">
          <div class="flex items-center gap-2">
            <span class="text-xl">🖨️</span>
            <h3 class="text-base font-black text-slate-800 dark:text-slate-100">Pre-Cuenta (Ticket Cliente)</h3>
          </div>
          <button @click="modalPreCuenta = false" class="text-slate-400 hover:text-slate-600 text-sm">✕</button>
        </div>

        <!-- Vista previa estilizada tipo papel térmico -->
        <div class="bg-amber-50/40 dark:bg-slate-950 p-4 rounded-2xl border border-amber-200/80 dark:border-slate-800 font-mono text-xs text-slate-800 dark:text-slate-200 space-y-3 shadow-inner">
          <div class="text-center border-b border-dashed border-slate-300 dark:border-slate-700 pb-2">
            <h4 class="font-bold text-sm tracking-widest uppercase">Edén Café</h4>
            <span class="text-3xs text-slate-500 block">Comida Tradicional y Café</span>
            <span class="text-3xs text-slate-400 block">*** PRE-CUENTA ***</span>
          </div>

          <div class="text-2xs space-y-0.5 border-b border-dashed border-slate-300 dark:border-slate-700 pb-2">
            <div>Ref: <strong>{{ obtenerNombreCabecera(ordenSeleccionada) }}</strong></div>
            <div>Folio: #{{ ordenSeleccionada.id }}</div>
            <div>Mesero: {{ ordenSeleccionada.mesero_nombre || 'N/A' }}</div>
            <div>Fecha: {{ new Date().toLocaleDateString('es-MX') }} {{ formatearHora(new Date()) }}</div>
          </div>

          <div class="space-y-1.5 max-h-48 overflow-y-auto text-2xs">
            <div v-for="it in itemsCobrables" :key="it.id" class="flex justify-between">
              <span>{{ it.cantidad }}x {{ it.producto_nombre }}</span>
              <span>${{ (Number(it.precio_unitario) * it.cantidad).toFixed(2) }}</span>
            </div>
          </div>

          <div class="border-t border-dashed border-slate-300 dark:border-slate-700 pt-2 space-y-1 text-xs">
            <div class="flex justify-between font-bold">
              <span>TOTAL:</span>
              <span class="text-sm">${{ Number(ordenSeleccionada.total).toFixed(2) }}</span>
            </div>
          </div>

          <div class="border-t border-dashed border-slate-300 dark:border-slate-700 pt-2 text-3xs text-center text-slate-500">
            Sugerencia propina (voluntaria):
            <div class="flex justify-around pt-1 text-2xs font-bold text-slate-700 dark:text-slate-300">
              <span>10%: ${{ (Number(ordenSeleccionada.total) * 0.10).toFixed(2) }}</span>
              <span>15%: ${{ (Number(ordenSeleccionada.total) * 0.15).toFixed(2) }}</span>
            </div>
          </div>

          <!-- Mensaje personalizado al pie en la vista previa -->
          <div v-if="mensajeTicket" class="border border-dashed border-slate-300 dark:border-slate-700 p-2 text-center text-3xs italic bg-white/70 dark:bg-slate-900/70 rounded-xl whitespace-pre-line text-slate-700 dark:text-slate-300">
            "{{ mensajeTicket }}"
          </div>
        </div>

        <!-- Selector rápido de mensaje en pre-cuenta -->
        <div class="text-xs space-y-1.5 pt-1">
          <div class="flex items-center justify-between">
            <span class="text-3xs font-bold text-slate-500">💬 Mensaje impreso al pie:</span>
            <button 
              type="button" 
              @click="mostrarEditorMensajeModal = !mostrarEditorMensajeModal"
              class="text-3xs text-eden-600 dark:text-eden-400 font-bold hover:underline"
            >
              {{ mostrarEditorMensajeModal ? 'Ocultar' : 'Cambiar mensaje' }}
            </button>
          </div>
          <div v-if="mostrarEditorMensajeModal" class="space-y-1.5 animate-in fade-in">
            <div class="flex flex-wrap gap-1">
              <button 
                v-for="preset in plantillasMensaje" 
                :key="preset.id"
                type="button"
                @click="seleccionarPlantilla(preset)"
                :class="[
                  'px-1.5 py-0.5 rounded text-3xs font-extrabold border',
                  mensajeTicket === preset.texto
                    ? 'bg-eden-600 text-white border-eden-600'
                    : 'bg-slate-100 dark:bg-slate-800 text-slate-600 dark:text-slate-300 border-slate-200 dark:border-slate-700'
                ]"
              >
                {{ preset.etiqueta }}
              </button>
            </div>
            <textarea
              v-model="mensajeTicket"
              rows="2"
              placeholder="Mensaje personalizado..."
              class="w-full p-1.5 bg-slate-50 dark:bg-slate-800 border border-slate-300 dark:border-slate-700 rounded-lg text-2xs font-mono"
            ></textarea>
          </div>
        </div>

        <div class="flex gap-2 pt-2">
          <button 
            @click="imprimirPreCuentaDirecto"
            class="flex-1 py-3 bg-eden-600 hover:bg-eden-700 text-white rounded-xl text-xs font-black transition active:scale-95 flex items-center justify-center gap-1.5"
          >
            <span>🖨️</span> Imprimir Ticket Térmico
          </button>
          <button 
            @click="modalPreCuenta = false"
            class="px-4 py-3 bg-slate-100 dark:bg-slate-800 text-slate-700 dark:text-slate-300 rounded-xl text-xs font-bold transition hover:bg-slate-200"
          >
            Cerrar
          </button>
        </div>
      </div>
    </div>

    <!-- ================= MODAL: ÉXITO DE COBRO Y TICKET FINAL ================= -->
    <div v-if="modalCobroExitoso && ultimoPago" class="fixed inset-0 bg-slate-900/60 backdrop-blur-sm flex items-center justify-center p-4 z-50">
      <div class="bg-white dark:bg-slate-900 rounded-3xl p-6 max-w-sm w-full shadow-2xl border border-slate-200 dark:border-slate-800 text-center space-y-4 animate-in fade-in zoom-in-95">
        <div class="w-16 h-16 rounded-full bg-emerald-100 dark:bg-emerald-950/80 text-emerald-600 flex items-center justify-center text-3xl mx-auto border-2 border-emerald-300 dark:border-emerald-800 shadow-sm">
          ✓
        </div>

        <div>
          <h3 class="text-xl font-black text-slate-800 dark:text-slate-100">¡Cobro Exitoso!</h3>
          <p class="text-xs text-slate-500 mt-1">
            La comanda ha sido liquidada y la mesa se encuentra libre para nuevos comensales.
          </p>
        </div>

        <div class="p-3.5 rounded-2xl bg-slate-50 dark:bg-slate-800/60 border border-slate-200 dark:border-slate-700 text-xs space-y-1.5 text-left font-mono">
          <div class="flex justify-between">
            <span class="text-slate-500">Folio Pago:</span>
            <span class="font-bold">#{{ ultimoPago.id }}</span>
          </div>
          <div class="flex justify-between">
            <span class="text-slate-500">Método:</span>
            <span class="font-bold uppercase">{{ ultimoPago.metodo }}</span>
          </div>
          <div class="flex justify-between">
            <span class="text-slate-500">Consumo:</span>
            <span class="font-bold">${{ Number(ultimoPago.monto).toFixed(2) }}</span>
          </div>
          <div v-if="Number(ultimoPago.propina || 0) > 0" class="flex justify-between text-eden-600 dark:text-eden-400">
            <span>Propina:</span>
            <span class="font-bold">+${{ Number(ultimoPago.propina).toFixed(2) }}</span>
          </div>
          <div v-if="ultimoPago.metodo === 'efectivo'" class="flex justify-between border-t border-slate-200 dark:border-slate-700 pt-1 text-emerald-700 dark:text-emerald-400 font-black">
            <span>Cambio entregado:</span>
            <span>${{ Number(ultimoPago.cambio).toFixed(2) }}</span>
          </div>
        </div>

        <!-- Mensaje para el ticket de venta -->
        <div class="text-left bg-slate-50 dark:bg-slate-800/50 p-2.5 rounded-xl border border-slate-200 dark:border-slate-700 space-y-1 text-xs">
          <div class="flex items-center justify-between">
            <span class="text-3xs font-bold text-slate-500">💬 Mensaje en ticket:</span>
            <button 
              type="button" 
              @click="mostrarEditorMensajeModal = !mostrarEditorMensajeModal"
              class="text-3xs text-eden-600 dark:text-eden-400 font-bold hover:underline"
            >
              {{ mostrarEditorMensajeModal ? 'Listo' : 'Modificar' }}
            </button>
          </div>
          <p v-if="!mostrarEditorMensajeModal" class="text-3xs text-slate-600 dark:text-slate-300 italic truncate">
            "{{ mensajeTicket || 'Sin mensaje adicional' }}"
          </p>
          <div v-if="mostrarEditorMensajeModal" class="space-y-1.5 pt-1 animate-in fade-in">
            <div class="flex flex-wrap gap-1">
              <button 
                v-for="preset in plantillasMensaje" 
                :key="preset.id"
                type="button"
                @click="seleccionarPlantilla(preset)"
                :class="[
                  'px-1.5 py-0.5 rounded text-3xs font-extrabold border',
                  mensajeTicket === preset.texto
                    ? 'bg-eden-600 text-white border-eden-600'
                    : 'bg-white dark:bg-slate-900 text-slate-600 dark:text-slate-300 border-slate-200 dark:border-slate-700'
                ]"
              >
                {{ preset.etiqueta }}
              </button>
            </div>
            <textarea
              v-model="mensajeTicket"
              rows="2"
              class="w-full p-1.5 bg-white dark:bg-slate-900 border border-slate-300 dark:border-slate-700 rounded-lg text-2xs font-mono"
            ></textarea>
          </div>
        </div>

        <div class="space-y-2 pt-2">
          <button 
            @click="imprimirTicketVentaDirecto"
            class="w-full py-3.5 bg-slate-900 dark:bg-eden-600 hover:bg-slate-800 text-white rounded-2xl text-xs font-black shadow-md transition active:scale-95 flex items-center justify-center gap-2"
          >
            <span>🖨️</span> Imprimir Ticket de Venta
          </button>
          <button 
            @click="cerrarModalCobroExitoso"
            class="w-full py-2.5 bg-slate-100 dark:bg-slate-800 hover:bg-slate-200 text-slate-700 dark:text-slate-300 rounded-xl text-xs font-bold transition"
          >
            Listo / Siguiente Comanda
          </button>
        </div>
      </div>
    </div>

    <!-- ================= MODAL: CORTE X (ARQUEO PARCIAL) ================= -->
    <div v-if="modalCorteX && datosCorteX" class="fixed inset-0 bg-slate-900/60 backdrop-blur-sm flex items-center justify-center p-4 z-50">
      <div class="bg-white dark:bg-slate-900 rounded-3xl p-6 max-w-md w-full shadow-2xl border border-slate-200 dark:border-slate-800 space-y-4">
        <div class="flex justify-between items-center border-b border-slate-100 dark:border-slate-800 pb-3">
          <div class="flex items-center gap-2">
            <span class="text-2xl">📊</span>
            <div>
              <h3 class="text-base font-black text-slate-800 dark:text-slate-100">Arqueo Parcial (Corte X)</h3>
              <span class="text-3xs text-slate-400">Resumen acumulado del turno o jornada</span>
            </div>
          </div>
          <button @click="modalCorteX = false" class="text-slate-400 hover:text-slate-600 text-sm">✕</button>
        </div>

        <div class="space-y-2.5 text-xs">
          <div class="flex justify-between py-1.5 border-b border-slate-100 dark:border-slate-800 text-slate-700 dark:text-slate-300">
            <span>Órdenes Liquidadas</span>
            <span class="font-bold">{{ datosCorteX.ordenes_cobradas }}</span>
          </div>
          <div v-if="Number(datosCorteX.monto_apertura || 0) > 0" class="flex justify-between py-1.5 border-b border-slate-100 dark:border-slate-800 text-slate-700 dark:text-slate-300">
            <span>Fondo Inicial de Caja</span>
            <span class="font-mono font-bold text-slate-900 dark:text-slate-100">${{ Number(datosCorteX.monto_apertura).toFixed(2) }}</span>
          </div>
          <div class="flex justify-between py-1.5 border-b border-slate-100 dark:border-slate-800 text-slate-700 dark:text-slate-300">
            <span>Ventas en Efectivo</span>
            <span class="font-mono font-bold text-slate-900 dark:text-slate-100">${{ Number(datosCorteX.total_efectivo).toFixed(2) }}</span>
          </div>
          <div class="flex justify-between py-1.5 border-b border-slate-100 dark:border-slate-800 text-slate-700 dark:text-slate-300">
            <span>Tarjetas (Crédito/Débito)</span>
            <span class="font-mono font-bold text-slate-900 dark:text-slate-100">${{ Number(datosCorteX.total_tarjeta).toFixed(2) }}</span>
          </div>
          <div class="flex justify-between py-1.5 border-b border-slate-100 dark:border-slate-800 text-slate-700 dark:text-slate-300">
            <span>Transferencias SPEI</span>
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
          <div v-if="Number(datosCorteX.total_efectivo_en_caja || 0) > 0" class="flex justify-between text-xs font-black p-2.5 rounded-xl bg-slate-50 dark:bg-slate-800 text-slate-800 dark:text-slate-200">
            <span>Efectivo Físico Esperado en Cajón:</span>
            <span class="font-mono">${{ Number(datosCorteX.total_efectivo_en_caja).toFixed(2) }}</span>
          </div>
        </div>

        <div class="pt-3 border-t border-slate-100 dark:border-slate-800 flex justify-end gap-2">
          <button 
            @click="modalCorteX = false"
            class="px-5 py-2.5 bg-slate-900 dark:bg-slate-700 text-white rounded-xl text-xs font-bold transition hover:bg-slate-800"
          >
            Cerrar Resumen
          </button>
        </div>
      </div>
    </div>

    <!-- ================= MODAL: ABRIR TURNO DE CAJA ================= -->
    <div v-if="modalAbrirTurno" class="fixed inset-0 bg-slate-900/60 backdrop-blur-sm flex items-center justify-center p-4 z-50">
      <div class="bg-white dark:bg-slate-900 rounded-3xl p-6 max-w-sm w-full shadow-2xl border border-slate-200 dark:border-slate-800 space-y-4">
        <div class="flex justify-between items-center border-b border-slate-100 dark:border-slate-800 pb-3">
          <div class="flex items-center gap-2">
            <span class="text-xl">🟢</span>
            <h3 class="text-base font-black text-slate-800 dark:text-slate-100">Apertura de Turno</h3>
          </div>
          <button @click="modalAbrirTurno = false" class="text-slate-400 hover:text-slate-600 text-sm">✕</button>
        </div>

        <div class="space-y-3 text-xs">
          <div>
            <label class="block font-bold text-slate-700 dark:text-slate-300 mb-1">
              Fondo de Caja Inicial (Cambio base en efectivo)
            </label>
            <input 
              v-model.number="formApertura.monto" 
              type="number"
              min="0"
              step="50"
              placeholder="Ej. 500.00"
              class="w-full text-xl font-mono font-black p-3 bg-white dark:bg-slate-800 border border-slate-300 dark:border-slate-700 rounded-xl text-slate-900 dark:text-slate-100 focus:outline-none focus:border-eden-500"
            />
          </div>

          <div>
            <label class="block font-bold text-slate-700 dark:text-slate-300 mb-1">
              Notas u observaciones (Opcional)
            </label>
            <input 
              v-model="formApertura.notas" 
              type="text"
              placeholder="Ej. Turno matutino, billetes chicos"
              class="w-full p-2.5 bg-white dark:bg-slate-800 border border-slate-300 dark:border-slate-700 rounded-xl text-xs text-slate-900 dark:text-slate-100 focus:outline-none focus:border-eden-500"
            />
          </div>
        </div>

        <div class="flex gap-2 pt-2">
          <button 
            @click="confirmarAbrirTurno"
            :disabled="guardandoTurno"
            class="flex-1 py-3 bg-eden-600 hover:bg-eden-700 text-white rounded-xl text-xs font-black transition active:scale-95"
          >
            {{ guardandoTurno ? 'Abriendo...' : 'Iniciar Turno' }}
          </button>
          <button 
            @click="modalAbrirTurno = false"
            class="px-4 py-3 bg-slate-100 dark:bg-slate-800 text-slate-700 dark:text-slate-300 rounded-xl text-xs font-bold transition hover:bg-slate-200"
          >
            Cancelar
          </button>
        </div>
      </div>
    </div>

    <!-- ================= MODAL: CIERRE DE TURNO (CORTE Z) ================= -->
    <div v-if="modalCerrarTurno" class="fixed inset-0 bg-slate-900/60 backdrop-blur-sm flex items-center justify-center p-4 z-50">
      <div class="bg-white dark:bg-slate-900 rounded-3xl p-6 max-w-md w-full shadow-2xl border border-slate-200 dark:border-slate-800 space-y-4">
        <div class="flex justify-between items-center border-b border-slate-100 dark:border-slate-800 pb-3">
          <div class="flex items-center gap-2">
            <span class="text-xl">🔒</span>
            <div>
              <h3 class="text-base font-black text-slate-800 dark:text-slate-100">Cierre de Turno (Corte Z)</h3>
              <span class="text-3xs text-slate-400">Arqueo definitivo y entrega de turno</span>
            </div>
          </div>
          <button @click="modalCerrarTurno = false" class="text-slate-400 hover:text-slate-600 text-sm">✕</button>
        </div>

        <div class="space-y-3 text-xs">
          <div class="p-3 bg-amber-50 dark:bg-amber-950/40 rounded-xl border border-amber-200 dark:border-amber-900/60 text-amber-900 dark:text-amber-300 text-2xs">
            ⚠️ Cuenta todo el dinero en efectivo del cajón físico (incluyendo el fondo inicial) e ingresa el monto a continuación:
          </div>

          <div>
            <label class="block font-bold text-slate-700 dark:text-slate-300 mb-1">
              Efectivo Contado en Caja ($)
            </label>
            <input 
              v-model.number="formCierre.monto_declarado" 
              type="number"
              min="0"
              step="1"
              placeholder="0.00"
              class="w-full text-2xl font-mono font-black p-3 bg-white dark:bg-slate-800 border-2 border-slate-300 dark:border-slate-700 rounded-xl text-slate-900 dark:text-slate-100 focus:outline-none focus:border-eden-500"
            />
          </div>

          <div v-if="cajaStore.turnoActivo" class="p-3 rounded-xl bg-slate-50 dark:bg-slate-800 space-y-1 font-mono text-2xs">
            <div class="flex justify-between">
              <span>Efectivo Esperado (Fondo + Ventas):</span>
              <span class="font-bold">${{ Number(cajaStore.turnoActivo.total_efectivo_en_caja).toFixed(2) }}</span>
            </div>
            <div class="flex justify-between font-bold" :class="diferenciaCierre >= 0 ? 'text-emerald-600' : 'text-rose-600'">
              <span>Diferencia:</span>
              <span>{{ diferenciaCierre >= 0 ? `+$${diferenciaCierre.toFixed(2)} (Sobrante/Exacto)` : `-$${Math.abs(diferenciaCierre).toFixed(2)} (Faltante)` }}</span>
            </div>
          </div>

          <div>
            <label class="block font-bold text-slate-700 dark:text-slate-300 mb-1">
              Notas finales de cierre
            </label>
            <input 
              v-model="formCierre.notas" 
              type="text"
              placeholder="Ej. Cuadre exacto, entrega a encargado"
              class="w-full p-2.5 bg-white dark:bg-slate-800 border border-slate-300 dark:border-slate-700 rounded-xl text-xs text-slate-900 dark:text-slate-100 focus:outline-none focus:border-eden-500"
            />
          </div>
        </div>

        <div class="flex gap-2 pt-2">
          <button 
            @click="confirmarCierreTurno"
            :disabled="guardandoTurno"
            class="flex-1 py-3 bg-rose-600 hover:bg-rose-700 text-white rounded-xl text-xs font-black transition active:scale-95"
          >
            {{ guardandoTurno ? 'Cerrando...' : 'Confirmar Cierre Definitivo' }}
          </button>
          <button 
            @click="modalCerrarTurno = false"
            class="px-4 py-3 bg-slate-100 dark:bg-slate-800 text-slate-700 dark:text-slate-300 rounded-xl text-xs font-bold transition hover:bg-slate-200"
          >
            Cancelar
          </button>
        </div>
      </div>
    </div>

    <!-- ================= MODAL: DESCUENTO O CUPÓN ================= -->
    <div v-if="modalDescuento" class="fixed inset-0 bg-slate-900/60 backdrop-blur-sm flex items-center justify-center p-4 z-50">
      <div class="bg-white dark:bg-slate-900 rounded-3xl p-6 max-w-md w-full shadow-2xl border border-slate-200 dark:border-slate-800 space-y-4">
        <div class="flex justify-between items-center border-b border-slate-100 dark:border-slate-800 pb-3">
          <div class="flex items-center gap-2">
            <span class="text-xl">🏷️</span>
            <div>
              <h3 class="text-base font-black text-slate-800 dark:text-slate-100">Descuento o Cupón</h3>
              <span class="text-3xs text-slate-400">Aplicar cortesía, porcentaje o código promocional</span>
            </div>
          </div>
          <button @click="modalDescuento = false" class="text-slate-400 hover:text-slate-600 text-sm font-bold">✕</button>
        </div>

        <!-- Selector de Tipo de Descuento (3 pestañas) -->
        <div class="grid grid-cols-3 gap-1.5 p-1 bg-slate-100 dark:bg-slate-800 rounded-2xl">
          <button 
            type="button"
            @click="formDescuento.tipo = 'porcentaje'"
            :class="[
              'py-2 rounded-xl text-xs font-black transition text-center',
              formDescuento.tipo === 'porcentaje' ? 'bg-white dark:bg-slate-900 text-eden-700 dark:text-eden-400 shadow-xs' : 'text-slate-500'
            ]"
          >
            % Porcentaje
          </button>
          <button 
            type="button"
            @click="formDescuento.tipo = 'fijo'"
            :class="[
              'py-2 rounded-xl text-xs font-black transition text-center',
              formDescuento.tipo === 'fijo' ? 'bg-white dark:bg-slate-900 text-eden-700 dark:text-eden-400 shadow-xs' : 'text-slate-500'
            ]"
          >
            $ Monto Fijo
          </button>
          <button 
            type="button"
            @click="formDescuento.tipo = 'cupon'"
            :class="[
              'py-2 rounded-xl text-xs font-black transition text-center',
              formDescuento.tipo === 'cupon' ? 'bg-white dark:bg-slate-900 text-eden-700 dark:text-eden-400 shadow-xs' : 'text-slate-500'
            ]"
          >
            🎟️ Cupón
          </button>
        </div>

        <!-- 1. Opción Porcentaje -->
        <div v-if="formDescuento.tipo === 'porcentaje'" class="space-y-3 text-xs">
          <label class="block font-bold text-slate-700 dark:text-slate-300">
            Porcentaje de Descuento
          </label>
          <div class="grid grid-cols-5 gap-1.5">
            <button 
              v-for="p in [5, 10, 15, 20, 50]" 
              :key="p"
              type="button"
              @click="formDescuento.valor = p"
              :class="[
                'py-2 rounded-xl font-black border transition active:scale-95 text-center',
                formDescuento.valor === p ? 'bg-eden-600 text-white border-eden-600' : 'bg-slate-50 dark:bg-slate-800 text-slate-700 dark:text-slate-300 border-slate-200 dark:border-slate-700'
              ]"
            >
              {{ p }}%
            </button>
          </div>
          <div>
            <span class="text-3xs text-slate-400 font-bold block mb-1">O ingresa un porcentaje específico:</span>
            <input 
              v-model.number="formDescuento.valor" 
              type="number" 
              min="1" 
              max="100" 
              step="1"
              placeholder="Ej. 25"
              class="w-full p-2.5 bg-slate-50 dark:bg-slate-800 border border-slate-300 dark:border-slate-700 rounded-xl text-sm font-mono font-black text-slate-800 dark:text-slate-100 focus:outline-none focus:border-eden-500"
            />
          </div>
        </div>

        <!-- 2. Opción Monto Fijo -->
        <div v-else-if="formDescuento.tipo === 'fijo'" class="space-y-3 text-xs">
          <label class="block font-bold text-slate-700 dark:text-slate-300">
            Monto Fijo en Pesos ($ MXN)
          </label>
          <div class="grid grid-cols-4 gap-1.5">
            <button 
              v-for="m in [20, 50, 100, 200]" 
              :key="m"
              type="button"
              @click="formDescuento.valor = m"
              :class="[
                'py-2 rounded-xl font-black border transition active:scale-95 text-center',
                formDescuento.valor === m ? 'bg-eden-600 text-white border-eden-600' : 'bg-slate-50 dark:bg-slate-800 text-slate-700 dark:text-slate-300 border-slate-200 dark:border-slate-700'
              ]"
            >
              ${{ m }}
            </button>
          </div>
          <div>
            <span class="text-3xs text-slate-400 font-bold block mb-1">O ingresa un monto libre:</span>
            <input 
              v-model.number="formDescuento.valor" 
              type="number" 
              min="1" 
              :max="subtotalSinEnvio"
              step="5"
              placeholder="0.00"
              class="w-full p-2.5 bg-slate-50 dark:bg-slate-800 border border-slate-300 dark:border-slate-700 rounded-xl text-sm font-mono font-black text-slate-800 dark:text-slate-100 focus:outline-none focus:border-eden-500"
            />
          </div>
        </div>

        <!-- 3. Opción Cupón -->
        <div v-else-if="formDescuento.tipo === 'cupon'" class="space-y-3 text-xs">
          <label class="block font-bold text-slate-700 dark:text-slate-300">
            Código de Cupón Promocional
          </label>
          <div class="flex flex-wrap gap-1.5">
            <button 
              v-for="c in [
                { cod: 'EDEN10', desc: '10% OFF' },
                { cod: 'BIENVENIDA', desc: '15% OFF' },
                { cod: 'PROMO20', desc: '20% OFF' },
                { cod: 'CAFE50', desc: '$50 OFF' }
              ]"
              :key="c.cod"
              type="button"
              @click="formDescuento.cupon = c.cod"
              :class="[
                'px-2.5 py-1.5 rounded-xl font-black text-2xs border transition active:scale-95 flex items-center gap-1',
                formDescuento.cupon === c.cod ? 'bg-eden-600 text-white border-eden-600' : 'bg-slate-50 dark:bg-slate-800 text-slate-700 dark:text-slate-300 border-slate-200 dark:border-slate-700'
              ]"
            >
              <span>🎟️</span>
              <span>{{ c.cod }} ({{ c.desc }})</span>
            </button>
          </div>
          <div>
            <input 
              v-model="formDescuento.cupon" 
              type="text" 
              placeholder="Ingresa código de cupón..."
              class="w-full p-2.5 bg-slate-50 dark:bg-slate-800 border border-slate-300 dark:border-slate-700 rounded-xl text-xs font-mono font-black uppercase text-slate-800 dark:text-slate-100 focus:outline-none focus:border-eden-500 tracking-wider"
            />
          </div>
        </div>

        <!-- Motivo del Descuento -->
        <div class="space-y-1.5 text-xs">
          <label class="block font-bold text-slate-700 dark:text-slate-300">
            Motivo o Justificación (Opcional)
          </label>
          <div class="flex flex-wrap gap-1">
            <button 
              v-for="mot in ['Cortesía', 'Convenio / Empleado', 'Cliente Frecuente', 'Promoción del Día', 'Aclaración']" 
              :key="mot"
              type="button"
              @click="formDescuento.motivo = mot"
              :class="[
                'px-2 py-1 rounded-lg text-3xs font-extrabold border',
                formDescuento.motivo === mot ? 'bg-slate-800 text-white' : 'bg-slate-50 dark:bg-slate-800 text-slate-600 dark:text-slate-300 border-slate-200 dark:border-slate-700'
              ]"
            >
              {{ mot }}
            </button>
          </div>
          <input 
            v-model="formDescuento.motivo"
            type="text"
            placeholder="Especificar motivo..."
            class="w-full p-2 bg-slate-50 dark:bg-slate-800 border border-slate-300 dark:border-slate-700 rounded-xl text-xs text-slate-800 dark:text-slate-100"
          />
        </div>

        <!-- PIN de Autorización -->
        <div class="space-y-1 text-xs pt-1 border-t border-slate-100 dark:border-slate-800">
          <label class="block font-bold text-slate-700 dark:text-slate-300">
            PIN de Autorización (Gerente / Administrador)
          </label>
          <input 
            v-model="formDescuento.pin_autorizacion"
            type="password"
            maxlength="4"
            inputmode="numeric"
            placeholder="•••• (Opcional si ya eres admin)"
            class="w-full p-2 bg-slate-50 dark:bg-slate-800 border border-slate-300 dark:border-slate-700 rounded-xl text-center font-mono tracking-widest text-sm"
          />
        </div>

        <!-- Resumen del Descuento -->
        <div class="p-3 rounded-2xl bg-slate-50 dark:bg-slate-800/60 border border-slate-200 dark:border-slate-700 text-xs font-mono space-y-1">
          <div class="flex justify-between">
            <span class="text-slate-500">Subtotal productos:</span>
            <span>${{ subtotalSinEnvio.toFixed(2) }}</span>
          </div>
          <div class="flex justify-between text-rose-600 dark:text-rose-400 font-bold">
            <span>Descuento estimado:</span>
            <span>-${{ montoDescuentoCalculado.toFixed(2) }}</span>
          </div>
          <div class="flex justify-between font-black text-sm border-t border-slate-200 dark:border-slate-700 pt-1 text-slate-900 dark:text-slate-100">
            <span>Nuevo Total Orden:</span>
            <span>${{ nuevoTotalConDescuento.toFixed(2) }}</span>
          </div>
        </div>

        <div class="flex gap-2 pt-2">
          <button 
            type="button"
            @click="confirmarAplicarDescuento"
            :disabled="aplicandoDescuento || montoDescuentoCalculado <= 0"
            class="flex-1 py-3 bg-eden-600 hover:bg-eden-700 disabled:opacity-40 text-white rounded-xl text-xs font-black transition active:scale-95 flex items-center justify-center gap-1.5"
          >
            <span v-if="aplicandoDescuento">Aplicando...</span>
            <span v-else>✓ Aplicar Descuento (-${{ montoDescuentoCalculado.toFixed(2) }})</span>
          </button>
          <button 
            type="button"
            @click="modalDescuento = false"
            class="px-4 py-3 bg-slate-100 dark:bg-slate-800 text-slate-700 dark:text-slate-300 rounded-xl text-xs font-bold transition hover:bg-slate-200"
          >
            Cancelar
          </button>
        </div>
      </div>
    </div>

  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted, watch } from 'vue'
import { useCajaStore } from '../stores/caja'
import { useMesasStore } from '../stores/mesas'
import { generarTicketPreCuenta, generarTicketVenta, imprimirContenidoHtml } from '../utils/ticketPrinter'

const cajaStore = useCajaStore()
const mesasStore = useMesasStore()

let timer = null
const cargandoManual = ref(false)

// Selección y filtro
const ordenSeleccionada = ref(null)
const filtroActivo = ref('todas')
const busqueda = ref('')

// Variables de pago
const metodoPago = ref('efectivo')
const tipoPropina = ref('pct') // 'pct' o 'monto'
const porcentajePropina = ref(0)
const propinaManual = ref(0)
const montoRecibido = ref(0)
const referenciaPago = ref('')
const cobrando = ref(false)

// Mensaje en Ticket (Personalizado o Seleccionado)
const mostrarEditorMensaje = ref(false)
const mostrarEditorMensajeModal = ref(false)
const mensajeTicket = ref(
  localStorage.getItem('eden_ticket_msg') ?? '🎉 ¡Gracias por su visita y preferencia! Vuelva pronto.'
)

const plantillasMensaje = [
  { id: 'gracias', etiqueta: '🎉 Agradecimiento', texto: '🎉 ¡Gracias por su visita y preferencia! Vuelva pronto.' },
  { id: 'wifi', etiqueta: '📶 Red Wi-Fi', texto: '📶 Wi-Fi Clientes: EdenCafe_Clientes\n🔑 Clave: CafeTradicional2026' },
  { id: 'factura', etiqueta: '🧾 Facturación', texto: '🧾 Solicite su factura enviando foto de su ticket a:\n📧 facturas@edencafe.com antes de fin de mes.' },
  { id: 'promo', etiqueta: '☕ Promo Café', texto: '☕ Presente este ticket en su próxima visita y reciba 10% de descuento en café americano.' },
  { id: 'cumple', etiqueta: '🎂 Cumpleaños', texto: '🎂 ¡Feliz cumpleaños! Gracias por celebrar con nosotros en Edén Café.' },
  { id: 'opinion', etiqueta: '⭐ Google Maps', texto: '⭐ ¿Le gustó nuestro servicio? Déjenos su opinión en Google Maps.' },
  { id: 'vacio', etiqueta: '🚫 Sin mensaje', texto: '' }
]

const seleccionarPlantilla = (preset) => {
  mensajeTicket.value = preset.texto
}

const guardarMensajeComoPredeterminado = () => {
  localStorage.setItem('eden_ticket_msg', mensajeTicket.value)
  alert('Mensaje guardado como predeterminado para futuros tickets.')
}

// Modales
const modalPreCuenta = ref(false)
const modalCobroExitoso = ref(false)
const ultimoPago = ref(null)
const ordenPagada = ref(null)

const modalCorteX = ref(false)
const datosCorteX = ref(null)

const modalAbrirTurno = ref(false)
const formApertura = ref({ monto: 500, notas: '' })

const modalCerrarTurno = ref(false)
const formCierre = ref({ monto_declarado: 0, notas: '' })
const guardandoTurno = ref(false)

// Modales y estado de Descuentos / Cupones
const modalDescuento = ref(false)
const aplicandoDescuento = ref(false)
const quitandoDescuento = ref(false)
const formDescuento = ref({
  tipo: 'porcentaje',
  valor: 10,
  cupon: 'EDEN10',
  motivo: 'Promoción del Día',
  pin_autorizacion: ''
})

// Lifecycle
onMounted(async () => {
  await cargarTodo()
  // Polling automático cada 4 segundos
  timer = setInterval(() => {
    cajaStore.cargarCuentasPendientes(true)
    cajaStore.obtenerTurnoActivo()
  }, 4000)
})

onUnmounted(() => {
  if (timer) clearInterval(timer)
})

const cargarTodo = async () => {
  await Promise.all([
    cajaStore.cargarCuentasPendientes(),
    cajaStore.obtenerTurnoActivo()
  ])
  if (cajaStore.cuentasPendientes.length > 0 && !ordenSeleccionada.value) {
    ordenSeleccionada.value = cajaStore.cuentasPendientes[0]
  }
}

const actualizarManual = async () => {
  cargandoManual.value = true
  try {
    await cargarTodo()
  } finally {
    setTimeout(() => {
      cargandoManual.value = false
    }, 400)
  }
}

// Mantener orden seleccionada actualizada cuando cambia el array de cuentas
watch(() => cajaStore.cuentasPendientes, (nuevas) => {
  if (!nuevas || nuevas.length === 0) {
    ordenSeleccionada.value = null
    return
  }
  if (ordenSeleccionada.value) {
    const vigente = nuevas.find(o => o.id === ordenSeleccionada.value.id)
    if (vigente) {
      ordenSeleccionada.value = vigente
    } else {
      ordenSeleccionada.value = nuevas[0]
    }
  } else {
    ordenSeleccionada.value = nuevas[0]
  }
}, { deep: true })

// Resetear montos al cambiar de orden seleccionada
watch(() => ordenSeleccionada.value?.id, () => {
  if (ordenSeleccionada.value) {
    tipoPropina.value = 'pct'
    porcentajePropina.value = 0
    propinaManual.value = 0
    referenciaPago.value = ''
    montoRecibido.value = Number(ordenSeleccionada.value.total)
  }
})

// Pestañas y filtros
const cuentasFiltradas = computed(() => {
  let list = cajaStore.cuentasPendientes || []

  // Filtro por pestaña
  if (filtroActivo.value === 'cuenta') {
    list = list.filter(o => o.mesa_estado === 'cuenta')
  } else if (filtroActivo.value === 'domicilio') {
    list = list.filter(o => o.tipo_pedido === 'domicilio')
  } else if (filtroActivo.value === 'llevar') {
    list = list.filter(o => o.tipo_pedido === 'para_llevar')
  } else if (filtroActivo.value === 'comedor') {
    list = list.filter(o => o.tipo_pedido === 'comedor' && o.mesa_estado !== 'cuenta')
  }

  // Filtro por texto de búsqueda
  if (busqueda.value.trim()) {
    const q = busqueda.value.toLowerCase().trim()
    list = list.filter(o => {
      const mesa = (o.mesa_numero || `Mesa ${o.mesa_id}`).toLowerCase()
      const mesero = (o.mesero_nombre || '').toLowerCase()
      const folio = String(o.id)
      const cliente = (o.datos_entrega?.cliente || '').toLowerCase()
      return mesa.includes(q) || mesero.includes(q) || folio.includes(q) || cliente.includes(q)
    })
  }

  return list
})

const tabsFiltro = computed(() => {
  const todas = cajaStore.cuentasPendientes || []
  const cuentasPiden = todas.filter(o => o.mesa_estado === 'cuenta')
  const envios = todas.filter(o => o.tipo_pedido === 'domicilio')
  const llevar = todas.filter(o => o.tipo_pedido === 'para_llevar')
  const comedor = todas.filter(o => o.tipo_pedido === 'comedor' && o.mesa_estado !== 'cuenta')

  return [
    {
      id: 'todas',
      label: 'Todas',
      emoji: '📋',
      count: todas.length,
      activeClass: 'bg-slate-900 dark:bg-slate-100 text-white dark:text-slate-900 shadow-sm'
    },
    {
      id: 'cuenta',
      label: 'Por Cobrar',
      emoji: '🔔',
      count: cuentasPiden.length,
      activeClass: 'bg-amber-500 text-white shadow-sm ring-2 ring-amber-400'
    },
    {
      id: 'domicilio',
      label: 'Envíos',
      emoji: '🛵',
      count: envios.length,
      activeClass: 'bg-blue-600 text-white shadow-sm'
    },
    {
      id: 'llevar',
      label: 'Para Llevar',
      emoji: '🛍️',
      count: llevar.length,
      activeClass: 'bg-orange-600 text-white shadow-sm'
    },
    {
      id: 'comedor',
      label: 'En Mesa',
      emoji: '🍽️',
      count: comedor.length,
      activeClass: 'bg-eden-600 text-white shadow-sm'
    }
  ]
})

const seleccionarOrden = (orden) => {
  ordenSeleccionada.value = orden
  montoRecibido.value = Number(orden.total)
}

// Detalle items cobrables
const itemsCobrables = computed(() => {
  if (!ordenSeleccionada.value?.items) return []
  return ordenSeleccionada.value.items.filter(i => i.estado !== 'cancelado')
})

const subtotalSinEnvio = computed(() => {
  if (!ordenSeleccionada.value) return 0
  if (ordenSeleccionada.value.subtotal != null) {
    return Number(ordenSeleccionada.value.subtotal)
  }
  return Number(ordenSeleccionada.value.total) - Number(ordenSeleccionada.value.costo_envio || 0) + Number(ordenSeleccionada.value.descuento || 0)
})

const abrirModalDescuento = () => {
  formDescuento.value = {
    tipo: 'porcentaje',
    valor: 10,
    cupon: 'EDEN10',
    motivo: 'Promoción del Día',
    pin_autorizacion: ''
  }
  modalDescuento.value = true
}

const montoDescuentoCalculado = computed(() => {
  if (!ordenSeleccionada.value) return 0
  const sub = subtotalSinEnvio.value
  if (formDescuento.value.tipo === 'porcentaje') {
    const pct = Math.min(100, Math.max(0, Number(formDescuento.value.valor || 0)))
    return (sub * pct) / 100
  } else if (formDescuento.value.tipo === 'fijo') {
    return Math.min(sub, Math.max(0, Number(formDescuento.value.valor || 0)))
  } else if (formDescuento.value.tipo === 'cupon') {
    const cod = (formDescuento.value.cupon || '').trim().toUpperCase()
    if (cod === 'EDEN10') return (sub * 10) / 100
    if (cod === 'EDEN15' || cod === 'BIENVENIDA') return (sub * 15) / 100
    if (cod === 'PROMO20') return (sub * 20) / 100
    if (cod === 'CAFE50') return Math.min(sub, 50)
    if (formDescuento.value.valor > 0) return Math.min(sub, Number(formDescuento.value.valor))
    return 0
  }
  return 0
})

const nuevoTotalConDescuento = computed(() => {
  if (!ordenSeleccionada.value) return 0
  const sub = subtotalSinEnvio.value
  const envio = Number(ordenSeleccionada.value.costo_envio || 0)
  return Math.max(0, sub + envio - montoDescuentoCalculado.value)
})

const confirmarAplicarDescuento = async () => {
  if (!ordenSeleccionada.value) return
  aplicandoDescuento.value = true
  try {
    const payload = {
      orden_id: ordenSeleccionada.value.id,
      tipo_descuento: formDescuento.value.tipo,
      valor: formDescuento.value.tipo === 'cupon' ? (formDescuento.value.valor || 0) : formDescuento.value.valor,
      cupon: formDescuento.value.tipo === 'cupon' ? formDescuento.value.cupon : null,
      motivo: formDescuento.value.motivo || null,
      pin_autorizacion: formDescuento.value.pin_autorizacion || null
    }
    const ordenActualizada = await cajaStore.aplicarDescuento(payload)
    ordenSeleccionada.value = ordenActualizada
    montoRecibido.value = Number(ordenActualizada.total) + montoPropina.value
    modalDescuento.value = false
    alert(`¡Descuento de $${Number(ordenActualizada.descuento).toFixed(2)} aplicado exitosamente!`)
  } catch (err) {
    alert(err.response?.data?.detail || 'Error al aplicar descuento.')
  } finally {
    aplicandoDescuento.value = false
  }
}

const quitarDescuentoActivo = async () => {
  if (!ordenSeleccionada.value) return
  if (!confirm('¿Deseas quitar el descuento aplicado a esta orden?')) return
  quitandoDescuento.value = true
  try {
    const ordenActualizada = await cajaStore.quitarDescuento(ordenSeleccionada.value.id)
    ordenSeleccionada.value = ordenActualizada
    montoRecibido.value = Number(ordenActualizada.total) + montoPropina.value
    alert('Descuento eliminado.')
  } catch (err) {
    alert(err.response?.data?.detail || 'Error al quitar descuento.')
  } finally {
    quitandoDescuento.value = false
  }
}

const montoPropina = computed(() => {
  if (!ordenSeleccionada.value) return 0
  if (tipoPropina.value === 'monto') {
    return Math.max(0, Number(propinaManual.value || 0))
  }
  return (Number(ordenSeleccionada.value.total) * (porcentajePropina.value || 0)) / 100
})

const totalConPropina = computed(() => {
  if (!ordenSeleccionada.value) return 0
  return Number(ordenSeleccionada.value.total) + montoPropina.value
})

const cambio = computed(() => {
  if (metodoPago.value !== 'efectivo') return 0
  return (montoRecibido.value || 0) - totalConPropina.value
})

const diferenciaCierre = computed(() => {
  if (!cajaStore.turnoActivo) return 0
  const esperado = Number(cajaStore.turnoActivo.total_efectivo_en_caja || 0)
  return (formCierre.value.monto_declarado || 0) - esperado
})

const seleccionarPorcentajePropina = (pct) => {
  tipoPropina.value = 'pct'
  porcentajePropina.value = pct
  // Ajustar monto recibido si estaba exacto
  if (metodoPago.value === 'efectivo' && montoRecibido.value <= totalConPropina.value) {
    montoRecibido.value = totalConPropina.value
  }
}

// Helpers visuales
const obtenerNombreCabecera = (orden) => {
  if (!orden) return ''
  if (orden.datos_entrega?.cliente) {
    return `${orden.datos_entrega.cliente} (${orden.mesa_numero || 'Envío'})`
  }
  return orden.mesa_numero || `Mesa ${orden.mesa_id || 'Mostrador'}`
}

const contarPlatillos = (orden) => {
  if (!orden?.items) return 0
  return orden.items
    .filter(i => i.estado !== 'cancelado')
    .reduce((acc, it) => acc + (it.cantidad || 1), 0)
}

const formatearHora = (fechaIso) => {
  if (!fechaIso) return ''
  const d = new Date(fechaIso)
  return d.toLocaleTimeString('es-MX', { hour: '2-digit', minute: '2-digit', hour12: true })
}

const badgeEstadoOrden = (estado) => {
  switch (estado) {
    case 'en_cola':
      return { texto: 'En Cola', clase: 'bg-amber-100 text-amber-800 dark:bg-amber-950 dark:text-amber-300' }
    case 'preparando':
      return { texto: 'En Preparación', clase: 'bg-indigo-100 text-indigo-800 dark:bg-indigo-950 dark:text-indigo-300' }
    case 'listo':
      return { texto: 'Listo en Cocina', clase: 'bg-emerald-100 text-emerald-800 dark:bg-emerald-950 dark:text-emerald-300' }
    case 'entregado':
      return { texto: 'Entregado a Mesa', clase: 'bg-teal-100 text-teal-800 dark:bg-teal-950 dark:text-teal-300' }
    default:
      return { texto: estado, clase: 'bg-slate-100 text-slate-700 dark:bg-slate-800 dark:text-slate-300' }
  }
}

// Procesar Pago
const procesarPago = async () => {
  if (!ordenSeleccionada.value) return
  cobrando.value = true
  const ordenACobrar = { ...ordenSeleccionada.value }

  try {
    const payload = {
      orden_id: ordenACobrar.id,
      metodo: metodoPago.value,
      monto_recibido: metodoPago.value === 'efectivo' ? montoRecibido.value : totalConPropina.value,
      propina: montoPropina.value
    }
    const pagoRes = await cajaStore.cobrarOrden(payload)
    await mesasStore.cargarMesas()

    // Mostrar modal de éxito
    ultimoPago.value = pagoRes
    ordenPagada.value = ordenACobrar
    modalCobroExitoso.value = true

    // Seleccionar siguiente comanda si existe
    if (cajaStore.cuentasPendientes.length > 0) {
      ordenSeleccionada.value = cajaStore.cuentasPendientes[0]
    } else {
      ordenSeleccionada.value = null
    }
  } catch (err) {
    alert(err.response?.data?.detail || 'Error al procesar el cobro.')
  } finally {
    cobrando.value = false
  }
}

const cerrarModalCobroExitoso = () => {
  modalCobroExitoso.value = false
  ultimoPago.value = null
  ordenPagada.value = null
}

// Tickets e impresión
const abrirPreCuenta = () => {
  modalPreCuenta.value = true
}

const imprimirPreCuentaDirecto = () => {
  if (!ordenSeleccionada.value) return
  const html = generarTicketPreCuenta(ordenSeleccionada.value, mensajeTicket.value)
  imprimirContenidoHtml(html)
  modalPreCuenta.value = false
}

const imprimirTicketVentaDirecto = () => {
  if (!ultimoPago.value) return
  const html = generarTicketVenta(ultimoPago.value, ordenPagada.value, mensajeTicket.value)
  imprimirContenidoHtml(html)
}

// Corte X
const abrirCorteX = async () => {
  const res = await cajaStore.obtenerCorteX()
  if (res) {
    datosCorteX.value = res
    modalCorteX.value = true
  } else {
    alert('No fue posible generar el corte parcial.')
  }
}

// Turno de Caja (Apertura y Cierre Corte Z)
const confirmarAbrirTurno = async () => {
  guardandoTurno.value = true
  try {
    await cajaStore.abrirTurno({
      monto_apertura: formApertura.value.monto || 0,
      notas: formApertura.value.notas || null
    })
    modalAbrirTurno.value = false
    alert('¡Turno de caja iniciado con éxito!')
  } catch (err) {
    alert(err.response?.data?.detail || 'Error al abrir turno.')
  } finally {
    guardandoTurno.value = false
  }
}

const abrirModalCerrarTurno = () => {
  if (cajaStore.turnoActivo) {
    formCierre.value.monto_declarado = Number(cajaStore.turnoActivo.total_efectivo_en_caja || 0)
    formCierre.value.notas = ''
  }
  modalCerrarTurno.value = true
}

const confirmarCierreTurno = async () => {
  if (!confirm('¿Estás seguro de cerrar definitivamente el turno de caja (Corte Z)?')) {
    return
  }
  guardandoTurno.value = true
  try {
    await cajaStore.cerrarTurno({
      monto_cierre_declarado: formCierre.value.monto_declarado || 0,
      notas: formCierre.value.notas || null
    })
    modalCerrarTurno.value = false
    alert('¡Cierre de turno (Corte Z) concluido con éxito!')
  } catch (err) {
    alert(err.response?.data?.detail || 'Error al cerrar turno.')
  } finally {
    guardandoTurno.value = false
  }
}
</script>

<style scoped>
/* Ocultar barra de desplazamiento sin perder funcionalidad */
.no-scrollbar::-webkit-scrollbar {
  display: none;
}
.no-scrollbar {
  -ms-overflow-style: none;
  scrollbar-width: none;
}
</style>

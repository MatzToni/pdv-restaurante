<template>
  <!-- Pantalla de Bloqueo si la mesa pertenece a otro mesero -->
  <div v-if="esMesaDeOtroMesero" class="h-[calc(100vh-5.5rem)] md:h-[calc(100vh-3rem)] flex items-center justify-center p-4">
    <div class="bg-white dark:bg-slate-900 rounded-3xl border border-slate-200 dark:border-slate-800 p-8 max-w-md w-full shadow-xl text-center space-y-4">
      <div class="w-16 h-16 rounded-2xl bg-amber-100 dark:bg-amber-950/60 text-amber-700 dark:text-amber-400 flex items-center justify-center text-3xl mx-auto shadow-inner">
        🔒
      </div>
      <h2 class="text-xl font-black text-slate-800 dark:text-slate-100">Mesa No Disponible</h2>
      <p class="text-sm text-slate-600 dark:text-slate-300">
        La <strong>{{ mesaNumero }}</strong> está asignada a <span class="font-extrabold text-eden-700 dark:text-eden-400">{{ mesaActual?.mesero_nombre || 'otro colaborador' }}</span>.
      </p>
      <p class="text-xs text-slate-500 dark:text-slate-400">
        Por políticas del restaurante, no tienes autorización para ver sus comandas ni agregarle rondas. Esta acción está restringida al mesero asignado o personal de jefatura.
      </p>
      <div class="pt-2">
        <button 
          @click="router.push('/')" 
          class="w-full py-3 bg-eden-600 hover:bg-eden-700 text-white rounded-xl font-bold text-xs shadow-sm transition active:scale-95 flex items-center justify-center gap-2"
        >
          <span>←</span> Volver al Mapa de Mesas
        </button>
      </div>
    </div>
  </div>

  <div v-else class="h-[calc(100vh-5.5rem)] md:h-[calc(100vh-3rem)] flex flex-col lg:flex-row gap-4">
    <!-- Menú y Selección de Platillos (Izquierda) -->
    <div class="flex-1 flex flex-col bg-white dark:bg-slate-900 rounded-2xl border border-slate-200 dark:border-slate-800 overflow-hidden shadow-sm transition-colors">
      <!-- Barra superior con regreso y categorías -->
      <div class="p-3 border-b border-slate-100 dark:border-slate-800 flex items-center gap-2 overflow-x-auto no-scrollbar bg-slate-50/50 dark:bg-slate-900/50">
        <button 
          @click="router.push('/')" 
          class="px-3 py-2 rounded-xl text-xs font-bold bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 text-slate-700 dark:text-slate-200 hover:bg-slate-100 dark:hover:bg-slate-700 shrink-0 transition"
        >
          ← Mesas
        </button>

        <button
          @click="categoriaSeleccionada = null"
          :class="[
            'px-4 py-2 rounded-xl text-xs font-bold transition-all shrink-0',
            categoriaSeleccionada === null 
              ? 'bg-slate-900 dark:bg-white text-white dark:text-slate-900 shadow-sm' 
              : 'bg-white dark:bg-slate-800 text-slate-600 dark:text-slate-300 hover:bg-slate-200 dark:hover:bg-slate-700 border border-slate-200 dark:border-slate-700'
          ]"
        >
          Todos los Platillos
        </button>
        <button
          v-for="cat in menuStore.categorias"
          :key="cat.id"
          @click="categoriaSeleccionada = cat.id"
          :class="[
            'px-4 py-2 rounded-xl text-xs font-bold transition-all shrink-0',
            categoriaSeleccionada === cat.id 
              ? 'bg-eden-600 text-white shadow-sm' 
              : 'bg-white dark:bg-slate-800 text-slate-600 dark:text-slate-300 hover:bg-slate-200 dark:hover:bg-slate-700 border border-slate-200 dark:border-slate-700'
          ]"
        >
          {{ cat.nombre }}
        </button>
      </div>

      <!-- Cuadrícula de Platillos Touch -->
      <div class="flex-1 p-4 overflow-y-auto">
        <div v-if="menuStore.cargando" class="text-center py-12 text-slate-400">
          <p class="text-sm">Cargando menú de Edén Café...</p>
        </div>

        <div v-else class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 xl:grid-cols-5 gap-3">
          <button
            v-for="item in platillosFiltrados"
            :key="item.id"
            @click="abrirModalExtras(item)"
            class="flex flex-col justify-between p-3.5 bg-slate-50 dark:bg-slate-800/60 hover:bg-eden-50/50 dark:hover:bg-eden-950/30 border border-slate-200 dark:border-slate-800 hover:border-eden-600 dark:hover:border-eden-500 rounded-2xl text-left transition-all active:scale-95 group shadow-sm min-h-[9.5rem] h-auto"
          >
            <div class="flex items-start gap-2.5">
              <!-- Miniatura de imagen si existe -->
              <div 
                v-if="item.imagen_url" 
                class="w-12 h-12 rounded-xl overflow-hidden shrink-0 border border-slate-200 dark:border-slate-700 bg-slate-200 dark:bg-slate-800"
              >
                <img 
                  :src="menuStore.obtenerUrlImagen(item.imagen_url)" 
                  :alt="item.nombre" 
                  class="w-full h-full object-cover group-hover:scale-105 transition-transform"
                  @error="$event.target.style.display = 'none'"
                />
              </div>

              <div class="flex-1 min-w-0">
                <div class="font-extrabold text-slate-800 dark:text-slate-100 text-sm group-hover:text-eden-700 dark:group-hover:text-eden-400 leading-snug line-clamp-2">
                  {{ item.nombre }}
                </div>
                <div class="text-xs text-slate-400 dark:text-slate-500 mt-0.5 line-clamp-2 leading-relaxed">
                  {{ item.descripcion }}
                </div>
              </div>
            </div>

            <div class="mt-2.5 pt-2 border-t border-slate-200/60 dark:border-slate-700/60 flex justify-between items-center w-full">
              <span class="font-black text-eden-600 dark:text-eden-400 text-base font-mono">
                ${{ Number(item.precio).toFixed(2) }}
              </span>
              <span class="text-xs font-bold bg-white dark:bg-slate-700 text-slate-700 dark:text-slate-200 px-2 py-0.5 rounded-lg border border-slate-200 dark:border-slate-600 group-hover:bg-eden-600 group-hover:text-white transition">
                + Opciones
              </span>
            </div>
          </button>
        </div>
      </div>
    </div>

    <!-- Comanda / Ticket Actual (Derecha) -->
    <div class="w-full lg:w-96 flex flex-col bg-white dark:bg-slate-900 rounded-2xl border border-slate-200 dark:border-slate-800 overflow-hidden shadow-sm transition-colors">
      <div class="p-4 border-b border-slate-100 dark:border-slate-800 flex justify-between items-center bg-slate-50 dark:bg-slate-800/50">
        <div>
          <div class="flex items-center gap-2">
            <h2 class="font-extrabold text-slate-800 dark:text-slate-100 text-base">{{ mesaNumero }}</h2>
            <span v-if="ordenActiva" class="text-2xs font-extrabold px-2 py-0.5 rounded-full uppercase" :class="badgeColorEstado(ordenActiva.estado)">
              {{ ordenActiva.estado }}
            </span>
          </div>
          <span class="text-xs text-slate-500 dark:text-slate-400 font-medium">Atiende: {{ authStore.usuarioActual?.nombre || 'Mesero' }}</span>
        </div>
        <button 
          v-if="itemsComanda.length > 0"
          @click="itemsComanda = []" 
          class="text-xs font-bold text-rose-500 dark:text-rose-400 hover:underline"
        >
          Limpiar
        </button>
      </div>

      <!-- Alertas de Observación / Falta de Ingrediente desde Cocina -->
      <div v-if="itemsEnObservacion.length > 0" class="p-3 bg-amber-500/10 dark:bg-amber-950/40 border-b border-amber-300 dark:border-amber-800/60 space-y-2">
        <div class="flex items-center gap-1.5 text-amber-700 dark:text-amber-300 text-xs font-black animate-pulse">
          <span>⚠️</span> ALERTA DE COCINA ({{ itemsEnObservacion.length }})
        </div>
        <div 
          v-for="itemObs in itemsEnObservacion" 
          :key="itemObs.id" 
          class="bg-white dark:bg-slate-900 p-2.5 rounded-xl border border-amber-300 dark:border-amber-700/60 text-xs space-y-1.5"
        >
          <div class="font-bold text-slate-800 dark:text-slate-100">{{ itemObs.producto_nombre }} ({{ itemObs.cantidad }}x)</div>
          <div class="text-amber-800 dark:text-amber-300 font-semibold italic bg-amber-50 dark:bg-amber-950/60 p-1.5 rounded-lg border border-amber-200 dark:border-amber-900/40">
            "{{ itemObs.observacion_cocina }}"
          </div>
          <div class="flex gap-2 pt-1">
            <button 
              @click="abrirModalResolver(itemObs)"
              class="flex-1 py-1 bg-eden-600 hover:bg-eden-700 text-white font-bold rounded-lg text-2xs transition active:scale-95"
            >
              ✓ Aclarar / Continuar
            </button>
            <button 
              @click="cancelarPorObservacion(itemObs)"
              class="px-2.5 py-1 bg-rose-100 dark:bg-rose-950/60 hover:bg-rose-200 text-rose-700 dark:text-rose-300 font-bold rounded-lg text-2xs transition active:scale-95"
            >
              ✕ Cancelar
            </button>
          </div>
        </div>
      </div>

      <!-- Lista de Items: Enviados previamente (si hay) y Nuevos por enviar -->
      <div class="flex-1 p-3 overflow-y-auto space-y-2.5">
        <!-- Platillos ya enviados a cocina -->
        <div v-if="ordenActiva && ordenActiva.items?.length > 0" class="space-y-1.5 border-b border-slate-200 dark:border-slate-800 pb-3">
          <div class="flex justify-between items-center text-2xs font-extrabold uppercase text-slate-400 tracking-wider">
            <span>Enviados a Cocina (#{{ ordenActiva.id }})</span>
            <span class="text-eden-600 dark:text-eden-400 font-mono">${{ Number(ordenActiva.total).toFixed(2) }}</span>
          </div>
          
          <div 
            v-for="itemAnt in ordenActiva.items" 
            :key="itemAnt.id"
            class="p-2 rounded-xl bg-slate-50/70 dark:bg-slate-800/40 border border-slate-200 dark:border-slate-800 flex justify-between items-center text-xs"
          >
            <div>
              <div class="font-bold text-slate-700 dark:text-slate-200">
                {{ itemAnt.cantidad }}x {{ itemAnt.producto_nombre }}
              </div>
              <div v-if="itemAnt.extras && itemAnt.extras.length > 0" class="flex flex-wrap gap-1 mt-0.5">
                <span v-for="(ex, ei) in itemAnt.extras" :key="ei" class="text-3xs bg-slate-200 dark:bg-slate-700 text-slate-700 dark:text-slate-300 px-1 py-0.2 rounded font-medium">
                  + {{ ex.nombre }}
                </span>
              </div>
              <div v-if="itemAnt.notas" class="text-3xs text-slate-500 italic">{{ itemAnt.notas }}</div>
            </div>
            <div class="text-right">
              <span class="text-3xs font-extrabold px-1.5 py-0.5 rounded uppercase" :class="badgeColorItem(itemAnt.estado)">
                {{ itemAnt.estado }}
              </span>
              <div class="text-2xs font-bold text-slate-600 dark:text-slate-400 mt-0.5">
                ${{ (Number(itemAnt.precio_unitario) * itemAnt.cantidad).toFixed(2) }}
              </div>
            </div>
          </div>
        </div>

        <!-- Platillos en preparación de la ronda actual -->
        <div v-if="itemsComanda.length === 0 && (!ordenActiva || ordenActiva.items?.length === 0)" class="h-44 flex flex-col items-center justify-center text-slate-400 text-sm">
          <span class="text-3xl mb-2">🍽️</span>
          <p class="font-bold">No hay platillos en la orden</p>
          <span class="text-xs text-slate-400 dark:text-slate-500 mt-1 text-center">Toca los platillos para configurar extras y agregarlos</span>
        </div>

        <div v-if="itemsComanda.length > 0" class="space-y-2">
          <div class="text-2xs font-extrabold uppercase text-eden-700 dark:text-eden-400 tracking-wider">
            <span>Ronda por enviar</span>
          </div>

          <div 
            v-for="(item, index) in itemsComanda" 
            :key="index"
            class="p-2.5 rounded-xl bg-slate-50 dark:bg-slate-800/60 border border-slate-200/80 dark:border-slate-700/80 space-y-1.5"
          >
            <div class="flex items-center justify-between">
              <div class="flex-1 min-w-0 pr-2">
                <h4 class="font-bold text-sm text-slate-800 dark:text-slate-100 truncate">{{ item.nombre }}</h4>
                <div class="text-xs text-slate-500 dark:text-slate-400 font-semibold">${{ item.precioUnitarioCalculado.toFixed(2) }} c/u</div>
              </div>
              <div class="flex items-center gap-1.5">
                <button @click="decrementar(index)" class="w-7 h-7 rounded-lg bg-white dark:bg-slate-700 border border-slate-300 dark:border-slate-600 text-slate-700 dark:text-slate-200 flex items-center justify-center font-bold text-sm hover:bg-slate-100 dark:hover:bg-slate-600">-</button>
                <span class="font-black text-sm w-5 text-center text-slate-800 dark:text-slate-100">{{ item.cantidad }}</span>
                <button @click="incrementar(index)" class="w-7 h-7 rounded-lg bg-white dark:bg-slate-700 border border-slate-300 dark:border-slate-600 text-slate-700 dark:text-slate-200 flex items-center justify-center font-bold text-sm hover:bg-slate-100 dark:hover:bg-slate-600">+</button>
                <span class="font-black text-sm text-slate-800 dark:text-slate-100 ml-2 w-16 text-right">${{ (item.precioUnitarioCalculado * item.cantidad).toFixed(2) }}</span>
              </div>
            </div>

            <!-- Extras del item -->
            <div v-if="item.extras.length > 0" class="flex flex-wrap gap-1">
              <span v-for="(ex, ei) in item.extras" :key="ei" class="text-3xs bg-eden-100 dark:bg-eden-950/60 text-eden-800 dark:text-eden-300 px-1.5 py-0.5 rounded-md font-bold border border-eden-200 dark:border-eden-800/50">
                + {{ ex.nombre }} (${{ Number(ex.precio).toFixed(2) }})
              </span>
            </div>

            <!-- Nota específica para cocina -->
            <input 
              v-model="item.notas"
              type="text"
              placeholder="Nota para cocina (ej. sin cebolla, término medio)"
              class="w-full text-xs p-1.5 bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 text-slate-800 dark:text-slate-100 rounded-lg focus:outline-none focus:border-eden-600"
            />
          </div>
        </div>
      </div>

      <!-- Resumen y Acciones (Pedir Cuenta / Enviar Comanda) -->
      <div class="p-4 border-t border-slate-100 dark:border-slate-800 bg-slate-50 dark:bg-slate-800/50 space-y-3">
        <!-- Notas generales de la mesa (si es nueva orden) -->
        <input 
          v-if="!ordenActiva"
          v-model="notasGenerales"
          type="text"
          placeholder="Notas de la comanda general..."
          class="w-full text-xs p-2 bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 text-slate-800 dark:text-slate-100 rounded-xl focus:outline-none focus:border-eden-600"
        />

        <div class="flex justify-between items-center text-lg font-black text-slate-900 dark:text-slate-100 border-t border-slate-200 dark:border-slate-700 pt-2">
          <span>Total Acumulado</span>
          <span class="text-eden-600 dark:text-eden-400">${{ granTotal.toFixed(2) }}</span>
        </div>

        <div class="flex gap-2">
          <!-- Botón Pedir Cuenta si ya hay orden activa -->
          <button 
            v-if="ordenActiva"
            @click="pedirCuentaMesa"
            class="flex-1 py-3 bg-amber-500 hover:bg-amber-600 text-white rounded-xl font-bold text-xs shadow-sm transition active:scale-95 flex items-center justify-center gap-1.5"
          >
            <span>🧾</span> Pedir Cuenta
          </button>

          <!-- Botón Enviar Comanda o Agregar Ronda -->
          <button 
            @click="enviarComandaCocina"
            :disabled="itemsComanda.length === 0 || enviando"
            class="flex-2 py-3 bg-eden-600 hover:bg-eden-700 disabled:opacity-50 text-white rounded-xl font-bold text-xs shadow-md transition active:scale-95 flex items-center justify-center gap-1.5"
          >
            <span v-if="enviando">Enviando...</span>
            <span v-else-if="ordenActiva">👨‍🍳 Enviar Ronda ({{ totalItemsRonda }})</span>
            <span v-else>👨‍🍳 Enviar a Cocina ({{ totalItemsRonda }})</span>
          </button>
        </div>
      </div>
    </div>

    <!-- MODAL TOUCH: SELECCIÓN DE EXTRAS Y MODIFICADORES -->
    <div v-if="modalExtras && productoSeleccionado" class="fixed inset-0 bg-slate-900/60 backdrop-blur-sm flex items-center justify-center p-4 z-50">
      <div class="bg-white dark:bg-slate-900 rounded-3xl p-6 max-w-lg w-full shadow-2xl border border-slate-200 dark:border-slate-800 space-y-4 max-h-[90vh] flex flex-col">
        <!-- Cabecera del platillo -->
        <div class="flex justify-between items-start border-b border-slate-100 dark:border-slate-800 pb-3">
          <div>
            <h3 class="text-lg font-black text-slate-800 dark:text-slate-100">{{ productoSeleccionado.nombre }}</h3>
            <p class="text-xs text-slate-500 dark:text-slate-400 mt-0.5">{{ productoSeleccionado.descripcion }}</p>
          </div>
          <span class="text-lg font-black text-eden-600 dark:text-eden-400">
            ${{ Number(productoSeleccionado.precio).toFixed(2) }}
          </span>
        </div>

        <div class="flex-1 overflow-y-auto space-y-4 pr-1">
          <!-- Selector de Cantidad -->
          <div class="flex items-center justify-between bg-slate-50 dark:bg-slate-800/60 p-3 rounded-2xl border border-slate-200 dark:border-slate-700">
            <span class="text-xs font-bold text-slate-700 dark:text-slate-300">Cantidad de Porciones:</span>
            <div class="flex items-center gap-3">
              <button 
                @click="tempCantidad > 1 ? tempCantidad-- : null"
                class="w-8 h-8 rounded-xl bg-white dark:bg-slate-700 text-slate-800 dark:text-slate-100 font-bold border border-slate-300 dark:border-slate-600 hover:bg-slate-100 flex items-center justify-center text-sm"
              >
                -
              </button>
              <span class="font-black text-base w-6 text-center text-slate-900 dark:text-slate-100">{{ tempCantidad }}</span>
              <button 
                @click="tempCantidad++"
                class="w-8 h-8 rounded-xl bg-white dark:bg-slate-700 text-slate-800 dark:text-slate-100 font-bold border border-slate-300 dark:border-slate-600 hover:bg-slate-100 flex items-center justify-center text-sm"
              >
                +
              </button>
            </div>
          </div>

          <!-- Opciones Extras con Costo -->
          <div class="space-y-2">
            <label class="text-xs font-black uppercase text-slate-500 dark:text-slate-400 tracking-wider">
              Extras Adicionales
            </label>
            <div class="grid grid-cols-2 gap-2">
              <button 
                v-for="extra in listaExtrasDisponibles" 
                :key="extra.nombre"
                type="button"
                @click="toggleExtra(extra)"
                :class="[
                  'p-2.5 rounded-xl border text-left text-xs font-bold flex justify-between items-center transition active:scale-95',
                  tieneExtra(extra.nombre)
                    ? 'border-eden-600 bg-eden-50 dark:bg-eden-950/40 text-eden-800 dark:text-eden-300 shadow-xs'
                    : 'border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-800 text-slate-700 dark:text-slate-300 hover:bg-slate-50 dark:hover:bg-slate-700'
                ]"
              >
                <span>{{ extra.nombre }}</span>
                <span class="font-extrabold text-2xs text-eden-600 dark:text-eden-400">+${{ extra.precio }}</span>
              </button>
            </div>
          </div>

          <!-- Modificadores de preparación rápidos (sin costo) -->
          <div class="space-y-2">
            <label class="text-xs font-black uppercase text-slate-500 dark:text-slate-400 tracking-wider">
              Preferencias Rápidas
            </label>
            <div class="flex flex-wrap gap-1.5">
              <button 
                v-for="mod in modificadoresRapidos" 
                :key="mod"
                type="button"
                @click="toggleModificador(mod)"
                :class="[
                  'px-3 py-1.5 rounded-xl text-2xs font-bold border transition active:scale-95',
                  tempNotas.includes(mod)
                    ? 'bg-slate-900 dark:bg-white text-white dark:text-slate-900 border-slate-900'
                    : 'bg-white dark:bg-slate-800 text-slate-600 dark:text-slate-300 border-slate-200 dark:border-slate-700 hover:bg-slate-100'
                ]"
              >
                {{ mod }}
              </button>
            </div>
          </div>

          <!-- Nota personalizada -->
          <div>
            <label class="text-xs font-bold text-slate-700 dark:text-slate-300">Nota especial para la cocina:</label>
            <input 
              v-model="tempNotas"
              type="text"
              placeholder="Ej. Salsa verde bien picosa, sin frijoles..."
              class="w-full mt-1 p-2.5 text-xs bg-white dark:bg-slate-800 border border-slate-300 dark:border-slate-700 rounded-xl focus:outline-none focus:border-eden-600 text-slate-800 dark:text-slate-100 font-medium"
            />
          </div>
        </div>

        <!-- Footer del Modal con Total -->
        <div class="pt-3 border-t border-slate-100 dark:border-slate-800 flex items-center justify-between gap-3">
          <div>
            <span class="text-2xs text-slate-400 block font-semibold">Total del platillo</span>
            <span class="text-lg font-black text-eden-600 dark:text-eden-400">
              ${{ modalTotalItem.toFixed(2) }}
            </span>
          </div>

          <div class="flex gap-2">
            <button 
              @click="modalExtras = false"
              class="px-4 py-2.5 rounded-xl text-xs font-bold text-slate-600 dark:text-slate-300 hover:bg-slate-100 dark:hover:bg-slate-800 transition"
            >
              Cancelar
            </button>
            <button 
              @click="confirmarAgregarConExtras"
              class="px-5 py-2.5 rounded-xl text-xs font-bold bg-eden-600 hover:bg-eden-700 text-white shadow-md transition active:scale-95"
            >
              ✓ Agregar a la Comanda
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- MODAL PARA RESOLVER OBSERVACIÓN / FALTA DE INGREDIENTE -->
    <div v-if="modalResolver && itemParaResolver" class="fixed inset-0 bg-slate-900/60 backdrop-blur-sm flex items-center justify-center p-4 z-50">
      <div class="bg-white dark:bg-slate-900 rounded-3xl p-6 max-w-md w-full shadow-2xl border border-slate-200 dark:border-slate-800 space-y-4">
        <div class="flex items-center gap-2 text-amber-600 dark:text-amber-400">
          <span class="text-2xl">👨‍🍳</span>
          <h3 class="text-lg font-black text-slate-800 dark:text-slate-100">Resolver Observación de Cocina</h3>
        </div>

        <div class="bg-amber-50 dark:bg-amber-950/50 p-3 rounded-2xl border border-amber-200 dark:border-amber-800/40 text-xs space-y-1">
          <div class="font-bold text-slate-800 dark:text-slate-100">Platillo: {{ itemParaResolver.producto_nombre }}</div>
          <div class="text-amber-800 dark:text-amber-300 font-semibold italic">"{{ itemParaResolver.observacion_cocina }}"</div>
        </div>

        <div>
          <label class="text-xs font-bold text-slate-700 dark:text-slate-300">Respuesta / Aclaración con el cliente:</label>
          <input 
            v-model="respuestaAclaracion" 
            type="text" 
            placeholder="Ej. Cliente acepta cambio por pechuga / salsa roja"
            class="w-full mt-1 p-2.5 text-xs font-semibold border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-800 text-slate-800 dark:text-slate-100 rounded-xl focus:outline-none focus:border-eden-600"
          />
        </div>

        <div class="flex justify-end gap-2 pt-2">
          <button 
            @click="modalResolver = false"
            class="px-4 py-2 text-xs font-bold text-slate-600 dark:text-slate-300 hover:bg-slate-100 dark:hover:bg-slate-800 rounded-xl"
          >
            Cerrar
          </button>
          <button 
            @click="confirmarResolucion"
            :disabled="!respuestaAclaracion.trim()"
            class="px-5 py-2 text-xs font-bold bg-eden-600 hover:bg-eden-700 disabled:opacity-50 text-white rounded-xl shadow-sm transition active:scale-95"
          >
            ✓ Enviar a Cocina y Continuar
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useMenuStore } from '../stores/menu'
import { useOrdenesStore } from '../stores/ordenes'
import { useAuthStore } from '../stores/auth'
import { useMesasStore } from '../stores/mesas'

const route = useRoute()
const router = useRouter()
const menuStore = useMenuStore()
const ordenesStore = useOrdenesStore()
const authStore = useAuthStore()
const mesasStore = useMesasStore()

const mesaId = computed(() => Number(route.query.mesaId) || 1)
const mesaNumero = computed(() => route.query.mesaNumero || `Mesa ${mesaId.value}`)

const esRolAlto = computed(() => {
  return ['administrador', 'gerente', 'jefe'].includes(authStore.rolActual)
})

const mesaActual = computed(() => {
  return mesasStore.mesas.find(m => m.id === mesaId.value)
})

const esMesaDeOtroMesero = computed(() => {
  if (!mesaActual.value || !mesaActual.value.mesero_id) return false
  if (esRolAlto.value) return false
  return mesaActual.value.mesero_id !== authStore.usuarioActual?.id
})

const categoriaSeleccionada = ref(null)
const itemsComanda = ref([])
const notasGenerales = ref('')
const enviando = ref(false)
const ordenActiva = ref(null)

// Modal de Extras
const modalExtras = ref(false)
const productoSeleccionado = ref(null)
const tempCantidad = ref(1)
const tempExtras = ref([])
const tempNotas = ref('')

// Modal Resolver Observación
const modalResolver = ref(false)
const itemParaResolver = ref(null)
const respuestaAclaracion = ref('')

const listaExtrasDisponibles = [
  { nombre: 'Shot extra de espresso', precio: 15 },
  { nombre: 'Leche de almendra', precio: 12 },
  { nombre: 'Leche de avena', precio: 12 },
  { nombre: 'Leche deslactosada', precio: 8 },
  { nombre: 'Jarabe saborizante', precio: 10 },
  { nombre: 'Queso extra', precio: 20 },
  { nombre: 'Aguacate extra', precio: 25 },
  { nombre: 'Tocino extra', precio: 25 },
  { nombre: 'Huevo extra', precio: 15 },
  { nombre: 'Proteína extra (Pollo)', precio: 35 }
]

const modificadoresRapidos = [
  'Descafeinado',
  'Sin cebolla',
  'Salsa aparte',
  'Término medio',
  'Bien cocido',
  'Para llevar'
]

onMounted(async () => {
  await Promise.all([
    menuStore.cargarCatalogo(),
    mesasStore.cargarMesas()
  ])
  if (!esMesaDeOtroMesero.value) {
    await cargarOrdenDeMesa()
  }
})

const cargarOrdenDeMesa = async () => {
  if (esMesaDeOtroMesero.value) {
    ordenActiva.value = null
    return
  }
  ordenActiva.value = await ordenesStore.obtenerOrdenActivaMesa(mesaId.value, authStore.usuarioActual?.id)
}

const itemsEnObservacion = computed(() => {
  if (!ordenActiva.value || !ordenActiva.value.items) return []
  return ordenActiva.value.items.filter(i => i.estado === 'en_observacion')
})

const platillosFiltrados = computed(() => {
  if (!categoriaSeleccionada.value) return menuStore.productos
  return menuStore.productos.filter(p => p.categoria_id === categoriaSeleccionada.value)
})

const totalRondaActual = computed(() => {
  return itemsComanda.value.reduce((acc, item) => acc + (item.precioUnitarioCalculado * item.cantidad), 0)
})

const totalItemsRonda = computed(() => {
  return itemsComanda.value.reduce((acc, i) => acc + i.cantidad, 0)
})

const granTotal = computed(() => {
  const activoTotal = ordenActiva.value ? Number(ordenActiva.value.total) : 0
  return activoTotal + totalRondaActual.value
})

const modalTotalItem = computed(() => {
  if (!productoSeleccionado.value) return 0
  const costoExtras = tempExtras.value.reduce((acc, ex) => acc + ex.precio, 0)
  return (Number(productoSeleccionado.value.precio) + costoExtras) * tempCantidad.value
})

const abrirModalExtras = (producto) => {
  productoSeleccionado.value = producto
  tempCantidad.value = 1
  tempExtras.value = []
  tempNotas.value = ''
  modalExtras.value = true
}

const toggleExtra = (extra) => {
  const idx = tempExtras.value.findIndex(e => e.nombre === extra.nombre)
  if (idx >= 0) {
    tempExtras.value.splice(idx, 1)
  } else {
    tempExtras.value.push({ nombre: extra.nombre, precio: extra.precio })
  }
}

const tieneExtra = (nombre) => {
  return tempExtras.value.some(e => e.nombre === nombre)
}

const toggleModificador = (mod) => {
  if (tempNotas.value.includes(mod)) {
    tempNotas.value = tempNotas.value.replace(mod, '').replace(/,\s*,/g, ',').trim()
  } else {
    tempNotas.value = tempNotas.value ? `${tempNotas.value}, ${mod}` : mod
  }
}

const confirmarAgregarConExtras = () => {
  if (!productoSeleccionado.value) return
  const costoExtras = tempExtras.value.reduce((acc, ex) => acc + ex.precio, 0)
  const precioUnitario = Number(productoSeleccionado.value.precio) + costoExtras

  itemsComanda.value.push({
    id: productoSeleccionado.value.id,
    nombre: productoSeleccionado.value.nombre,
    precioBase: Number(productoSeleccionado.value.precio),
    precioUnitarioCalculado: precioUnitario,
    cantidad: tempCantidad.value,
    extras: [...tempExtras.value],
    notas: tempNotas.value
  })

  modalExtras.value = false
}

const incrementar = (idx) => { itemsComanda.value[idx].cantidad++ }
const decrementar = (idx) => {
  if (itemsComanda.value[idx].cantidad > 1) {
    itemsComanda.value[idx].cantidad--
  } else {
    itemsComanda.value.splice(idx, 1)
  }
}

const enviarComandaCocina = async () => {
  if (esMesaDeOtroMesero.value) {
    alert('Esta mesa está asignada a otro mesero. No tienes permisos para agregar rondas.')
    return
  }
  if (itemsComanda.value.length === 0) return
  enviando.value = true
  try {
    const itemsPayload = itemsComanda.value.map(i => ({
      producto_id: i.id,
      cantidad: i.cantidad,
      notas: i.notas || null,
      extras: i.extras.map(e => ({ nombre: e.nombre, precio: e.precio }))
    }))

    if (ordenActiva.value) {
      // Agregar ronda adicional a la orden existente pasando usuario_id
      await ordenesStore.agregarItemsAOrden(ordenActiva.value.id, itemsPayload, authStore.usuarioActual?.id)
      alert(`¡Ronda adicional enviada a Cocina/Barra para ${mesaNumero.value}!`)
    } else {
      // Crear nueva comanda
      const ordenPayload = {
        mesa_id: mesaId.value,
        mesero_id: authStore.usuarioActual?.id || 1,
        notas: notasGenerales.value || null,
        items: itemsPayload
      }
      await ordenesStore.enviarComanda(ordenPayload)
      alert(`¡Comanda enviada a Cocina/Barra para ${mesaNumero.value}!`)
    }

    itemsComanda.value = []
    notasGenerales.value = ''
    await cargarOrdenDeMesa()
  } catch (err) {
    alert(err.response?.data?.detail || 'Error al enviar la comanda a cocina.')
  } finally {
    enviando.value = false
  }
}

const pedirCuentaMesa = async () => {
  if (esMesaDeOtroMesero.value) return
  if (!ordenActiva.value) return
  if (!confirm(`¿Solicitar cuenta para ${mesaNumero.value}? La mesa pasará a estado 'Por Cobrar' en Caja.`)) return
  try {
    await ordenesStore.pedirCuenta(ordenActiva.value.id)
    alert(`Mesa ${mesaNumero.value} enviada a Caja para cobro.`)
    router.push('/')
  } catch (err) {
    alert(err.response?.data?.detail || 'Error al pedir la cuenta.')
  }
}

const abrirModalResolver = (item) => {
  itemParaResolver.value = item
  respuestaAclaracion.value = ''
  modalResolver.value = true
}

const confirmarResolucion = async () => {
  if (!itemParaResolver.value || !respuestaAclaracion.value.trim()) return
  try {
    await ordenesStore.resolverObservacionItem(itemParaResolver.value.id, {
      accion: 'continuar',
      respuesta: respuestaAclaracion.value.trim()
    })
    modalResolver.value = false
    await cargarOrdenDeMesa()
    alert('Aclaración enviada exitosamente a la cocina.')
  } catch (err) {
    alert('Error al resolver la observación.')
  }
}

const cancelarPorObservacion = async (item) => {
  if (!confirm(`¿Deseas cancelar el platillo "${item.producto_nombre}" debido a la incidencia reportada por cocina?`)) return
  try {
    await ordenesStore.resolverObservacionItem(item.id, {
      accion: 'cancelar'
    })
    await cargarOrdenDeMesa()
    alert('Platillo cancelado sin merma de insumos.')
  } catch (err) {
    alert('Error al cancelar el platillo.')
  }
}

const badgeColorEstado = (estado) => {
  switch (estado) {
    case 'en_cola': return 'bg-blue-100 text-blue-800 dark:bg-blue-900/60 dark:text-blue-200'
    case 'preparando': return 'bg-amber-100 text-amber-800 dark:bg-amber-900/60 dark:text-amber-200'
    case 'listo': return 'bg-emerald-100 text-emerald-800 dark:bg-emerald-900/60 dark:text-emerald-200'
    case 'entregado': return 'bg-purple-100 text-purple-800 dark:bg-purple-900/60 dark:text-purple-200'
    default: return 'bg-slate-100 text-slate-800 dark:bg-slate-800 dark:text-slate-200'
  }
}

const badgeColorItem = (estado) => {
  switch (estado) {
    case 'en_observacion': return 'bg-rose-500 text-white animate-pulse'
    case 'pendiente': return 'bg-slate-200 text-slate-700 dark:bg-slate-700 dark:text-slate-300'
    case 'preparando': return 'bg-amber-200 text-amber-800 dark:bg-amber-900 dark:text-amber-200'
    case 'listo': return 'bg-emerald-200 text-emerald-800 dark:bg-emerald-900 dark:text-emerald-200'
    case 'entregado': return 'bg-purple-200 text-purple-800 dark:bg-purple-900 dark:text-purple-200'
    case 'cancelado': return 'bg-rose-200 text-rose-800 dark:bg-rose-900 dark:text-rose-200'
    default: return 'bg-slate-200 text-slate-700'
  }
}
</script>

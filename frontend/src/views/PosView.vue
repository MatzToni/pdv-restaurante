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

  <!-- Pantalla de Bloqueo si es pedido de envío/mostrador y el usuario es mesero -->
  <div v-else-if="esPedidoExternoNoPermitido" class="h-[calc(100vh-5.5rem)] md:h-[calc(100vh-3rem)] flex items-center justify-center p-4">
    <div class="bg-white dark:bg-slate-900 rounded-3xl border border-slate-200 dark:border-slate-800 p-8 max-w-md w-full shadow-xl text-center space-y-4">
      <div class="w-16 h-16 rounded-2xl bg-amber-100 dark:bg-amber-950/60 text-amber-700 dark:text-amber-400 flex items-center justify-center text-3xl mx-auto shadow-inner">
        🛍️
      </div>
      <h2 class="text-xl font-black text-slate-800 dark:text-slate-100">Función Restringida</h2>
      <p class="text-sm text-slate-600 dark:text-slate-300">
        Los pedidos de <strong>entrega a domicilio y mostrador</strong> no están habilitados para meseros.
      </p>
      <p class="text-xs text-slate-500 dark:text-slate-400">
        Por políticas del restaurante, los meseros atienden exclusivamente mesas físicas en salón. Los pedidos para llevar o entrega son gestionados por mostrador, jefatura o administración.
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

        <!-- Banner Comidas Corridas del Día si está activo -->
        <div 
          v-if="menuStore.menuDelDia?.activo && comidasCorridasActivas.length > 0"
          class="mb-4 p-4 rounded-2xl bg-gradient-to-r from-amber-500/15 via-eden-500/15 to-emerald-500/15 border border-amber-300 dark:border-amber-700/60 shadow-2xs space-y-3"
        >
          <div class="flex items-center justify-between">
            <div class="flex items-center gap-2.5">
              <span class="text-2xl">🍱</span>
              <div>
                <h3 class="font-black text-slate-800 dark:text-slate-100 text-sm">
                  Menú del Día
                </h3>
                <span class="text-3xs font-extrabold text-amber-700 dark:text-amber-400">
                  Horario de servicio: {{ menuStore.menuDelDia.hora_inicio || '12:00' }} a {{ menuStore.menuDelDia.hora_fin || '18:00' }}
                </span>
              </div>
            </div>
            <span class="text-3xs font-black uppercase px-2.5 py-0.5 rounded-full bg-emerald-600 text-white">
              {{ comidasCorridasActivas.length }} opciones hoy
            </span>
          </div>

          <!-- Botones de cada Comida Corrida -->
          <div class="grid grid-cols-1 sm:grid-cols-2 gap-2.5">
            <button 
              v-for="cc in comidasCorridasActivas"
              :key="cc.id || cc.nombre"
              @click="abrirModalComidaCorrida(cc)"
              class="p-3 bg-white dark:bg-slate-800 hover:border-amber-500 border border-slate-200 dark:border-slate-700 rounded-xl text-left transition active:scale-95 shadow-2xs flex justify-between items-center group"
            >
              <div class="flex items-center gap-2.5 min-w-0 flex-1 pr-2">
                <!-- Miniatura de foto si existe -->
                <div 
                  v-if="cc.imagen_url" 
                  class="w-12 h-12 rounded-xl overflow-hidden shrink-0 border border-slate-200 dark:border-slate-700 bg-slate-100 dark:bg-slate-800"
                >
                  <img 
                    :src="menuStore.obtenerUrlImagen(cc.imagen_url)" 
                    :alt="cc.nombre" 
                    class="w-full h-full object-cover" 
                    @error="$event.target.style.display = 'none'"
                  />
                </div>
                <div class="min-w-0 flex-1">
                  <h4 class="font-black text-xs text-slate-800 dark:text-slate-100 group-hover:text-amber-600 truncate">
                    🍱 {{ cc.nombre || 'Comida Corrida' }}
                  </h4>
                  <p class="text-3xs text-slate-400 truncate mt-0.5">
                    🥣 {{ cc.entradas?.[0] || 'Entrada' }} + 🍖 {{ cc.platos_fuertes?.[0] || 'Fuerte' }} + 🥤 {{ cc.bebidas?.[0] || 'Bebida' }}
                  </p>
                </div>
              </div>
              <div class="text-right shrink-0">
                <span class="text-xs font-black text-eden-600 dark:text-eden-400 font-mono block">
                  ${{ Number(cc.precio || 95).toFixed(2) }}
                </span>
                <span class="text-3xs font-extrabold text-amber-600 dark:text-amber-400">
                  + Elegir
                </span>
              </div>
            </button>
          </div>
        </div>

        <!-- Banner informativo si las comidas corridas están agotadas hoy -->
        <div 
          v-else-if="menuStore.menuDelDia?.activo && (menuStore.menuDelDia.comidas_corridas?.length || 0) > 0"
          class="mb-4 p-3 rounded-2xl bg-amber-50 dark:bg-amber-950/30 border border-amber-300 dark:border-amber-800/60 shadow-2xs flex items-center justify-between text-xs"
        >
          <div class="flex items-center gap-2">
            <span class="text-xl">🍱</span>
            <div>
              <span class="font-black text-slate-800 dark:text-slate-100 block">Menú del Día: Agotado</span>
              <span class="text-3xs text-slate-500 dark:text-slate-400">Todas las opciones de menú del día se han marcado como agotadas por hoy.</span>
            </div>
          </div>
          <span class="text-3xs font-black uppercase px-2 py-0.5 rounded-full bg-rose-600 text-white shrink-0">
            Agotadas Hoy
          </span>
        </div>

        <div v-if="platillosFiltrados.length === 0 && !menuStore.cargando" class="text-center py-12 text-slate-400">
          <span class="text-3xl block mb-2">🍽️</span>
          <p class="text-sm font-bold text-slate-600 dark:text-slate-300">No hay platillos disponibles en esta categoría</p>
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
        <div v-if="ordenActiva && ordenActiva.items?.length > 0" class="space-y-2 border-b border-slate-200 dark:border-slate-800 pb-3">
          <div class="flex justify-between items-center text-2xs font-extrabold uppercase text-slate-400 tracking-wider">
            <span>Enviados a Cocina (#{{ ordenActiva.id }})</span>
            <span class="text-eden-600 dark:text-eden-400 font-mono">${{ Number(ordenActiva.total).toFixed(2) }}</span>
          </div>

          <!-- Banner Alerta: Platillos Listos en Barra para entregar -->
          <div 
            v-if="itemsListosParaEntrega.length > 0" 
            class="p-2.5 bg-emerald-500/15 border border-emerald-500/40 rounded-2xl flex items-center justify-between gap-2 shadow-xs"
          >
            <div class="flex items-center gap-2">
              <span class="text-lg">🔔</span>
              <div>
                <div class="text-xs font-black text-emerald-800 dark:text-emerald-200">
                  {{ itemsListosParaEntrega.length }} platillo(s) listo(s) en barra
                </div>
                <div class="text-3xs text-emerald-700 dark:text-emerald-400 font-medium">
                  Listo para servir en la mesa
                </div>
              </div>
            </div>
            <button 
              @click="entregarTodosListos"
              class="px-2.5 py-1.5 min-h-[36px] bg-emerald-600 hover:bg-emerald-700 text-white rounded-xl text-3xs font-black shadow-xs transition active:scale-95 shrink-0 flex items-center gap-1"
            >
              <span>✓</span>
              <span>Entregar Todo</span>
            </button>
          </div>
          
          <div 
            v-for="itemAnt in ordenActiva.items" 
            :key="itemAnt.id"
            :class="[
              'p-2.5 rounded-xl border flex flex-col gap-1.5 text-xs transition-all',
              ['listo', 'recibido_mesero'].includes(itemAnt.estado)
                ? 'bg-emerald-50 dark:bg-emerald-950/40 border-emerald-300 dark:border-emerald-700/80 shadow-2xs ring-1 ring-emerald-500/30'
                : itemAnt.estado === 'entregado'
                ? 'bg-slate-50/70 dark:bg-slate-800/40 border-slate-200 dark:border-slate-800'
                : 'bg-white dark:bg-slate-800/60 border-slate-200 dark:border-slate-700'
            ]"
          >
            <div class="flex justify-between items-start gap-2">
              <div class="flex-1 min-w-0">
                <div class="font-bold text-slate-800 dark:text-slate-100 text-xs">
                  {{ itemAnt.cantidad }}x {{ itemAnt.producto_nombre }}
                </div>
                <div v-if="itemAnt.extras && itemAnt.extras.length > 0" class="flex flex-wrap gap-1 mt-0.5">
                  <span v-for="(ex, ei) in itemAnt.extras" :key="ei" class="text-3xs bg-slate-200 dark:bg-slate-700 text-slate-700 dark:text-slate-300 px-1 py-0.2 rounded font-medium">
                    + {{ ex.nombre }}
                  </span>
                </div>
                <div v-if="itemAnt.notas" class="text-3xs text-slate-500 italic mt-0.5">{{ itemAnt.notas }}</div>
              </div>
              <div class="text-right shrink-0">
                <span class="text-3xs font-extrabold px-1.5 py-0.5 rounded uppercase" :class="badgeColorItem(itemAnt.estado)">
                  {{ textoEstadoItem(itemAnt.estado) }}
                </span>
                <div class="text-2xs font-bold text-slate-600 dark:text-slate-400 mt-0.5">
                  ${{ (Number(itemAnt.precio_unitario) * itemAnt.cantidad).toFixed(2) }}
                </div>
              </div>
            </div>

            <!-- Botón de acción para el mesero cuando está listo en barra -->
            <div 
              v-if="['listo', 'recibido_mesero'].includes(itemAnt.estado)"
              class="pt-1.5 border-t border-emerald-200/60 dark:border-emerald-800/60 flex justify-between items-center gap-2"
            >
              <span class="text-3xs font-extrabold text-emerald-700 dark:text-emerald-300 flex items-center gap-1">
                <span>🍽️</span> Listo en Barra
              </span>
              <button 
                @click="marcarItemEntregado(itemAnt)"
                class="px-3 py-1.5 min-h-[34px] bg-emerald-600 hover:bg-emerald-700 text-white rounded-xl text-3xs font-black shadow-xs transition active:scale-95 flex items-center gap-1"
                title="Marcar este platillo como servido en la mesa del cliente"
              >
                <span>✓</span>
                <span>Entregar al Cliente</span>
              </button>
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
          <!-- Botón Pedir Cuenta / Ir a Caja si ya hay orden activa -->
          <button 
            v-if="ordenActiva"
            @click="pedirCuentaMesa"
            class="flex-1 py-3 bg-amber-500 hover:bg-amber-600 text-white rounded-xl font-bold text-xs shadow-sm transition active:scale-95 flex items-center justify-center gap-1.5"
          >
            <span>{{ esExterno ? '💵' : '🧾' }}</span>
            <span>{{ esExterno ? 'Ir a Caja' : 'Pedir Cuenta' }}</span>
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

    <!-- Modal Selección Comida Corrida (Menú del Día) -->
    <div v-if="modalMenuDelDia && ccSeleccionada" class="fixed inset-0 bg-slate-900/60 backdrop-blur-sm flex items-center justify-center p-4 z-50">
      <div class="bg-white dark:bg-slate-900 rounded-3xl p-6 max-w-lg w-full shadow-2xl border border-slate-200 dark:border-slate-800 space-y-4 max-h-[90vh] flex flex-col">
        <!-- Header Modal -->
        <div class="flex justify-between items-center border-b border-slate-100 dark:border-slate-800 pb-3">
          <div class="flex items-center gap-2.5">
            <div 
              v-if="ccSeleccionada.imagen_url" 
              class="w-10 h-10 rounded-xl overflow-hidden shrink-0 border border-slate-200 dark:border-slate-700 bg-slate-100 dark:bg-slate-800"
            >
              <img 
                :src="menuStore.obtenerUrlImagen(ccSeleccionada.imagen_url)" 
                :alt="ccSeleccionada.nombre" 
                class="w-full h-full object-cover" 
                @error="$event.target.style.display = 'none'"
              />
            </div>
            <span v-else class="text-2xl">🍱</span>
            <div>
              <h3 class="text-base font-black text-slate-800 dark:text-slate-100">{{ ccSeleccionada.nombre || 'Comida Corrida' }}</h3>
              <span class="text-xs font-bold text-amber-600 dark:text-amber-400">
                Horario: {{ menuStore.menuDelDia?.hora_inicio || '12:00' }} - {{ menuStore.menuDelDia?.hora_fin || '18:00' }}
              </span>
            </div>
          </div>
          <button @click="modalMenuDelDia = false" class="text-slate-400 hover:text-slate-600 font-bold text-lg">✕</button>
        </div>

        <div class="flex-1 overflow-y-auto space-y-4 pr-1">
          <!-- 1. Entrada -->
          <div v-if="ccSeleccionada.entradas?.length" class="space-y-1.5">
            <label class="text-xs font-black uppercase text-slate-700 dark:text-slate-300 flex items-center justify-between">
              <span>🥣 1. Entrada</span>
              <span class="text-3xs text-amber-700 dark:text-amber-400 font-bold">{{ mddEntradaSeleccionada }}</span>
            </label>
            <div class="grid grid-cols-1 sm:grid-cols-2 gap-2">
              <button
                v-for="ent in ccSeleccionada.entradas"
                :key="ent"
                type="button"
                @click="mddEntradaSeleccionada = ent"
                class="p-2.5 rounded-xl border text-left text-xs font-bold transition active:scale-95 flex items-center justify-between"
                :class="mddEntradaSeleccionada === ent ? 'border-amber-500 bg-amber-50 dark:bg-amber-950/40 text-amber-900 dark:text-amber-200 shadow-2xs' : 'border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-800 text-slate-700 dark:text-slate-300'"
              >
                <span>{{ ent }}</span>
                <span v-if="mddEntradaSeleccionada === ent">✓</span>
              </button>
            </div>
          </div>

          <!-- 2. Plato Fuerte con Guarnición -->
          <div v-if="ccSeleccionada.platos_fuertes?.length" class="space-y-1.5">
            <label class="text-xs font-black uppercase text-slate-700 dark:text-slate-300 flex items-center justify-between">
              <span>🍖 2. Plato Fuerte con Guarnición</span>
              <span class="text-3xs text-amber-700 dark:text-amber-400 font-bold">{{ mddFuerteSeleccionado }}</span>
            </label>
            <div class="grid grid-cols-1 sm:grid-cols-2 gap-2">
              <button
                v-for="pf in ccSeleccionada.platos_fuertes"
                :key="pf"
                type="button"
                @click="mddFuerteSeleccionado = pf"
                class="p-2.5 rounded-xl border text-left text-xs font-bold transition active:scale-95 flex items-center justify-between"
                :class="mddFuerteSeleccionado === pf ? 'border-amber-500 bg-amber-50 dark:bg-amber-950/40 text-amber-900 dark:text-amber-200 shadow-2xs' : 'border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-800 text-slate-700 dark:text-slate-300'"
              >
                <span>{{ pf }}</span>
                <span v-if="mddFuerteSeleccionado === pf">✓</span>
              </button>
            </div>
          </div>

          <!-- 3. Bebida -->
          <div v-if="ccSeleccionada.bebidas?.length" class="space-y-1.5">
            <label class="text-xs font-black uppercase text-slate-700 dark:text-slate-300 flex items-center justify-between">
              <span>🥤 3. Bebida del Día</span>
              <span class="text-3xs text-amber-700 dark:text-amber-400 font-bold">{{ mddBebidaSeleccionada }}</span>
            </label>
            <div class="grid grid-cols-1 sm:grid-cols-2 gap-2">
              <button
                v-for="be in ccSeleccionada.bebidas"
                :key="be"
                type="button"
                @click="mddBebidaSeleccionada = be"
                class="p-2.5 rounded-xl border text-left text-xs font-bold transition active:scale-95 flex items-center justify-between"
                :class="mddBebidaSeleccionada === be ? 'border-amber-500 bg-amber-50 dark:bg-amber-950/40 text-amber-900 dark:text-amber-200 shadow-2xs' : 'border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-800 text-slate-700 dark:text-slate-300'"
              >
                <span>{{ be }}</span>
                <span v-if="mddBebidaSeleccionada === be">✓</span>
              </button>
            </div>
          </div>

          <!-- 4. Postre (Opcional) -->
          <div v-if="ccSeleccionada.postres?.length" class="space-y-1.5">
            <label class="text-xs font-black uppercase text-slate-700 dark:text-slate-300 flex items-center justify-between">
              <span>🍮 4. Postre (Opcional)</span>
              <span class="text-3xs text-amber-700 dark:text-amber-400 font-bold">{{ mddPostreSeleccionado || 'Sin postre' }}</span>
            </label>
            <div class="grid grid-cols-2 gap-2">
              <button
                type="button"
                @click="mddPostreSeleccionado = ''"
                class="p-2.5 rounded-xl border text-left text-xs font-bold transition active:scale-95"
                :class="!mddPostreSeleccionado ? 'border-slate-400 bg-slate-100 dark:bg-slate-700 text-slate-800 dark:text-slate-100' : 'border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-800 text-slate-500'"
              >
                Sin postre
              </button>
              <button
                v-for="po in ccSeleccionada.postres"
                :key="po"
                type="button"
                @click="mddPostreSeleccionado = po"
                class="p-2.5 rounded-xl border text-left text-xs font-bold transition active:scale-95 flex items-center justify-between"
                :class="mddPostreSeleccionado === po ? 'border-amber-500 bg-amber-50 dark:bg-amber-950/40 text-amber-900 dark:text-amber-200 shadow-2xs' : 'border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-800 text-slate-700 dark:text-slate-300'"
              >
                <span>{{ po }}</span>
                <span v-if="mddPostreSeleccionado === po">✓</span>
              </button>
            </div>
          </div>

          <!-- Para Llevar y Notas -->
          <div class="p-3 bg-amber-50/60 dark:bg-amber-950/40 rounded-2xl border border-amber-200 dark:border-amber-900/50 space-y-2">
            <div class="flex items-center justify-between">
              <span class="text-xs font-black text-slate-800 dark:text-slate-100">¿Para Llevar?</span>
              <button 
                type="button" 
                @click="mddParaLlevar = !mddParaLlevar"
                class="px-3 py-1.5 rounded-xl font-bold text-xs transition active:scale-95"
                :class="mddParaLlevar ? 'bg-amber-500 text-white' : 'bg-white dark:bg-slate-700 text-slate-700 dark:text-slate-200 border border-slate-300 dark:border-slate-600'"
              >
                {{ mddParaLlevar ? '✓ Sí, Empacar (+$' + mddCargoDesechable + ')' : 'Comer Aquí' }}
              </button>
            </div>
            <input 
              v-model="mddNotas"
              type="text" 
              maxlength="150"
              placeholder="Nota especial (ej. salsa verde aparte, agua sin hielo)"
              class="w-full p-2 text-xs bg-white dark:bg-slate-800 border border-slate-300 dark:border-slate-700 rounded-xl text-slate-800 dark:text-slate-100 focus:outline-none focus:border-amber-500"
            />
          </div>
        </div>

        <!-- Footer Modal -->
        <div class="pt-3 border-t border-slate-100 dark:border-slate-800 flex items-center justify-between gap-3">
          <div>
            <span class="text-2xs text-slate-400 block font-semibold">Total Comida</span>
            <span class="text-lg font-black text-eden-600 dark:text-eden-400 font-mono">
              ${{ (Number(ccSeleccionada.precio || 95) + (mddParaLlevar ? mddCargoDesechable : 0)).toFixed(2) }}
            </span>
          </div>
          <div class="flex gap-2">
            <button 
              @click="modalMenuDelDia = false" 
              class="px-4 py-2 text-xs font-bold text-slate-600 dark:text-slate-300 hover:bg-slate-100 dark:hover:bg-slate-800 rounded-xl"
            >
              Cancelar
            </button>
            <button 
              @click="confirmarAgregarMenuDelDia"
              class="px-5 py-2 text-xs font-black bg-amber-500 hover:bg-amber-600 text-white rounded-xl shadow-xs transition active:scale-95 flex items-center gap-1.5"
            >
              <span>+ Agregar a Comanda</span>
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
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

const ordenIdParam = computed(() => route.query.ordenId ? Number(route.query.ordenId) : null)
const mesaIdParam = computed(() => route.query.mesaId ? Number(route.query.mesaId) : null)
const tipoPedidoParam = computed(() => {
  if (route.query.tipoPedido) return route.query.tipoPedido
  if (ordenActiva.value?.tipo_pedido) return ordenActiva.value.tipo_pedido
  return mesaIdParam.value ? 'comedor' : 'para_llevar'
})

const esRolAlto = computed(() => {
  return ['administrador', 'gerente', 'jefe'].includes(authStore.rolActual)
})

const esExterno = computed(() => {
  return tipoPedidoParam.value === 'domicilio' || tipoPedidoParam.value === 'para_llevar' ||
    Boolean(ordenActiva.value && ['domicilio', 'para_llevar'].includes(ordenActiva.value.tipo_pedido))
})

const esPedidoExternoNoPermitido = computed(() => {
  if (esRolAlto.value) return false
  return esExterno.value && ['mesero', 'auxiliar_general'].includes(authStore.rolActual)
})

const mesaActual = computed(() => {
  if (!mesaIdParam.value) return null
  return mesasStore.mesas.find(m => m.id === mesaIdParam.value)
})

const esMesaDeOtroMesero = computed(() => {
  if (esExterno.value) return false
  if (!mesaActual.value || !mesaActual.value.mesero_id) return false
  if (esRolAlto.value) return false
  return mesaActual.value.mesero_id !== authStore.usuarioActual?.id
})

const mesaNumero = computed(() => {
  if (ordenActiva.value) {
    if (ordenActiva.value.tipo_pedido === 'domicilio') {
      const cli = ordenActiva.value.datos_entrega?.cliente
      return `🛵 Envío #${ordenActiva.value.id}${cli ? ` - ${cli}` : ''}`
    } else if (ordenActiva.value.tipo_pedido === 'para_llevar') {
      const cli = ordenActiva.value.datos_entrega?.cliente
      return `🛍️ Mostrador #${ordenActiva.value.id}${cli ? ` - ${cli}` : ''}`
    }
  }
  if (route.query.mesaNumero) return route.query.mesaNumero
  if (mesaIdParam.value) return `Mesa ${mesaIdParam.value}`
  if (tipoPedidoParam.value === 'domicilio') return '🛵 Pedido para Envío'
  if (tipoPedidoParam.value === 'para_llevar') return '🛍️ Pedido Mostrador'
  return 'Comanda'
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

// Modal Comida Corrida (Menú del Día)
const modalMenuDelDia = ref(false)
const ccSeleccionada = ref(null)
const mddEntradaSeleccionada = ref('')
const mddFuerteSeleccionado = ref('')
const mddBebidaSeleccionada = ref('')
const mddPostreSeleccionado = ref('')
const mddParaLlevar = ref(false)
const mddCargoDesechable = ref(5)
const mddNotas = ref('')

const comidasCorridasActivas = computed(() => {
  if (!menuStore.menuDelDia?.activo) return []
  return (menuStore.menuDelDia.comidas_corridas || []).filter(c => c.activo !== false)
})

const abrirModalComidaCorrida = (cc) => {
  ccSeleccionada.value = cc
  mddEntradaSeleccionada.value = cc.entradas?.[0] || ''
  mddFuerteSeleccionado.value = cc.platos_fuertes?.[0] || ''
  mddBebidaSeleccionada.value = cc.bebidas?.[0] || ''
  mddPostreSeleccionado.value = cc.postres?.[0] || ''
  mddParaLlevar.value = false
  mddCargoDesechable.value = 5
  mddNotas.value = ''
  modalMenuDelDia.value = true
}

const confirmarAgregarMenuDelDia = () => {
  if (!ccSeleccionada.value) return
  const cc = ccSeleccionada.value
  const precioBase = Number(cc.precio || 95.0)
  const cargoDesechable = mddParaLlevar.value ? Number(mddCargoDesechable.value || 0) : 0
  const precioUnitario = precioBase + cargoDesechable

  let notasPartes = []
  if (mddEntradaSeleccionada.value) {
    notasPartes.push(`🥣 Entrada: ${mddEntradaSeleccionada.value}`)
  }
  if (mddFuerteSeleccionado.value) {
    notasPartes.push(`🍖 Fuerte: ${mddFuerteSeleccionado.value}`)
  }
  if (mddBebidaSeleccionada.value) {
    notasPartes.push(`🥤 Bebida: ${mddBebidaSeleccionada.value}`)
  }
  if (mddPostreSeleccionado.value) {
    notasPartes.push(`🍮 Postre: ${mddPostreSeleccionado.value}`)
  }
  if (mddNotas.value.trim()) {
    notasPartes.push(`Nota: ${mddNotas.value.trim()}`)
  }
  if (mddParaLlevar.value) {
    notasPartes.push('[PARA LLEVAR]')
  }

  const prod = menuStore.productos.find(p => p.tipo_item === 'menu_del_dia') || menuStore.productos[0]

  itemsComanda.value.push({
    id: prod ? prod.id : 9999,
    nombre: cc.nombre,
    precioBase: precioBase,
    precio: precioUnitario,
    cantidad: 1,
    notas: notasPartes.join(' | '),
    categoria_id: prod?.categoria_id,
    requiere_cocina: true,
    cargo_desechable: cargoDesechable
  })

  modalMenuDelDia.value = false
}

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

let timerOrden = null

onMounted(async () => {
  await Promise.all([
    menuStore.cargarCatalogo(),
    mesasStore.cargarMesas()
  ])
  await cargarOrden()

  // Polling automático para que el mesero reciba avisos de barra/cocina en tiempo real
  timerOrden = setInterval(() => {
    cargarOrden()
  }, 3500)
})

onUnmounted(() => {
  if (timerOrden) {
    clearInterval(timerOrden)
  }
})

const itemsListosParaEntrega = computed(() => {
  if (!ordenActiva.value || !ordenActiva.value.items) return []
  return ordenActiva.value.items.filter(i => ['listo', 'recibido_mesero'].includes(i.estado))
})

const marcarItemEntregado = async (item) => {
  try {
    await ordenesStore.cambiarEstadoItem(item.id, 'entregado')
    await cargarOrden()
  } catch (err) {
    alert(err.response?.data?.detail || 'Error al marcar platillo como entregado.')
  }
}

const entregarTodosListos = async () => {
  if (!ordenActiva.value) return
  try {
    await ordenesStore.entregarItemsOrden(ordenActiva.value.id)
    await cargarOrden()
    alert('¡Todos los platillos listos han sido marcados como entregados al comensal!')
  } catch (err) {
    alert(err.response?.data?.detail || 'Error al entregar los platillos.')
  }
}

const cargarOrden = async () => {
  if (esPedidoExternoNoPermitido.value) {
    ordenActiva.value = null
    return
  }
  if (ordenIdParam.value) {
    ordenActiva.value = await ordenesStore.obtenerOrden(ordenIdParam.value, authStore.usuarioActual?.id)
    return
  }
  if (mesaIdParam.value) {
    if (esMesaDeOtroMesero.value) {
      ordenActiva.value = null
      return
    }
    ordenActiva.value = await ordenesStore.obtenerOrdenActivaMesa(mesaIdParam.value, authStore.usuarioActual?.id)
  }
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
  if (esPedidoExternoNoPermitido.value) {
    alert('Los meseros no tienen autorización para pedidos de entrega a domicilio o mostrador.')
    return
  }
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
      extras: (i.extras || []).map(e => ({ nombre: e.nombre, precio: e.precio })),
      cargo_desechable: i.cargo_desechable || 0
    }))

    if (ordenActiva.value) {
      // Agregar ronda adicional a la orden existente pasando usuario_id
      await ordenesStore.agregarItemsAOrden(ordenActiva.value.id, itemsPayload, authStore.usuarioActual?.id)
      alert(`¡Ronda adicional enviada a Cocina/Barra para ${mesaNumero.value}!`)
    } else {
      // Crear nueva comanda
      const ordenPayload = {
        mesa_id: mesaIdParam.value,
        mesero_id: authStore.usuarioActual?.id || 1,
        tipo_pedido: tipoPedidoParam.value || 'comedor',
        notas: notasGenerales.value || null,
        items: itemsPayload
      }
      const nueva = await ordenesStore.enviarComanda(ordenPayload)
      ordenActiva.value = nueva
      alert(`¡Comanda enviada a Cocina/Barra para ${mesaNumero.value}!`)
    }

    itemsComanda.value = []
    notasGenerales.value = ''
    await cargarOrden()
  } catch (err) {
    alert(err.response?.data?.detail || 'Error al enviar la comanda a cocina.')
  } finally {
    enviando.value = false
  }
}

const pedirCuentaMesa = async () => {
  if (esMesaDeOtroMesero.value || esPedidoExternoNoPermitido.value) return
  if (!ordenActiva.value) return
  if (esExterno.value) {
    router.push('/caja')
    return
  }

  // Si hay platillos listos en barra sin entregar, ofrecer entregarlos directamente
  if (itemsListosParaEntrega.value.length > 0) {
    if (confirm(`Hay ${itemsListosParaEntrega.value.length} platillo(s) listos en barra. ¿Deseas marcarlos como entregados al cliente y solicitar la cuenta?`)) {
      try {
        await ordenesStore.entregarItemsOrden(ordenActiva.value.id)
        await cargarOrden()
      } catch (e) {
        console.error('Error al entregar items pendientes:', e)
      }
    } else {
      return
    }
  }

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
    case 'listo': return 'bg-emerald-100 text-emerald-800 dark:bg-emerald-900/60 dark:text-emerald-200 font-bold'
    case 'entregado': return 'bg-purple-100 text-purple-800 dark:bg-purple-900/60 dark:text-purple-200'
    default: return 'bg-slate-100 text-slate-800 dark:bg-slate-800 dark:text-slate-200'
  }
}

const textoEstadoItem = (estado) => {
  switch (estado) {
    case 'en_observacion': return '⚠️ Incidencia'
    case 'pendiente': return '⏳ En cocina'
    case 'preparando': return '👨‍🍳 Preparando'
    case 'listo': return '🟢 Listo en barra'
    case 'recibido_mesero': return '🟢 Listo en barra'
    case 'entregado': return '✓ Servido'
    case 'cancelado': return '✕ Cancelado'
    default: return estado
  }
}

const badgeColorItem = (estado) => {
  switch (estado) {
    case 'en_observacion': return 'bg-rose-500 text-white animate-pulse'
    case 'pendiente': return 'bg-slate-200 text-slate-700 dark:bg-slate-700 dark:text-slate-300'
    case 'preparando': return 'bg-amber-200 text-amber-800 dark:bg-amber-900 dark:text-amber-200'
    case 'listo': return 'bg-emerald-200 text-emerald-800 dark:bg-emerald-900 dark:text-emerald-200 font-bold'
    case 'recibido_mesero': return 'bg-blue-200 text-blue-800 dark:bg-blue-900 dark:text-blue-200 font-bold'
    case 'entregado': return 'bg-purple-200 text-purple-800 dark:bg-purple-900 dark:text-purple-200 font-bold'
    case 'cancelado': return 'bg-rose-200 text-rose-800 dark:bg-rose-900 dark:text-rose-200'
    default: return 'bg-slate-200 text-slate-700'
  }
}
</script>

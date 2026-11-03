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

        <!-- Botón para pedidos externos sin mesa (Mostrador o Envío a domicilio): Exclusivo roles de jefe para arriba -->
        <button 
          v-if="esRolAlto"
          @click="iniciarPedidoExterno"
          class="px-3.5 py-1.5 bg-amber-600 hover:bg-amber-700 text-white rounded-xl text-xs font-bold shadow-sm transition active:scale-95 flex items-center gap-1.5"
          title="Tomar pedido sin mesa para recoger en mostrador o entrega a domicilio"
        >
          <span>🛍️</span> + Pedido Mostrador / Envío
        </button>

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

      <!-- Pedidos activos para Envío y Para Llevar (Exclusivo jefatura / administración) -->
      <div v-if="esRolAlto && ordenesEspecialesActivas.length > 0" class="p-4 bg-white dark:bg-slate-900 rounded-2xl border border-slate-200 dark:border-slate-800 shadow-sm space-y-3">
        <div class="flex justify-between items-center">
          <div class="flex items-center gap-2">
            <span class="text-base">🛍️</span>
            <h3 class="text-xs font-black uppercase text-slate-700 dark:text-slate-300 tracking-wider">
              Pedidos de Mostrador y Envíos en Curso ({{ ordenesEspecialesActivas.length }})
            </h3>
          </div>
        </div>
        <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-3">
          <div 
            v-for="ord in ordenesEspecialesActivas" 
            :key="ord.id"
            @click="abrirOrdenEnComandero(ord)"
            class="p-3.5 rounded-xl border flex flex-col justify-between gap-2.5 transition shadow-xs cursor-pointer hover:shadow-md hover:border-eden-500 active:scale-95 group"
            :class="[
              ord.tipo_pedido === 'domicilio' ? 'bg-blue-50/50 dark:bg-blue-950/20 border-blue-200 dark:border-blue-800' : 'bg-amber-50/50 dark:bg-amber-950/20 border-amber-200 dark:border-amber-800',
              tieneObservacionCocina(ord) ? 'ring-2 ring-amber-500 border-amber-500 dark:border-amber-400' : ''
            ]"
          >
            <div class="space-y-2">
              <div class="flex justify-between items-start">
                <div>
                  <span class="text-xs font-black text-slate-900 dark:text-slate-100 block group-hover:text-eden-700 dark:group-hover:text-eden-400 transition-colors">
                    {{ ord.tipo_pedido === 'domicilio' ? '🛵 Envío Domicilio' : '🛍️ Mostrador (Llevar)' }} #{{ ord.id }}
                  </span>
                  <span class="text-2xs font-bold text-slate-600 dark:text-slate-300">
                    {{ ord.datos_entrega?.cliente || ord.mesero_nombre || 'Cliente' }}
                  </span>
                </div>
                <span class="text-3xs font-extrabold uppercase px-2 py-0.5 rounded-full" :class="badgeColorEstado(ord.estado)">
                  {{ ord.estado }}
                </span>
              </div>

              <!-- Alerta directa si Cocina reportó incidencia o falta de ingrediente -->
              <div 
                v-if="tieneObservacionCocina(ord)" 
                class="p-2.5 rounded-xl bg-amber-500/20 border border-amber-400 dark:border-amber-600 text-amber-900 dark:text-amber-200 text-2xs space-y-1.5"
              >
                <div class="font-black flex items-center justify-between">
                  <span class="flex items-center gap-1 animate-pulse">⚠️ Cocina solicita aclaración</span>
                  <span class="bg-amber-600 text-white text-3xs px-1.5 py-0.2 rounded-full font-bold">{{ itemsObservados(ord).length }}</span>
                </div>
                <div v-for="itemObs in itemsObservados(ord)" :key="itemObs.id" class="text-3xs italic font-semibold line-clamp-2">
                  "{{ itemObs.producto_nombre }}: {{ itemObs.observacion_cocina }}"
                </div>
                <button 
                  @click.stop="abrirModalAclaracionEspecial(ord)"
                  class="w-full py-1.5 bg-amber-600 hover:bg-amber-700 active:scale-95 text-white rounded-lg font-black text-2xs uppercase tracking-wide transition shadow-xs flex items-center justify-center gap-1"
                >
                  <span>💬</span> Atender Aclaración
                </button>
              </div>

              <div v-if="ord.datos_entrega?.direccion" class="text-3xs text-slate-600 dark:text-slate-400 truncate">
                📍 {{ ord.datos_entrega.direccion }}
              </div>
            </div>

            <div class="flex justify-between items-center pt-2 border-t border-slate-200/60 dark:border-slate-800 gap-1.5">
              <span class="font-mono font-black text-xs text-eden-600 dark:text-eden-400">${{ Number(ord.total).toFixed(2) }}</span>
              <div class="flex items-center gap-2">
                <span class="text-3xs font-bold text-slate-400 group-hover:text-eden-600 dark:group-hover:text-eden-400 transition flex items-center gap-0.5">
                  Ver comanda →
                </span>
                <button 
                  @click.stop="cancelarPedidoEspecial(ord)"
                  class="p-1 hover:bg-rose-50 text-slate-400 hover:text-rose-600 dark:hover:bg-rose-950/50 rounded-lg text-3xs font-bold transition"
                  title="Cancelar pedido especial"
                >
                  ✕
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Cuadrícula unificada de Mesas -->
      <div class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 2xl:grid-cols-6 gap-3 sm:gap-3.5">
        <div 
          v-for="mesa in mesasFiltradas" 
          :key="mesa.id"
          @click="abrirOpcionesMesa(mesa)"
          :class="[
            'p-3.5 sm:p-4 rounded-2xl border-2 transition-all cursor-pointer flex flex-col justify-between min-h-[8.5rem] h-auto active:scale-95 shadow-sm',
            mesa.estado === 'libre' ? 'border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 hover:border-emerald-500 hover:shadow-md' :
            mesa.estado === 'ocupada' ? 'border-amber-400 dark:border-amber-600 bg-amber-50/70 dark:bg-amber-950/30 hover:border-amber-500' :
            'border-rose-400 dark:border-rose-600 bg-rose-50/70 dark:bg-rose-950/30 hover:border-rose-500'
          ]"
        >
          <div class="flex justify-between items-start gap-1">
            <span class="font-bold text-sm sm:text-base text-slate-800 dark:text-slate-100 truncate">{{ mesa.numero }}</span>
            <div class="flex items-center gap-1.5 shrink-0">
              <span v-if="getAlertaMesa(mesa.id)" 
                :class="[
                  'text-3xs font-black px-2 py-0.5 rounded-full uppercase whitespace-nowrap shrink-0 shadow-2xs',
                  getAlertaMesa(mesa.id).tipo === 'observacion' ? 'bg-amber-500 text-white animate-pulse' : 'bg-emerald-600 text-white'
                ]">
                {{ getAlertaMesa(mesa.id).texto }}
              </span>
              <span 
                :class="[
                  'w-2.5 h-2.5 rounded-full shrink-0',
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
                : (esRolAlto 
                  ? 'text-slate-700 dark:text-slate-200 bg-slate-100 dark:bg-slate-800 border-slate-200/80 dark:border-slate-700/60'
                  : 'text-amber-800 dark:text-amber-300 bg-amber-50 dark:bg-amber-950/40 border-amber-200 dark:border-amber-900/60 font-semibold')"
              :title="'Mesero: ' + mesa.mesero_nombre"
            >
              <span class="text-xs">{{ mesa.mesero_id === authStore.usuarioActual?.id ? '🤵' : (esRolAlto ? '🤵' : '🔒') }}</span>
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
              maxlength="50"
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
        
        <!-- Encabezado: Nombre de la Mesa y Badge de Estado -->
        <div class="flex justify-between items-center border-b border-slate-100 dark:border-slate-800 pb-3">
          <div>
            <h3 class="text-xl font-black text-slate-800 dark:text-slate-100">{{ mesaSeleccionada.numero }}</h3>
            <p v-if="mesaSeleccionada.mesero_nombre" class="text-xs font-semibold text-eden-700 dark:text-eden-400 mt-0.5 flex items-center gap-1">
              <span>🤵</span> Mesero: {{ mesaSeleccionada.mesero_nombre }}
            </p>
            <p v-else class="text-xs font-medium text-slate-400 mt-0.5">
              Mesa libre (sin asignar)
            </p>
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

        <!-- Selector de delegación exclusivo para Roles Altos (Admin, Gerente, Jefe) -->
        <div 
          v-if="esRolAlto && colaboradoresAtencion.length > 0" 
          class="p-2.5 bg-slate-50 dark:bg-slate-800/60 rounded-xl border border-slate-200/60 dark:border-slate-700/60 flex items-center justify-between gap-2"
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

        <!-- Aviso si la mesa pertenece a otro mesero -->
        <div 
          v-if="esMesaDeOtroMesero(mesaSeleccionada)" 
          class="p-4 rounded-2xl bg-amber-50 dark:bg-amber-950/40 border border-amber-300 dark:border-amber-800 text-center space-y-2"
        >
          <div class="text-3xl">🔒</div>
          <div class="font-extrabold text-amber-900 dark:text-amber-200 text-sm">
            Mesa de otro mesero
          </div>
          <p class="text-xs text-amber-800 dark:text-amber-300">
            Esta mesa está asignada a <strong>{{ mesaSeleccionada.mesero_nombre }}</strong>. Por políticas del restaurante, solo el mesero responsable o personal de jefatura pueden ver sus comandas y agregar rondas.
          </p>
        </div>

        <!-- FLUJO PRINCIPAL DE ACCIONES DE LA MESA -->
        <div v-else class="space-y-3 pt-1">
          <!-- 1. CUANDO LA MESA ESTÁ "LIBRE": ÚNICO BOTÓN PRINCIPAL "TOMAR MESA" -->
          <template v-if="mesaSeleccionada.estado === 'libre'">
            <button 
              @click="tomarMesaAsignarAMi(mesaSeleccionada)"
              class="w-full py-4 bg-eden-600 hover:bg-eden-700 active:scale-95 text-white rounded-2xl font-black text-sm shadow-md transition flex items-center justify-center gap-2"
            >
              <span class="text-lg">👋</span>
              <span>Tomar Mesa</span>
            </button>
            <p class="text-center text-2xs text-slate-400 font-medium">
              Selecciona para asignarte la mesa e iniciar la atención.
            </p>
          </template>

          <!-- 2. CUANDO LA MESA YA ESTÁ TOMADA / OCUPADA O EN CUENTA -->
          <template v-else>
            <!-- Tomar Orden / Agregar Rondas en Comandero -->
            <button 
              @click="abrirComandero(mesaSeleccionada)"
              class="w-full py-3.5 bg-eden-600 hover:bg-eden-700 text-white rounded-xl font-black text-xs shadow-sm transition active:scale-95 flex items-center justify-center gap-2"
            >
              <span>📝</span>
              <span>{{ tieneConsumoActivo(mesaSeleccionada) ? 'Ver / Agregar Rondas' : 'Tomar Orden (Comandero)' }}</span>
            </button>

            <!-- Solicitar Cuenta: ÚNICAMENTE visible si tiene consumos y todos los platillos están servidos/entregados -->
            <button 
              v-if="puedeSolicitarCuenta(mesaSeleccionada)"
              @click="solicitarCuentaMesa(mesaSeleccionada)"
              class="w-full py-2.5 bg-rose-50 dark:bg-rose-950/40 hover:bg-rose-100 border border-rose-300 dark:border-rose-800 text-rose-700 dark:text-rose-300 rounded-xl font-bold text-xs transition active:scale-95 flex items-center justify-center gap-1.5"
            >
              <span>🧾</span> Solicitar Cuenta (Pasar a Por Cobrar)
            </button>

            <!-- Aviso si la mesa tiene platillos en cocina pendientes -->
            <div 
              v-else-if="mesaSeleccionada.estado === 'ocupada' && tieneItemsEnCocinaMesa(mesaSeleccionada)"
              class="p-2 bg-amber-50 dark:bg-amber-950/40 border border-amber-200 dark:border-amber-800/60 rounded-xl text-center text-xs font-bold text-amber-800 dark:text-amber-300"
            >
              ⏳ Platillos en preparación / por entregar en cocina
            </div>

            <!-- Si está en estado cuenta: Botón Ir a Caja y Botón Reabrir Mesa -->
            <template v-if="mesaSeleccionada.estado === 'cuenta'">
              <button 
                @click="router.push('/caja')"
                class="w-full py-2.5 bg-purple-600 hover:bg-purple-700 text-white rounded-xl font-bold text-xs shadow-sm transition active:scale-95 flex items-center justify-center gap-1.5"
              >
                <span>💵</span> Ir a Caja para Cobrar
              </button>
              <button 
                @click="reabrirMesaOcupada(mesaSeleccionada)"
                class="w-full py-2 bg-amber-50 dark:bg-amber-950/40 hover:bg-amber-100 text-amber-800 dark:text-amber-300 border border-amber-300 dark:border-amber-800 rounded-xl font-bold text-xs transition active:scale-95 flex items-center justify-center gap-1.5"
                title="Cancelar solicitud de cuenta y regresar la mesa al estado ocupada"
              >
                <span>🔄</span> Reabrir Mesa (Volver a Ocupada)
              </button>
            </template>

            <!-- El botón "Liberar Mesa" solo visible si no hay consumo activo o la comanda fue cancelada / pagada -->
            <button 
              v-if="puedeLiberarMesa(mesaSeleccionada)"
              @click="liberarMesaSinConsumo(mesaSeleccionada)"
              class="w-full py-2.5 bg-slate-100 dark:bg-slate-800 hover:bg-rose-50 dark:hover:bg-rose-950/30 text-slate-700 dark:text-slate-300 hover:text-rose-700 dark:hover:text-rose-300 border border-slate-200 dark:border-slate-700 hover:border-rose-300 dark:hover:border-rose-800/60 rounded-xl font-bold text-xs transition active:scale-95 flex items-center justify-center gap-1.5"
              title="Liberar mesa si no han realizado pedido o comanda cancelada/pagada"
            >
              <span>🪑</span> Liberar Mesa
            </button>
          </template>

          <!-- Opción de editar mesa (solo roles altos) -->
          <button 
            v-if="esRolAlto"
            @click="abrirEditarMesa(mesaSeleccionada)"
            class="w-full py-2 bg-slate-100 dark:bg-slate-800 hover:bg-slate-200 dark:hover:bg-slate-700 text-slate-600 dark:text-slate-400 rounded-xl font-semibold text-2xs transition active:scale-95 flex items-center justify-center gap-1.5 border border-slate-200 dark:border-slate-700"
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
              maxlength="50"
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

    <!-- Modal para Resolver Aclaración de Cocina en Pedidos de Envío o Para Llevar -->
    <div v-if="modalAclaracionEspecial && ordenSeleccionadaAclaracion" class="fixed inset-0 bg-slate-900/60 backdrop-blur-sm flex items-center justify-center p-4 z-50">
      <div class="bg-white dark:bg-slate-900 rounded-3xl p-6 max-w-md w-full shadow-2xl border border-slate-200 dark:border-slate-800 space-y-4">
        <div class="flex items-center justify-between border-b border-slate-100 dark:border-slate-800 pb-3">
          <div class="flex items-center gap-2">
            <span class="text-2xl">👨‍🍳</span>
            <div>
              <h3 class="text-base font-black text-slate-800 dark:text-slate-100">
                Aclaración de Cocina · {{ ordenSeleccionadaAclaracion.tipo_pedido === 'domicilio' ? 'Envío' : 'Para Llevar' }} #{{ ordenSeleccionadaAclaracion.id }}
              </h3>
              <p class="text-2xs text-slate-400 font-semibold">
                Cliente: {{ ordenSeleccionadaAclaracion.datos_entrega?.cliente || 'Mostrador' }}
              </p>
            </div>
          </div>
          <button @click="modalAclaracionEspecial = false" class="text-slate-400 hover:text-slate-600 font-bold text-sm">✕</button>
        </div>

        <div class="space-y-3 max-h-[60vh] overflow-y-auto">
          <div 
            v-for="item in itemsObservados(ordenSeleccionadaAclaracion)" 
            :key="item.id"
            class="p-3 bg-amber-50 dark:bg-amber-950/40 rounded-2xl border border-amber-200 dark:border-amber-800/60 space-y-2 text-xs"
          >
            <div class="font-black text-slate-800 dark:text-slate-100 flex justify-between items-center">
              <span>{{ item.producto_nombre }} ({{ item.cantidad }}x)</span>
              <span class="text-3xs uppercase px-2 py-0.5 rounded-full bg-amber-200 dark:bg-amber-900 text-amber-900 dark:text-amber-200 font-bold">En Observación</span>
            </div>
            
            <div class="p-2 bg-white dark:bg-slate-900 rounded-xl border border-amber-200 dark:border-amber-800/40 text-amber-900 dark:text-amber-200 font-semibold italic text-xs">
              "{{ item.observacion_cocina }}"
            </div>

            <div>
              <label class="text-2xs font-extrabold text-slate-600 dark:text-slate-400">Instrucción / Respuesta para Cocina:</label>
              <input 
                v-model="respuestasAclaracionEspecial[item.id]"
                type="text"
                maxlength="200"
                placeholder="Ej. Cambiar a salsa roja / sin cebolla"
                class="w-full mt-1 p-2 text-xs font-semibold border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-800 text-slate-800 dark:text-slate-100 rounded-xl focus:outline-none focus:border-eden-600"
                @keyup.enter="enviarRespuestaAclaracion(item.id, 'continuar')"
              />
            </div>

            <div class="flex gap-2 pt-1">
              <button 
                @click="enviarRespuestaAclaracion(item.id, 'cancelar')"
                class="px-3 py-1.5 bg-rose-50 dark:bg-rose-950/40 hover:bg-rose-100 text-rose-700 dark:text-rose-300 border border-rose-300 dark:border-rose-800 rounded-xl font-bold text-2xs transition active:scale-95"
              >
                ✕ Cancelar Platillo
              </button>
              <button 
                @click="enviarRespuestaAclaracion(item.id, 'continuar')"
                :disabled="!respuestasAclaracionEspecial[item.id]?.trim()"
                class="flex-1 py-1.5 bg-eden-600 hover:bg-eden-700 disabled:opacity-50 text-white rounded-xl font-bold text-2xs shadow-xs transition active:scale-95"
              >
                ✓ Responder y Continuar
              </button>
            </div>
          </div>
        </div>

        <div class="pt-2 border-t border-slate-100 dark:border-slate-800 flex justify-between items-center">
          <button 
            @click="cancelarPedidoCompletoDesdeAclaracion"
            class="px-3 py-1.5 bg-rose-50 dark:bg-rose-950/40 hover:bg-rose-100 text-rose-600 dark:text-rose-400 border border-rose-200 dark:border-rose-900 rounded-xl text-xs font-bold transition active:scale-95"
            title="Cancelar toda la orden si el cliente ya no desea el pedido"
          >
            ✕ Cancelar Todo el Pedido
          </button>
          <button 
            @click="modalAclaracionEspecial = false"
            class="px-4 py-2 text-xs font-bold text-slate-500 hover:text-slate-700"
          >
            Cerrar
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
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

const esMesaDeOtroMesero = (mesa) => {
  if (!mesa || !mesa.mesero_id) return false
  if (esRolAlto.value) return false
  return mesa.mesero_id !== authStore.usuarioActual?.id
}

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

let timerMesas = null

onMounted(() => {
  mesasStore.cargarMesas()
  ordenesStore.cargarOrdenesActivas()
  authStore.cargarUsuarios()

  timerMesas = setInterval(() => {
    mesasStore.cargarMesas()
    ordenesStore.cargarOrdenesActivas()
  }, 4500)
})

onUnmounted(() => {
  if (timerMesas) clearInterval(timerMesas)
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
  if (!['mesero', 'auxiliar_general', 'administrador', 'gerente', 'jefe'].includes(rol)) {
    alert('Solo los meseros y personal de servicio pueden tomar mesas.')
    return
  }
  try {
    const data = await mesasStore.asignarMesero(mesa.id, authStore.usuarioActual.id)
    mesa.mesero_id = data.mesero_id
    mesa.mesero_nombre = data.mesero_nombre
    mesa.estado = data.estado
    mesa.tiene_consumo = data.tiene_consumo
    if (mesaSeleccionada.value && mesaSeleccionada.value.id === mesa.id) {
      mesaSeleccionada.value.mesero_id = data.mesero_id
      mesaSeleccionada.value.mesero_nombre = data.mesero_nombre
      mesaSeleccionada.value.estado = data.estado
      mesaSeleccionada.value.tiene_consumo = data.tiene_consumo
    }
  } catch (err) {
    console.error('Error al asignarse la mesa:', err)
    alert(err.response?.data?.detail || 'Error al asignarse la mesa.')
  }
}

const reabrirMesaOcupada = async (mesa) => {
  if (!confirm(`¿Deseas cancelar la solicitud de cuenta y reabrir ${mesa.numero} como 'Ocupada'?`)) return
  try {
    await mesasStore.cambiarEstadoMesa(mesa.id, 'ocupada')
    mesa.estado = 'ocupada'
    alert(`La ${mesa.numero} ha vuelto al estado 'Ocupada'.`)
  } catch (err) {
    alert(err.response?.data?.detail || 'Error al reabrir la mesa.')
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
      await ordenesStore.cancelarOrden(ord.id, { motivo: 'Clientes se retiraron sin consumir', genera_merma: false })
    } catch (err) {
      console.warn('Error cancelando orden activa:', err)
    }
  } else if (ord) {
    try {
      await ordenesStore.cancelarOrden(ord.id, { motivo: 'Liberada sin consumo', genera_merma: false })
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
    mesa.tiene_consumo = false
    if (mesaSeleccionada.value && mesaSeleccionada.value.id === mesa.id) {
      mesaSeleccionada.value.estado = 'libre'
      mesaSeleccionada.value.mesero_id = null
      mesaSeleccionada.value.mesero_nombre = null
      mesaSeleccionada.value.tiene_consumo = false
    }
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
    mesa.tiene_consumo = data.tiene_consumo
    if (mesaSeleccionada.value && mesaSeleccionada.value.id === mesa.id) {
      mesaSeleccionada.value.mesero_id = data.mesero_id
      mesaSeleccionada.value.mesero_nombre = data.mesero_nombre
      mesaSeleccionada.value.estado = data.estado
      mesaSeleccionada.value.tiene_consumo = data.tiene_consumo
    }
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

const tieneConsumoActivo = (mesa) => {
  if (!mesa) return false
  const ord = ordenesStore.ordenesActivas.find(
    o => o.mesa_id === mesa.id && o.estado !== 'pagado' && o.estado !== 'cancelada'
  )
  if (ord) {
    return Boolean(ord.items && ord.items.some(i => i.estado !== 'cancelado'))
  }
  return mesa.tiene_consumo === true
}

const tieneItemsEnCocinaMesa = (mesa) => {
  if (!mesa) return false
  const ord = ordenesStore.ordenesActivas.find(
    o => o.mesa_id === mesa.id && o.estado !== 'pagado' && o.estado !== 'cancelada'
  )
  if (!ord || !ord.items) return false
  return ord.items.some(i => ['pendiente', 'preparando', 'listo', 'recibido_mesero', 'en_observacion'].includes(i.estado))
}

const puedeSolicitarCuenta = (mesa) => {
  if (!mesa || mesa.estado !== 'ocupada') return false
  const ord = ordenesStore.ordenesActivas.find(
    o => o.mesa_id === mesa.id && o.estado !== 'pagado' && o.estado !== 'cancelada'
  )
  if (!ord || !ord.items) return false
  const itemsValidos = ord.items.filter(i => i.estado !== 'cancelado')
  if (itemsValidos.length === 0) return false
  // Ningún platillo debe estar pendiente, en preparación o por entregar al cliente
  return !itemsValidos.some(i => ['pendiente', 'preparando', 'listo', 'recibido_mesero', 'en_observacion'].includes(i.estado))
}

const puedeLiberarMesa = (mesa) => {
  if (!mesa || mesa.estado === 'libre') return false
  const ordActiva = ordenesStore.ordenesActivas.find(
    o => o.mesa_id === mesa.id && o.estado !== 'pagado' && o.estado !== 'cancelada'
  )
  // Si no hay comanda activa, la mesa no tiene consumos registrados: se puede liberar
  if (!ordActiva) return true

  // Si hay comanda activa, solo se puede liberar si todos sus items fueron cancelados
  const tieneItemsVigentes = ordActiva.items?.some(i => i.estado !== 'cancelado')
  if (tieneItemsVigentes) return false

  return true
}

const solicitarCuentaMesa = async (mesa) => {
  if (!puedeSolicitarCuenta(mesa)) {
    alert(`No se puede solicitar la cuenta de la Mesa "${mesa.numero}" mientras haya platillos pendientes o en preparación en cocina. Deben servirse o cancelarse primero.`)
    return
  }
  try {
    const ord = ordenesStore.ordenesActivas.find(
      o => o.mesa_id === mesa.id && o.estado !== 'pagado' && o.estado !== 'cancelada'
    )
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

const modalAclaracionEspecial = ref(false)
const ordenSeleccionadaAclaracion = ref(null)
const respuestasAclaracionEspecial = ref({})

const tieneObservacionCocina = (ord) => {
  return Boolean(ord.items?.some(i => i.estado === 'en_observacion'))
}

const itemsObservados = (ord) => {
  if (!ord || !ord.items) return []
  return ord.items.filter(i => i.estado === 'en_observacion')
}

const abrirModalAclaracionEspecial = (ord) => {
  ordenSeleccionadaAclaracion.value = ord
  respuestasAclaracionEspecial.value = {}
  modalAclaracionEspecial.value = true
}

const enviarRespuestaAclaracion = async (itemId, accion) => {
  const resp = respuestasAclaracionEspecial.value[itemId] || ''
  if (accion === 'continuar' && !resp.trim()) {
    alert('Por favor ingresa la aclaración o instrucción para la cocina.')
    return
  }
  if (accion === 'cancelar') {
    if (!confirm('¿Deseas cancelar este platillo por la incidencia de cocina? Se cancelará sin merma de insumos.')) {
      return
    }
  }

  try {
    await ordenesStore.resolverObservacionItem(itemId, {
      accion,
      respuesta: resp.trim() || undefined
    })
    const ordId = ordenSeleccionadaAclaracion.value?.id
    await ordenesStore.cargarOrdenesActivas()
    if (ordId) {
      const ordActualizada = ordenesStore.ordenesActivas.find(o => o.id === ordId)
      if (ordActualizada && tieneObservacionCocina(ordActualizada)) {
        ordenSeleccionadaAclaracion.value = ordActualizada
      } else {
        modalAclaracionEspecial.value = false
        ordenSeleccionadaAclaracion.value = null
      }
    }
    alert(accion === 'continuar' ? 'Aclaración enviada exitosamente a la cocina.' : 'Platillo cancelado.')
  } catch (err) {
    console.error('Error resolviendo observación:', err)
    alert(err.response?.data?.detail || 'Error al resolver la observación.')
  }
}

const abrirOrdenEnComandero = (ord) => {
  router.push({
    name: 'pos',
    query: {
      ordenId: ord.id,
      tipoPedido: ord.tipo_pedido,
      mesaNumero: ord.tipo_pedido === 'domicilio' ? `🛵 Envío #${ord.id}` : `🛍️ Llevar #${ord.id}`
    }
  })
}

const cancelarPedidoEspecial = async (ord) => {
  const label = ord.tipo_pedido === 'domicilio' ? 'de envío a domicilio' : 'para llevar'
  if (!confirm(`¿Deseas cancelar el pedido ${label} #${ord.id}? Esta acción cancelará la orden en cocina y caja.`)) return
  const motivo = prompt('Motivo de cancelación:', 'Cliente canceló el pedido')
  if (!motivo?.trim()) return
  try {
    await ordenesStore.cancelarOrden(ord.id, {
      motivo: motivo.trim(),
      genera_merma: false
    })
    alert('Pedido cancelado exitosamente.')
  } catch (err) {
    console.error('Error cancelando pedido especial:', err)
    alert(err.response?.data?.detail || 'Error al cancelar el pedido.')
  }
}

const cancelarPedidoCompletoDesdeAclaracion = async () => {
  if (!ordenSeleccionadaAclaracion.value) return
  const ord = ordenSeleccionadaAclaracion.value
  const label = ord.tipo_pedido === 'domicilio' ? 'de envío' : 'para llevar'
  if (!confirm(`¿Deseas cancelar el pedido ${label} #${ord.id} completo?`)) return
  const motivo = prompt('Motivo de cancelación:', 'Cancelado por falta de insumos / cliente canceló')
  if (!motivo?.trim()) return
  try {
    await ordenesStore.cancelarOrden(ord.id, {
      motivo: motivo.trim(),
      genera_merma: false
    })
    modalAclaracionEspecial.value = false
    ordenSeleccionadaAclaracion.value = null
    alert('Pedido cancelado exitosamente.')
  } catch (err) {
    console.error('Error cancelando pedido:', err)
    alert(err.response?.data?.detail || 'Error al cancelar el pedido.')
  }
}

const iniciarPedidoExterno = () => {
  if (!esRolAlto.value) {
    alert('Los pedidos de mostrador y entrega a domicilio deben ser autorizados y registrados por personal de jefatura o administración.')
    return
  }
  router.push({
    name: 'pos',
    query: {
      tipoPedido: 'para_llevar'
    }
  })
}

const ordenesEspecialesActivas = computed(() => {
  return ordenesStore.ordenesActivas.filter(o => 
    ['domicilio', 'para_llevar'].includes(o.tipo_pedido) &&
    !['pagado', 'cancelada'].includes(o.estado)
  )
})

const badgeColorEstado = (estado) => {
  switch (estado) {
    case 'en_cola': return 'bg-slate-200 text-slate-700 dark:bg-slate-700 dark:text-slate-200'
    case 'preparando': return 'bg-amber-100 text-amber-800 dark:bg-amber-950 dark:text-amber-300'
    case 'listo': return 'bg-emerald-100 text-emerald-800 dark:bg-emerald-950 dark:text-emerald-300'
    case 'entregado': return 'bg-purple-100 text-purple-800 dark:bg-purple-950 dark:text-purple-300'
    default: return 'bg-slate-100 text-slate-600'
  }
}

const getAlertaMesa = (mesaId) => {
  const ord = ordenesStore.ordenesActivas.find(o => o.mesa_id === mesaId && o.estado !== 'pagado' && o.estado !== 'cancelada')
  if (!ord) return null
  const tieneObservacion = ord.items?.some(i => i.estado === 'en_observacion')
  if (tieneObservacion) return { tipo: 'observacion', texto: '⚠️ Cocina' }
  const tieneListo = ord.items?.some(i => ['listo', 'recibido_mesero'].includes(i.estado))
  if (tieneListo) return { tipo: 'listo', texto: '🔔 Listo' }
  return null
}

const abrirComandero = async (mesa) => {
  if (esMesaDeOtroMesero(mesa)) {
    alert(`Esta mesa está asignada a ${mesa.mesero_nombre || 'otro colaborador'}. No tienes permisos para ver sus comandas ni agregar rondas.`)
    return
  }
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

<template>
  <div class="space-y-6 max-w-6xl mx-auto">
    <!-- Header Principal -->
    <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 bg-white dark:bg-slate-900 p-6 rounded-3xl border border-slate-200 dark:border-slate-800 shadow-sm transition-colors">
      <div>
        <div class="flex items-center gap-2.5">
          <h1 class="text-2xl font-black text-slate-800 dark:text-slate-100 tracking-tight">Ajustes del Sistema</h1>
          <span class="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-3xs font-extrabold bg-eden-100 dark:bg-eden-950/80 text-eden-800 dark:text-eden-300 border border-eden-300 dark:border-eden-800">
            Administración General
          </span>
        </div>
        <p class="text-slate-500 dark:text-slate-400 text-xs sm:text-sm mt-0.5">
          Identidad del negocio, guía de hardware (impresoras y cajón) y gestión de personal
        </p>
      </div>

      <!-- Pestañas de Navegación Superior -->
      <div class="flex items-center gap-1.5 p-1 bg-slate-100 dark:bg-slate-800/80 rounded-2xl border border-slate-200/80 dark:border-slate-700/60 overflow-x-auto no-scrollbar">
        <button
          v-for="tab in tabs"
          :key="tab.id"
          @click="tabActiva = tab.id"
          :class="[
            'px-3.5 py-2 rounded-xl text-xs font-black transition-all flex items-center gap-1.5 shrink-0 min-h-[38px]',
            tabActiva === tab.id
              ? 'bg-white dark:bg-slate-900 text-slate-900 dark:text-white shadow-xs border border-slate-200/60 dark:border-slate-700'
              : 'text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-white'
          ]"
        >
          <span>{{ tab.emoji }}</span>
          <span>{{ tab.label }}</span>
        </button>
      </div>
    </div>

    <!-- ======================================================== -->
    <!-- PESTAÑA 1: IDENTIDAD Y RESTAURANTE                        -->
    <!-- ======================================================== -->
    <div v-if="tabActiva === 'identidad'" class="space-y-6 animate-in fade-in">
      <div class="grid grid-cols-1 lg:grid-cols-12 gap-6 items-start">
        
        <!-- Tarjeta de Logo e Identidad Visual (5 cols) -->
        <div class="lg:col-span-5 bg-white dark:bg-slate-900 p-6 rounded-3xl border border-slate-200 dark:border-slate-800 shadow-sm space-y-5 text-center">
          <div class="space-y-1">
            <h3 class="text-base font-black text-slate-800 dark:text-slate-100">Logotipo del Restaurante</h3>
            <p class="text-xs text-slate-400">Se muestra en la barra lateral, menú digital y tickets impresos</p>
          </div>

          <!-- Vista Previa del Logo Actual -->
          <div class="relative w-36 h-36 mx-auto">
            <div class="w-full h-full rounded-full p-2 bg-white dark:bg-slate-800 border-2 border-slate-200 dark:border-slate-700 shadow-md ring-4 ring-eden-500/20 flex items-center justify-center overflow-hidden">
              <img 
                :src="formIdentidad.logoUrl || '/logo.png'" 
                alt="Logo Restaurante" 
                class="w-full h-full object-contain rounded-full"
                @error="formIdentidad.logoUrl = '/logo.png'"
              />
            </div>
            <span class="absolute bottom-1 right-1 w-5 h-5 rounded-full bg-emerald-500 ring-2 ring-white dark:ring-slate-900 animate-pulse shadow-sm"></span>
          </div>

          <!-- Selector de Archivo de Imagen -->
          <div class="space-y-2">
            <label class="block">
              <input 
                type="file" 
                accept="image/*"
                @change="manejarSubidaLogo"
                class="hidden"
                ref="inputLogoRef"
              />
              <button 
                type="button"
                @click="$refs.inputLogoRef.click()"
                class="w-full py-2.5 px-4 bg-eden-600 hover:bg-eden-700 text-white rounded-xl text-xs font-black shadow-sm transition active:scale-95 flex items-center justify-center gap-1.5"
              >
                <span>📁</span>
                <span>Cambiar Imagen del Logo</span>
              </button>
            </label>

            <button 
              type="button"
              @click="restaurarLogoPorDefecto"
              class="w-full py-2 px-3 text-2xs font-bold text-slate-500 hover:text-slate-700 dark:hover:text-slate-300 transition"
            >
              Restaurar logo predeterminado
            </button>
          </div>

          <!-- Vista previa mini del ticket -->
          <div class="p-3.5 bg-slate-50 dark:bg-slate-800/50 rounded-2xl border border-slate-200 dark:border-slate-700 text-left font-mono text-2xs space-y-1">
            <div class="text-center font-bold text-slate-800 dark:text-slate-100 uppercase tracking-wider text-xs">
              {{ formIdentidad.nombreRestaurante || 'Nombre del Restaurante' }}
            </div>
            <div class="text-center text-slate-400 text-3xs">
              {{ formIdentidad.slogan || 'Slogan del restaurante' }}
            </div>
            <div v-if="formIdentidad.direccion" class="text-center text-slate-400 text-3xs">
              {{ formIdentidad.direccion }}
            </div>
            <div v-if="formIdentidad.telefono" class="text-center text-slate-400 text-3xs">
              Tel: {{ formIdentidad.telefono }}
            </div>
          </div>
        </div>

        <!-- Formulario de Datos del Restaurante (7 cols) -->
        <div class="lg:col-span-7 bg-white dark:bg-slate-900 p-6 rounded-3xl border border-slate-200 dark:border-slate-800 shadow-sm space-y-4">
          <div class="border-b border-slate-100 dark:border-slate-800 pb-3">
            <h3 class="text-base font-black text-slate-800 dark:text-slate-100">Información del Establecimiento</h3>
            <p class="text-xs text-slate-400">Datos generales del negocio mostrados a clientes y comensales</p>
          </div>

          <div class="grid grid-cols-1 sm:grid-cols-2 gap-3.5 text-xs">
            <!-- Nombre del Negocio -->
            <div class="sm:col-span-2">
              <label class="block font-bold text-slate-700 dark:text-slate-300 mb-1">
                Nombre Comercial del Restaurante / Cafetería
              </label>
              <input 
                v-model="formIdentidad.nombreRestaurante" 
                type="text"
                placeholder="Ej. Edén Café"
                class="w-full p-2.5 bg-slate-50 dark:bg-slate-800 border border-slate-300 dark:border-slate-700 rounded-xl text-xs font-bold text-slate-800 dark:text-slate-100 focus:outline-none focus:border-eden-500 font-mono"
              />
            </div>

            <!-- Slogan o Subtítulo -->
            <div class="sm:col-span-2">
              <label class="block font-bold text-slate-700 dark:text-slate-300 mb-1">
                Slogan o Descripción Corta
              </label>
              <input 
                v-model="formIdentidad.slogan" 
                type="text"
                placeholder="Ej. Comida Tradicional y Café de Especialidad"
                class="w-full p-2.5 bg-slate-50 dark:bg-slate-800 border border-slate-300 dark:border-slate-700 rounded-xl text-xs text-slate-800 dark:text-slate-100 focus:outline-none focus:border-eden-500"
              />
            </div>

            <!-- Teléfono -->
            <div>
              <label class="block font-bold text-slate-700 dark:text-slate-300 mb-1">
                Teléfono de Contacto / WhatsApp
              </label>
              <input 
                v-model="formIdentidad.telefono" 
                type="text"
                placeholder="Ej. 961 123 4567"
                class="w-full p-2.5 bg-slate-50 dark:bg-slate-800 border border-slate-300 dark:border-slate-700 rounded-xl text-xs text-slate-800 dark:text-slate-100 focus:outline-none focus:border-eden-500"
              />
            </div>

            <!-- RFC / Facturación -->
            <div>
              <label class="block font-bold text-slate-700 dark:text-slate-300 mb-1">
                RFC o Identificador Fiscal
              </label>
              <input 
                v-model="formIdentidad.rfc" 
                type="text"
                placeholder="Ej. ECA240101XYZ"
                class="w-full p-2.5 bg-slate-50 dark:bg-slate-800 border border-slate-300 dark:border-slate-700 rounded-xl text-xs text-slate-800 dark:text-slate-100 focus:outline-none focus:border-eden-500 uppercase font-mono"
              />
            </div>

            <!-- Dirección -->
            <div class="sm:col-span-2">
              <label class="block font-bold text-slate-700 dark:text-slate-300 mb-1">
                Dirección Física
              </label>
              <input 
                v-model="formIdentidad.direccion" 
                type="text"
                placeholder="Ej. Av. Central Poniente #123, Tuxtla Gutiérrez, Chiapas"
                class="w-full p-2.5 bg-slate-50 dark:bg-slate-800 border border-slate-300 dark:border-slate-700 rounded-xl text-xs text-slate-800 dark:text-slate-100 focus:outline-none focus:border-eden-500"
              />
            </div>

            <!-- Días de Servicio -->
            <div>
              <label class="block font-bold text-slate-700 dark:text-slate-300 mb-1">
                Días de Servicio
              </label>
              <input 
                v-model="formIdentidad.diasServicio" 
                type="text"
                placeholder="Ej. Lunes a Domingo"
                class="w-full p-2.5 bg-slate-50 dark:bg-slate-800 border border-slate-300 dark:border-slate-700 rounded-xl text-xs text-slate-800 dark:text-slate-100 focus:outline-none focus:border-eden-500"
              />
            </div>

            <!-- Horario Apertura / Cierre -->
            <div class="flex items-center gap-2">
              <div class="flex-1">
                <label class="block font-bold text-slate-700 dark:text-slate-300 mb-1">
                  Apertura
                </label>
                <input 
                  v-model="formIdentidad.horarioApertura" 
                  type="time"
                  class="w-full p-2 bg-slate-50 dark:bg-slate-800 border border-slate-300 dark:border-slate-700 rounded-xl text-xs text-slate-800 dark:text-slate-100 focus:outline-none focus:border-eden-500"
                />
              </div>
              <div class="flex-1">
                <label class="block font-bold text-slate-700 dark:text-slate-300 mb-1">
                  Cierre
                </label>
                <input 
                  v-model="formIdentidad.horarioCierre" 
                  type="time"
                  class="w-full p-2 bg-slate-50 dark:bg-slate-800 border border-slate-300 dark:border-slate-700 rounded-xl text-xs text-slate-800 dark:text-slate-100 focus:outline-none focus:border-eden-500"
                />
              </div>
            </div>

            <!-- Pie de Ticket Predeterminado -->
            <div class="sm:col-span-2">
              <label class="block font-bold text-slate-700 dark:text-slate-300 mb-1">
                Mensaje por Defecto al Pie del Ticket
              </label>
              <textarea 
                v-model="formIdentidad.mensajeTicket" 
                rows="2"
                placeholder="Ej. ¡Gracias por su visita y preferencia! Vuelva pronto."
                class="w-full p-2.5 bg-slate-50 dark:bg-slate-800 border border-slate-300 dark:border-slate-700 rounded-xl text-xs text-slate-800 dark:text-slate-100 focus:outline-none focus:border-eden-500"
              ></textarea>
            </div>
          </div>

          <!-- Botón Guardar -->
          <div class="pt-4 border-t border-slate-100 dark:border-slate-800 flex justify-end">
            <button 
              type="button"
              @click="guardarIdentidad"
              class="px-6 py-3 bg-eden-600 hover:bg-eden-700 text-white rounded-xl text-xs font-black shadow-md transition active:scale-95 flex items-center gap-2"
            >
              <span>💾</span>
              <span>Guardar Cambios de Identidad</span>
            </button>
          </div>
        </div>

      </div>

      <!-- ======================================================== -->
      <!-- SECCIÓN: PERSONALIZACIÓN DE LA CARTA DIGITAL (MENÚ WEB)  -->
      <!-- ======================================================== -->
      <div class="bg-white dark:bg-slate-900 p-6 sm:p-7 rounded-3xl border border-slate-200 dark:border-slate-800 shadow-sm space-y-6">
        <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-3 border-b border-slate-100 dark:border-slate-800 pb-4">
          <div class="flex items-center gap-3">
            <div class="w-10 h-10 rounded-2xl bg-eden-100 dark:bg-eden-950/80 text-eden-700 dark:text-eden-300 flex items-center justify-center text-xl shrink-0">
              📖
            </div>
            <div>
              <h3 class="text-base font-black text-slate-800 dark:text-slate-100">
                Textos de la Carta Digital (Menú Web para Clientes)
              </h3>
              <p class="text-xs text-slate-400">
                Personaliza los títulos, descripciones y leyendas de pie de página visibles para los comensales
              </p>
            </div>
          </div>
          <a 
            href="/carta" 
            target="_blank"
            class="px-3.5 py-2 rounded-xl bg-slate-100 dark:bg-slate-800 hover:bg-slate-200 dark:hover:bg-slate-700 text-xs font-bold text-slate-700 dark:text-slate-300 transition flex items-center gap-1.5 self-start sm:self-center shrink-0 border border-slate-200 dark:border-slate-700"
          >
            <span>🔗</span> Ver Carta en Vivo
          </a>
        </div>

        <div class="grid grid-cols-1 lg:grid-cols-12 gap-6 items-start">
          <!-- Formulario de Configuración de Textos (7 cols) -->
          <div class="lg:col-span-7 space-y-4">
            <!-- Título Principal de la Carta -->
            <div>
              <label class="block font-bold text-slate-700 dark:text-slate-300 text-xs mb-1">
                Título Superior de la Carta
              </label>
              <input 
                v-model="formIdentidad.tituloCarta" 
                type="text"
                placeholder="Ej. Nuestra Carta, Menú Digital, Especialidades del Día"
                class="w-full p-2.5 bg-slate-50 dark:bg-slate-800 border border-slate-300 dark:border-slate-700 rounded-xl text-xs font-bold text-slate-800 dark:text-slate-100 focus:outline-none focus:border-eden-500"
              />
              <div class="flex flex-wrap gap-1.5 pt-1.5">
                <button
                  v-for="sug in ['Nuestra Carta', 'Menú Digital', 'Carta & Especialidades', 'Nuestras Delicias']"
                  :key="sug"
                  type="button"
                  @click="formIdentidad.tituloCarta = sug"
                  class="px-2 py-0.5 text-3xs font-semibold rounded-lg bg-slate-100 dark:bg-slate-800 hover:bg-slate-200 dark:hover:bg-slate-700 text-slate-600 dark:text-slate-300 border border-slate-200 dark:border-slate-700 transition"
                >
                  {{ sug }}
                </button>
              </div>
            </div>

            <!-- Descripción / Subtítulo Superior -->
            <div>
              <label class="block font-bold text-slate-700 dark:text-slate-300 text-xs mb-1">
                Descripción / Subtítulo Superior
              </label>
              <textarea 
                v-model="formIdentidad.subtituloCarta" 
                rows="3"
                placeholder="Ej. Platillos preparados al momento con ingredientes frescos, recetas mexicanas tradicionales y café tostado artesanal."
                class="w-full p-2.5 bg-slate-50 dark:bg-slate-800 border border-slate-300 dark:border-slate-700 rounded-xl text-xs text-slate-800 dark:text-slate-100 focus:outline-none focus:border-eden-500"
              ></textarea>
              <div class="flex flex-wrap gap-1.5 pt-1.5">
                <button
                  type="button"
                  @click="formIdentidad.subtituloCarta = 'Platillos preparados al momento con ingredientes frescos, recetas mexicanas tradicionales y café tostado artesanal.'"
                  class="px-2 py-0.5 text-3xs font-semibold rounded-lg bg-slate-100 dark:bg-slate-800 hover:bg-slate-200 dark:hover:bg-slate-700 text-slate-600 dark:text-slate-300 border border-slate-200 dark:border-slate-700 transition"
                >
                  Estándar tradicional
                </button>
                <button
                  type="button"
                  @click="formIdentidad.subtituloCarta = 'Café de altura, desayunos completos, comidas tradicionales y repostería casera.'"
                  class="px-2 py-0.5 text-3xs font-semibold rounded-lg bg-slate-100 dark:bg-slate-800 hover:bg-slate-200 dark:hover:bg-slate-700 text-slate-600 dark:text-slate-300 border border-slate-200 dark:border-slate-700 transition"
                >
                  Café y Repostería
                </button>
                <button
                  type="button"
                  @click="formIdentidad.subtituloCarta = 'Sabores auténticos hechos con pasión para deleitar tu paladar.'"
                  class="px-2 py-0.5 text-3xs font-semibold rounded-lg bg-slate-100 dark:bg-slate-800 hover:bg-slate-200 dark:hover:bg-slate-700 text-slate-600 dark:text-slate-300 border border-slate-200 dark:border-slate-700 transition"
                >
                  Sabores y Pasión
                </button>
              </div>
            </div>

            <!-- Leyenda al Pie de la Carta -->
            <div>
              <div class="flex items-center justify-between mb-1">
                <label class="block font-bold text-slate-700 dark:text-slate-300 text-xs">
                  Leyenda de Impuestos y Precios en el Pie de la Carta
                </label>
                <span class="text-3xs text-slate-400">Footer de la Carta</span>
              </div>
              <textarea 
                v-model="formIdentidad.notaPieCarta" 
                rows="2"
                placeholder="Ej. Precios incluyen IVA. Para dudas sobre ingredientes o alérgenos, consulta a tu mesero."
                class="w-full p-2.5 bg-slate-50 dark:bg-slate-800 border border-slate-300 dark:border-slate-700 rounded-xl text-xs text-slate-800 dark:text-slate-100 focus:outline-none focus:border-eden-500"
              ></textarea>
              <div class="flex flex-wrap gap-1.5 pt-1.5">
                <button
                  type="button"
                  @click="formIdentidad.notaPieCarta = 'Precios incluyen IVA. Para dudas sobre ingredientes o alérgenos, consulta a tu mesero.'"
                  class="px-2 py-0.5 text-3xs font-semibold rounded-lg bg-slate-100 dark:bg-slate-800 hover:bg-slate-200 dark:hover:bg-slate-700 text-slate-600 dark:text-slate-300 border border-slate-200 dark:border-slate-700 transition"
                >
                  IVA + Alérgenos
                </button>
                <button
                  type="button"
                  @click="formIdentidad.notaPieCarta = 'Todos los precios incluyen IVA (16%). Aceptamos efectivo y tarjetas.'"
                  class="px-2 py-0.5 text-3xs font-semibold rounded-lg bg-slate-100 dark:bg-slate-800 hover:bg-slate-200 dark:hover:bg-slate-700 text-slate-600 dark:text-slate-300 border border-slate-200 dark:border-slate-700 transition"
                >
                  IVA + Métodos de pago
                </button>
                <button
                  type="button"
                  @click="formIdentidad.notaPieCarta = 'Precios en MXN con impuestos incluidos. La propina no es obligatoria.'"
                  class="px-2 py-0.5 text-3xs font-semibold rounded-lg bg-slate-100 dark:bg-slate-800 hover:bg-slate-200 dark:hover:bg-slate-700 text-slate-600 dark:text-slate-300 border border-slate-200 dark:border-slate-700 transition"
                >
                  Propina no obligatoria
                </button>
                <button
                  type="button"
                  @click="formIdentidad.notaPieCarta = 'Precios más IVA en caso de requerir comprobante fiscal o factura.'"
                  class="px-2 py-0.5 text-3xs font-semibold rounded-lg bg-slate-100 dark:bg-slate-800 hover:bg-slate-200 dark:hover:bg-slate-700 text-slate-600 dark:text-slate-300 border border-slate-200 dark:border-slate-700 transition"
                >
                  Más IVA para factura
                </button>
              </div>
            </div>
          </div>

          <!-- Vista Previa Interactiva de la Carta (5 cols) -->
          <div class="lg:col-span-5 p-5 rounded-2xl bg-slate-50 dark:bg-slate-800/50 border border-slate-200 dark:border-slate-700 space-y-4">
            <div class="flex items-center justify-between border-b border-slate-200/80 dark:border-slate-700/80 pb-2">
              <span class="text-3xs font-black uppercase text-slate-400 tracking-wider">
                Vista Previa de la Carta
              </span>
              <span class="text-3xs px-2 py-0.5 rounded-full bg-emerald-100 dark:bg-emerald-950/80 text-emerald-700 dark:text-emerald-300 font-bold">
                En vivo
              </span>
            </div>

            <!-- Mini Encabezado de la Carta -->
            <div class="bg-white dark:bg-slate-900 p-4 rounded-xl border border-slate-200 dark:border-slate-800 text-center space-y-2 shadow-2xs">
              <span class="text-3xs font-bold text-slate-400 uppercase tracking-widest block">Parte Superior (Hero)</span>
              <div v-if="formIdentidad.slogan" class="inline-block px-2.5 py-0.5 rounded-full bg-eden-100 dark:bg-eden-950/60 text-eden-800 dark:text-eden-300 text-3xs font-black uppercase">
                {{ formIdentidad.slogan }}
              </div>
              <h4 class="text-base font-black text-slate-800 dark:text-slate-100 tracking-tight">
                {{ formIdentidad.tituloCarta || 'Nuestra Carta' }}
              </h4>
              <p class="text-3xs text-slate-500 dark:text-slate-400 leading-snug">
                {{ formIdentidad.subtituloCarta || 'Platillos preparados al momento...' }}
              </p>
            </div>

            <!-- Mini Pie de Página de la Carta -->
            <div class="bg-white dark:bg-slate-900 p-4 rounded-xl border border-slate-200 dark:border-slate-800 text-center space-y-2.5 shadow-2xs">
              <span class="text-3xs font-bold text-slate-400 uppercase tracking-widest block">Pie de Página (Footer)</span>
              <div class="flex items-center justify-center gap-2">
                <img :src="formIdentidad.logoUrl || '/logo.png'" class="w-6 h-6 rounded-full object-contain" />
                <span class="font-black text-slate-800 dark:text-slate-100 text-xs">{{ formIdentidad.nombreRestaurante || 'Edén Café' }}</span>
              </div>
              <div class="text-3xs text-slate-500 dark:text-slate-400 space-y-0.5">
                <div>🕒 {{ formIdentidad.diasServicio }}: {{ formIdentidad.horarioApertura }} - {{ formIdentidad.horarioCierre }}</div>
                <div v-if="formIdentidad.direccion">📍 {{ formIdentidad.direccion }}</div>
                <div v-if="formIdentidad.telefono">📞 {{ formIdentidad.telefono }}</div>
              </div>
              <div class="pt-1.5 border-t border-slate-100 dark:border-slate-800 text-3xs text-slate-400">
                {{ formIdentidad.notaPieCarta || 'Precios incluyen IVA.' }}
              </div>
            </div>
          </div>
        </div>

        <!-- Botón Guardar Cambios de la Carta -->
        <div class="pt-3 border-t border-slate-100 dark:border-slate-800 flex justify-end">
          <button 
            type="button"
            @click="guardarIdentidad"
            class="px-6 py-3 bg-eden-600 hover:bg-eden-700 text-white rounded-xl text-xs font-black shadow-md transition active:scale-95 flex items-center gap-2"
          >
            <span>💾</span>
            <span>Guardar Configuración de la Carta</span>
          </button>
        </div>
      </div>
    </div>

    <!-- ======================================================== -->
    <!-- PESTAÑA 2: GUÍA DE HARDWARE Y DISPOSITIVOS                -->
    <!-- ======================================================== -->
    <div v-if="tabActiva === 'hardware'" class="space-y-6 animate-in fade-in">
      
      <!-- Banner de Resumen Rápido -->
      <div class="bg-gradient-to-r from-slate-900 to-slate-800 text-white p-6 rounded-3xl shadow-md border border-slate-700 space-y-3">
        <div class="flex items-center gap-3">
          <div class="w-12 h-12 rounded-2xl bg-eden-600 flex items-center justify-center text-2xl shadow-sm shrink-0">
            🔌
          </div>
          <div>
            <h2 class="text-lg font-black tracking-tight">Conexión de Impresora Térmica y Cajón de Dinero</h2>
            <p class="text-xs text-slate-300">
              Guía técnica y física para enlazar correctamente los periféricos de Punto de Venta en Edén Café
            </p>
          </div>
        </div>
      </div>

      <!-- Diagrama Visual de Conexión Física -->
      <div class="bg-white dark:bg-slate-900 p-6 rounded-3xl border border-slate-200 dark:border-slate-800 shadow-sm space-y-4">
        <h3 class="font-black text-slate-800 dark:text-slate-100 text-base flex items-center gap-2">
          <span>📐</span> Diagrama de Flujo de Conexión
        </h3>

        <div class="grid grid-cols-1 md:grid-cols-3 gap-4 text-center">
          <!-- Paso 1 -->
          <div class="p-4 rounded-2xl bg-slate-50 dark:bg-slate-800/60 border border-slate-200 dark:border-slate-700 space-y-2">
            <div class="w-10 h-10 rounded-xl bg-amber-100 dark:bg-amber-950/80 text-amber-700 dark:text-amber-400 flex items-center justify-center mx-auto text-xl font-bold">
              1
            </div>
            <h4 class="font-extrabold text-xs text-slate-800 dark:text-slate-200">🪙 Cajón de Cobro</h4>
            <p class="text-3xs text-slate-500">
              Tiene un cable con conector telefónico <strong>RJ11 / RJ12</strong>. Se conecta <em>directamente a la impresora</em> en el puerto <strong>DK</strong>.
            </p>
          </div>

          <!-- Paso 2 -->
          <div class="p-4 rounded-2xl bg-slate-50 dark:bg-slate-800/60 border border-slate-200 dark:border-slate-700 space-y-2">
            <div class="w-10 h-10 rounded-xl bg-eden-100 dark:bg-eden-950/80 text-eden-700 dark:text-eden-400 flex items-center justify-center mx-auto text-xl font-bold">
              2
            </div>
            <h4 class="font-extrabold text-xs text-slate-800 dark:text-slate-200">🖨️ Impresora Térmica</h4>
            <p class="text-3xs text-slate-500">
              Se conecta a la PC mediante cable <strong>USB</strong> (o vía red local Ethernet/Wi-Fi). Recibe la orden de impresión y corta el papel.
            </p>
          </div>

          <!-- Paso 3 -->
          <div class="p-4 rounded-2xl bg-slate-50 dark:bg-slate-800/60 border border-slate-200 dark:border-slate-700 space-y-2">
            <div class="w-10 h-10 rounded-xl bg-emerald-100 dark:bg-emerald-950/80 text-emerald-700 dark:text-emerald-400 flex items-center justify-center mx-auto text-xl font-bold">
              3
            </div>
            <h4 class="font-extrabold text-xs text-slate-800 dark:text-slate-200">⚡ Apertura Automática</h4>
            <p class="text-3xs text-slate-500">
              Al imprimir el ticket, la impresora envía un pulso eléctrico de 24V al cable RJ11, <strong>botando el cerrojo del cajón al instante</strong>.
            </p>
          </div>
        </div>
      </div>

      <!-- Pasos detallados para configurar -->
      <div class="grid grid-cols-1 md:grid-cols-2 gap-6 items-start">
        
        <!-- Tarjeta Paso a Paso -->
        <div class="bg-white dark:bg-slate-900 p-6 rounded-3xl border border-slate-200 dark:border-slate-800 shadow-sm space-y-4">
          <h3 class="font-black text-slate-800 dark:text-slate-100 text-sm flex items-center gap-2">
            <span>⚙️</span> Configuración del Controlador (Driver)
          </h3>

          <ol class="space-y-3 text-xs text-slate-600 dark:text-slate-300 list-decimal list-inside">
            <li class="pl-1">
              <strong>Instalar el Driver:</strong> Descarga e instala el controlador de tu impresora térmica (Epson, Xprinter, EC Line, 3nStar, etc.).
            </li>
            <li class="pl-1">
              <strong>Acceder a Propiedades:</strong> En Windows, abre <em>Panel de Control -> Dispositivos e Impresoras -> Clic derecho en tu impresora -> Propiedades de la Impresora</em>.
            </li>
            <li class="pl-1">
              <strong>Habilitar Cajón:</strong> En la pestaña <em>Configuración de Dispositivo</em> o <em>Parámetros de impresión</em>, busca la opción <strong>Cash Drawer / Cajón de Dinero</strong>.
            </li>
            <li class="pl-1">
              <strong>Elegir Momento de Apertura:</strong> Selecciona <strong>`Open before printing`</strong> (Abrir antes de imprimir) o <strong>`Open after printing`</strong> (Abrir después).
            </li>
            <li class="pl-1">
              <strong>Guardar:</strong> Da clic en Aceptar. A partir de ese momento, cada impresión botará el cajón automáticamente sin tocar la llave.
            </li>
          </ol>
        </div>

        <!-- Tarjeta Modo Kiosko e Impresión Silenciosa -->
        <div class="bg-white dark:bg-slate-900 p-6 rounded-3xl border border-slate-200 dark:border-slate-800 shadow-sm space-y-4">
          <div class="flex items-center justify-between">
            <h3 class="font-black text-slate-800 dark:text-slate-100 text-sm flex items-center gap-2">
              <span>🚀</span> Impresión Instantánea (Modo Kiosko)
            </h3>
            <span class="text-3xs font-extrabold uppercase bg-amber-100 text-amber-800 dark:bg-amber-950 dark:text-amber-300 px-2 py-0.5 rounded">
              Recomendado en Caja
            </span>
          </div>

          <p class="text-xs text-slate-500 dark:text-slate-400">
            Por defecto, el navegador web abre una ventana de vista previa antes de imprimir. Si deseas que imprima en <strong>menos de 1 segundo sin mostrar ventanas emergentes</strong>, activa el Modo Kiosko en Chrome:
          </p>

          <div class="p-3 bg-slate-900 text-slate-100 rounded-2xl text-xs font-mono space-y-1.5 shadow-inner">
            <span class="text-3xs text-slate-400 block font-sans">Comando a agregar en el acceso directo:</span>
            <div class="text-eden-400 font-bold select-all">
              chrome.exe --kiosk-printing
            </div>
          </div>

          <ul class="text-xs text-slate-500 space-y-1 list-disc list-inside">
            <li>Haz clic derecho en el acceso directo de Chrome -> <em>Propiedades</em>.</li>
            <li>En el campo <em>Destino (Target)</em>, añade al final: <code class="bg-slate-100 dark:bg-slate-800 px-1 py-0.5 rounded text-2xs">--kiosk-printing</code></li>
            <li>Abre el sistema desde ese acceso directo y los tickets saldrán al instante con 1 solo clic.</li>
          </ul>
        </div>

      </div>

      <!-- Probador de Hardware en Vivo -->
      <div class="bg-gradient-to-r from-emerald-50 via-teal-50 to-eden-50 dark:from-emerald-950/40 dark:via-teal-950/40 dark:to-eden-950/40 p-6 rounded-3xl border border-emerald-300 dark:border-emerald-800 shadow-sm space-y-4">
        <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-3">
          <div>
            <h3 class="font-black text-slate-800 dark:text-slate-100 text-base flex items-center gap-2">
              <span>🧪</span> Herramienta de Prueba de Hardware
            </h3>
            <p class="text-xs text-slate-500 dark:text-slate-400 mt-0.5">
              Envía un ticket de prueba para verificar que la impresora imprime nítidamente y que el cajón se abra
            </p>
          </div>

          <!-- Selector de Ancho de Papel -->
          <div class="flex items-center gap-2">
            <span class="text-xs font-bold text-slate-700 dark:text-slate-300">Ancho de papel:</span>
            <div class="flex gap-1 p-1 bg-white dark:bg-slate-900 rounded-xl border border-slate-200 dark:border-slate-700">
              <button 
                type="button"
                @click="anchoPapel = '80mm'"
                :class="[
                  'px-3 py-1 rounded-lg text-xs font-black transition',
                  anchoPapel === '80mm' ? 'bg-eden-600 text-white' : 'text-slate-500'
                ]"
              >
                80 mm (Estándar)
              </button>
              <button 
                type="button"
                @click="anchoPapel = '58mm'"
                :class="[
                  'px-3 py-1 rounded-lg text-xs font-black transition',
                  anchoPapel === '58mm' ? 'bg-eden-600 text-white' : 'text-slate-500'
                ]"
              >
                58 mm (Chica)
              </button>
            </div>
          </div>
        </div>

        <div class="pt-2 flex justify-end">
          <button 
            type="button"
            @click="imprimirTicketPrueba"
            class="px-6 py-3.5 bg-slate-900 hover:bg-slate-800 text-white rounded-2xl text-xs font-black shadow-md transition active:scale-95 flex items-center gap-2"
          >
            <span>🖨️</span>
            <span>Imprimir Ticket de Prueba y Burlar Cajón</span>
          </button>
        </div>
      </div>

    </div>

    <!-- ======================================================== -->
    <!-- PESTAÑA 3: PERSONAL Y COLABORADORES                       -->
    <!-- ======================================================== -->
    <div v-if="tabActiva === 'personal'" class="space-y-4 animate-in fade-in">
      <!-- Embebe la vista completa de Usuarios / RH -->
      <UsuariosView />
    </div>

  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import { useRoute } from 'vue-router'
import { useConfiguracionStore } from '../stores/configuracion'
import { generarTicketPruebaHardware, imprimirContenidoHtml } from '../utils/ticketPrinter'
import UsuariosView from './UsuariosView.vue'

const route = useRoute()
const configStore = useConfiguracionStore()

const tabActiva = ref('identidad')
const anchoPapel = ref('80mm')
const inputLogoRef = ref(null)

const tabs = [
  { id: 'identidad', label: 'Identidad & Negocio', emoji: '🏢' },
  { id: 'hardware', label: 'Hardware & Dispositivos', emoji: '🖨️' },
  { id: 'personal', label: 'Personal & Usuarios', emoji: '👥' }
]

// Formulario reactivo para identidad
const formIdentidad = ref({
  nombreRestaurante: '',
  slogan: '',
  logoUrl: '',
  telefono: '',
  direccion: '',
  rfc: '',
  diasServicio: '',
  horarioApertura: '',
  horarioCierre: '',
  mensajeTicket: '',
  tituloCarta: '',
  subtituloCarta: '',
  notaPieCarta: ''
})

onMounted(async () => {
  if (route.query.tab && ['identidad', 'hardware', 'personal'].includes(route.query.tab)) {
    tabActiva.value = route.query.tab
  }

  // Cargar datos actuales del backend / store
  await configStore.cargarConfiguracion()
  formIdentidad.value = {
    nombreRestaurante: configStore.nombreRestaurante,
    slogan: configStore.slogan,
    logoUrl: configStore.logoUrl,
    telefono: configStore.telefono,
    direccion: configStore.direccion,
    rfc: configStore.rfc,
    diasServicio: configStore.diasServicio,
    horarioApertura: configStore.horarioApertura,
    horarioCierre: configStore.horarioCierre,
    mensajeTicket: configStore.mensajeTicket,
    tituloCarta: configStore.tituloCarta,
    subtituloCarta: configStore.subtituloCarta,
    notaPieCarta: configStore.notaPieCarta
  }
  anchoPapel.value = configStore.anchoPapelTicket || '80mm'
})

watch(() => route.query.tab, (nuevoTab) => {
  if (nuevoTab && ['identidad', 'hardware', 'personal'].includes(nuevoTab)) {
    tabActiva.value = nuevoTab
  }
})

const manejarSubidaLogo = async (e) => {
  const archivo = e.target.files?.[0]
  if (!archivo) return
  try {
    const urlBase64 = await configStore.subirLogo(archivo)
    formIdentidad.value.logoUrl = urlBase64
    alert('¡Logo actualizado con éxito!')
  } catch (err) {
    alert(err.message || 'Error al procesar la imagen del logo.')
  }
}

const restaurarLogoPorDefecto = () => {
  formIdentidad.value.logoUrl = '/logo.png'
  configStore.guardarConfiguracion({ logoUrl: '/logo.png' })
  alert('Se ha restaurado el logo oficial predeterminado.')
}

const guardarIdentidad = async () => {
  await configStore.guardarConfiguracion({
    ...formIdentidad.value,
    anchoPapelTicket: anchoPapel.value
  })
  // Guardar también mensaje en la clave de tickets
  if (formIdentidad.value.mensajeTicket) {
    localStorage.setItem('eden_ticket_msg', formIdentidad.value.mensajeTicket)
  }
  alert('¡Configuración de identidad guardada correctamente y sincronizada en todo el sistema!')
}

const imprimirTicketPrueba = () => {
  configStore.guardarConfiguracion({ anchoPapelTicket: anchoPapel.value })
  const html = generarTicketPruebaHardware(anchoPapel.value)
  imprimirContenidoHtml(html)
}
</script>

<style scoped>
/* Ocultar barra de scroll en chips horizontales */
.no-scrollbar::-webkit-scrollbar {
  display: none;
}
.no-scrollbar {
  -ms-overflow-style: none;
  scrollbar-width: none;
}
</style>

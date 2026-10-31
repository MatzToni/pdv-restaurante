<template>
  <div class="space-y-6 max-w-6xl mx-auto">
    <!-- Header -->
    <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 bg-white dark:bg-slate-900 p-6 rounded-2xl shadow-sm border border-slate-200 dark:border-slate-800 transition-colors">
      <div>
        <h1 class="text-2xl font-black text-slate-800 dark:text-slate-100 tracking-tight">Expedientes y Personal (RH)</h1>
        <p class="text-slate-500 dark:text-slate-400 text-sm">Control de colaboradores, roles, turnos, acceso a terminales y documentación</p>
      </div>

      <button 
        @click="abrirModalNuevoUsuario"
        class="px-4 py-2 bg-eden-600 hover:bg-eden-700 text-white rounded-xl text-xs font-bold shadow-sm transition active:scale-95 flex items-center gap-1.5"
      >
        <span>+</span> Registrar Colaborador
      </button>
    </div>

    <!-- Filtros de Turno y Resumen -->
    <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-3">
      <div class="flex gap-1.5 overflow-x-auto no-scrollbar pb-1">
        <button
          v-for="t in ['todos', 'matutino', 'vespertino', 'nocturno', 'completo']"
          :key="t"
          @click="filtroTurno = t"
          :class="[
            'px-3.5 py-1.5 rounded-xl text-xs font-bold capitalize transition-all shrink-0',
            filtroTurno === t
              ? 'bg-eden-600 text-white shadow-sm'
              : 'bg-white dark:bg-slate-900 text-slate-600 dark:text-slate-300 hover:bg-slate-100 dark:hover:bg-slate-800 border border-slate-200 dark:border-slate-800'
          ]"
        >
          {{ t === 'todos' ? 'Todos los Turnos' : `Turno ${t}` }}
        </button>
      </div>

      <span class="text-xs text-slate-400 dark:text-slate-500 font-semibold">
        {{ usuariosFiltrados.length }} colaboradores registrados
      </span>
    </div>

    <!-- Lista de Colaboradores -->
    <div class="bg-white dark:bg-slate-900 rounded-2xl border border-slate-200 dark:border-slate-800 shadow-sm overflow-hidden transition-colors">
      <div class="divide-y divide-slate-100 dark:divide-slate-800">
        <div v-if="authStore.usuarios.length === 0" class="p-12 text-center text-slate-400">
          No hay colaboradores registrados.
        </div>
        <div 
          v-for="u in usuariosFiltrados" 
          :key="u.id"
          class="p-4 sm:p-5 flex flex-col md:flex-row justify-between items-start md:items-center gap-4 hover:bg-slate-50/70 dark:hover:bg-slate-800/40 transition"
        >
          <div class="flex items-center gap-3.5">
            <div class="w-11 h-11 rounded-2xl bg-slate-100 dark:bg-slate-800 border border-slate-200 dark:border-slate-700 flex items-center justify-center font-black text-slate-700 dark:text-slate-200 text-base shadow-2xs">
              {{ u.nombre.charAt(0) }}
            </div>
            <div>
              <div class="flex items-center gap-2">
                <h4 class="font-extrabold text-sm text-slate-800 dark:text-slate-100">{{ u.nombre }}</h4>
                <span 
                  v-if="u.acceso_sistema" 
                  title="Tiene acceso al sistema con login/PIN"
                  class="text-xs bg-emerald-100 dark:bg-emerald-950/60 text-emerald-800 dark:text-emerald-300 px-1.5 py-0.5 rounded font-bold"
                >
                  🔑 Acceso PDV
                </span>
                <span 
                  v-else 
                  title="Personal operativo sin acceso a terminal"
                  class="text-xs bg-slate-100 dark:bg-slate-800 text-slate-500 px-1.5 py-0.5 rounded font-medium"
                >
                  Sin acceso PDV
                </span>
              </div>
              <div class="text-xs text-slate-400 flex items-center gap-2 mt-0.5">
                <span>{{ u.email }}</span>
                <span v-if="u.telefono">• 📞 {{ u.telefono }}</span>
              </div>
            </div>
          </div>

          <div class="flex flex-wrap items-center gap-2.5 self-end md:self-center">
            <!-- Badges -->
            <span :class="[
              'px-2.5 py-1 rounded-full text-2xs font-extrabold uppercase',
              u.rol === 'administrador' ? 'bg-red-100 dark:bg-red-950/60 text-red-800 dark:text-red-300' :
              u.rol === 'gerente' ? 'bg-amber-100 dark:bg-amber-950/60 text-amber-800 dark:text-amber-300' :
              u.rol === 'jefe' ? 'bg-indigo-100 dark:bg-indigo-950/60 text-indigo-800 dark:text-indigo-300' :
              u.rol === 'cocina' ? 'bg-orange-100 dark:bg-orange-950/60 text-orange-800 dark:text-orange-300' :
              u.rol === 'mesero' ? 'bg-emerald-100 dark:bg-emerald-950/60 text-emerald-800 dark:text-emerald-300' :
              'bg-slate-100 dark:bg-slate-800 text-slate-700 dark:text-slate-300'
            ]">
              {{ u.rol }}
            </span>

            <span class="px-2.5 py-1 rounded-full text-2xs font-bold bg-slate-100 dark:bg-slate-800 text-slate-600 dark:text-slate-300 capitalize border border-slate-200 dark:border-slate-700">
              Turno: {{ u.turno }}
            </span>

            <span v-if="u.pin_seguridad" class="text-2xs font-mono text-slate-400 bg-slate-100 dark:bg-slate-800 px-2 py-1 rounded border border-slate-200 dark:border-slate-700">
              PIN: ••••
            </span>

            <!-- Botones de Acción: Editar y Expediente -->
            <button 
              @click="abrirModalEditar(u)"
              title="Editar datos de este colaborador"
              class="px-2.5 py-1.5 bg-slate-100 dark:bg-slate-800 hover:bg-slate-200 dark:hover:bg-slate-700 text-slate-700 dark:text-slate-200 rounded-xl text-xs font-bold transition active:scale-95 flex items-center gap-1 border border-slate-200 dark:border-slate-700"
            >
              ✏️ Editar
            </button>

            <button 
              @click="verDetalleColaborador(u.id)"
              class="px-3 py-1.5 bg-slate-900 dark:bg-slate-800 hover:bg-slate-800 dark:hover:bg-slate-700 text-white rounded-xl text-xs font-bold transition active:scale-95 flex items-center gap-1"
            >
              📋 Ver Expediente
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Modal / Drawer: Detalle y Expediente del Colaborador -->
    <div v-if="modalDetalle && usuarioDetalle" class="fixed inset-0 bg-slate-900/60 backdrop-blur-sm flex items-center justify-center p-4 z-50 overflow-y-auto">
      <div class="bg-white dark:bg-slate-900 rounded-3xl max-w-2xl w-full shadow-2xl border border-slate-200 dark:border-slate-800 overflow-hidden my-8">
        <!-- Cabecera del Expediente -->
        <div class="p-6 bg-slate-900 text-white flex justify-between items-start">
          <div>
            <span class="text-2xs uppercase tracking-widest text-eden-400 font-extrabold">Expediente de Personal</span>
            <h2 class="text-xl font-black">{{ usuarioDetalle.nombre }}</h2>
            <div class="flex items-center gap-2 mt-1">
              <span class="px-2 py-0.5 rounded text-2xs font-extrabold uppercase bg-slate-800 text-slate-300">
                {{ usuarioDetalle.rol }}
              </span>
              <span class="text-xs text-slate-400">
                Turno: <strong class="text-white capitalize">{{ usuarioDetalle.turno }}</strong>
              </span>
            </div>
          </div>
          <div class="flex items-center gap-2">
            <button 
              @click="abrirModalEditar(usuarioDetalle)"
              class="px-3 py-1.5 bg-eden-600 hover:bg-eden-700 text-white text-xs font-bold rounded-xl flex items-center gap-1 transition shadow-xs"
            >
              ✏️ Editar
            </button>
            <button 
              @click="modalDetalle = false" 
              class="w-8 h-8 rounded-full bg-slate-800 hover:bg-slate-700 text-slate-300 flex items-center justify-center text-sm font-bold"
            >
              ✕
            </button>
          </div>
        </div>

        <!-- Pestañas del Expediente -->
        <div class="flex border-b border-slate-100 dark:border-slate-800 bg-slate-50 dark:bg-slate-800/40 px-6">
          <button 
            @click="tabExpediente = 'laboral'"
            :class="[
              'py-3 px-4 text-xs font-bold border-b-2 transition-all',
              tabExpediente === 'laboral' 
                ? 'border-eden-600 text-eden-600 dark:text-eden-400' 
                : 'border-transparent text-slate-500 hover:text-slate-800'
            ]"
          >
            Datos Laborales y Personales
          </button>
          <button 
            @click="tabExpediente = 'documentos'"
            :class="[
              'py-3 px-4 text-xs font-bold border-b-2 transition-all flex items-center gap-1.5',
              tabExpediente === 'documentos' 
                ? 'border-eden-600 text-eden-600 dark:text-eden-400' 
                : 'border-transparent text-slate-500 hover:text-slate-800'
            ]"
          >
            <span>📁 Documentos</span>
            <span class="text-2xs bg-eden-100 dark:bg-eden-900/60 text-eden-800 dark:text-eden-300 px-1.5 py-0.2 rounded-full font-bold">
              {{ usuarioDetalle.documentos?.length || 0 }}
            </span>
          </button>
        </div>

        <!-- Contenido Pestaña 1: Datos Laborales y Personales -->
        <div v-if="tabExpediente === 'laboral'" class="p-6 space-y-4 max-h-[60vh] overflow-y-auto">
          <div class="grid grid-cols-1 sm:grid-cols-2 gap-4 text-xs">
            <div class="p-3 rounded-xl bg-slate-50 dark:bg-slate-800/60 border border-slate-100 dark:border-slate-800">
              <span class="text-slate-400 font-bold block mb-0.5">Correo Electrónico</span>
              <span class="font-bold text-slate-800 dark:text-slate-100 text-sm">{{ usuarioDetalle.email }}</span>
            </div>

            <div class="p-3 rounded-xl bg-slate-50 dark:bg-slate-800/60 border border-slate-100 dark:border-slate-800">
              <span class="text-slate-400 font-bold block mb-0.5">Teléfono Móvil</span>
              <span class="font-bold text-slate-800 dark:text-slate-100 text-sm">{{ usuarioDetalle.telefono || 'No registrado' }}</span>
            </div>

            <div class="p-3 rounded-xl bg-slate-50 dark:bg-slate-800/60 border border-slate-100 dark:border-slate-800">
              <span class="text-slate-400 font-bold block mb-0.5">CURP</span>
              <span class="font-mono font-bold text-slate-800 dark:text-slate-100 text-sm">{{ usuarioDetalle.curp || 'No registrado' }}</span>
            </div>

            <div class="p-3 rounded-xl bg-slate-50 dark:bg-slate-800/60 border border-slate-100 dark:border-slate-800">
              <span class="text-slate-400 font-bold block mb-0.5">RFC</span>
              <span class="font-mono font-bold text-slate-800 dark:text-slate-100 text-sm">{{ usuarioDetalle.rfc || 'No registrado' }}</span>
            </div>

            <div class="p-3 rounded-xl bg-slate-50 dark:bg-slate-800/60 border border-slate-100 dark:border-slate-800">
              <span class="text-slate-400 font-bold block mb-0.5">NSS (Seguro Social)</span>
              <span class="font-mono font-bold text-slate-800 dark:text-slate-100 text-sm">{{ usuarioDetalle.nss || 'No registrado' }}</span>
            </div>

            <div class="p-3 rounded-xl bg-slate-50 dark:bg-slate-800/60 border border-slate-100 dark:border-slate-800">
              <span class="text-slate-400 font-bold block mb-0.5">Salario Diario</span>
              <span class="font-bold text-eden-600 dark:text-eden-400 text-sm">${{ Number(usuarioDetalle.salario_diario || 0).toFixed(2) }} MXN</span>
            </div>

            <div class="p-3 rounded-xl bg-slate-50 dark:bg-slate-800/60 border border-slate-100 dark:border-slate-800 sm:col-span-2">
              <span class="text-slate-400 font-bold block mb-0.5">Contacto de Emergencia</span>
              <span class="font-bold text-slate-800 dark:text-slate-100">
                {{ usuarioDetalle.contacto_emergencia_nombre || 'No registrado' }} 
                <span v-if="usuarioDetalle.contacto_emergencia_telefono" class="text-slate-400 font-normal">({{ usuarioDetalle.contacto_emergencia_telefono }})</span>
              </span>
            </div>

            <div class="p-3 rounded-xl bg-slate-50 dark:bg-slate-800/60 border border-slate-100 dark:border-slate-800 sm:col-span-2">
              <span class="text-slate-400 font-bold block mb-0.5">Dirección / Domicilio</span>
              <span class="text-slate-700 dark:text-slate-300">{{ usuarioDetalle.direccion || 'Sin domicilio registrado' }}</span>
            </div>
          </div>
        </div>

        <!-- Contenido Pestaña 2: Documentos Almacenados -->
        <div v-else class="p-6 space-y-4 max-h-[60vh] overflow-y-auto">
          <!-- Formulario Agregar Documento -->
          <div class="p-4 rounded-2xl bg-slate-50 dark:bg-slate-800/60 border border-slate-200 dark:border-slate-700 space-y-3">
            <h4 class="font-black text-xs uppercase tracking-wider text-slate-700 dark:text-slate-200">+ Registrar Documento en Expediente</h4>
            
            <div class="grid grid-cols-1 sm:grid-cols-2 gap-2">
              <div>
                <label class="text-2xs font-bold text-slate-500">Tipo de Documento</label>
                <select 
                  v-model="formDoc.tipo" 
                  class="w-full mt-1 p-2 text-xs font-semibold border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-800 text-slate-800 dark:text-slate-100 rounded-xl focus:outline-none focus:border-eden-600"
                >
                  <option value="identificacion_ine">Identificación Oficial (INE)</option>
                  <option value="rfc">Constancia RFC / SAT</option>
                  <option value="curp">CURP Certificada</option>
                  <option value="nss_seguro">Número de Seguro Social (NSS)</option>
                  <option value="contrato_laboral">Contrato Laboral</option>
                  <option value="certificado_salud">Certificado Médico / Manejo de Alimentos</option>
                  <option value="comprobante_domicilio">Comprobante de Domicilio</option>
                  <option value="otro">Otro Documento</option>
                </select>
              </div>

              <div>
                <label class="text-2xs font-bold text-slate-500">Título / Nombre del Documento</label>
                <input 
                  v-model="formDoc.titulo" 
                  type="text" 
                  placeholder="Ej. Constancia Salubridad 2026" 
                  class="w-full mt-1 p-2 text-xs font-semibold border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-800 text-slate-800 dark:text-slate-100 rounded-xl focus:outline-none focus:border-eden-600"
                />
              </div>

              <div>
                <label class="text-2xs font-bold text-slate-500">Fecha de Vencimiento (Opcional)</label>
                <input 
                  v-model="formDoc.fecha_vencimiento" 
                  type="date" 
                  class="w-full mt-1 p-2 text-xs font-semibold border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-800 text-slate-800 dark:text-slate-100 rounded-xl focus:outline-none focus:border-eden-600"
                />
              </div>

              <div>
                <label class="text-2xs font-bold text-slate-500">Ruta / Archivo o Referencia</label>
                <input 
                  v-model="formDoc.url_archivo" 
                  type="text" 
                  placeholder="/documentos/cert_salud.pdf" 
                  class="w-full mt-1 p-2 text-xs font-semibold border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-800 text-slate-800 dark:text-slate-100 rounded-xl focus:outline-none focus:border-eden-600"
                />
              </div>
            </div>

            <button 
              @click="guardarDocumento"
              :disabled="!formDoc.titulo"
              class="w-full py-2 bg-eden-600 hover:bg-eden-700 disabled:opacity-50 text-white font-bold text-xs rounded-xl transition shadow-sm"
            >
              Guardar Documento en Expediente
            </button>
          </div>

          <!-- Lista de Documentos Cargados -->
          <div class="space-y-2">
            <div v-if="!usuarioDetalle.documentos || usuarioDetalle.documentos.length === 0" class="text-center py-6 text-slate-400 text-xs">
              No hay documentos cargados en el expediente de este colaborador.
            </div>

            <div 
              v-for="doc in usuarioDetalle.documentos" 
              :key="doc.id"
              class="p-3 rounded-xl bg-slate-50 dark:bg-slate-800/60 border border-slate-200 dark:border-slate-700 flex justify-between items-center"
            >
              <div>
                <div class="font-bold text-xs text-slate-800 dark:text-slate-100 flex items-center gap-1.5">
                  <span>📄</span> {{ doc.titulo }}
                </div>
                <div class="text-2xs text-slate-400 flex items-center gap-2 mt-0.5">
                  <span class="capitalize font-semibold text-eden-600 dark:text-eden-400">{{ doc.tipo.replace('_', ' ') }}</span>
                  <span v-if="doc.fecha_vencimiento">• Vence: {{ doc.fecha_vencimiento }}</span>
                </div>
              </div>

              <button 
                @click="eliminarDocumento(doc.id)"
                class="text-xs text-rose-500 hover:text-rose-700 font-bold px-2 py-1 rounded hover:bg-rose-50 dark:hover:bg-rose-950/40 transition"
              >
                Eliminar
              </button>
            </div>
          </div>
        </div>

        <div class="p-4 bg-slate-50 dark:bg-slate-800/40 border-t border-slate-100 dark:border-slate-800 flex justify-end">
          <button 
            @click="modalDetalle = false"
            class="px-5 py-2 bg-slate-900 dark:bg-slate-800 hover:bg-slate-800 text-white rounded-xl text-xs font-bold"
          >
            Cerrar Expediente
          </button>
        </div>
      </div>
    </div>

    <!-- Modal Registrar o Editar Colaborador -->
    <div v-if="modalUsuario" class="fixed inset-0 bg-slate-900/60 backdrop-blur-sm flex items-center justify-center p-4 z-50 overflow-y-auto">
      <div class="bg-white dark:bg-slate-900 rounded-3xl p-6 sm:p-7 max-w-lg w-full shadow-2xl border border-slate-200 dark:border-slate-800 space-y-4 my-8 flex flex-col max-h-[90vh]">
        <div class="flex justify-between items-center border-b border-slate-100 dark:border-slate-800 pb-3">
          <h3 class="text-lg font-black text-slate-800 dark:text-slate-100">
            {{ editandoId ? 'Editar Información del Colaborador' : 'Registrar Nuevo Colaborador' }}
          </h3>
          <button @click="modalUsuario = false" class="text-slate-400 hover:text-slate-600 font-bold">✕</button>
        </div>

        <div class="space-y-3.5 overflow-y-auto pr-1 flex-1">
          <!-- Nombre Completo -->
          <div>
            <label class="text-xs font-bold text-slate-700 dark:text-slate-300">Nombre Completo *</label>
            <input 
              v-model="formUsuario.nombre" 
              type="text" 
              placeholder="Ej. María Elena González" 
              class="w-full mt-1 p-2.5 text-xs font-semibold border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-800 text-slate-800 dark:text-slate-100 rounded-xl focus:outline-none focus:border-eden-600"
            />
          </div>

          <!-- Correo y Teléfono -->
          <div class="grid grid-cols-2 gap-2">
            <div>
              <label class="text-xs font-bold text-slate-700 dark:text-slate-300">Correo Electrónico *</label>
              <input 
                v-model="formUsuario.email" 
                type="email" 
                placeholder="maria@edencafe.com" 
                class="w-full mt-1 p-2.5 text-xs font-semibold border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-800 text-slate-800 dark:text-slate-100 rounded-xl focus:outline-none focus:border-eden-600"
              />
            </div>

            <div>
              <label class="text-xs font-bold text-slate-700 dark:text-slate-300">Teléfono Móvil</label>
              <input 
                v-model="formUsuario.telefono" 
                type="tel" 
                placeholder="555-000-0000" 
                class="w-full mt-1 p-2.5 text-xs font-semibold border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-800 text-slate-800 dark:text-slate-100 rounded-xl focus:outline-none focus:border-eden-600"
              />
            </div>
          </div>

          <!-- Rol y Turno -->
          <div class="grid grid-cols-2 gap-2">
            <div>
              <label class="text-xs font-bold text-slate-700 dark:text-slate-300">Rol del Personal *</label>
              <select 
                v-model="formUsuario.rol" 
                class="w-full mt-1 p-2.5 text-xs font-semibold border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-800 text-slate-800 dark:text-slate-100 rounded-xl focus:outline-none focus:border-eden-600"
              >
                <option value="administrador">Administrador (Total)</option>
                <option value="gerente">Gerente</option>
                <option value="jefe">Jefe de Turno</option>
                <option value="cocina">Cocina / Barra</option>
                <option value="mesero">Mesero / Salón</option>
                <option value="auxiliar_general">Auxiliar General (Almacén)</option>
              </select>
            </div>

            <div>
              <label class="text-xs font-bold text-slate-700 dark:text-slate-300">Turno de Trabajo *</label>
              <select 
                v-model="formUsuario.turno" 
                class="w-full mt-1 p-2.5 text-xs font-semibold border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-800 text-slate-800 dark:text-slate-100 rounded-xl focus:outline-none focus:border-eden-600"
              >
                <option value="matutino">Turno Matutino</option>
                <option value="vespertino">Turno Vespertino</option>
                <option value="nocturno">Turno Nocturno</option>
                <option value="completo">Turno Completo</option>
                <option value="mixto">Turno Mixto</option>
              </select>
            </div>
          </div>

          <!-- Switch Acceso al Sistema PDV -->
          <label class="flex items-center gap-3 p-3 rounded-xl bg-slate-50 dark:bg-slate-800 border border-slate-200 dark:border-slate-700 cursor-pointer">
            <input 
              v-model="formUsuario.acceso_sistema" 
              type="checkbox" 
              class="w-4 h-4 rounded text-eden-600 focus:ring-eden-500"
            />
            <div class="text-xs">
              <span class="font-bold text-slate-800 dark:text-slate-200 block">¿Habilitar acceso a terminales y comandero?</span>
              <span class="text-slate-400 block">Permite iniciar sesión con su PIN o contraseña en el PDV.</span>
            </div>
          </label>

          <!-- PIN DE SEGURIDAD CON MÁSCARA ESTRICTA DE 4 DÍGITOS -->
          <div v-if="formUsuario.acceso_sistema" class="p-3.5 rounded-2xl bg-slate-50 dark:bg-slate-800/80 border border-slate-200 dark:border-slate-700 space-y-2">
            <div class="flex justify-between items-center">
              <label class="text-xs font-black text-slate-700 dark:text-slate-300">
                PIN de Autorización y Acceso *
              </label>
              <span 
                class="text-3xs font-mono font-black px-2 py-0.5 rounded-full"
                :class="(formUsuario.pin_seguridad || '').length === 4 ? 'bg-emerald-100 text-emerald-800 dark:bg-emerald-950 dark:text-emerald-300' : 'bg-slate-200 dark:bg-slate-700 text-slate-600 dark:text-slate-300'"
              >
                {{ (formUsuario.pin_seguridad || '').length }} / 4 dígitos
              </span>
            </div>

            <!-- Input con máscara estricta que solo admite números de 0 a 9 y máximo 4 caracteres -->
            <div class="space-y-1.5">
              <input 
                :value="formUsuario.pin_seguridad" 
                @input="sanitizarPin"
                type="password" 
                maxlength="4"
                inputmode="numeric"
                pattern="[0-9]*"
                placeholder="••••" 
                class="w-full p-2.5 text-center text-xl tracking-[0.6em] font-mono font-black border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-900 text-slate-800 dark:text-slate-100 rounded-xl focus:outline-none focus:border-eden-600"
              />

              <!-- Indicadores visuales de 4 esferas -->
              <div class="flex justify-center items-center gap-2.5 py-1">
                <div 
                  v-for="d in 4" 
                  :key="d"
                  :class="[
                    'w-3 h-3 rounded-full border-2 transition-all',
                    (formUsuario.pin_seguridad || '').length >= d 
                      ? 'bg-eden-600 border-eden-600 scale-110 shadow-xs' 
                      : 'border-slate-300 dark:border-slate-600'
                  ]"
                ></div>
              </div>
            </div>

            <p class="text-3xs text-slate-400 text-center">
              Solo se permiten 4 números (0-9). Se utiliza para login táctil y autorizaciones de caja o cancelaciones.
            </p>
          </div>

          <!-- Salario y Fecha de Ingreso -->
          <div class="grid grid-cols-2 gap-2">
            <div>
              <label class="text-xs font-bold text-slate-700 dark:text-slate-300">Salario Diario ($ MXN)</label>
              <input 
                v-model.number="formUsuario.salario_diario" 
                type="number" 
                step="10.00"
                placeholder="0.00" 
                class="w-full mt-1 p-2.5 text-xs font-semibold border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-800 text-slate-800 dark:text-slate-100 rounded-xl focus:outline-none focus:border-eden-600 font-mono"
              />
            </div>

            <div>
              <label class="text-xs font-bold text-slate-700 dark:text-slate-300">Fecha de Ingreso</label>
              <input 
                v-model="formUsuario.fecha_ingreso" 
                type="date" 
                class="w-full mt-1 p-2.5 text-xs font-semibold border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-800 text-slate-800 dark:text-slate-100 rounded-xl focus:outline-none focus:border-eden-600"
              />
            </div>
          </div>

          <!-- Documentación Oficial -->
          <div class="grid grid-cols-3 gap-2">
            <div>
              <label class="text-3xs font-bold text-slate-700 dark:text-slate-300">CURP</label>
              <input 
                v-model="formUsuario.curp" 
                type="text" 
                placeholder="18 caracteres" 
                class="w-full mt-1 p-2 text-xs font-mono uppercase border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-800 text-slate-800 dark:text-slate-100 rounded-xl focus:outline-none focus:border-eden-600"
              />
            </div>
            <div>
              <label class="text-3xs font-bold text-slate-700 dark:text-slate-300">RFC</label>
              <input 
                v-model="formUsuario.rfc" 
                type="text" 
                placeholder="13 caracteres" 
                class="w-full mt-1 p-2 text-xs font-mono uppercase border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-800 text-slate-800 dark:text-slate-100 rounded-xl focus:outline-none focus:border-eden-600"
              />
            </div>
            <div>
              <label class="text-3xs font-bold text-slate-700 dark:text-slate-300">NSS</label>
              <input 
                v-model="formUsuario.nss" 
                type="text" 
                placeholder="Seguro Social" 
                class="w-full mt-1 p-2 text-xs font-mono border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-800 text-slate-800 dark:text-slate-100 rounded-xl focus:outline-none focus:border-eden-600"
              />
            </div>
          </div>

          <!-- Contacto de Emergencia -->
          <div class="grid grid-cols-2 gap-2">
            <div>
              <label class="text-xs font-bold text-slate-700 dark:text-slate-300">Contacto de Emergencia</label>
              <input 
                v-model="formUsuario.contacto_emergencia_nombre" 
                type="text" 
                placeholder="Nombre familiar" 
                class="w-full mt-1 p-2.5 text-xs font-semibold border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-800 text-slate-800 dark:text-slate-100 rounded-xl focus:outline-none focus:border-eden-600"
              />
            </div>
            <div>
              <label class="text-xs font-bold text-slate-700 dark:text-slate-300">Tel. Emergencia</label>
              <input 
                v-model="formUsuario.contacto_emergencia_telefono" 
                type="tel" 
                placeholder="555-000-0000" 
                class="w-full mt-1 p-2.5 text-xs font-semibold border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-800 text-slate-800 dark:text-slate-100 rounded-xl focus:outline-none focus:border-eden-600"
              />
            </div>
          </div>

          <!-- Estatus Activo / Inactivo -->
          <label class="flex items-center gap-2 p-2.5 rounded-xl bg-slate-50 dark:bg-slate-800 border border-slate-200 dark:border-slate-700 cursor-pointer">
            <input 
              v-model="formUsuario.activo" 
              type="checkbox" 
              class="w-4 h-4 rounded text-emerald-600 focus:ring-emerald-500"
            />
            <span class="text-xs font-bold text-slate-700 dark:text-slate-300">
              Colaborador activo en nómina y plantilla
            </span>
          </label>
        </div>

        <div class="flex gap-2 pt-3 border-t border-slate-100 dark:border-slate-800">
          <button 
            @click="modalUsuario = false" 
            class="flex-1 py-2.5 bg-slate-100 dark:bg-slate-800 hover:bg-slate-200 dark:hover:bg-slate-700 text-slate-700 dark:text-slate-300 rounded-xl font-bold text-xs transition"
          >
            Cancelar
          </button>
          <button 
            @click="guardarUsuario" 
            :disabled="!formUsuario.nombre || !formUsuario.email || guardando"
            class="flex-1 py-2.5 bg-eden-600 hover:bg-eden-700 disabled:opacity-50 text-white rounded-xl font-bold text-xs transition shadow-sm"
          >
            <span v-if="guardando">Guardando...</span>
            <span v-else>{{ editandoId ? 'Guardar Cambios' : 'Registrar Colaborador' }}</span>
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useAuthStore } from '../stores/auth'
import api from '../api'

const authStore = useAuthStore()

const filtroTurno = ref('todos')
const modalUsuario = ref(false)
const editandoId = ref(null)
const guardando = ref(false)
const modalDetalle = ref(false)
const tabExpediente = ref('laboral')
const usuarioDetalle = ref(null)

const formUsuario = ref({
  nombre: '',
  email: '',
  telefono: '',
  rol: 'mesero',
  turno: 'matutino',
  acceso_sistema: true,
  pin_seguridad: '',
  password: 'edencafe123',
  curp: '',
  rfc: '',
  nss: '',
  salario_diario: 0,
  fecha_ingreso: '',
  contacto_emergencia_nombre: '',
  contacto_emergencia_telefono: '',
  activo: true
})

const formDoc = ref({
  tipo: 'identificacion_ine',
  titulo: '',
  fecha_vencimiento: '',
  url_archivo: ''
})

onMounted(() => {
  authStore.cargarUsuarios()
})

const usuariosFiltrados = computed(() => {
  if (filtroTurno.value === 'todos') return authStore.usuarios
  return authStore.usuarios.filter(u => u.turno === filtroTurno.value)
})

// Sanitiza el PIN para aceptar estrictamente números y máximo 4 dígitos
const sanitizarPin = (e) => {
  const digitos = e.target.value.replace(/\D/g, '').slice(0, 4)
  formUsuario.value.pin_seguridad = digitos
}

const abrirModalNuevoUsuario = () => {
  editandoId.value = null
  formUsuario.value = {
    nombre: '',
    email: '',
    telefono: '',
    rol: 'mesero',
    turno: 'matutino',
    acceso_sistema: true,
    pin_seguridad: '',
    password: 'edencafe123',
    curp: '',
    rfc: '',
    nss: '',
    salario_diario: 0,
    fecha_ingreso: '',
    contacto_emergencia_nombre: '',
    contacto_emergencia_telefono: '',
    activo: true
  }
  modalUsuario.value = true
}

const abrirModalEditar = async (u) => {
  editandoId.value = u.id
  formUsuario.value = {
    nombre: u.nombre || '',
    email: u.email || '',
    telefono: u.telefono || '',
    rol: u.rol || 'mesero',
    turno: u.turno || 'matutino',
    acceso_sistema: u.acceso_sistema ?? true,
    pin_seguridad: u.pin_seguridad || '',
    password: '',
    curp: u.curp || '',
    rfc: u.rfc || '',
    nss: u.nss || '',
    salario_diario: Number(u.salario_diario || 0),
    fecha_ingreso: u.fecha_ingreso || '',
    contacto_emergencia_nombre: u.contacto_emergencia_nombre || '',
    contacto_emergencia_telefono: u.contacto_emergencia_telefono || '',
    activo: u.activo ?? true
  }
  modalUsuario.value = true
}

const verDetalleColaborador = async (id) => {
  try {
    const { data } = await api.get(`/usuarios/${id}`)
    usuarioDetalle.value = data
    tabExpediente.value = 'laboral'
    modalDetalle.value = true
  } catch (err) {
    alert('Error al obtener el expediente del colaborador.')
  }
}

const guardarUsuario = async () => {
  if (formUsuario.value.acceso_sistema && formUsuario.value.pin_seguridad) {
    if (formUsuario.value.pin_seguridad.length !== 4) {
      alert('El PIN de seguridad debe contener exactamente 4 dígitos numéricos.')
      return
    }
  }

  guardando.value = true
  try {
    if (editandoId.value) {
      // Actualizar colaborador existente
      const payload = { ...formUsuario.value }
      if (!payload.password) delete payload.password // No sobrescribir si no se cambió
      
      const res = await authStore.actualizarUsuario(editandoId.value, payload)
      if (usuarioDetalle.value && usuarioDetalle.value.id === editandoId.value) {
        usuarioDetalle.value = { ...usuarioDetalle.value, ...res }
      }
      alert('Información del colaborador actualizada correctamente.')
    } else {
      // Crear nuevo colaborador
      await authStore.crearUsuario(formUsuario.value)
      alert('Colaborador registrado exitosamente.')
    }
    modalUsuario.value = false
  } catch (err) {
    alert(err.response?.data?.detail || 'Error al guardar la información del colaborador.')
  } finally {
    guardando.value = false
  }
}

const guardarDocumento = async () => {
  if (!usuarioDetalle.value || !formDoc.value.titulo) return
  try {
    const payload = {
      tipo: formDoc.value.tipo,
      titulo: formDoc.value.titulo,
      url_archivo: formDoc.value.url_archivo || null,
      fecha_vencimiento: formDoc.value.fecha_vencimiento || null
    }
    const { data } = await api.post(`/usuarios/${usuarioDetalle.value.id}/documentos`, payload)
    if (!usuarioDetalle.value.documentos) usuarioDetalle.value.documentos = []
    usuarioDetalle.value.documentos.push(data)
    formDoc.value = { tipo: 'identificacion_ine', titulo: '', fecha_vencimiento: '', url_archivo: '' }
    alert('Documento guardado en el expediente.')
  } catch (err) {
    alert('Error al registrar documento.')
  }
}

const eliminarDocumento = async (docId) => {
  if (!confirm('¿Eliminar este documento del expediente?')) return
  try {
    await api.delete(`/usuarios/documentos/${docId}`)
    usuarioDetalle.value.documentos = usuarioDetalle.value.documentos.filter(d => d.id !== docId)
  } catch (err) {
    alert('Error al eliminar documento.')
  }
}
</script>

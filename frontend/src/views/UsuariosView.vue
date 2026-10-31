<template>
  <div class="space-y-6 max-w-5xl mx-auto">
    <!-- Header -->
    <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 bg-white p-6 rounded-2xl shadow-sm border border-slate-200">
      <div>
        <h1 class="text-2xl font-black text-slate-800 tracking-tight">Personal y Roles (RBAC)</h1>
        <p class="text-slate-500 text-sm">Administración de usuarios, roles y PINs de seguridad</p>
      </div>

      <button 
        @click="modalNuevoUsuario = true"
        class="px-4 py-2 bg-eden-600 hover:bg-eden-700 text-white rounded-xl text-xs font-bold shadow-sm transition active:scale-95 flex items-center gap-1.5"
      >
        <span>+</span> Registrar Nuevo Usuario
      </button>
    </div>

    <!-- Usuario en Turno Activo Card -->
    <div class="bg-slate-900 text-white p-5 rounded-2xl flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 shadow-md">
      <div>
        <span class="text-2xs font-extrabold uppercase tracking-widest text-eden-400">Sesión en Turno</span>
        <h3 class="text-xl font-black">{{ authStore.usuarioActual.nombre }}</h3>
        <p class="text-xs text-slate-400 font-mono">{{ authStore.usuarioActual.email }}</p>
      </div>
      <div class="flex items-center gap-2">
        <span class="px-3 py-1 rounded-full text-xs font-bold bg-eden-500/20 text-eden-300 border border-eden-500/40 uppercase">
          Rol: {{ authStore.usuarioActual.rol }}
        </span>
      </div>
    </div>

    <!-- Lista de Usuarios y Roles -->
    <div class="bg-white rounded-2xl border border-slate-200 shadow-sm overflow-hidden">
      <div class="p-4 border-b border-slate-100 flex justify-between items-center">
        <h3 class="font-bold text-slate-800 text-sm">Equipo de Edén Café</h3>
        <span class="text-xs text-slate-400">{{ authStore.usuarios.length }} usuarios registrados</span>
      </div>

      <div class="divide-y divide-slate-100">
        <div 
          v-for="u in authStore.usuarios" 
          :key="u.id"
          class="p-4 flex flex-col sm:flex-row justify-between items-start sm:items-center gap-3 hover:bg-slate-50/70 transition"
        >
          <div class="flex items-center gap-3">
            <div class="w-10 h-10 rounded-full bg-slate-100 border border-slate-200 flex items-center justify-center font-black text-slate-700 text-sm">
              {{ u.nombre.charAt(0) }}
            </div>
            <div>
              <h4 class="font-bold text-sm text-slate-800">{{ u.nombre }}</h4>
              <span class="text-xs text-slate-400">{{ u.email }}</span>
            </div>
          </div>

          <div class="flex items-center gap-3">
            <span :class="[
              'px-3 py-1 rounded-full text-2xs font-extrabold uppercase',
              u.rol === 'administrador' ? 'bg-red-100 text-red-800' :
              u.rol === 'gerente' ? 'bg-amber-100 text-amber-800' :
              u.rol === 'jefe' ? 'bg-indigo-100 text-indigo-800' :
              u.rol === 'cocina' ? 'bg-orange-100 text-orange-800' :
              u.rol === 'mesero' ? 'bg-emerald-100 text-emerald-800' :
              'bg-slate-100 text-slate-700'
            ]">
              {{ u.rol }}
            </span>

            <span v-if="u.pin_seguridad" class="text-2xs font-mono text-slate-400 bg-slate-100 px-2 py-0.5 rounded">
              PIN: ••••
            </span>

            <button 
              @click="authStore.cambiarUsuarioTurno(u)"
              class="px-3 py-1 bg-white hover:bg-slate-100 border border-slate-200 text-slate-700 rounded-lg text-xs font-bold transition active:scale-95"
            >
              Usar en Turno
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Modal Registrar Nuevo Usuario -->
    <div v-if="modalNuevoUsuario" class="fixed inset-0 bg-slate-900/60 backdrop-blur-sm flex items-center justify-center p-4 z-50">
      <div class="bg-white rounded-3xl p-6 max-w-sm w-full shadow-2xl border border-slate-200 space-y-4">
        <h3 class="text-lg font-black text-slate-800">Registrar Personal</h3>

        <div class="space-y-3">
          <div>
            <label class="text-xs font-bold text-slate-700">Nombre Completo</label>
            <input 
              v-model="formUsuario.nombre" 
              type="text" 
              placeholder="Ej. María González" 
              class="w-full mt-1 p-2.5 text-xs font-semibold border border-slate-300 rounded-xl focus:outline-none focus:border-eden-600"
            />
          </div>

          <div>
            <label class="text-xs font-bold text-slate-700">Correo Electrónico</label>
            <input 
              v-model="formUsuario.email" 
              type="email" 
              placeholder="maria@edencafe.com" 
              class="w-full mt-1 p-2.5 text-xs font-semibold border border-slate-300 rounded-xl focus:outline-none focus:border-eden-600"
            />
          </div>

          <div>
            <label class="text-xs font-bold text-slate-700">Rol del Usuario</label>
            <select 
              v-model="formUsuario.rol" 
              class="w-full mt-1 p-2.5 text-xs font-semibold border border-slate-300 rounded-xl focus:outline-none focus:border-eden-600"
            >
              <option value="administrador">Administrador (Control Total)</option>
              <option value="gerente">Gerente (Cancelaciones / Cortes)</option>
              <option value="jefe">Jefe de Turno</option>
              <option value="cocina">Cocina (KDS)</option>
              <option value="mesero">Mesero (Comandero)</option>
              <option value="auxiliar_general">Auxiliar General (Almacén)</option>
            </select>
          </div>

          <div>
            <label class="text-xs font-bold text-slate-700">PIN de Autorización (4 dígitos)</label>
            <input 
              v-model="formUsuario.pin_seguridad" 
              type="password" 
              maxlength="4"
              placeholder="1234" 
              class="w-full mt-1 p-2.5 text-xs font-mono tracking-widest border border-slate-300 rounded-xl focus:outline-none focus:border-eden-600"
            />
          </div>

          <div>
            <label class="text-xs font-bold text-slate-700">Contraseña de Acceso</label>
            <input 
              v-model="formUsuario.password" 
              type="password" 
              placeholder="••••••••" 
              class="w-full mt-1 p-2.5 text-xs font-semibold border border-slate-300 rounded-xl focus:outline-none focus:border-eden-600"
            />
          </div>
        </div>

        <div class="flex gap-2 pt-2">
          <button 
            @click="modalNuevoUsuario = false" 
            class="flex-1 py-2.5 bg-slate-100 hover:bg-slate-200 text-slate-700 rounded-xl font-bold text-xs transition"
          >
            Cancelar
          </button>
          <button 
            @click="guardarUsuario" 
            :disabled="!formUsuario.nombre || !formUsuario.email || !formUsuario.password"
            class="flex-1 py-2.5 bg-eden-600 hover:bg-eden-700 disabled:opacity-50 text-white rounded-xl font-bold text-xs transition shadow-sm"
          >
            Guardar Usuario
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useAuthStore } from '../stores/auth'

const authStore = useAuthStore()

const modalNuevoUsuario = ref(false)
const formUsuario = ref({
  nombre: '',
  email: '',
  rol: 'mesero',
  pin_seguridad: '',
  password: ''
})

onMounted(() => {
  authStore.cargarUsuarios()
})

const guardarUsuario = async () => {
  try {
    await authStore.crearUsuario(formUsuario.value)
    modalNuevoUsuario.value = false
    formUsuario.value = { nombre: '', email: '', rol: 'mesero', pin_seguridad: '', password: '' }
    alert('Usuario registrado exitosamente con su rol asignado.')
  } catch (err) {
    alert(err.response?.data?.detail || 'Error al registrar usuario.')
  }
}
</script>

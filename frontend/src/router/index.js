import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore, RUTA_INICIAL_POR_ROL } from '../stores/auth'
import LoginView from '../views/LoginView.vue'
import CartaView from '../views/CartaView.vue'
import MesasView from '../views/MesasView.vue'
import PosView from '../views/PosView.vue'
import CocinaView from '../views/CocinaView.vue'
import CajaView from '../views/CajaView.vue'
import InventarioView from '../views/InventarioView.vue'
import UsuariosView from '../views/UsuariosView.vue'
import PlatillosView from '../views/PlatillosView.vue'

const routes = [
  {
    path: '/login',
    name: 'login',
    component: LoginView,
    meta: { publico: true, title: 'Acceso - Edén Café' }
  },
  {
    path: '/carta',
    name: 'carta',
    component: CartaView,
    meta: { publico: true, title: 'Menú Digital — Edén Café' }
  },
  {
    path: '/',
    name: 'mesas',
    component: MesasView,
    meta: { 
      title: 'Mesas y Salón',
      roles: ['administrador', 'gerente', 'jefe', 'mesero']
    }
  },
  {
    path: '/pos',
    name: 'pos',
    component: PosView,
    meta: { 
      title: 'Comandero Móvil',
      roles: ['administrador', 'gerente', 'jefe', 'mesero']
    }
  },
  {
    path: '/cocina',
    name: 'cocina',
    component: CocinaView,
    meta: { 
      title: 'Cocina / KDS',
      roles: ['administrador', 'gerente', 'jefe', 'cocina']
    }
  },
  {
    path: '/caja',
    name: 'caja',
    component: CajaView,
    meta: { 
      title: 'Caja y Cobros',
      roles: ['administrador', 'gerente', 'jefe']
    }
  },
  {
    path: '/inventario',
    name: 'inventario',
    component: InventarioView,
    meta: { 
      title: 'Inventario y Almacén',
      roles: ['administrador', 'gerente', 'auxiliar_general']
    }
  },
  {
    path: '/usuarios',
    name: 'usuarios',
    component: UsuariosView,
    meta: { 
      title: 'Personal y Roles',
      roles: ['administrador']
    }
  },
  {
    path: '/platillos',
    name: 'platillos',
    component: PlatillosView,
    meta: { 
      title: 'Platillos y Menú',
      roles: ['administrador', 'gerente']
    }
  },
  {
    path: '/:pathMatch(.*)*',
    redirect: '/'
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// Control de Acceso y Permisos por Rol (Navigation Guard)
router.beforeEach((to, from, next) => {
  const authStore = useAuthStore()

  // 1. Si la ruta es pública (login o carta para clientes)
  if (to.meta.publico) {
    if (to.name === 'login' && authStore.estaAutenticado) {
      const rutaDefecto = RUTA_INICIAL_POR_ROL[authStore.usuarioActual.rol] || '/'
      return next(rutaDefecto)
    }
    return next()
  }

  // 2. Si no ha iniciado sesión, enviar a /login
  if (!authStore.estaAutenticado) {
    return next({ path: '/login', query: { redirect: to.fullPath } })
  }

  // 3. Validar si el rol del usuario tiene permiso para entrar a esta ruta
  const rol = authStore.usuarioActual.rol
  if (to.meta.roles && !to.meta.roles.includes(rol)) {
    const rutaPermitida = RUTA_INICIAL_POR_ROL[rol] || '/'
    return next(rutaPermitida)
  }

  next()
})

export default router

import { createRouter, createWebHistory } from 'vue-router'
import MesasView from '../views/MesasView.vue'
import PosView from '../views/PosView.vue'
import CocinaView from '../views/CocinaView.vue'
import CajaView from '../views/CajaView.vue'
import InventarioView from '../views/InventarioView.vue'
import UsuariosView from '../views/UsuariosView.vue'

const routes = [
  {
    path: '/',
    name: 'mesas',
    component: MesasView,
    meta: { title: 'Mesas y Salón' }
  },
  {
    path: '/pos',
    name: 'pos',
    component: PosView,
    meta: { title: 'Comandero Móvil' }
  },
  {
    path: '/cocina',
    name: 'cocina',
    component: CocinaView,
    meta: { title: 'Cocina / KDS' }
  },
  {
    path: '/caja',
    name: 'caja',
    component: CajaView,
    meta: { title: 'Caja y Cobros' }
  },
  {
    path: '/inventario',
    name: 'inventario',
    component: InventarioView,
    meta: { title: 'Inventario y Almacén' }
  },
  {
    path: '/usuarios',
    name: 'usuarios',
    component: UsuariosView,
    meta: { title: 'Personal y Roles' }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router

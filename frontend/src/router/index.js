import { createRouter, createWebHistory } from 'vue-router'
import MesasView from '../views/MesasView.vue'
import PosView from '../views/PosView.vue'
import CocinaView from '../views/CocinaView.vue'
import CajaView from '../views/CajaView.vue'

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
    meta: { title: 'Toma de Pedidos' }
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
    meta: { title: 'Caja y Cobro' }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router

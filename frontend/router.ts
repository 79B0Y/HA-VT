import { createRouter, createWebHashHistory } from 'vue-router'

const routes = [
  {
    path: '/',
    name: 'Dashboard',
    component: () => import('./pages/Dashboard.vue')
  },
  {
    path: '/devices',
    name: 'Devices',
    component: () => import('./pages/Devices.vue')
  },
  {
    path: '/logs',
    name: 'Logs',
    component: () => import('./pages/Logs.vue')
  },
  {
    path: '/mongo',
    name: 'MongoStats',
    component: () => import('./pages/MongoStats.vue')
  }
]

const router = createRouter({
  history: createWebHashHistory(),
  routes
})

export default router

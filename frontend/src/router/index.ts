import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView,
    },
    // {
    //   path: '/encryption',
    //   name: 'encryption',
    //   component: () => import('../views/EncryptionView.vue'),
    // },
    // {
    //   path: '/decryption',
    //   name: 'decryption',
    //   component: () => import('../views/DecryptionView.vue'),
    // },
    // {
    //   path: '/tools',
    //   name: 'tools',
    //   component: () => import('../views/ToolsView.vue'),
    // },
  ],
})

export default router

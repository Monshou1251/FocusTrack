// src/router/index.js
import { useAuthStore } from '@/store/auth'
import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import Login from '../views/Login.vue'
import MainView from '../views/MainView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    { path: '/', name: 'home', component: HomeView },
    { path: '/login', name: 'login', component: Login },
    { path: '/main', name: 'main', component: MainView, meta: { requiresAuth: true } }
  ]
})

router.beforeEach(async (to, from, next) => {
  const authStore = useAuthStore()

  // 🔒 Только если переходим на защищённую страницу и user ещё не загружен
  if (to.meta.requiresAuth && !authStore.user) {
    try {
      await authStore.fetchCurrentUser()
    } catch (e) {
      return next({ name: 'login' }) // ⛔ не авторизован
    }
  }

  next()
})

export default router

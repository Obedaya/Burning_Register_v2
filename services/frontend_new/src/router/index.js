import { createRouter, createWebHistory } from 'vue-router'
import RegisterView from '../views/RegisterView.vue'
import StatisticsView from '../views/StatisticsView.vue'
import AdminView from '../views/AdminView.vue'

const routes = [
  {
    path: '/',
    name: 'home',
    component: RegisterView,
    meta: {
      title: 'Burning Register'
    }
  },
  {
    path: '/statistics',
    name: 'statistics',
    component: StatisticsView,
    meta: {
      title: 'Burning Register - Statistics'
    }
  },
  {
    path: '/admin',
    name: 'admin',
    component: AdminView,
    meta: {
      title: 'Burning Register - Admin'
    }
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

router.beforeEach((to) => {
  document.title = to.meta?.title ?? 'Burning Register'
})

export default router

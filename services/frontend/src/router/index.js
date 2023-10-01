import { createRouter, createWebHistory } from 'vue-router'
import RegisterView from '../views/RegisterView.vue'
import StatisticsView from '../views/StatisticsView.vue'
import AdminView from '../views/AdminView.vue'

const routes = [
  {
    path: '/',
    name: 'home',
    component: RegisterView
  },
  {
    path: '/statistics',
    name: 'statistics',
    component: StatisticsView
  },
  {
    path: '/admin',
    name: 'admin',
    component: AdminView
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router

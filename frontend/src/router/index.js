import { createRouter, createWebHistory } from 'vue-router'
import Login from '../views/Login.vue'
import InstructorDashboard from '../views/instructor/InstructorDashboard.vue'
import InstructorSchedule from '../views/instructor/InstructorSchedule.vue'
import InstructorHistory from '../views/instructor/InstructorHistory.vue'
import AdminDashboard from '../views/admin/AdminDashboard.vue'

const routes = [
  {
    path: '/',
    redirect: '/login'
  },
  {
    path: '/login',
    name: 'login',
    component: Login
  },
  // Instructor routes
  {
    path: '/instructor',
    name: 'instructorDashboard',
    component: InstructorDashboard,
    meta: { requiresAuth: true, requiresInstructor: true }
  },
  {
    path: '/instructor/schedule',
    name: 'instructorSchedule',
    component: InstructorSchedule,
    meta: { requiresAuth: true, requiresInstructor: true }
  },
  {
    path: '/instructor/history',
    name: 'instructorHistory',
    component: InstructorHistory,
    meta: { requiresAuth: true, requiresInstructor: true }
  },
  // Admin routes
  {
    path: '/admin',
    name: 'adminDashboard',
    component: AdminDashboard,
    meta: { requiresAuth: true, requiresAdmin: true }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// Navigation guard for authentication and role-based access
router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('token')
  const userRole = localStorage.getItem('userRole')

  // Check if route requires authentication
  if (to.matched.some(record => record.meta.requiresAuth)) {
    if (!token) {
      next('/login')
      return
    }

    // Check role requirements
    if (to.meta.requiresAdmin && userRole !== 'Admin') {
      next('/')
      return
    }

    if (to.meta.requiresInstructor && !['Instructor', 'Admin'].includes(userRole)) {
      next('/')
      return
    }
  }

  // If on login page and already authenticated, redirect to appropriate dashboard
  if (to.path === '/login' && token) {
    if (userRole === 'Admin') {
      next('/admin')
    } else if (userRole === 'Instructor') {
      next('/instructor')
    } else {
      next('/')
    }
    return
  }

  next()
})

export default router

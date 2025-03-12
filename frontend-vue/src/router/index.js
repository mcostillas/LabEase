import { createRouter, createWebHistory } from 'vue-router'
import LandingPage from '../views/LandingPage.vue'
import LoginPage from '../views/LoginPage.vue'
import SignupPage from '../views/SignupPage.vue'
import BookingForm from '../views/BookingForm.vue'
import AdminDashboard from '../views/admin/AdminDashboard.vue'
import LogBook from '../views/admin/LogBook.vue'
import AdminNotifications from '../views/admin/AdminNotifications.vue'
import InstructorDashboard from '../views/instructor/InstructorDashboard.vue'
import InstructorSchedule from '../views/instructor/InstructorSchedule.vue'
import InstructorHistory from '../views/instructor/InstructorHistory.vue'
import InstructorNotifications from '../views/instructor/InstructorNotifications.vue'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      name: 'landing',
      component: LandingPage
    },
    {
      path: '/login',
      name: 'login',
      component: LoginPage
    },
    {
      path: '/signup',
      name: 'signup',
      component: SignupPage
    },
    {
      path: '/booking',
      name: 'booking',
      component: BookingForm,
      meta: { requiresAuth: true }
    },
    {
      path: '/admin',
      name: 'admin',
      component: AdminDashboard,
      meta: { requiresAuth: true, requiresAdmin: true }
    },
    {
      path: '/admin/log-book',
      name: 'logBook',
      component: LogBook,
      meta: { requiresAuth: true, requiresAdmin: true }
    },
    {
      path: '/admin/notifications',
      name: 'adminNotifications',
      component: AdminNotifications,
      meta: { requiresAuth: true, requiresAdmin: true }
    },
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
    {
      path: '/instructor/notifications',
      name: 'instructorNotifications',
      component: InstructorNotifications,
      meta: { requiresAuth: true, requiresInstructor: true }
    }
  ]
})

// Navigation guard for protected routes
router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('labease_auth_token')
  const userData = JSON.parse(localStorage.getItem('labease_user_data') || 'null')

  if (to.meta.requiresAuth && !token) {
    next('/login')
    return
  }

  if (to.meta.requiresAdmin && (!userData || userData.role !== 'admin')) {
    next('/')
    return
  }

  if (to.meta.requiresInstructor && (!userData || userData.role !== 'instructor')) {
    next('/')
    return
  }

  next()
})

export default router

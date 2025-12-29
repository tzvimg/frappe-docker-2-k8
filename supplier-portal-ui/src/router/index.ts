import { createRouter, createWebHistory } from 'vue-router'
import type { RouteRecordRaw } from 'vue-router'
import { useAuthStore } from '@/stores'

const routes: RouteRecordRaw[] = [
  {
    path: '/login',
    name: 'Login',
    component: () => import('@/views/LoginView.vue'),
    meta: { requiresAuth: false },
  },
  {
    path: '/',
    name: 'Dashboard',
    component: () => import('@/views/DashboardView.vue'),
    meta: { requiresAuth: true },
  },
  {
    path: '/inquiries',
    name: 'InquiryList',
    component: () => import('@/views/InquiryListView.vue'),
    meta: { requiresAuth: true },
  },
  {
    path: '/inquiries/new',
    name: 'InquiryNew',
    component: () => import('@/views/InquiryFormView.vue'),
    meta: { requiresAuth: true },
  },
  {
    path: '/inquiries/:name',
    name: 'InquiryDetail',
    component: () => import('@/views/InquiryDetailView.vue'),
    meta: { requiresAuth: true },
    props: true,
  },
  {
    path: '/profile',
    name: 'Profile',
    component: () => import('@/views/ProfileView.vue'),
    meta: { requiresAuth: true },
  },
  {
    path: '/:pathMatch(.*)*',
    redirect: '/',
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

// Flag to track if we're currently initializing auth
let isInitializing = false

// Navigation guard for authentication
router.beforeEach(async (to, _from, next) => {
  const authStore = useAuthStore()

  // Initialize auth state on first navigation (only once)
  if (!authStore.initialized && !isInitializing) {
    isInitializing = true
    await authStore.initialize()
    isInitializing = false
  }

  const isAuthenticated = authStore.isAuthenticated

  // Redirect to login if route requires auth and user is not authenticated
  if (to.meta.requiresAuth && !isAuthenticated) {
    next({ name: 'Login', query: { redirect: to.fullPath } })
  }
  // Redirect to dashboard if user is authenticated and trying to access login
  else if (to.name === 'Login' && isAuthenticated) {
    next({ name: 'Dashboard' })
  }
  // Otherwise, proceed normally
  else {
    next()
  }
})

export default router

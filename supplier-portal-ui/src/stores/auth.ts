/**
 * Authentication Store
 * Manages user authentication state, session persistence, and supplier context
 */

import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { login as apiLogin, logout as apiLogout, getCurrentUser, type CurrentUser } from '@/api/auth'
import type { Supplier } from '@/types'

const AUTH_KEY = 'user_authenticated'

export const useAuthStore = defineStore('auth', () => {
  // State
  const user = ref<CurrentUser['user'] | null>(null)
  const supplier = ref<Supplier | null>(null)
  const loading = ref(false)
  const error = ref<string | null>(null)
  const initialized = ref(false)

  // Getters
  const isAuthenticated = computed(() => !!user.value)
  const supplierName = computed(() => supplier.value?.supplier_name || '')
  const userName = computed(() => user.value?.full_name || user.value?.email || '')

  /**
   * Initialize auth state from session
   * Should be called on app startup
   */
  async function initialize(): Promise<boolean> {
    if (initialized.value) return isAuthenticated.value

    const wasAuthenticated = localStorage.getItem(AUTH_KEY) === 'true'
    if (!wasAuthenticated) {
      initialized.value = true
      return false
    }

    // Try to restore session by fetching current user
    try {
      loading.value = true
      const currentUser = await getCurrentUser()
      if (currentUser.user) {
        user.value = currentUser.user
        supplier.value = currentUser.supplier
        localStorage.setItem(AUTH_KEY, 'true')
        return true
      }
    } catch (e) {
      // Session expired or invalid
      console.warn('Session restoration failed:', e)
      clearAuthState()
    } finally {
      loading.value = false
      initialized.value = true
    }

    return false
  }

  /**
   * Login with email and password
   */
  async function login(email: string, password: string): Promise<boolean> {
    loading.value = true
    error.value = null

    try {
      await apiLogin(email, password)

      // Verify login was successful by getting current user
      const currentUser = await getCurrentUser()
      if (currentUser.user) {
        user.value = currentUser.user
        supplier.value = currentUser.supplier
        localStorage.setItem(AUTH_KEY, 'true')
        return true
      }

      error.value = 'אירעה שגיאה בהתחברות'
      return false
    } catch (e: unknown) {
      error.value = 'שם משתמש או סיסמה שגויים'
      console.error('Login error:', e)
      return false
    } finally {
      loading.value = false
    }
  }

  /**
   * Logout current user
   */
  async function logout(): Promise<void> {
    try {
      await apiLogout()
    } catch (e) {
      console.warn('Logout API call failed:', e)
    } finally {
      clearAuthState()
    }
  }

  /**
   * Clear all auth state
   */
  function clearAuthState(): void {
    user.value = null
    supplier.value = null
    error.value = null
    localStorage.removeItem(AUTH_KEY)
  }

  /**
   * Check if session is still valid
   * Can be called periodically or on focus
   */
  async function checkSession(): Promise<boolean> {
    if (!isAuthenticated.value) return false

    try {
      const currentUser = await getCurrentUser()
      if (currentUser.user) {
        user.value = currentUser.user
        supplier.value = currentUser.supplier
        return true
      }
    } catch (e) {
      console.warn('Session check failed:', e)
      clearAuthState()
    }

    return false
  }

  /**
   * Clear error message
   */
  function clearError(): void {
    error.value = null
  }

  return {
    // State
    user,
    supplier,
    loading,
    error,
    initialized,

    // Getters
    isAuthenticated,
    supplierName,
    userName,

    // Actions
    initialize,
    login,
    logout,
    clearAuthState,
    checkSession,
    clearError,
  }
})

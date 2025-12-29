/**
 * Authentication API
 */

import { login as clientLogin, logout as clientLogout, callSupplierPortal } from './client'
import type { Supplier } from '@/types'

export interface CurrentUser {
  user: {
    name: string
    email: string
    full_name: string
    user_type: string
    enabled: number
  }
  supplier: Supplier | null
}

/**
 * Login with email and password
 */
export async function login(email: string, password: string): Promise<{ message: string; full_name?: string }> {
  return clientLogin(email, password)
}

/**
 * Logout current user
 */
export async function logout(): Promise<void> {
  return clientLogout()
}

/**
 * Get current user info and linked supplier
 */
export async function getCurrentUser(): Promise<CurrentUser> {
  return callSupplierPortal<CurrentUser>('get_current_user')
}

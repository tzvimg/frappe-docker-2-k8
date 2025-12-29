/**
 * Supplier API
 */

import { callSupplierPortal } from './client'
import type { SupplierActivityDomain, ContactPerson } from '@/types'

export interface SupplierProfile {
  name: string
  supplier_id: string
  supplier_name: string
  phone?: string
  email?: string
  address?: string
  activity_domains: SupplierActivityDomain[]
  contact_persons?: ContactPerson[]
}

export interface UpdateSupplierProfileParams {
  supplier_name?: string
  phone?: string
  email?: string
  address?: string
}

export interface UpdateResult {
  success: boolean
  message: string
}

/**
 * Get full supplier profile for current user
 */
export async function getSupplierProfile(): Promise<SupplierProfile> {
  return callSupplierPortal<SupplierProfile>('get_supplier_profile')
}

/**
 * Update supplier profile fields
 */
export async function updateSupplierProfile(params: UpdateSupplierProfileParams): Promise<UpdateResult> {
  return callSupplierPortal<UpdateResult>('update_supplier_profile', params)
}

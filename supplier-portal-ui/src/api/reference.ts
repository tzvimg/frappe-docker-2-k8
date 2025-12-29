/**
 * Reference Data API
 */

import { callSupplierPortal } from './client'
import type { ActivityDomainCategory, InquiryTopicCategory, SupplierRole, ContactPersonRole } from '@/types'

export interface InquiryStatus {
  value: string
  label: string
  type: 'open' | 'closed'
}

export interface InquiryContext {
  value: string
  label: string
}

export interface ReferenceData {
  activity_domains: ActivityDomainCategory[]
  inquiry_topics: InquiryTopicCategory[]
  supplier_roles: SupplierRole[]
  contact_person_roles: ContactPersonRole[]
  inquiry_statuses: InquiryStatus[]
  inquiry_contexts: InquiryContext[]
}

/**
 * Get all reference data
 * This method allows guest access for build-time data fetching
 */
export async function getReferenceData(): Promise<ReferenceData> {
  return callSupplierPortal<ReferenceData>('get_reference_data')
}

// Auto-generated index file
// Re-exports all generated types

export type { Supplier } from './supplier'
export { supplierFields } from './supplier'
export type { SupplierInquiry } from './supplier-inquiry'
export { supplierInquiryFields } from './supplier-inquiry'
export type { ActivityDomainCategory } from './activity-domain-category'
export { activityDomainCategoryFields } from './activity-domain-category'
export type { InquiryTopicCategory } from './inquiry-topic-category'
export { inquiryTopicCategoryFields } from './inquiry-topic-category'
export type { ContactPerson } from './contact-person'
export { contactPersonFields } from './contact-person'
export type { SupplierRole } from './supplier-role'
export { supplierRoleFields } from './supplier-role'
export type { SupplierActivityDomain } from './supplier-activity-domain'
export { supplierActivityDomainFields } from './supplier-activity-domain'
export type { ContactPersonRole } from './contact-person-role'
export { contactPersonRoleFields } from './contact-person-role'

// Common Frappe types
export interface FrappeDoc {
  name: string
  creation?: string
  modified?: string
  modified_by?: string
  owner?: string
  docstatus?: 0 | 1 | 2
}

export interface FrappeListResponse<T> {
  data: T[]
  total: number
  page: number
  page_size: number
  total_pages: number
}

export interface FrappeResponse<T> {
  message: T
}

export interface FrappeError {
  exc_type: string
  exception: string
  _server_messages?: string
}

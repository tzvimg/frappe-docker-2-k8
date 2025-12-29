// Auto-generated index file
// Re-exports all generated types

export { Supplier, supplierFields } from './supplier'
export { SupplierInquiry, supplierInquiryFields } from './supplier-inquiry'
export { ActivityDomainCategory, activityDomainCategoryFields } from './activity-domain-category'
export { InquiryTopicCategory, inquiryTopicCategoryFields } from './inquiry-topic-category'
export { ContactPerson, contactPersonFields } from './contact-person'
export { SupplierRole, supplierRoleFields } from './supplier-role'
export { SupplierActivityDomain, supplierActivityDomainFields } from './supplier-activity-domain'
export { ContactPersonRole, contactPersonRoleFields } from './contact-person-role'

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

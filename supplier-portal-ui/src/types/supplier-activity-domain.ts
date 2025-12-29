// Auto-generated file - do not edit manually
// Generated from: supplier_activity_domain.json

/**
 * Supplier Activity Domain DocType
 * Auto-generated from Frappe DocType definition
 */
export interface SupplierActivityDomain {
  /** Document name (primary key) */
  name: string
  /** Creation timestamp */
  creation?: string
  /** Last modified timestamp */
  modified?: string
  /** Modified by user */
  modified_by?: string
  /** Owner user */
  owner?: string
  /** Document status (0=Draft, 1=Submitted, 2=Cancelled) */
  docstatus?: 0 | 1 | 2
  /** קטגורית תחום פעילות */
  activity_domain_category: string
}

/**
 * Field metadata for Supplier Activity Domain
 */
export const supplierActivityDomainFields = {
  activity_domain_category: {
    fieldtype: 'Link',
    label: 'קטגורית תחום פעילות',
    required: true,
    options: 'Activity Domain Category',
  },
} as const

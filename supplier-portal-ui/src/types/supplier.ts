// Auto-generated file - do not edit manually
// Generated from: supplier.json

import type { SupplierActivityDomain } from './supplier-activity-domain'

/**
 * Supplier DocType
 * Auto-generated from Frappe DocType definition
 */
export interface Supplier {
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
  /** מזהה ספק */
  supplier_id: string
  /** שם ספק */
  supplier_name: string
  /** תחומי פעילות */
  activity_domains?: SupplierActivityDomain[]
  /** כתובת */
  address?: string
  /** טלפון */
  phone?: string
  /** כתובת דוא"ל */
  email?: string
}

/**
 * Field metadata for Supplier
 */
export const supplierFields = {
  supplier_id: {
    fieldtype: 'Data',
    label: 'מזהה ספק',
    required: true,
  },
  supplier_name: {
    fieldtype: 'Data',
    label: 'שם ספק',
    required: true,
  },
  activity_domains: {
    fieldtype: 'Table',
    label: 'תחומי פעילות',
    required: false,
    options: 'Supplier Activity Domain',
  },
  address: {
    fieldtype: 'Text',
    label: 'כתובת',
    required: false,
  },
  phone: {
    fieldtype: 'Phone',
    label: 'טלפון',
    required: false,
  },
  email: {
    fieldtype: 'Data',
    label: 'כתובת דוא"ל',
    required: false,
    options: 'Email',
  },
} as const

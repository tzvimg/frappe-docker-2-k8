// Auto-generated file - do not edit manually
// Generated from: supplier_role.json

/**
 * Supplier Role DocType
 * Auto-generated from Frappe DocType definition
 */
export interface SupplierRole {
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
  /** שם תפקיד */
  role_name: string
  /** כותרת בעברית */
  role_title_he: string
}

/**
 * Field metadata for Supplier Role
 */
export const supplierRoleFields = {
  role_name: {
    fieldtype: 'Data',
    label: 'שם תפקיד',
    required: true,
  },
  role_title_he: {
    fieldtype: 'Data',
    label: 'כותרת בעברית',
    required: true,
  },
} as const

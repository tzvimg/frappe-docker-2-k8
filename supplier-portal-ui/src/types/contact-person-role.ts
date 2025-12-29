// Auto-generated file - do not edit manually
// Generated from: contact_person_role.json

/**
 * Contact Person Role DocType
 * Auto-generated from Frappe DocType definition
 */
export interface ContactPersonRole {
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
  /** תפקיד */
  role: string
}

/**
 * Field metadata for Contact Person Role
 */
export const contactPersonRoleFields = {
  role: {
    fieldtype: 'Link',
    label: 'תפקיד',
    required: true,
    options: 'Supplier Role',
  },
} as const

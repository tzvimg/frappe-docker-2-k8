// Auto-generated file - do not edit manually
// Generated from: contact_person.json

import type { ContactPersonRole } from './contact-person-role'

/**
 * Contact Person DocType
 * Auto-generated from Frappe DocType definition
 */
export interface ContactPerson {
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
  /** שם איש קשר */
  contact_name: string
  /** שיוך לספק */
  supplier_link: string
  /** כתובת דוא"ל */
  email?: string
  /** טלפון נייד */
  mobile_phone?: string
  /** סניף */
  branch?: string
  /** תפקיד ראשי */
  primary_role_type?: 'ספק' | 'איש קשר של ספק'
  /** רשימת תפקידים משויכים */
  assigned_roles?: ContactPersonRole[]
}

/**
 * Field metadata for Contact Person
 */
export const contactPersonFields = {
  contact_name: {
    fieldtype: 'Data',
    label: 'שם איש קשר',
    required: true,
  },
  supplier_link: {
    fieldtype: 'Link',
    label: 'שיוך לספק',
    required: true,
    options: 'Supplier',
  },
  email: {
    fieldtype: 'Data',
    label: 'כתובת דוא"ל',
    required: false,
    options: 'Email',
  },
  mobile_phone: {
    fieldtype: 'Phone',
    label: 'טלפון נייד',
    required: false,
  },
  branch: {
    fieldtype: 'Data',
    label: 'סניף',
    required: false,
  },
  primary_role_type: {
    fieldtype: 'Select',
    label: 'תפקיד ראשי',
    required: false,
    options: ['ספק', 'איש קשר של ספק'],
  },
  assigned_roles: {
    fieldtype: 'Table',
    label: 'רשימת תפקידים משויכים',
    required: false,
    options: 'Contact Person Role',
  },
} as const

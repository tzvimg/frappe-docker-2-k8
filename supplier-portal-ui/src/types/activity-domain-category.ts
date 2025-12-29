// Auto-generated file - do not edit manually
// Generated from: activity_domain_category.json

/**
 * Activity Domain Category DocType
 * Auto-generated from Frappe DocType definition
 */
export interface ActivityDomainCategory {
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
  /** קוד קטגוריה */
  category_code: string
  /** שם קטגוריה */
  category_name: string
}

/**
 * Field metadata for Activity Domain Category
 */
export const activityDomainCategoryFields = {
  category_code: {
    fieldtype: 'Data',
    label: 'קוד קטגוריה',
    required: true,
  },
  category_name: {
    fieldtype: 'Data',
    label: 'שם קטגוריה',
    required: true,
  },
} as const

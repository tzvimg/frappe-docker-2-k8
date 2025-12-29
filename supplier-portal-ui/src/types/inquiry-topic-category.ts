// Auto-generated file - do not edit manually
// Generated from: inquiry_topic_category.json

/**
 * Inquiry Topic Category DocType
 * Auto-generated from Frappe DocType definition
 */
export interface InquiryTopicCategory {
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
  /** קטגוריית אב */
  parent_category?: string
  /** Left */
  lft?: number
  /** Right */
  rgt?: number
  /** Is Group */
  is_group?: boolean
  /** Old Parent */
  old_parent?: string
  /** Parent Inquiry Topic Category */
  parent_inquiry_topic_category?: string
}

/**
 * Field metadata for Inquiry Topic Category
 */
export const inquiryTopicCategoryFields = {
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
  parent_category: {
    fieldtype: 'Link',
    label: 'קטגוריית אב',
    required: false,
    options: 'Inquiry Topic Category',
  },
  lft: {
    fieldtype: 'Int',
    label: 'Left',
    required: false,
  },
  rgt: {
    fieldtype: 'Int',
    label: 'Right',
    required: false,
  },
  is_group: {
    fieldtype: 'Check',
    label: 'Is Group',
    required: false,
  },
  old_parent: {
    fieldtype: 'Link',
    label: 'Old Parent',
    required: false,
    options: 'Inquiry Topic Category',
  },
  parent_inquiry_topic_category: {
    fieldtype: 'Link',
    label: 'Parent Inquiry Topic Category',
    required: false,
    options: 'Inquiry Topic Category',
  },
} as const

// Auto-generated file - do not edit manually
// Generated from: supplier_inquiry.json

/**
 * Supplier Inquiry DocType
 * Auto-generated from Frappe DocType definition
 */
export interface SupplierInquiry {
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
  supplier_link: string
  /** קטגורית נושא פנייה */
  topic_category: string
  /** תיאור הפנייה */
  inquiry_description: string
  /** הקשר הפנייה */
  inquiry_context: 'ספק עצמו' | 'מבוטח'
  /** מספר זהות של המבוטח */
  insured_id_number?: string
  /** שם מלא של המבוטח */
  insured_full_name?: string
  /** קבצים מצורפים */
  attachments?: string
  /** סטטוס פנייה */
  inquiry_status?: 'סגור' | 'נסגר – ניתן מענה' | 'דורש השלמות / המתנה' | 'בטיפול' | 'מיון וניתוב' | 'פנייה חדשה התקבלה'
  /** שיוך לתפקיד מטפל בפניה */
  assigned_role?: string
  /** מזהה הפקיד שמטפל בפנייה */
  assigned_employee_id?: string
  /** המענה לפנייה - מלל */
  response_text?: string
  /** המענה לפנייה - קבצים */
  response_attachments?: string
  /** Amended From */
  amended_from?: string
}

/**
 * Field metadata for Supplier Inquiry
 */
export const supplierInquiryFields = {
  supplier_link: {
    fieldtype: 'Link',
    label: 'מזהה ספק',
    required: true,
    options: 'Supplier',
  },
  topic_category: {
    fieldtype: 'Link',
    label: 'קטגורית נושא פנייה',
    required: true,
    options: 'Inquiry Topic Category',
  },
  inquiry_description: {
    fieldtype: 'Text Editor',
    label: 'תיאור הפנייה',
    required: true,
  },
  inquiry_context: {
    fieldtype: 'Select',
    label: 'הקשר הפנייה',
    required: true,
    options: ['ספק עצמו', 'מבוטח'],
  },
  insured_id_number: {
    fieldtype: 'Data',
    label: 'מספר זהות של המבוטח',
    required: false,
  },
  insured_full_name: {
    fieldtype: 'Data',
    label: 'שם מלא של המבוטח',
    required: false,
  },
  attachments: {
    fieldtype: 'Attach',
    label: 'קבצים מצורפים',
    required: false,
  },
  inquiry_status: {
    fieldtype: 'Select',
    label: 'סטטוס פנייה',
    required: false,
    options: ['סגור', 'נסגר – ניתן מענה', 'דורש השלמות / המתנה', 'בטיפול', 'מיון וניתוב', 'פנייה חדשה התקבלה'],
    default: 'פנייה חדשה התקבלה',
  },
  assigned_role: {
    fieldtype: 'Link',
    label: 'שיוך לתפקיד מטפל בפניה',
    required: false,
    options: 'Supplier Role',
  },
  assigned_employee_id: {
    fieldtype: 'Link',
    label: 'מזהה הפקיד שמטפל בפנייה',
    required: false,
    options: 'User',
  },
  response_text: {
    fieldtype: 'Text Editor',
    label: 'המענה לפנייה - מלל',
    required: false,
  },
  response_attachments: {
    fieldtype: 'Attach',
    label: 'המענה לפנייה - קבצים',
    required: false,
  },
  amended_from: {
    fieldtype: 'Link',
    label: 'Amended From',
    required: false,
    options: 'Supplier Inquiry',
  },
} as const

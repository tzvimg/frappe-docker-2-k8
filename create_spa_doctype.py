#!/usr/bin/env python3
"""Create Service Provider Application DocType"""

import frappe

frappe.init(site='development.localhost')
frappe.connect()

print("Creating Service Provider Application DocType...")

doc = frappe.new_doc('DocType')
doc.name = 'Service Provider Application'
doc.module = 'Nursing Management'
doc.custom = 0
doc.is_submittable = 1
doc.track_changes = 1
doc.autoname = 'format:SPA-{#####}'

# Section 1: Basic Information
doc.append('fields', {'fieldname': 'basic_info_section', 'fieldtype': 'Section Break', 'label': 'פרטי ספק'})
doc.append('fields', {'fieldname': 'provider_name', 'fieldtype': 'Data', 'label': 'שם נותן השירות', 'reqd': 1})
doc.append('fields', {'fieldname': 'hp_number', 'fieldtype': 'Data', 'label': 'מספר ח"פ', 'reqd': 1, 'length': 9})
doc.append('fields', {'fieldname': 'column_break_1', 'fieldtype': 'Column Break'})
doc.append('fields', {'fieldname': 'service_type', 'fieldtype': 'Select', 'label': 'סוג שירות', 'options': 'טיפול בבית\nמרכז יום\nקהילה תומכת\nמוצרי ספיגה', 'reqd': 1})
doc.append('fields', {'fieldname': 'branch_type', 'fieldtype': 'Data', 'label': 'סוג סניף'})
doc.append('fields', {'fieldname': 'column_break_2', 'fieldtype': 'Column Break'})
doc.append('fields', {'fieldname': 'contact_person', 'fieldtype': 'Data', 'label': 'איש קשר'})
doc.append('fields', {'fieldname': 'phone', 'fieldtype': 'Data', 'label': 'טלפון'})
doc.append('fields', {'fieldname': 'email', 'fieldtype': 'Data', 'label': 'אימייל', 'options': 'Email', 'reqd': 1})
doc.append('fields', {'fieldname': 'address', 'fieldtype': 'Small Text', 'label': 'כתובת'})

# Section 2: Application Status
doc.append('fields', {'fieldname': 'status_section', 'fieldtype': 'Section Break', 'label': 'סטטוס בקשה'})
doc.append('fields', {'fieldname': 'workflow_state', 'fieldtype': 'Link', 'label': 'סטטוס', 'options': 'Workflow State', 'read_only': 1})
doc.append('fields', {'fieldname': 'application_date', 'fieldtype': 'Date', 'label': 'תאריך הגשה', 'default': 'Today', 'read_only': 1})
doc.append('fields', {'fieldname': 'column_break_3', 'fieldtype': 'Column Break'})
doc.append('fields', {'fieldname': 'assigned_to', 'fieldtype': 'Link', 'label': 'מטופל על ידי', 'options': 'User'})

# Section 3: Document Checklist
doc.append('fields', {'fieldname': 'documents_section', 'fieldtype': 'Section Break', 'label': 'רשימת מסמכים'})
doc.append('fields', {'fieldname': 'application_document_checklist', 'fieldtype': 'Table', 'label': 'רשימת מסמכים נדרשים', 'options': 'Application Document Checklist'})

# Section 4: HQ Review
doc.append('fields', {'fieldname': 'hq_section', 'fieldtype': 'Section Break', 'label': 'בדיקת מטה'})
doc.append('fields', {'fieldname': 'hq_check_status', 'fieldtype': 'Select', 'label': 'סטטוס בדיקת מטה', 'options': '\nתקין\nלא תקין'})
doc.append('fields', {'fieldname': 'hq_reviewer', 'fieldtype': 'Link', 'label': 'בודק מטה', 'options': 'User'})
doc.append('fields', {'fieldname': 'column_break_4', 'fieldtype': 'Column Break'})
doc.append('fields', {'fieldname': 'hq_review_date', 'fieldtype': 'Date', 'label': 'תאריך בדיקת מטה'})
doc.append('fields', {'fieldname': 'hq_notes', 'fieldtype': 'Text Editor', 'label': 'הערות מטה'})

# Section 5: Data Clarification
doc.append('fields', {'fieldname': 'data_section', 'fieldtype': 'Section Break', 'label': 'הבהרת נתונים'})
doc.append('fields', {'fieldname': 'data_clarification_status', 'fieldtype': 'Select', 'label': 'סטטוס הבהרת נתונים', 'options': '\nתקין\nלא תקין'})
doc.append('fields', {'fieldname': 'bi_verification', 'fieldtype': 'Check', 'label': 'אומת מול ביטוח לאומי'})
doc.append('fields', {'fieldname': 'column_break_5', 'fieldtype': 'Column Break'})
doc.append('fields', {'fieldname': 'data_reviewer', 'fieldtype': 'Link', 'label': 'בודק נתונים', 'options': 'User'})
doc.append('fields', {'fieldname': 'data_review_date', 'fieldtype': 'Date', 'label': 'תאריך בדיקת נתונים'})
doc.append('fields', {'fieldname': 'data_notes', 'fieldtype': 'Text Editor', 'label': 'הערות בדיקת נתונים'})

# Section 6: Rejection Handling
doc.append('fields', {'fieldname': 'rejection_section', 'fieldtype': 'Section Break', 'label': 'טיפול בדחייה'})
doc.append('fields', {'fieldname': 'rejection_reason', 'fieldtype': 'Text Editor', 'label': 'סיבת דחייה'})
doc.append('fields', {'fieldname': 'column_break_6', 'fieldtype': 'Column Break'})
doc.append('fields', {'fieldname': 'rejection_date', 'fieldtype': 'Date', 'label': 'תאריך דחייה', 'read_only': 1})

# Section 7: Final Processing
doc.append('fields', {'fieldname': 'final_section', 'fieldtype': 'Section Break', 'label': 'טיפול סופי'})
doc.append('fields', {'fieldname': 'agreement_prepared', 'fieldtype': 'Check', 'label': 'הסכם הוכן'})
doc.append('fields', {'fieldname': 'agreement_file', 'fieldtype': 'Attach', 'label': 'קובץ הסכם'})
doc.append('fields', {'fieldname': 'column_break_7', 'fieldtype': 'Column Break'})
doc.append('fields', {'fieldname': 'nursing_system_synced', 'fieldtype': 'Check', 'label': 'שוקף במערכת סיעוד'})
doc.append('fields', {'fieldname': 'created_service_provider', 'fieldtype': 'Link', 'label': 'נותן שירות שנוצר', 'options': 'Service Provider', 'read_only': 1})
doc.append('fields', {'fieldname': 'approval_date', 'fieldtype': 'Date', 'label': 'תאריך אישור סופי'})

# Section 8: Communication Log
doc.append('fields', {'fieldname': 'communication_section', 'fieldtype': 'Section Break', 'label': 'תיעוד תקשורת'})
doc.append('fields', {'fieldname': 'communication_history', 'fieldtype': 'Text Editor', 'label': 'היסטוריית תקשורת', 'read_only': 1})

# Permissions
doc.append('permissions', {'role': 'System Manager', 'read': 1, 'write': 1, 'create': 1, 'delete': 1, 'submit': 1, 'cancel': 1, 'amend': 1})

doc.insert(ignore_permissions=True)
frappe.db.commit()

print("✓✓✓ Service Provider Application DocType created successfully!")
print(f"  - Total fields: {len(doc.fields)}")
print(f"  - Submittable: {doc.is_submittable}")
print(f"  - Auto-naming: {doc.autoname}")

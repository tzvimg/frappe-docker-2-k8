#!/usr/bin/env python3
"""
Script to create Application Document Checklist child table DocType
Part of Service Provider Application workflow implementation
"""

create_script = """
import frappe

def create_application_document_checklist():
    # Check if DocType already exists
    if frappe.db.exists('DocType', 'Application Document Checklist'):
        print('Application Document Checklist DocType already exists')
        return

    # Create the child table DocType
    doc = frappe.new_doc('DocType')
    doc.name = 'Application Document Checklist'
    doc.module = 'Nursing Management'
    doc.custom = 0
    doc.istable = 1  # This makes it a child table
    doc.editable_grid = 1
    doc.track_changes = 0
    doc.is_submittable = 0

    # Add fields
    fields = [
        {
            'fieldname': 'document_type',
            'fieldtype': 'Select',
            'label': 'סוג מסמך',
            'options': 'אישור ניהול תקין\\nתעודת עוסק מורשה\\nאישור ביטוח\\nהסכם בט\\"ל\\nפרטי בנק\\nרשיון עסק',
            'reqd': 1,
            'in_list_view': 1,
            'columns': 2
        },
        {
            'fieldname': 'status',
            'fieldtype': 'Select',
            'label': 'סטטוס',
            'options': 'חסר\\nהוגש\\nתקין\\nלא תקין',
            'default': 'חסר',
            'reqd': 1,
            'in_list_view': 1,
            'columns': 1
        },
        {
            'fieldname': 'attached_file',
            'fieldtype': 'Attach',
            'label': 'קובץ מצורף',
            'in_list_view': 1,
            'columns': 2
        },
        {
            'fieldname': 'notes',
            'fieldtype': 'Small Text',
            'label': 'הערות',
            'in_list_view': 0
        }
    ]

    for field in fields:
        doc.append('fields', field)

    # Add System Manager permissions
    doc.append('permissions', {
        'role': 'System Manager',
        'read': 1,
        'write': 1,
        'create': 1,
        'delete': 1
    })

    # Insert the DocType
    doc.insert(ignore_permissions=True)
    frappe.db.commit()

    print(f'✓ Application Document Checklist child table created successfully')
    return doc

# Execute
try:
    result = create_application_document_checklist()
    print('Done!')
except Exception as e:
    print(f'Error: {e}')
    import traceback
    traceback.print_exc()
"""

print(create_script)

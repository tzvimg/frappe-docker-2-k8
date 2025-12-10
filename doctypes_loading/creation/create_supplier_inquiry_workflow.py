"""
Create Supplier Inquiry DocType and Workflow
Based on workflow1.md specification for managing supplier inquiries

This script creates:
1. Supplier Inquiry DocType (פניית ספק)
2. Workflow with 6 states
3. Role-based permissions
"""

import frappe
from frappe import _


@frappe.whitelist()
def create_supplier_inquiry_doctype():
    """Create the Supplier Inquiry DocType"""

    # Check if DocType already exists
    if frappe.db.exists("DocType", "Supplier Inquiry"):
        frappe.msgprint("⚠ Supplier Inquiry DocType already exists. Skipping creation.")
        return {"success": False, "message": "Already exists"}

    doc = frappe.get_doc({
        'doctype': 'DocType',
        'name': 'Supplier Inquiry',
        'module': 'Siud',
        'autoname': 'format:INQ-{#####}',
        'naming_rule': 'By fieldname',
        'is_submittable': 0,
        'track_changes': 1,
        'title_field': 'subject_category',
        'search_fields': 'supplier_id,subject_category,inquiry_status',
        'fields': [
            # Section: Basic Inquiry Information
            {
                'fieldname': 'inquiry_details_section',
                'fieldtype': 'Section Break',
                'label': 'פרטי הפנייה',
            },
            {
                'fieldname': 'supplier_id',
                'fieldtype': 'Link',
                'label': 'מזהה ספק',
                'options': 'Supplier',
                'reqd': 1,
                'in_list_view': 1,
                'in_standard_filter': 1,
            },
            {
                'fieldname': 'column_break_1',
                'fieldtype': 'Column Break',
            },
            {
                'fieldname': 'inquiry_status',
                'fieldtype': 'Select',
                'label': 'סטטוס פנייה',
                'options': '\nפנייה חדשה התקבלה\nמיון וניתוב\nבטיפול\nדורש השלמות / המתנה\nנסגר – ניתן מענה\nסגור',
                'default': 'פנייה חדשה התקבלה',
                'in_list_view': 1,
                'in_standard_filter': 1,
                'read_only': 1,
            },

            # Section: Subject and Description
            {
                'fieldname': 'subject_section',
                'fieldtype': 'Section Break',
                'label': 'נושא הפנייה',
            },
            {
                'fieldname': 'subject_category_level1',
                'fieldtype': 'Select',
                'label': 'קטגוריית נושא - רמה 1',
                'options': '\nנושאים מקצועיים\nתלונות\nחשבונות שוטפים\nפניות כלליות',
                'reqd': 1,
                'in_list_view': 1,
            },
            {
                'fieldname': 'subject_category_level2',
                'fieldtype': 'Select',
                'label': 'קטגוריית נושא - רמה 2',
                'options': '',
                'depends_on': 'subject_category_level1',
            },
            {
                'fieldname': 'subject_category',
                'fieldtype': 'Data',
                'label': 'קטגוריה מלאה',
                'read_only': 1,
                'in_list_view': 0,
            },
            {
                'fieldname': 'inquiry_description',
                'fieldtype': 'Text Editor',
                'label': 'תיאור הפנייה',
                'reqd': 1,
            },

            # Section: Context of Inquiry
            {
                'fieldname': 'inquiry_context_section',
                'fieldtype': 'Section Break',
                'label': 'הקשר הפנייה',
            },
            {
                'fieldname': 'inquiry_context',
                'fieldtype': 'Select',
                'label': 'הפנייה עבור',
                'options': '\nהספק עצמו\nמבוטח',
                'default': 'הספק עצמו',
                'reqd': 1,
            },
            {
                'fieldname': 'column_break_2',
                'fieldtype': 'Column Break',
            },
            {
                'fieldname': 'insured_id_number',
                'fieldtype': 'Data',
                'label': 'מספר זהות מבוטח',
                'depends_on': 'eval:doc.inquiry_context=="מבוטח"',
                'mandatory_depends_on': 'eval:doc.inquiry_context=="מבוטח"',
                'length': 9,
            },
            {
                'fieldname': 'insured_full_name',
                'fieldtype': 'Data',
                'label': 'שם מלא מבוטח',
                'depends_on': 'eval:doc.inquiry_context=="מבוטח"',
                'mandatory_depends_on': 'eval:doc.inquiry_context=="מבוטח"',
            },

            # Section: Attachments
            {
                'fieldname': 'attachments_section',
                'fieldtype': 'Section Break',
                'label': 'קבצים מצורפים',
            },
            {
                'fieldname': 'attached_files',
                'fieldtype': 'Attach',
                'label': 'קובץ מצורף',
            },

            # Section: Assignment and Handling
            {
                'fieldname': 'assignment_section',
                'fieldtype': 'Section Break',
                'label': 'שיוך וטיפול',
            },
            {
                'fieldname': 'assigned_role',
                'fieldtype': 'Link',
                'label': 'תפקיד מטפל',
                'options': 'Role',
            },
            {
                'fieldname': 'column_break_3',
                'fieldtype': 'Column Break',
            },
            {
                'fieldname': 'handling_clerk',
                'fieldtype': 'Link',
                'label': 'פקיד מטפל',
                'options': 'User',
            },

            # Section: Response
            {
                'fieldname': 'response_section',
                'fieldtype': 'Section Break',
                'label': 'המענה לפנייה',
            },
            {
                'fieldname': 'response_text',
                'fieldtype': 'Text Editor',
                'label': 'תוכן המענה',
            },
            {
                'fieldname': 'response_files',
                'fieldtype': 'Attach',
                'label': 'קבצים במענה',
            },

            # Section: Internal Notes
            {
                'fieldname': 'internal_notes_section',
                'fieldtype': 'Section Break',
                'label': 'הערות פנימיות',
                'collapsible': 1,
            },
            {
                'fieldname': 'internal_notes',
                'fieldtype': 'Text Editor',
                'label': 'תיעוד תקשורת ובירורים',
            },

            # Section: Metadata
            {
                'fieldname': 'metadata_section',
                'fieldtype': 'Section Break',
                'label': 'מידע מערכתי',
                'collapsible': 1,
            },
            {
                'fieldname': 'created_date',
                'fieldtype': 'Datetime',
                'label': 'תאריך יצירה',
                'read_only': 1,
                'default': 'Now',
            },
            {
                'fieldname': 'column_break_4',
                'fieldtype': 'Column Break',
            },
            {
                'fieldname': 'last_updated',
                'fieldtype': 'Datetime',
                'label': 'עודכן לאחרונה',
                'read_only': 1,
            },
        ],
        'permissions': [
            {
                'role': 'System Manager',
                'read': 1,
                'write': 1,
                'create': 1,
                'delete': 1,
                'export': 1,
                'print': 1,
                'email': 1,
            },
            {
                'role': 'Service Provider User',
                'read': 1,
                'write': 1,
                'create': 1,
                'if_owner': 1,
            },
            {
                'role': 'Handling Clerk',
                'read': 1,
                'write': 1,
                'export': 1,
                'print': 1,
                'email': 1,
            },
            {
                'role': 'Sorting Clerk',
                'read': 1,
                'write': 1,
                'export': 1,
            },
        ]
    })

    doc.insert()
    frappe.db.commit()
    frappe.msgprint(f"✓ Created Supplier Inquiry DocType")

    return {"success": True, "doctype": "Supplier Inquiry"}


@frappe.whitelist()
def create_supplier_inquiry_workflow():
    """Create the workflow for Supplier Inquiry"""

    # Check if Workflow already exists
    if frappe.db.exists("Workflow", "Supplier Inquiry Workflow"):
        frappe.msgprint("⚠ Supplier Inquiry Workflow already exists. Skipping creation.")
        return {"success": False, "message": "Already exists"}

    workflow = frappe.get_doc({
        'doctype': 'Workflow',
        'workflow_name': 'Supplier Inquiry Workflow',
        'document_type': 'Supplier Inquiry',
        'is_active': 1,
        'workflow_state_field': 'inquiry_status',
        'send_email_alert': 1,

        # Workflow States
        'states': [
            {
                'state': 'פנייה חדשה התקבלה',
                'doc_status': '0',
                'allow_edit': 'Service Provider User',
                'message': 'הפנייה התקבלה ממתינה למיון',
            },
            {
                'state': 'מיון וניתוב',
                'doc_status': '0',
                'allow_edit': 'Sorting Clerk',
                'message': 'הפנייה בתהליך מיון והקצאה לגורם מטפל',
            },
            {
                'state': 'בטיפול',
                'doc_status': '0',
                'allow_edit': 'Handling Clerk',
                'message': 'הפנייה בטיפול פעיל',
            },
            {
                'state': 'דורש השלמות / המתנה',
                'doc_status': '0',
                'allow_edit': 'Handling Clerk',
                'message': 'הפנייה ממתינה למידע נוסף או תגובה חיצונית',
            },
            {
                'state': 'נסגר – ניתן מענה',
                'doc_status': '0',
                'allow_edit': 'Handling Clerk',
                'message': 'הפנייה נסגרה ונמסר מענה לספק',
            },
            {
                'state': 'סגור',
                'doc_status': '1',
                'allow_edit': '',
                'message': 'הפנייה בארכיון',
            },
        ],

        # Workflow Transitions
        'transitions': [
            # From: פנייה חדשה התקבלה
            {
                'state': 'פנייה חדשה התקבלה',
                'action': 'העבר למיון',
                'next_state': 'מיון וניתוב',
                'allowed': 'Sorting Clerk',
                'allow_self_approval': 0,
            },

            # From: מיון וניתוב
            {
                'state': 'מיון וניתוב',
                'action': 'הקצה לטיפול',
                'next_state': 'בטיפול',
                'allowed': 'Sorting Clerk',
                'allow_self_approval': 0,
                'condition': 'doc.handling_clerk',
            },

            # From: בטיפול
            {
                'state': 'בטיפול',
                'action': 'דרוש השלמות',
                'next_state': 'דורש השלמות / המתנה',
                'allowed': 'Handling Clerk',
                'allow_self_approval': 1,
            },
            {
                'state': 'בטיפול',
                'action': 'סגור עם מענה',
                'next_state': 'נסגר – ניתן מענה',
                'allowed': 'Handling Clerk',
                'allow_self_approval': 1,
                'condition': 'doc.response_text',
            },

            # From: דורש השלמות / המתנה
            {
                'state': 'דורש השלמות / המתנה',
                'action': 'חזור לטיפול',
                'next_state': 'בטיפול',
                'allowed': 'Handling Clerk',
                'allow_self_approval': 1,
            },
            {
                'state': 'דורש השלמות / המתנה',
                'action': 'סגור עם מענה',
                'next_state': 'נסגר – ניתן מענה',
                'allowed': 'Handling Clerk',
                'allow_self_approval': 1,
                'condition': 'doc.response_text',
            },

            # From: נסגר – ניתן מענה
            {
                'state': 'נסגר – ניתן מענה',
                'action': 'העבר לארכיון',
                'next_state': 'סגור',
                'allowed': 'System Manager',
                'allow_self_approval': 1,
            },
            {
                'state': 'נסגר – ניתן מענה',
                'action': 'פתח מחדש',
                'next_state': 'בטיפול',
                'allowed': 'Handling Clerk',
                'allow_self_approval': 1,
            },
        ]
    })

    workflow.insert()
    frappe.db.commit()
    frappe.msgprint(f"✓ Created Supplier Inquiry Workflow with {len(workflow.states)} states and {len(workflow.transitions)} transitions")

    return {"success": True, "workflow": "Supplier Inquiry Workflow"}


@frappe.whitelist()
def create_required_roles():
    """Create roles required for the workflow"""

    roles = [
        {
            'role_name': 'Service Provider User',
            'desk_access': 0,  # Portal access only
        },
        {
            'role_name': 'Sorting Clerk',
            'desk_access': 1,
        },
        {
            'role_name': 'Handling Clerk',
            'desk_access': 1,
        },
    ]

    created_roles = []

    for role_data in roles:
        if not frappe.db.exists("Role", role_data['role_name']):
            role = frappe.get_doc({
                'doctype': 'Role',
                'role_name': role_data['role_name'],
                'desk_access': role_data['desk_access'],
            })
            role.insert()
            created_roles.append(role_data['role_name'])
            frappe.msgprint(f"✓ Created role: {role_data['role_name']}")
        else:
            frappe.msgprint(f"⚠ Role already exists: {role_data['role_name']}")

    frappe.db.commit()

    return {"success": True, "created_roles": created_roles}


@frappe.whitelist()
def create_supplier_doctype():
    """Create a simple Supplier DocType if it doesn't exist"""

    if frappe.db.exists("DocType", "Supplier"):
        frappe.msgprint("⚠ Supplier DocType already exists. Skipping creation.")
        return {"success": False, "message": "Already exists"}

    doc = frappe.get_doc({
        'doctype': 'DocType',
        'name': 'Supplier',
        'module': 'Siud',
        'autoname': 'format:SUP-{#####}',
        'naming_rule': 'By fieldname',
        'fields': [
            {
                'fieldname': 'supplier_name',
                'fieldtype': 'Data',
                'label': 'שם הספק',
                'reqd': 1,
                'in_list_view': 1,
            },
            {
                'fieldname': 'hp_number',
                'fieldtype': 'Data',
                'label': 'מספר ח"פ',
                'unique': 1,
                'length': 9,
            },
            {
                'fieldname': 'contact_person',
                'fieldtype': 'Data',
                'label': 'איש קשר',
            },
            {
                'fieldname': 'email',
                'fieldtype': 'Data',
                'label': 'דוא"ל',
                'options': 'Email',
            },
            {
                'fieldname': 'phone',
                'fieldtype': 'Data',
                'label': 'טלפון',
            },
        ],
        'permissions': [
            {
                'role': 'System Manager',
                'read': 1,
                'write': 1,
                'create': 1,
                'delete': 1,
            },
        ]
    })

    doc.insert()
    frappe.db.commit()
    frappe.msgprint(f"✓ Created Supplier DocType")

    return {"success": True, "doctype": "Supplier"}


@frappe.whitelist()
def create_all():
    """Master function to create all components for Supplier Inquiry workflow"""

    frappe.msgprint("=" * 60)
    frappe.msgprint("Starting Supplier Inquiry Workflow Creation")
    frappe.msgprint("=" * 60)

    results = {}

    # Step 1: Create required roles
    frappe.msgprint("\n1️⃣ Creating required roles...")
    results['roles'] = create_required_roles()

    # Step 2: Create Supplier DocType (dependency)
    frappe.msgprint("\n2️⃣ Creating Supplier DocType...")
    results['supplier'] = create_supplier_doctype()

    # Step 3: Create Supplier Inquiry DocType
    frappe.msgprint("\n3️⃣ Creating Supplier Inquiry DocType...")
    results['supplier_inquiry'] = create_supplier_inquiry_doctype()

    # Step 4: Create Workflow
    frappe.msgprint("\n4️⃣ Creating Supplier Inquiry Workflow...")
    results['workflow'] = create_supplier_inquiry_workflow()

    frappe.msgprint("\n" + "=" * 60)
    frappe.msgprint("✅ Supplier Inquiry Workflow Setup Complete!")
    frappe.msgprint("=" * 60)
    frappe.msgprint("\n📋 Next steps:")
    frappe.msgprint("   1. Run: bench --site development.localhost clear-cache")
    frappe.msgprint("   2. Run: bench --site development.localhost migrate")
    frappe.msgprint("   3. Access the system at http://localhost:8000")
    frappe.msgprint("   4. Navigate to: Supplier Inquiry to test the workflow")
    frappe.msgprint("\n")

    return results


@frappe.whitelist()
def delete_all():
    """Delete all created components (for development/testing)"""

    frappe.msgprint("🗑️ Deleting Supplier Inquiry Workflow components...")

    # Delete in reverse order of creation
    items_to_delete = [
        ("Workflow", "Supplier Inquiry Workflow"),
        ("DocType", "Supplier Inquiry"),
        ("DocType", "Supplier"),
    ]

    for doctype, name in items_to_delete:
        if frappe.db.exists(doctype, name):
            frappe.delete_doc(doctype, name, force=1)
            frappe.msgprint(f"✓ Deleted {doctype}: {name}")
        else:
            frappe.msgprint(f"⚠ {doctype} {name} does not exist")

    frappe.db.commit()
    frappe.msgprint("✅ Deletion complete!")

    return {"success": True}
